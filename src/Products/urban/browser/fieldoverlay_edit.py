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
        specificfeatures = licence_config.specificfeatures
        row_number = int(self.request['arg']) - 1
        spf_id = self.context.getSpecificFeatures()[row_number]['id']
        vocterm = getattr(specificfeatures, spf_id)
        fields = vocterm.extraValue.encode()
        if fields:
            return fields.split('|')
        return []
