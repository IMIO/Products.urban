# -*- coding: utf-8 -*-

from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


architect_popup_template = utils.named_template_adapter(
    ViewPageTemplateFile('templates/architect_popup.pt'))


class UrbanReferenceBrowserPopup(ReferenceBrowserPopup):
    """
    """
