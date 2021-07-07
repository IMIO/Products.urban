# -*- coding: utf-8 -*-

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


architect_popup_template = utils.named_template_adapter(
    ViewPageTemplateFile('templates/architect_popup.pt'))

notary_popup_template = utils.named_template_adapter(
    ViewPageTemplateFile('templates/notary_popup.pt'))


class UrbanReferenceBrowserPopup(ReferenceBrowserPopup):
    """
    """
    def get_creation_url(self):
        url = 'http://localhost:8081/Plone/urban/{}/createObject'.format(self.context.id)
        return url

    def get_type_name_value(self):
        val = '{}'.format(''.join(self.context.immediatelyAddableTypes).encode('utf-8'))
        return val
