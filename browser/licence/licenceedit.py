# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView


class LicenceEditView(BrowserView):
    """
      This manage methods common in all licences view
    """
    def __init__(self, context, request):
        super(LicenceEditView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getLicenceConfig(self):
        context = aq_inner(self.context)
        return context.getLicenceConfig()

    def getTabs(self):
        return self.getLicenceConfig().getActiveTabs()

    def getEditFieldsMacro(self):
        macro_name = 'editLicenceFieldsMacro'
        return self.getMacro(macro_name)

    def getEditFieldsWithoutTabbingMacro(self):
        macro_name = 'editLicenceFieldsNoTabbingMacro'
        return self.getMacro(macro_name)

    def getEditFieldsWithTabbingMacro(self):
        macro_name = 'editLicenceFieldsWithTabbingMacro'
        return self.getMacro(macro_name)

    def getMacro(self, macro_name):
        context = aq_inner(self.context)
        macros_view = self.getMacroViewName()
        macro = context.unrestrictedTraverse('{view}/{macro}'.format(view=macros_view, macro=macro_name))
        return macro

    def getMacroViewName(self):
        return 'licenceedit'
