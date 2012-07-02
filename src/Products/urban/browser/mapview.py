from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Acquisition import aq_inner, aq_base
from Products.urban.interfaces import IInquiry

class MapView(BrowserView):
    """
      This manage the view of maps displayed on licences and urbanInquiryEvents
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

    def getListCapaKey(self):
        """
           Return the list of capaKeys for each parcel
        """
        listCapaKey = []
        context = aq_inner(self.context)
        
        "Allow to show the map without the licence object"
        if not hasattr(aq_base(context), "getParcels"):
            return listCapaKey
        
        for parcel in context.getParcels():
            divisioncode = parcel.getDivisionCode()
            section = parcel.getSection()
            radical = parcel.getRadical()
            puissance = parcel.getPuissance()
            exposant = parcel.getExposant()
            bis = parcel.getBis()
            if not puissance:
                puissance = 0
            if not exposant:
                exposant = "_"
            if not bis:
                bis = 0
#            nis section (radical 0x) / (bis 0x) (exposant si blanc _)  (puissance 00x)
            try:
                capaKey = "%s%s%04d/%02d%s%03d" % (divisioncode, section, int(radical), int(bis), exposant, int(puissance))
            except ValueError:
                capaKey = ""
            listCapaKey.append(capaKey)

        return listCapaKey

    def getListProprietariesCapaKey(self):
        """
           Return the list of capaKeys for each parcel of concerned proprietaries
        """
        listCapaKey = []
        context = aq_inner(self.context)

        "Allow to show the map without the licence object"
        if not hasattr(aq_base(context), "getParcels"):
            return listCapaKey

        #add the inquiry parcels if possible
        if IInquiry.providedBy(context):
            #get last inquiry
            lastInquiry = context.getLastInquiry()
            if lastInquiry:
                # only display active parcels on the map
                for parcel in lastInquiry.getParcels(onlyActive=True):
                    divisioncode = parcel.getDivisionCode()
                    section = parcel.getSection()
                    radical = parcel.getRadical()
                    puissance = parcel.getPuissance()
                    exposant = parcel.getExposant()
                    bis = parcel.getBis()
                    if not puissance:
                        puissance = 0
                    if not exposant:
                        exposant = "_"
                    if not bis:
                        bis = 0
                    try:
                        capaKey = "%s%s%04d/%02d%s%03d" % (divisioncode, section, int(radical), int(bis), exposant, int(puissance))
                    except ValueError:
                        capaKey = ""
                    listCapaKey.append(capaKey)
        return listCapaKey

class FullMapView(MapView):
    """
        Display a full screen map
    """
    def __init__(self, context, request):
        super(MapView, self).__init__(context, request)
        
class MapMacros(BrowserView):
    """
      This manage the macros of Map
    """        