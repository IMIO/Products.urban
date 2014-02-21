# -*- coding: utf-8 -*-

from Products.urban.browser.licence.licenceedit import LicenceEditView

from plone import api


class UrbanCertificateBaseEditView(LicenceEditView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(UrbanCertificateBaseEditView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getMacroViewName(self):
        return 'urbancertificatebase_edit'

    def getFields(self, schemata):
        """Returns a list of editable fields for the given instance
        """
        fields = []
        for field in schemata.fields():
            if field.writeable(self.context, debug=False):
                portal_urban = api.portal.get_tool('portal_urban')
                licence_config = portal_urban.getUrbanConfig(self, urbanConfigId=self.context.portal_type)
                visible = field.getName() in licence_config.getUsedAttributes() or not field.widget.condition
                fields.append({'field': field, 'visible': visible})
        return fields
