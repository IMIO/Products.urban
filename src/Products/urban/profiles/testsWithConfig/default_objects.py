# -*- coding: utf-8 -*-

default_objects = {
    "notaries": [
        "Notary",
        {
            "id": "notary1",
            "name1": "NotaryName1",
            "name2": "NotarySurname1",
            "email": "maitre.duchnoque@notaire.be",
        },
    ],
    "geometricians": [
        "Geometrician",
        {
            "id": "geometrician1",
            "name1": "GeometricianName1",
            "name2": "GeometricianSurname1",
            "email": "geo.trouvetout@geometre.be",
        },
    ],
    "parcellings": [
        "ParcellingTerm",
        {
            "id": "p1",
            "title": u"Lotissement 1 (André Ledieu - 01/01/2005 - 10)",
            "label": "Lotissement 1",
            "subdividerName": "André Ledieu",
            "authorizationDate": "2005/01/01",
            "approvaleDate": "2005/01/12",
            "numberOfParcels": 10,
        },
    ],
    "foldermanagers": [
        "FolderManager",
        {
            "id": "foldermanager1",
            "name1": "Dumont",
            "name2": "Jean",
            "grade": "agent-technique",
            "ploneUserId": "urbanmanager",
        },
    ],
}
