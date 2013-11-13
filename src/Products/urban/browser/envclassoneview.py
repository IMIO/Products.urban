from Products.urban.browser.licenceview import LicenceView


class EnvClassOneView(LicenceView):
    """
      This manage the view of EnvClassOne
    """
    def __init__(self, context, request):
        super(EnvClassOneView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getMacroViewName(self):
        return 'envclassone-macros'


class EnvClassOneMacros(LicenceView):
    """
      This manage the macros of EnvClassOne
    """
