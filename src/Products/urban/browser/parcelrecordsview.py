# encoding: utf-8

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as _

from Products.urban.interfaces import IGenericLicence
from Products.urban import services

from plone import api


class ParcelRecordsView(BrowserView):
    """
    This manage the view of the popup showing the licences related to some parcels
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        parcel_id = self.request.get("id", "")
        parcel = getattr(context, parcel_id, None)
        self.capakey = parcel and parcel.get_capakey() or ""
        if not self.capakey:
            plone_utils = api.portal.get_tool("plone_utils")
            plone_utils.addPortalMessage(_("Nothing to show !!!"), type="error")

    def get_related_licences_displays(self, capakey=None):
        """
        Returns the licences related to a parcel
        """
        licence_brains, capakeys, historic = self.search_licences(
            capakey or self.capakey
        )
        display = self.get_display(licence_brains)
        historic_display = self.get_historic_display(historic, licence_brains)
        return display, historic_display

    def get_display(self, licence_brains, short=False):
        context = aq_inner(self.context)
        related_items = []
        for brain in licence_brains:
            if brain.id != context.id:
                title = (short and brain.getReference) or (
                    len(brain.Title) < 40
                    and brain.Title
                    or "{}...".format(brain.Title[:40])
                )
                item_infos = {
                    "title": title,
                    "description": brain.Description,
                    "url": brain.getURL(),
                    "class": "state-{} contenttype-{}".format(
                        brain.review_state, brain.portal_type.lower()
                    ),
                }
                related_items.append(item_infos)
        return related_items

    def search_licences(self, capakey=None):
        """
        Do the search and return licence brains
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool("portal_catalog")
        capakeys = [capakey]
        session = services.cadastre.new_session()
        historic = session.query_parcel_historic(capakey)
        session.close()
        capakeys.extend(historic.get_all_capakeys())

        related_brains = catalog(
            object_provides=IGenericLicence.__identifier__,
            parcelInfosIndex=capakeys,
            sort_on="sortable_title",
        )

        return related_brains, capakeys, historic

    def get_historic_display(self, parcels_historic, related_brains):
        table = parcels_historic.table_display()

        for line in table:
            for element in line:
                if not element.display():  # ignore blanks
                    continue
                parcel = element
                licence_brains = []
                for brain in related_brains:
                    if parcel.capakey in brain.parcelInfosIndex:
                        licence_brains.append(brain)
                licences = self.get_display(licence_brains, short=True)
                setattr(parcel, "licences", licences)
        return table
