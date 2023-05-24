# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.urban.config import URBAN_TYPES
from Products.urban import utils

from collective.eeafaceted.collectionwidget.browser.views import RenderTermView

from plone import api


class RenderLicenceTermView(RenderTermView):

    def __call__(self, term, category, widget):
        self.term = term
        self.category = category
        self.widget = widget
        self.collection = term.value
        collection_id = self.collection.split("/")[-1]
        for urban_type in URBAN_TYPES:
            if 'collection_' + urban_type.lower() == collection_id:
                self.licence_type = urban_type
                return ViewPageTemplateFile("templates/licence_term.pt")(self)
        return self.index()

    def is_schedule_context(self):
        return 'schedule' in self.request.getURL()

    def get_licence_creation_URL(self, licence_type):
        context = aq_inner(self.context)
        base_url = context.absolute_url()
        folder_id = utils.getLicenceFolderId(licence_type)
        url = '{base_url}/{folder_id}/createObject?type_name={licence_type}'.format(
            base_url=base_url, folder_id=folder_id, licence_type=licence_type)
        return url

    def get_add_licence_link(self, licence_type):
        """ """
        member = api.user.get_current()
        context = aq_inner(self.context)
        portal_types = api.portal.get_tool('portal_types')
        meta_type = portal_types[licence_type].content_meta_type
        if not member.has_permission('urban: Add {}'.format(meta_type), context):
            return ''

        href = self.get_licence_creation_URL(licence_type)
        link_template = (
            u'<a href="{href}" id="create-{licence_type}-link">'
            u'<img class="urban-add-icon" src="icon_add.gif" /></a>'
        )
        link = link_template.format(
            href=href,
            licence_type=licence_type,
        )
        return link

    def get_link_class(self, licence_type):
        return "content-shortcuts contenttype-{}".format(licence_type.lower())

    def display_number_of_items(self):
        """If true, display the number of items in the collection."""
        return False
