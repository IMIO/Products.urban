# -*- coding: utf-8 -*-
from collective.documentgenerator.browser.generation_view import MailingLoopPersistentDocumentGenerationView
from Products.CMFPlone.utils import safe_unicode

from Products.urban.setuphandlers import _


class UrbanMailingLoopPersistentDocumentGenerationView(MailingLoopPersistentDocumentGenerationView):
    """
    """

    def _get_title(self, doc_name, gen_context):
        splitted_name = doc_name.split('.')
        extension = splitted_name[-1]
        returned_title = u"{}, {}".format(_('urban_mailing_file_prefix'), safe_unicode(self.document.title))
        return returned_title, extension
