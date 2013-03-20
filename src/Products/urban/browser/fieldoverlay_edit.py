# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class FieldEditView(BrowserView):
    """
      This manage methods of CU1/CU2 specific features fields view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getFieldIds(self):
        licence_config = self.context.getLicenceConfig()
        vocname = self.request['vocname']
        specificfeatures = getattr(licence_config, vocname)
        spf_id = self.request['spf_id']
        vocterm = getattr(specificfeatures, spf_id)
        return vocterm.getRelatedFields()
