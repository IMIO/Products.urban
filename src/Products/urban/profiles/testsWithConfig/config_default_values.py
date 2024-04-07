# -*- coding: utf-8 -*-

from Products.urban.config import URBAN_TYPES

vocabularies_with_HTML_description = [
    "specificfeatures",
    "roadspecificfeatures",
    "locationspecificfeatures",
    "townshipspecificfeatures",
    "opinionstoaskifworks",
    "investigationarticles",
]

default_values = {
    "BuildLicence": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {
                "id": "uap",
                "title": u"UAP (permis d'urbanisme avec avis préalable du FD)",
            },
            {
                "id": "udc",
                "title": u"UDC (permis dans PCA, 'RCU, 'LOTISSEMENT, 'parfois avec demande de dérogation)",
            },
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (annexe 20) en 2 exemplaires",
            },
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "attestation_archi",
                "title": u"Attestation de l'architecte (annexe 21) en 2 exemplaires",
            },
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (annexe 20) en 2 exemplaires",
            },
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (annexe 20) en 2 exemplaires",
            },
        ],
        "pebcategories": [
            "UrbanVocabularyTerm",
            {"id": "not_applicable", "title": "peb_not_applicable"},
        ],
    },
    "ParcelOutLicence": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "lap", "title": u"LAP (permis de lotir avec avis préalable du FD)"},
        ],
        "lotusages": [
            "UrbanVocabularyTerm",
            {"id": "buildable", "title": u"Lot bâtissable"},
        ],
        "equipmenttypes": [
            "UrbanVocabularyTerm",
            {"id": "telecom", "title": u"Télécomunication"},
        ],
    },
    "UrbanCertificateOne": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "cu1", "title": u"CU1 (certificat d'urbanisme 1)"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
    },
    "UrbanCertificateTwo": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "cu2", "title": u"CU2 (certificat d'urbanisme 2)"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
        ],
    },
    "EnvClassOne": {
        "decisions": [
            "UrbanVocabularyTerm",
            {"id": "octrois", "title": u"Octrois", "extraValue": "Recevable"},
        ],
    },
    "EnvClassThree": {
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
        ],
    },
    "Division": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "dup", "title": u"DIV (Division notariale)"},
        ],
    },
    "MiscDemand": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "apct", "title": u"Avis préalable construction ou transformation"},
        ],
    },
    "Declaration": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "dup", "title": u"DUP (Déclaration Urbanistique Préalable)"},
        ],
        "articles": [
            "UrbanVocabularyTerm",
            {
                "id": "263_1_1",
                "title": u"article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins",
                "extraValue": "263 §1er 1°",
                "description": "« article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins pour autant qu’ils relèvent des actes et travaux visés à l’article 262, 4°, b, d, e et g, mais n’en remplissent pas les conditions; »",
            },
        ],
    },
    "shared_vocabularies": {
        "townshipfoldercategories": [
            "UrbanVocabularyTerm",
            URBAN_TYPES,
            {"id": "abattre", "title": u"Abattre"},
        ],
        "rubrics": [
            "Folder",
            ["EnvClassOne", "EnvClassTwo", "EnvClassThree"],
        ],
        "decisions": [
            "UrbanVocabularyTerm",
            [
                "BuildLicence",
                "ParcelOutLicence",
                "Declaration",
                "Division",
                "NotaryLetter",
                "UrbanCertificateOne",
                "UrbanCertificateTwo",
                "EnvClassThree",
                "MiscDemand",
            ],
            {"id": "favorable", "title": u"Favorable", "extraValue": "Recevable"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            ["NotaryLetter", "MiscDemand", "Division", "Declaration"],
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            ["NotaryLetter", "MiscDemand", "Division", "Declaration"],
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            ["NotaryLetter", "MiscDemand", "Division", "Declaration"],
        ],
        "inadmissibilityreasons": [
            "UrbanVocabularyTerm",
            ["EnvClassOne", "EnvClassTwo", "EnvClassThree"],
            {"id": "missing_parts", "title": u"Pièces/renseignements manquants"},
        ],
        "applicationreasons": [
            "UrbanVocabularyTerm",
            ["EnvClassOne", "EnvClassTwo", "EnvClassThree"],
            {
                "id": "new_business",
                "title": u"Mise en activité d'un établissement nouveau",
            },
        ],
        "specificfeatures": [
            "SpecificFeatureTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "schema-developpement-espace-regional",
                "title": u"Option particulière du schéma de développement de l'espace régional",
                "description": "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>",
            },
            {
                "id": "situe-en-zone",
                "title": u"Situé en Zone [...]",
                "description": "<p>est situé en [[object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                "relatedFields": ["folderZone", ""],
            },
        ],
        "roadspecificfeatures": [
            "SpecificFeatureTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "raccordable-egout",
                "title": u"Raccordable à l'égout",
                "description": "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>",
            },
        ],
        "locationspecificfeatures": [
            "SpecificFeatureTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "schema-developpement-espace-regional",
                "title": u"Option particulière du schéma de développement de l'espace régional",
                "description": "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>",
            },
        ],
        "townshipspecificfeatures": [
            "SpecificFeatureTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "zone-a-risque",
                "title": u"Se trouve dans une zone à risque",
                "description": "<p>se trouve dans une zone à risque (faible moyen élevé}, dans la cartographie Aléa d'inondation par débordement de cours d'eau - dressée dans le cadre du plan P.L.U.I.E.S et annexée à l'arrêté du Gouvernement Wallon, adopté en date du 13 juillet 2008;</p>",
                "relatedFields": ["floodingLevel", ""],
            },
        ],
        "opinionstoaskifworks": [
            "UrbanVocabularyTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "ores-gaz-electricite",
                "title": u"ORES - Gaz-Electricité",
                "description": u"<p>Adresse</p>",
            },
        ],
        "basement": [
            "UrbanVocabularyTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {
                "id": "zone-carriere",
                "title": u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les carrières souterraines",
            },
        ],
        "zip": [
            "UrbanVocabularyTerm",
            ["UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter"],
            {"id": "type-1", "title": u"Type 1: zone à forte pression foncière"},
            {
                "id": "type-2",
                "title": u"Type 2: zone de requalification des noyaux d'habitat",
            },
            {
                "id": "type-3",
                "title": u"Type 3: zons de développement global de quartier",
            },
            {"id": "type-4", "title": u"Type 4: zones de cités sociales à requalifier"},
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            ["BuildLicence", "ParcelOutLicence", "UrbanCertificateTwo"],
            {
                "id": "330-1",
                "title": u"330 1° - « [...] bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et [...] »",
                "description": "<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu'à cinquante mètres de part et d'autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 1°",
            },
        ],
        "folderdelays": [
            "UrbanDelay",
            ["BuildLicence", "ParcelOutLicence", "UrbanCertificateTwo"],
            {"id": "30j", "title": u"30 jours", "deadLineDelay": 30, "alertDelay": 20},
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            ["BuildLicence", "ParcelOutLicence", "UrbanCertificateTwo"],
            {"id": "dero-ps", "title": u"au Plan de secteur"},
        ],
        "folderbuildworktypes": [
            "UrbanVocabularyTerm",
            ["BuildLicence", "ParcelOutLicence", "UrbanCertificateTwo"],
            {
                "id": "ncmu",
                "title": u"Nouvelle construction - Maison unifamiliale",
                "extraValue": "N_UNI",
            },
        ],
    },
    "global": {
        "recoursedecisions": [
            "UrbanVocabularyTerm",
            {"id": "confirme", "title": u"Cofirmé"},
        ],
        "pcas": [
            "PcaTerm",
            {
                "id": "pca1",
                "label": u"Plan communal d'aménagement 1",
                "number": "1",
                "decreeDate": "2009/01/01",
                "decreeType": "royal",
            },
        ],
        "pashs": [
            "UrbanVocabularyTerm",
            {
                "id": "zone-epuration-collective",
                "title": u"Zone d'assainissement collectif",
            },
        ],
        "folderroadtypes": [
            "UrbanVocabularyTerm",
            {"id": "com", "title": u"Communale"},
        ],
        "folderprotectedbuildings": [
            "UrbanVocabularyTerm",
            {"id": "classe", "title": u"classé ou assimilé"},
        ],
        "folderroadequipments": [
            "UrbanVocabularyTerm",
            {"id": "eau", "title": u"distribution d'eau"},
        ],
        "folderroadcoatings": [
            "UrbanVocabularyTerm",
            {"id": "filetseau", "title": u"Filets d'eau"},
        ],
        "folderzones": [
            "UrbanVocabularyTerm",
            {"id": "zh", "title": u"zone d'habitat"},
        ],
        "rcu": [
            "UrbanVocabularyTerm",
            {"id": "rcu-aire-a", "title": u"Aire A habitat centre des villages"},
        ],
        "ssc": [
            "UrbanVocabularyTerm",
            {
                "id": "ssc-centre-ville",
                "title": u"Zone d'habitat urbain de centre-ville",
            },
        ],
        "prenu": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Revitalisation urbaine de XXX"},
        ],
        "prevu": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Rénovation urbaine de XXX"},
        ],
        "airportnoisezone": [
            "UrbanVocabularyTerm",
            {"id": "zone-expo-a", "title": u"Zone A au plan d'Exposition au bruit"},
        ],
        "noteworthytrees": [
            "UrbanVocabularyTerm",
            {"id": "arbres", "title": u"Arbres remarquables"},
        ],
        "persons_titles": [
            "PersonTitleTerm",
            {
                "id": "master",
                "title": u"Maître",
                "extraValue": "Maître",
                "abbreviation": "Me",
                "gender": "male",
                "multiplicity": "single",
            },
            {
                "id": "masters",
                "title": u"Maîtres",
                "extraValue": "Maîtres",
                "abbreviation": "Mes",
                "gender": "male",
                "multiplicity": "plural",
            },
            {
                "id": "mister",
                "title": u"Mister",
                "extraValue": "Mister",
                "abbreviation": "Mr",
                "gender": "male",
                "multiplicity": "single",
            },
            {
                "id": "madam",
                "title": u"Madam",
                "extraValue": "Madam",
                "abbreviation": "Mme",
                "gender": "female",
                "multiplicity": "single",
            },
            {
                "id": "mister_and_madam",
                "title": u"Mister and Madam",
                "extraValue": "Mister and Madam",
                "abbreviation": "Mr and Mme",
                "gender": "male",
                "multiplicity": "plural",
            },
            {
                "id": "madam_or_mister",
                "title": u"Madame/Monsieur",
                "extraValue": "Madame, Monsieur",
                "abbreviation": "Mme, Mr",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Monsieur, Madame",
            },
        ],
        "persons_grades": [
            "UrbanVocabularyTerm",
            {"id": "agent-accueil", "title": "Agent d'accueil"},
        ],
        "country": [
            "UrbanVocabularyTerm",
            {"id": "belgium", "title": "Belgique"},
            {"id": "germany", "title": "Allemagne"},
        ],
        "externaldecisions": [
            "UrbanVocabularyTerm",
            {"id": "favorable", "title": u"Favorable"},
            {"id": "favorable-conditionnel", "title": u"Favorable conditionnel"},
            {"id": "defavorable", "title": u"Défavorable"},
        ],
        "exploitationconditions": [
            "Folder",
        ],
        "foldermanagers": [
            "FolderManager",
        ],
        "streets": [
            "City",
        ],
        "globaltemplates": [
            "UrbanTemplate",
        ],
    },
}
