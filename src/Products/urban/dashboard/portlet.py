# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.formlib import form
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban.dashboard import utils


class ICategorySwitchPortlet(IPortletDataProvider):
    """ A portlet that shows a switch button between procedure categories """


class Assignment(base.Assignment):
    implements(ICategorySwitchPortlet)

    @property
    def title(self):
        return u'Category Switch'


class Renderer(base.Renderer):

    def render(self):
        return ViewPageTemplateFile('templates/portlet_categoryswitch.pt')(self)

    @property
    def available(self):
        return True

    @property
    def category(self):
        return utils.get_procedure_category(self.context, self.request)

    @property
    def url(self):
        return api.portal.get().absolute_url()

    @property
    def collection_uid(self):
        brains = api.content.find(
            id="collection_all_licences",
            portal_type="DashboardCollection",
        )
        if not brains:
            return ""
        return brains[0].UID


class AddForm(base.AddForm):
    form_fields = form.Fields(ICategorySwitchPortlet)
    label = _(u"Add Category Switch Portlet")
    description = _(u"This portlet shows a switch button between procedure categories.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ICategorySwitchPortlet)
    label = _(u"Edit Category Switch Portlet")
    description = _(u"This portlet shows a switch button between procedure categories.")
