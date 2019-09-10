# encoding: utf-8

from Products.Five import BrowserView

from Products.urban.interfaces import IGenericLicence

from plone import api


class FixStreetsView(BrowserView):
    """
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """
          Parse licences and check if the linked street UID exist in streets config.
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
        licences = [l.getObject() for l in licence_brains if IGenericLicence.providedBy(l.getObject())]
        for licence in licences:
            address = licence.getWorkLocations()
            for wl in address:
                street_brains = catalog(UID=wl['street'])
                if not street_brains:
                    wl['street'] = ''
                    licence.setWorkLocations(address)
                    print("***FIX*** street UID in licence {} don't exist in Urban Config : street UID is set to empty,"
                          " please fill a correct street in the licence work locations"
                          .format(licence.reference))
