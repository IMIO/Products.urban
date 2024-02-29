# -*- coding: utf-8 -*-

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
        {
            "id": "p2",
            "title": u"Lotissement 2 (Ets Tralala - 01/06/2007 - 8)",
            "label": "Lotissement 2",
            "subdividerName": "Ets Tralala",
            "authorizationDate": "2007/06/01",
            "approvaleDate": "2007/06/12",
            "numberOfParcels": 8,
        },
        {
            "id": "p3",
            "title": u"Lotissement 3 (SPRL Construction - 02/05/2001 - 15)",
            "label": "Lotissement 3",
            "subdividerName": "SPRL Construction",
            "authorizationDate": "2001/05/02",
            "approvaleDate": "2001/05/10",
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
