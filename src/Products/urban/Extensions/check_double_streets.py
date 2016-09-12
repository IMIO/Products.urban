from plone import api


def count():
    cat = api.portal.get_tool('portal_catalog')

    all_streets = set([brain.getObject() for brain in cat(portal_type='Street')])
    already_checked = set([])
    result = {}
    referenced_licences = {}

    for street in all_streets:
        if street not in already_checked:
            street_title = street.getStreetName()
            doubles_street = cat(street_name=street_title, portal_type='Street')
            doubles_street = [s.getObject() for s in doubles_street if s.UID != street.UID()]
            doubles_street = [s for s in doubles_street if str_cpm(s.Title(), street.Title())]
            if doubles_street and street_title:
                doubles = doubles_street + [street]
                print street_title, len(doubles)

                result[street_title] = doubles
                for double in doubles:
                    already_checked.add(double)
                referenced_licences.update(get_licences(doubles))

    streets_with_doubles = len(result)
    total_of_double_streets = sum([len(v) for v in result.values()])
    total_of_referenced_licences = sum([len(v) for v in referenced_licences.values()])
    print "found {} streets with doubles for a total of {} streets referenced by {} licences".format(
        streets_with_doubles, total_of_double_streets, total_of_referenced_licences
    )


def str_cpm(string_1, string_2):
    return string_1.replace(' ', '') == string_2.replace(' ', '')


def get_licences(streets):
    cat = api.portal.get_tool('portal_catalog')
    referenced_licences = {}

    for street in streets:
        licences = [b.getObject() for b in cat(StreetsUID=street.UID())]
        if licences:
            referenced_licences[street] = licences
            msg = "'{}' used by {}".format(
                street.Title(), ', '.join(["'" + l.getReference() + "'" for l in licences])
            )
            print msg
    return referenced_licences
