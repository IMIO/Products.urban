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
        cfg = self.getLicenceConfig()
        available_tabs = self.context.schema.getSchemataNames()
        tabs = []
        for active_tab in cfg.getActiveTabs():
            tab = {
                "id": "urban_{}".format(active_tab["value"]),
                "display_name": active_tab["display_name"],
            }
            if tab["id"] in available_tabs:
                tabs.append(tab)
        return tabs

    def getEditFieldsMacro(self):
        macro_name = "editLicenceFieldsMacro"
        return self.getMacro(macro_name)

    def getEditFieldsWithoutTabbingMacro(self):
        macro_name = "editLicenceFieldsNoTabbingMacro"
        return self.getMacro(macro_name)

    def getEditFieldsWithTabbingMacro(self):
        macro_name = "editLicenceFieldsWithTabbingMacro"
        return self.getMacro(macro_name)

    def getMacro(self, macro_name):
        context = aq_inner(self.context)
        macros_view = self.getMacroViewName()
        macro = context.unrestrictedTraverse(
            "{view}/{macro}".format(view=macros_view, macro=macro_name)
        )
        return macro

    def getMacroViewName(self):
        return "licenceedit"


class CODT_IntegratedLicenceEditView(LicenceEditView):
    """ """

    def getTabs(self):
        cfg = self.getLicenceConfig()
        available_tabs = self.context.schema.getSchemataNames()
        tabs = []
        for active_tab in cfg.getActiveTabs():
            tab = {
                "id": "urban_{}".format(active_tab["value"]),
                "display_name": active_tab["display_name"],
            }
            if tab["id"] in available_tabs:
                # only display environment tab if unique or environment licence
                if (
                    tab["id"] == "urban_environment"
                    and "dgo3" not in self.context.getRegional_authority()
                ):
                    continue
                tabs.append(tab)
        return tabs
