from plone import api
from Products.urban.interfaces import IGenericLicence


def display():
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    licences = [l.getObject() for l in licence_brains if IGenericLicence.providedBy(l.getObject())]
    for licence in licences:
        address = licence.getWorkLocations()
        for wl in address:
            street_brains = catalog(UID=wl['street'])
            if not street_brains:
                return ("***FIX*** street UID in licence {} don't exist in Urban Config : "
                        " please fill a correct street in the licence work locations"
                        .format(licence.reference))
