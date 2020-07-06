from plone import api


def fix_streets():
    cat = api.portal.get_tool("portal_catalog")

    all_streets = set([brain.getObject() for brain in cat(portal_type="Street")])
    already_checked = set([])

    for street in all_streets:
        if street not in already_checked:
            street_title = street.getStreetName()
            doubles_street = cat(street_name=street_title, portal_type="Street")
            doubles_street = [
                s.getObject() for s in doubles_street if s.UID != street.UID()
            ]
            doubles_street = [
                s for s in doubles_street if str_cpm(s.Title(), street.Title())
            ]
            if doubles_street and street_title:
                doubles = doubles_street + [street]
                enabled_streets = [
                    street
                    for street in doubles
                    if api.content.get_state(street) == "enabled"
                ]
                disabled_streets = [
                    street
                    for street in doubles
                    if api.content.get_state(street) == "disabled"
                ]
                active_doubles = len(enabled_streets)
                for enabled_street in enabled_streets:
                    api.content.transition(obj=enabled_street, to_state="disabled")
                double_street = doubles[0]
                new_street_id = "{}{}".format(
                    double_street.id[-1] in [str(i) for i in range(len(doubles))]
                    and double_street.id[0:-1]
                    or double_street.id,
                    str(len(doubles)),
                )
                new_street = api.content.create(
                    container=double_street.aq_parent,
                    type=double_street.portal_type,
                    id=new_street_id,
                    title=double_street.Title(),
                    streetName=double_street.getStreetName(),
                    startDate=double_street.getStartDate(),
                    regionalRoad=double_street.getRegionalRoad(),
                )
                new_street.reindexObject()
                print "created new street %s" % new_street.Title()
                for double in doubles:
                    already_checked.add(double)


def fix():
    cat = api.portal.get_tool("portal_catalog")

    all_streets = set([brain.getObject() for brain in cat(portal_type="Street")])
    already_checked = set([])

    for street in all_streets:
        if street not in already_checked:
            street_title = street.getStreetName()
            doubles_street = cat(street_name=street_title, portal_type="Street")
            doubles_street = [
                s.getObject() for s in doubles_street if s.UID != street.UID()
            ]
            doubles_street = [
                s for s in doubles_street if str_cpm(s.Title(), street.Title())
            ]
            if doubles_street and street_title:
                doubles = doubles_street + [street]
                enabled_streets = [
                    street
                    for street in doubles
                    if api.content.get_state(street) == "enabled"
                ]
                disabled_streets = [
                    street
                    for street in doubles
                    if api.content.get_state(street) == "disabled"
                ]
                active_doubles = len(enabled_streets)
                if active_doubles != 1:
                    print "theres still enabled %i double streets for: %s" % (
                        active_doubles,
                        street_title,
                    )
                    continue
                else:
                    licences_to_fix = get_licences(disabled_streets)
                    if licences_to_fix:
                        if active_doubles == 1:
                            fix_licences(licences_to_fix, enabled_streets[0])
                        else:
                            print "there is no enabled street to use as a fix"

                for double in doubles:
                    already_checked.add(double)


def fix_licences(licences_to_fix, right_street):
    for wrong_street, licences in licences_to_fix.iteritems():
        for licence in licences:
            fixed_address = licence.getWorkLocations()
            for street in fixed_address:
                if street["street"] == wrong_street.UID():
                    street["street"] = right_street.UID()
                    licence.setWorkLocations(fixed_address)
                    print "fixed licence %s" % licence.Title()
                    break


def str_cpm(string_1, string_2):
    return string_1.replace(" ", "") == string_2.replace(" ", "")


def get_licences(streets):
    cat = api.portal.get_tool("portal_catalog")
    referenced_licences = {}

    for street in streets:
        licences = [b.getObject() for b in cat(StreetsUID=street.UID())]
        if licences:
            referenced_licences[street] = licences
    return referenced_licences
