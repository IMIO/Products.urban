# -*- coding: utf-8 -*-

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


contact_popup_template = utils.named_template_adapter(
    ViewPageTemplateFile('templates/contact_popup.pt'))


class UrbanReferenceBrowserPopup(ReferenceBrowserPopup):
    """
    """
    def get_creation_url(self):
        url = 'http://localhost:8081/Plone/urban/{}/createObject'.format(self.context.id)
        return url

    def get_type_name_value(self):
        val = '{}'.format(self.context.immediatelyAddableTypes[0].encode('utf-8'))
        return val

    def get_submit_value(self):
        if self.context.id == 'architects':
            valeur = 'Encoder un nouvel Architecte'
            return valeur
        elif self.context.id == 'notaries':
            valeur = 'Encoder un nouveau Notaire'
            return valeur
        elif self.context.id == 'geometricians':
            valeur = 'Encoder un nouveau Géomètre'
            return valeur
        else:
            valeur = 'Encoder nouveau'
            return valeur

    def get_submit_class(self):
        classe = 'context contenttype-{}'.format(self.context.immediatelyAddableTypes[0].encode('utf-8').lower())
        return classe
