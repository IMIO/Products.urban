from plone import api
from Products.urban.interfaces import IGenericLicence


def check():
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    licences = [l.getObject() for l in licence_brains if IGenericLicence.providedBy(l.getObject())]
    invalid_licences = set()
    for licence in licences:
        invalid_parcels = []
        for parcel in licence.getParcels():
            try:
                parcel.get_capakey()
            except:
                invalid_parcels.append(parcel)
                invalid_licences.add(parcel.aq_parent)
                error_log = "<p> Parcelle invalide: {} </p>".format(parcel.Title())
                licence.setDescription(licence.Description() + error_log)
                parcel.section = None
                parcel.radical = None
                parcel.puissance = None
                parcel.exposant = None
                parcel.bis = None
                parcel.partie = None
        api.content.delete(objects=invalid_parcels)

    log = open('invalid_parcels.txt', 'w')
    for licence in invalid_licences:
        log.write(licence.Title() + '\n')
    log.close()
