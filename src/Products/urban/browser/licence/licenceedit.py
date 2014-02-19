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

    def getTabs(self):
        return self.getLicenceConfig().getActiveTabs()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = '{}_macro'.format(tab)
        macros_view = self.getMacroViewName()
        macro = context.unrestrictedTraverse('{view}/{macro}'.format(view=macros_view, macro=macro_name))
        return macro

    def getMacroViewName(self):
        return 'licencetabs-macros'
