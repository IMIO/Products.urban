# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.urban.browser.licence.licenceedit import LicenceEditView


class UrbanCertificateBaseEditView(LicenceEditView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(UrbanCertificateBaseEditView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getEditFieldsMacro(self):
        context = aq_inner(self.context)
        macro_name = 'editLicenceFieldsMacro'
        macros_view = 'urbancertificatebase_edit'
        macro = context.unrestrictedTraverse('{view}/{macro}'.format(view=macros_view, macro=macro_name))
        return macro

    def getFields(self, schemata):
        """Returns a list of editable fields for the given instance
        """
        fields = []
        for field in schemata.fields():
            if field.writeable(self.context, debug=False):
                licence_config = self.context.getLicenceConfig()
                visible = field.getName() in licence_config.getUsedAttributes() or not field.widget.condition
                fields.append({'field': field, 'visible': visible})
        return fields
