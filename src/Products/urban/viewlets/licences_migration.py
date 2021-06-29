# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from eea.facetednavigation.interfaces import IFacetedNavigable

from imio.dashboard.utils import getDashboardQueryResult

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
        faceted_context = bool(IFacetedNavigable.providedBy(self.context))
        return faceted_context and allowed

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
        for brain in brains:
            self.copy_one_licence(brain.getObject(), 'Inspection')

        # migrate applicants to proprietaries
        portal = api.portal.get()
        root = portal.urban.inspections
        logger = logging.getLogger('urban: migrate miscdemands to inspection')
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

    def copy_one_licence(self, original_licence, destination_type):
        site = api.portal.get()
        destination_folder = getLicenceFolder(destination_type)
        duplicated_licence_id = destination_folder.invokeFactory(
            destination_type,
            id=site.generateUniqueId(destination_type),
        )
        duplicated_licence = getattr(destination_folder, duplicated_licence_id)

        for content in original_licence.objectValues():
            copied_content = api.content.copy(source=content, target=duplicated_licence)
            if IUrbanEvent.providedBy(content):
                eventconfigs = getattr(site.portal_urban, destination_type.lower()).eventconfigs
                copied_content.setUrbaneventtypes(getattr(eventconfigs, content.getUrbaneventtypes().id))
            copied_content.reindexObject()

        for tab in original_licence.schema.getSchemataNames():
            if tab in ['default', 'metadata']:
                continue
            fields = original_licence.schema.getSchemataFields(tab)
            for original_field in fields:
                destination_field = duplicated_licence.getField(original_field.getName())
                if destination_field:
                    destination_mutator = destination_field.getMutator(duplicated_licence)
                    value = original_field.getAccessor(original_licence)()
                    destination_mutator(value)

        postCreationActions(duplicated_licence, None)

        duplicated_licence.reindexObject()
        return duplicated_licence
