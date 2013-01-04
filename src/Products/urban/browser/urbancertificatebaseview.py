from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView

class UrbanCertificateBaseView(LicenceView):
    """
      This manage the view of UrbanCertificate and NotaryLetter Classes
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getSpecificFeatures(self, subtype=''):
        context = aq_inner(self.context)
        accessor = getattr(context, 'get%sSpecificFeatures' % subtype.capitalize())
        specific_features = accessor()
        return [spf['value'] for spf in specific_features if not spf.has_key('check') or spf['check']]

class UrbanCertificateBaseMacros(LicenceView):
    """
      This manage the macros of  UrbanCertificate and NotaryLetter Classes
    """
