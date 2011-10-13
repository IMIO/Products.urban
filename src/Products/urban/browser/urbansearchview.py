from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import URBAN_TYPES 

class UrbanSearchView(BrowserView):
    """
      This manage the view of UrbanSearch
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def AvailableStreets(self):
        context = aq_inner(self.context)
        voc = UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", sort_on="sortable_title", 
                              inUrbanConfig=False, allowedStates=['enabled', 'disabled'])
        return voc.getDisplayList(context).sortedByValue().items()

    def getLicenceTypes(self):
        return URBAN_TYPES

class UrbanSearchMacros(BrowserView):
    """
      This manage the macros of UrbanSearch
    """
