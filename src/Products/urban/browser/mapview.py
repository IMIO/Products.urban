# -*- coding: utf-8 -*-

from Acquisition import aq_inner, aq_base

from Products.CMFPlone import PloneMessageFactory as _
from Products.Five import BrowserView
from Products.urban.config import MAP_VIEWER_CFG
from Products.urban.config import URBANMAP_CFG
from Products.urban.config import NIS
from Products.urban.fingerpointing import map_logger
from Products.urban.interfaces import IInquiry
from Products.urban.browser.table.urbantable import ParcelsTable

from plone import api


class MapView(BrowserView):
    """
      This manage the view of maps displayed on licences and urbanInquiryEvents
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)
        plone_utils = api.portal.get_tool('plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_an_applicant'), type="warning")

    def __call__(self, **kwargs):
        map_logger.log_map_access(self.context, self.request)
        map_call = super(MapView, self).__call__(**kwargs)
        return map_call

    def isUsingTabbing(self):
        context = aq_inner(self.context)
        portal_urban = api.portal.get_tool('portal_urban')
        return portal_urban.getLicenceConfig(context).getUseTabbingForDisplay()

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parceltable = ParcelsTable(self.context, self.request, values=parcels)
        parceltable.update()
        return parceltable.render()

    def getMapConfig(self):
        """
        """
        city_name = URBANMAP_CFG.urbanmap.get('imiomap_name', '')
        directory = self.get_map_directory()
        urbanmap_host = URBANMAP_CFG.urbanmap.get('url', '')
        script = """
            var dojoConfig = {{
            async: true,
            parseOnLoad: true,
            isDebug: false,
            locale: 'fr',
            configBasePath: '//{}/static/{}/{}',
            packages: [{{
            name: 'exemple',
            location: '//{}/static/widget'
            }},{{
            name: 'urbanmap',
            location: '//{}/static/urbanmap'
            }}]
            }};
            """.format(urbanmap_host, city_name, directory, urbanmap_host, urbanmap_host)
        return script

    def get_map_directory(self):
        return 'fr'

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
                if isinstance(capaKey, unicode):
                    capaKey = capaKey.encode('utf-8')
                listCapaKey.append(capaKey)

        return listCapaKey

    def getOldParcels(self):
        return []
        context = aq_inner(self.context)
        return [parcel.get_historic() for parcel in context.getParcels() if parcel.getOutdated()]

    def getListProprietariesCapaKey(self):
        """
           Return the list of capaKeys for each parcel of concerned proprietaries
        """
        listCapaKey = []
        context = aq_inner(self.context)

        "Allow to show the map without the licence object"
        if not hasattr(aq_base(context), "getParcels"):
            return listCapaKey

        # add the inquiry parcels if possible
        if IInquiry.providedBy(context):
            # get last inquiry
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

    def getParcels(self):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        if request.get('show_old_parcel'):
            return True
        return [parcel for parcel in context.getParcels() if parcel.getIsOfficialParcel() and not parcel.getOutdated()]

    def get_mapviewer_url(self):
        url = MAP_VIEWER_CFG.viewer.get('url', '')
        return url

    def get_mapviewer_js_id(self):
        js_id = MAP_VIEWER_CFG.viewer.get('javascript_id', '')
        return js_id

    def get_urbanmap_url(self):
        url = URBANMAP_CFG.urbanmap.get('url', '')
        return url

    def get_NIS(self):
        return NIS


class FullMapView(MapView):
    """
        Display a full screen map
    """
    def __init__(self, context, request):
        super(MapView, self).__init__(context, request)

    def isUrbanUser(self):
        member = api.user.get_current()
        is_map_user = member.has_role('UrbanMapReader')
        is_manager = member.has_role('Manager')
        return is_map_user or is_manager

    def get_map_directory(self):
        return 'frfullmap'
