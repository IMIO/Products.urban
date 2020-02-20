# encoding: utf-8

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.urban import UrbanMessage as _

from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope.formlib import form
from zope.interface import implements


class IUrbanToolsPortlet(IPortletDataProvider):
    """ A portlet listing various urban functionnalities."""


class ToolsAssignment(base.Assignment):
    implements(IUrbanToolsPortlet)

    def title(self):
        return u"Urban tools widget"


class ToolsRenderer(base.Renderer):

    @property
    def available(self):
        if api.user.is_anonymous():
            return False

        site = api.portal.get()
        if self.context == site.urban:
            context = self.context.buildlicences
        else:
            context = self.context

        roles = api.user.get_roles(user=api.user.get_current(), obj=context)
        available = 'Manager' in roles or 'Editor' in roles or 'Reader' in roles
        return available

    def site_url(self):
        portal = api.portal.get()
        url = portal.absolute_url()
        return url

    def render(self):
        return ViewPageTemplateFile('templates/portlet_urbantools.pt')(self)

    def is_opinion_editor(self):
        current_user = api.user.get_current()
        if api.user.has_permission('Manage portal'):
            return True

        user_groups = api.group.get_groups(user=current_user)
        group_ids = [g.id for g in user_groups]
        if 'opinions_editors' in group_ids:
            return True

        return False


class ToolsAddForm(base.AddForm):
    form_fields = form.Fields(IUrbanToolsPortlet)
    label = _(u"Add Urban tools Portlet")
    description = _(u"This portlet lists various urban functionnalities.")

    def create(self, data):
        return ToolsAssignment(**data)


class ToolsEditForm(base.EditForm):
    form_fields = form.Fields(IUrbanToolsPortlet)
    label = _(u"Edit Urban tools Portlet")
    description = _(u"This portlet lists various urban functionnalities.")


class IUrbanConfigPortlet(IPortletDataProvider):
    """ A portlet listing urban configuration."""


class ConfigAssignment(base.Assignment):
    implements(IUrbanConfigPortlet)

    def title(self):
        return u"Urban config widget"


class ConfigRenderer(base.Renderer):

    @property
    def available(self):
        if api.user.is_anonymous():
            return False
        if api.user.has_permission('Manage portal'):
            return True

        site = api.portal.get()
        if self.context == site.urban:
            context = self.context.buildlicences
        else:
            context = self.context

        current_user = api.user.get_current()
        roles = api.user.get_roles(user=current_user, obj=context)
        groups = [g.id for g in api.group.get_groups(user=current_user)]
        available = 'Manager' in roles or 'urban_editors' in groups or 'environment_editors' in groups or 'urban_managers' in groups
        return available

    def render(self):
        return ViewPageTemplateFile('templates/portlet_urbanconfig.pt')(self)

    def is_urban_manager(self):
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        is_manager = member.has_role('Manager') or member.has_role('Editor', api.portal.get_tool('portal_urban'))
        return is_manager


class ConfigAddForm(base.AddForm):
    form_fields = form.Fields(IUrbanConfigPortlet)
    label = _(u"Add Urban config Portlet")
    description = _(u"This portlet lists urban configuration.")

    def create(self, data):
        return ConfigAssignment(**data)


class ConfigEditForm(base.EditForm):
    form_fields = form.Fields(IUrbanConfigPortlet)
    label = _(u"Edit Urban config Portlet")
    description = _(u"This portlet lists urban configuration.")


class IUrbanScheduledLicencesPortlet(IPortletDataProvider):
    """ A portlet listing scheduled licences."""


class ScheduledLicencesAssignment(base.Assignment):
    implements(IUrbanScheduledLicencesPortlet)

    def title(self):
        return u"Urban scheduled licences widget"


class ScheduledLicencesRenderer(base.Renderer):

    @property
    def available(self):
        return True
        if api.user.is_anonymous():
            return False

        site = api.portal.get()
        if self.context == site.urban:
            context = self.context.buildlicences
        else:
            context = self.context

        roles = api.user.get_roles(user=api.user.get_current(), obj=context)
        available = 'Manager' in roles or 'Editor' in roles or 'Reader' in roles
        return available

    def site_url(self):
        portal = api.portal.get()
        url = portal.absolute_url()
        return url

    def render(self):
        return ViewPageTemplateFile('templates/portlet_scheduled_licences.pt')(self)

    def scheduled_licences_links(self):
        urban_tool = api.portal.get_tool('portal_urban')
        licence_configs = urban_tool.objectValues('LicenceConfig')
        site_url = api.portal.get().absolute_url()
        links = []

        for licence_cfg in licence_configs:
            schedule_cfg = getattr(licence_cfg, 'schedule', None)
            if schedule_cfg and schedule_cfg.enabled and not schedule_cfg.is_empty():
                portal_type = schedule_cfg.get_scheduled_portal_type()
                licence_type = portal_type.lower()
                href = '{}/urban/schedule/{}'.format(site_url, licence_type)
                klass = 'content-shortcuts contenttype-{}'.format(licence_type)
                links.append((href, klass, portal_type))

        return links


class ScheduledLicencesAddForm(base.AddForm):
    form_fields = form.Fields(IUrbanScheduledLicencesPortlet)
    label = _(u"Add Urban scheduled licences Portlet")
    description = _(u"This portlet lists scheduled licences.")

    def create(self, data):
        return ScheduledLicencesAssignment(**data)


class ScheduledLicencesEditForm(base.EditForm):
    form_fields = form.Fields(IUrbanScheduledLicencesPortlet)
    label = _(u"Edit Urban scheduled licences Portlet")
    description = _(u"This portlet lists scheduled licences.")
