from plone import api
from Products.urban.interfaces import IGenericLicence


def check_licences_with_no_parcels():
    catalog = api.portal.get_tool('portal_catalog')
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__)
    licences = [l.getObject() for l in licence_brains]
    licences = [l for l in licences if not l.getParcels()]
    log = open('no_parcels.txt', 'w')
    for licence in licences:
        log.write(licence.Title() + '\n')
    log.close()


def remove_invalid_parcels():
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


def fix_parcels_division():
    catalog = api.portal.get_tool('portal_catalog')
    portal_urban = api.portal.get_tool('portal_urban')
    divisions_by_name = dict([(row['name'], row['division']) for row in portal_urban.getDivisionsRenaming()])
    encoded_divisions_by_name = dict([(row['name'].decode('utf-8'), row['division']) for row in portal_urban.getDivisionsRenaming()])
    divisions_by_name.update(encoded_divisions_by_name)

    wrong_values = [v for v in catalog.Indexes['parcelInfosIndex'].uniqueValues() if v and not v[0].isdigit()]
    licence_brains = catalog(object_provides=IGenericLicence.__identifier__, parcelInfosIndex=wrong_values)

    for licence_brain in licence_brains:
        licence = licence_brain.getObject()
        for parcel in licence.getParcels():
            if not parcel.division.isdigit() and parcel.division in divisions_by_name:
                print "fixed parcel %s" % parcel.capakey
                parcel.division = str(divisions_by_name[parcel.division])
            elif not parcel.division.isdigit():
                print "COULD NOT fix parcel %s" % parcel.capakey
        licence.reindexObject(idxs=['parcelInfosIndex'])
