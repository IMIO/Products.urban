# -*- coding: utf-8 -*-

from datetime import date

default_objects = {
    "notaries": [
        "Notary",
        {
            "id": "notary1",
            "name1": "NotaryName1",
            "name2": "NotarySurname1",
            "email": "maitre.duchnoque@notaire.be",
        },
        {
            "id": "notary2",
            "name1": "André",
            "name2": "Sanfrapper",
            "email": "maitre.andre@notaire.be",
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
        "Parcelling",
        {
            "id": "p1",
            "label": u"Lotissement 1",
            "subdividerName": u"André Ledieu",
            "authorizationDate": date(2005, 1, 1),
            "approvalDate": date(2005, 1, 12),
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
