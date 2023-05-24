# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.facetednavigation.interfaces import IFacetedNavigable
from collective.eeafaceted.dashboard.utils import getDashboardQueryResult

from plone import api
from plone.app.layout.viewlets import ViewletBase

from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.archetypes import InplaceATFolderMigrator

from Products.urban.events.licenceEvents import postCreationActions
from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import getLicenceFolder

import logging


class ToInspectionViewlet(ViewletBase):
    """For displaying on dashboards."""

    render = ViewPageTemplateFile('./templates/to_inspections.pt')

    def available(self):
        """
        This viewlet is only visible on buildlicences faceted view if we queried by date.
        """
        allowed_contexts = [
            'miscdemands',
        ]
        allowed = self.context.id in allowed_contexts
        is_admin = api.user.has_permission("cmf.AddPortalMember", user=api.user.get_current())
        faceted_context = bool(IFacetedNavigable.providedBy(self.context))
        return faceted_context and allowed and is_admin

    def get_links_info(self):
        base_url = self.context.absolute_url()
        url = '{base_url}/copy_to_inspections'.format(base_url=base_url)
        link = {'link': url, 'title': 'Migrer vers l\'inspection'}
        return [link]


class UrbanWalker(CustomQueryWalker):
    """
    """
    def walk(self):
        root = self.additionalQuery['root']
        to_explore = set([root])
        while to_explore:
            current = to_explore.pop()
            if hasattr(current, 'objectValues'):
                for content in current.objectValues():
                    to_explore.add(content)
            if current.portal_type == self.src_portal_type:
                yield current


class ApplicantMigrator(InplaceATFolderMigrator):
    """
    """
    walker = UrbanWalker
    src_meta_type = "Applicant"
    src_portal_type = "Applicant"
    dst_meta_type = "Applicant"
    dst_portal_type = "Proprietary"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


class CorporationMigrator(InplaceATFolderMigrator):
    """
    """
    walker = UrbanWalker
    src_meta_type = "Corporation"
    src_portal_type = "Corporation"
    dst_meta_type = "Corporation"
    dst_portal_type = "CorporationProprietary"

    def __init__(self, *args, **kwargs):
        InplaceATFolderMigrator.__init__(self, *args, **kwargs)


class MigrateToInspection(BrowserView):

    def __call__(self):
        brains = getDashboardQueryResult(self.context)
        portal_urban = api.portal.get_tool('portal_urban')
        # disable singleton document generation
        old_value = portal_urban.getGenerateSingletonDocuments()
        portal_urban.setGenerateSingletonDocuments(False)
        migrated = self.migrate_to_inspections(brains)
        # restore previous singleton document generation value
        portal_urban.setGenerateSingletonDocuments(old_value)
        return migrated

    def migrate_to_inspections(self, brains):
        # migrate cfg
        portal_urban = api.portal.get_tool('portal_urban')
        for eventconfig in portal_urban.miscdemand.eventconfigs.objectValues():
            inspection_cfg = portal_urban.inspection.eventconfigs
            if eventconfig.id not in inspection_cfg.objectIds():
                copied_cfg = api.content.copy(eventconfig, inspection_cfg)
                api.content.transition(copied_cfg, 'disable')

        # migrate licences
        states_mapping = {
            'accepted': 'ended',
            'refused': 'ended',
            'retired': 'ended',
        }
        for brain in brains:
            self.copy_one_licence(brain.getObject(), 'Inspection', states_mapping)

        # migrate applicants to proprietaries
        portal = api.portal.get()
        root = portal.urban.inspections
        logger = logging.getLogger('urban: migrate miscdemands to inspection')
        # to avoid link integrity problems, disable checks
        portal.portal_properties.site_properties.enable_link_integrity_checks = False
        for migrator in [ApplicantMigrator, CorporationMigrator]:
            walker = migrator.walker(
                portal,
                migrator,
                query={'root': root},
                logger=logger,
                purl=portal.portal_url
            )
            walker.go()
            # we need to reset the class variable to avoid using current query in
            # next use of CustomQueryWalker
            walker.__class__.additionalQuery = {}
        # re-enable linkintegrity checks
        portal.portal_properties.site_properties.enable_link_integrity_checks = True

    def copy_one_licence(self, original_licence, destination_type, states_mapping={}):
        site = api.portal.get()
        destination_folder = getLicenceFolder(destination_type)
        copied_licence_id = destination_folder.invokeFactory(
            destination_type,
            id=original_licence.id,
        )
        copied_licence = getattr(destination_folder, copied_licence_id)

        for content in original_licence.objectValues():
            copied_content = api.content.copy(source=content, target=copied_licence)
            if IUrbanEvent.providedBy(content):
                eventconfigs = getattr(site.portal_urban, destination_type.lower()).eventconfigs
                copied_content.setUrbaneventtypes(getattr(eventconfigs, content.getUrbaneventtypes().id))
            copied_content.reindexObject()

        for tab in original_licence.schema.getSchemataNames():
            if tab in ['default', 'metadata']:
                continue
            fields = original_licence.schema.getSchemataFields(tab)
            for original_field in fields:
                destination_field = copied_licence.getField(original_field.getName())
                if destination_field:
                    destination_mutator = destination_field.getMutator(copied_licence)
                    value = original_field.getAccessor(original_licence)()
                    destination_mutator(value)

        original_state = api.content.get_state(original_licence)
        if original_state in states_mapping:
            new_state = states_mapping[original_state]
            workflow_tool = api.portal.get_tool('portal_workflow')
            workflow_def = workflow_tool.getWorkflowsFor(copied_licence)[0]
            workflow_id = workflow_def.getId()
            workflow_state = workflow_tool.getStatusOf(workflow_id, copied_licence)
            workflow_state['review_state'] = new_state
            workflow_tool.setStatusOf(workflow_id, copied_licence, workflow_state.copy())

        postCreationActions(copied_licence, None)

        copied_licence.reindexObject()
        return copied_licence
