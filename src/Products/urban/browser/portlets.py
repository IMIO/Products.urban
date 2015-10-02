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
        roles = api.user.get_roles(user=api.user.get_current(), obj=self.context)
        available = 'Manager' in roles or 'Editor' in roles
        return available

    def render(self):
        return ViewPageTemplateFile('templates/portlet_urbantools.pt')(self)


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
        roles = api.user.get_roles(user=api.user.get_current(), obj=self.context)
        available = 'Manager' in roles or 'Editor' in roles
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
