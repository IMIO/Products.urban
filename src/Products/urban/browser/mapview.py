from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Acquisition import aq_inner, aq_base
from Products.urban.interfaces import IInquiry
from Products.urban.browser.urbantable import ParcelsTable


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

    def isUsingTabbing(self):
        context = aq_inner(self.context)
        portal_urban = getToolByName(context, 'portal_urban')
        return portal_urban.getUrbanConfig(context).getUseTabbingForDisplay()

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parceltable = ParcelsTable(parcels, self.request)
        parceltable.update()
        return parceltable.render()

    def getListCapaKey(self):
        """
           Return the list of capaKeys for each parcel
        """
        listCapaKey = []
        context = aq_inner(self.context)
        request = aq_inner(self.request)

        "Allow to show the map without the licence object"
        if not hasattr(aq_base(context), "getParcels"):
            return listCapaKey

        if request.get('show_old_parcel'):
            listCapaKey = ["%s%s%04d/%02d%s%03d" % (request.get('division'), request.get('section'), int(request.get('radical')),
                                                    int(request.get('bis')), request.get('exposant'), int(request.get('puissance')))]
        else:
            for parcel in self.getParcels():
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

    def getOldParcels(self):
        context = aq_inner(self.context)
        return [parcel.getHistoric().getHistoricForDisplay() for parcel in context.getParcels() if parcel.getOutdated()]

    def getParcels(self):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        if request.get('show_old_parcel'):
            return True
        return [parcel for parcel in context.getParcels() if parcel.getIsOfficialParcel() and not parcel.getOutdated()]


class FullMapView(MapView):
    """
        Display a full screen map
    """
    def __init__(self, context, request):
        super(MapView, self).__init__(context, request)

    def isUrbanUser(self):
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        is_map_user = member.has_role('UrbanMapReader')
        is_manager = member.has_role('Manager')
        return is_map_user or is_manager
