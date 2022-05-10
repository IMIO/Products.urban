# -*- coding: utf-8 -*-

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone')


contact_popup_template = utils.named_template_adapter(
    ViewPageTemplateFile('templates/contact_popup.pt'))


class UrbanReferenceBrowserPopup(ReferenceBrowserPopup):
    """
    """
    def get_creation_url(self, portal_type):
        if self.context.id == 'urban':
            url = u'{}/{}s/createObject'.format(self.context.absolute_url(), portal_type.lower())
        else:
            url = u'{}/createObject'.format(self.context.absolute_url())
        return url

    def get_submit_value(self, portal_type):
        translated_type = translate(_(portal_type), 'plone', context=self.request)
        return u'Encoder un {}'.format(translated_type)

    def get_submit_class(self, portal_type):
        classe = 'context contenttype-{}'.format(portal_type.lower())
        return classe
