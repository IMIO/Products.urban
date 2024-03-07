print '"code division";"uid";"nom rue";"entité";"code postal"'
streets_folder = container.portal_urban.streets
division = {
    "Besonrieux": "13",
    "Boussoit": "9",
    "Haine-Saint-Paul": "5",
    "Haine-Saint-Pierre": "4",
    "Houdeng-Aimeries": "11",
    "Houdeng-Goegnies": "12",
    "La Louvière": "0",
    "Maurage": "8",
    "Saint-Vaast": "6",
    "Strépy-Bracquegnies": "10",
    "Trivières": "7",
}
for city in streets_folder.objectValues():
    for street in city.objectValues():
        line = '"%s";"%s";"%s";"%s";"%s"' % (
            division[city.Title()],
            street.UID(),
            street.getStreetName(),
            city.Title(),
            city.getZipCode(),
        )
        print line
        print "in", streets_folder.absolute_url()
        return printed
