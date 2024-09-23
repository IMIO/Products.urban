# -*- coding: utf-8 -*-

from datetime import date

default_objects = {
    "notaries": [
        "Notary",
        {
            "id": "notary1",
            "name1": "NotaryName1",
            "name2": "NotarySurname1",
            "email": "maitre.duchnoque@imio.be",
        },
        {
            "id": "notary2",
            "name1": "NotaryName2",
            "name2": "NotarySurname2",
            "email": "kawabounga@gmail.com",
        },
        {
            "id": "notary3",
            "name1": "NotaryName3",
            "name2": "NotarySurname3",
            "email": "nono.robot@notaire.be",
        },
    ],
    "geometricians": [
        "Geometrician",
        {
            "id": "geometrician1",
            "name1": "GeometricianName1",
            "name2": "GeometricianSurname1",
        },
        {
            "id": "geometrician2",
            "name1": "GeometricianName2",
            "name2": "GeometricianSurname2",
        },
        {
            "id": "geometrician3",
            "name1": "GeometricianName3",
            "name2": "GeometricianSurname3",
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
        {
            "id": "p2",
            "label": u"Lotissement 2",
            "subdividerName": u"Ets Tralala",
            "authorizationDate": date(2007, 6, 1),
            "approvalDate": date(2007, 6, 12),
            "numberOfParcels": 8,
        },
        {
            "id": "p3",
            "label": u"Lotissement 3",
            "subdividerName": u"SPRL Construction",
            "authorizationDate": date(2001, 5, 2),
            "approvalDate": date(2001, 5, 10),
            "numberOfParcels": 15,
        },
    ],
    "foldermanagers": [
        "FolderManager",
        {
            "id": "foldermanager1",
            "personTitle": "mister",
            "name1": "Dumont",
            "name2": "Jean",
            "grade": "agent-technique",
            "ploneUserId": "admin",
        },
        {
            "id": "foldermanager2",
            "personTitle": "mister",
            "name1": "Schmidt",
            "name2": "Alain",
            "grade": "directeur-general",
        },
        {
            "id": "foldermanager3",
            "personTitle": "mister",
            "name1": "Robert",
            "name2": "Patrick",
            "grade": "responsable-administratif",
        },
    ],
}
