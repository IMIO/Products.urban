# -*- coding: utf-8 -*-
from datetime import datetime
from Products.urban.config import URBAN_TYPES

codt_2024_start_validity_date = datetime(2024, 4, 1)

vocabularies_with_HTML_description = [
    "specificfeatures",
    "roadspecificfeatures",
    "locationspecificfeatures",
    "townshipspecificfeatures",
    "opinionstoaskifworks",
    "investigationarticles",
]

default_values = {
    "CODT_BuildLicence": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "30j", "title": u"30 jours", "deadLineDelay": 30, "alertDelay": 20},
            {"id": "60j", "title": u"60 jours", "deadLineDelay": 60, "alertDelay": 20},
            {"id": "75j", "title": u"75 jours", "deadLineDelay": 70, "alertDelay": 20},
            {
                "id": "105j",
                "title": u"105 jours",
                "deadLineDelay": 105,
                "alertDelay": 20,
            },
            {
                "id": "115j",
                "title": u"115 jours",
                "deadLineDelay": 115,
                "alertDelay": 20,
            },
            {
                "id": "145j",
                "title": u"145 jours",
                "deadLineDelay": 145,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "foldercategories": [
            "UrbanVocabularyTerm",
            {
                "id": "uco",
                "title": u"UCO: permis d’urbanisme du Collège avec AVIS du FD (sans «écart»)",
            },
            {
                "id": "uco-d",
                "title": u"UCO/D: permis d'urbanisme avec dérogation du FD pour Plan Secteur / norme GRU ",
            },
            {
                "id": "uco-a",
                "title": u"UCO/A: permis d’urbanisme du Collège avec avis FACULTATIF du FD",
            },
            {"id": "uco-pd", "title": u"UCO/PD : permis d’urbanisme direct du Collège"},
            {
                "id": "uco-fd",
                "title": u"UCO/ED : permis avec écart et/ou dérogation Plan Secteur / norme GRU",
            },
            {
                "id": "AO",
                "title": u"/AO: Permis d’urbanisme communal avec avis obligatoire du FD",
                "description": u"<p>/AO: Permis d’urbanisme communal avec avis obligatoire du FD<br />Pour le cas visé Art. D.IV.15, Al. 1er, et D.IV.17.</p>",
                "extraValue": "AO",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "AF",
                "title": u"/AF: Permis d’urbanisme communal avec avis facultatif du FD",
                "description": u"<p>/AF: Permis d’urbanisme communal avec avis facultatif du FD<br />Pour le cas visé à l’Art. D.IV.14, Al. 2 et à la demande du Co</p>",
                "extraValue": "AF",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "PIL",
                "title": u"/PIL: Permis d’urbanisme communal RELATIF a DES PROJETS D’impact limité.",
                "description": u"<p>/PIL: Permis d’urbanisme communal RELATIF a DES PROJETS D’impact limité<br />Pour le cas visé à l’Art. R.IV. 1-1 TABLEAU et DISPENSÉ AVIS obligatoire </p>",
                "extraValue": "PIL",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "SA",
                "title": u"/SA: Permis d’urbanisme communal sans avis du FD (hors du champ d’application du R.IV. 1-1 tableau)",
                "description": u"<p>/SA: Permis d’urbanisme communal sans avis du FD (hors du champ d’application du R.IV. 1-1 tableau)<br />DISPENSÉ AVIS obligatoire du FD, Art. D.IV. 16, Al. 1, 1° et 2°</p>",
                "extraValue": "SA",
                "startValidity": codt_2024_start_validity_date,
            },
            {"id": "inconnu", "title": u"Inconnu"},
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {
                "id": "annexe4",
                "title": u"Annexe 4 - Demande de permis avec concours d'un architecte",
            },
            {
                "id": "annexe5",
                "title": u"Annexe 5 - Modification de la destination ou modification de la répartition des surfaces de vente",
            },
            {
                "id": "annexe6",
                "title": u"Annexe 6 - Modification sensible du relief du sol - dépôt de véhicules, de mitrailles, de matériaux ou de déchets - installations mobiles - travaux d'aménagement au sol aux abords d'une construction autorisée",
            },
            {
                "id": "annexe7",
                "title": u"Annexe 7 - Boisement - déboisement - abattage - culture de sapins de Noël - modification de l'aspect d'un ou plusieurs arbres ou haies remarquables - défrichement - modification de la végétation",
            },
            {"id": "annexe8", "title": u"Annexe 8 - Travaux techniques"},
            {
                "id": "annexe9",
                "title": u"Annexe 9 - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
            {
                "id": "div_16_1a",
                "title": u"DIV.16 1° a) SD pluricommunal ou SDC qui vise l’optimisation spatiale (uniquement les actes et travaux entièrement dans une centralité)",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "div_16_1b",
                "title": u"DIV.16 1° b) une commission communale, un GCU et soit : (1) SD pluricommunal, (2) SDC, (3) SD pluricommunal et un SDC qui a partiellement cessé de produire ses effets",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "div_16_1c",
                "title": u"DIV.16 1° c) SOL",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "div_16_1d",
                "title": u"DIV.16 1° d) permis d’urbanisation non périmé",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "div_16_2",
                "title": u"DIV.16 2° pas d’écart par rapport aux schémas, à la carte d’affectation des sols, aux guides d’urbanisme ou au permis d’urbanisation, si entièrement dans une zone d’enjeu communal",
                "startValidity": codt_2024_start_validity_date,
            },
            {
                "id": "div_16_3",
                "title": u"DIV 16 3° pas d’écart par rapport à la carte d’affectation des sols ou au GRU",
                "startValidity": codt_2024_start_validity_date,
            },
        ],
    },
    "CODT_ParcelOutLicence": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "30j", "title": u"30 jours", "deadLineDelay": 30, "alertDelay": 20},
            {"id": "60j", "title": u"60 jours", "deadLineDelay": 60, "alertDelay": 20},
            {"id": "75j", "title": u"75 jours", "deadLineDelay": 70, "alertDelay": 20},
            {
                "id": "105j",
                "title": u"105 jours",
                "deadLineDelay": 105,
                "alertDelay": 20,
            },
            {
                "id": "115j",
                "title": u"115 jours",
                "deadLineDelay": 115,
                "alertDelay": 20,
            },
            {
                "id": "145j",
                "title": u"145 jours",
                "deadLineDelay": 145,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "foldercategories": [
            "UrbanVocabularyTerm",
            {
                "id": "uco",
                "title": u"Hors SDC/SOL/GCU - UCO: permis d’urbanisme du Collège avec AVIS du FD (sans «écart»)",
            },
            {
                "id": "uco-d",
                "title": u"Hors SDC/SOL/GCU – UCO/D: permis d'urbanisme avec dérogation du FD pour Plan Secteur / norme GRU ",
            },
            {
                "id": "uco-a",
                "title": u"Dans SDC/SOL/GCU - UCO/A: permis d’urbanisme du Collège avec avis FACULTATIF du FD",
            },
            {
                "id": "uco-pd",
                "title": u"Dans SDC/SOL/GCU – UCO/PD : permis d’urbanisme direct du Collège",
            },
            {
                "id": "uco-fd",
                "title": u"Dans SDC/SOL/GCU – UCO/ED : permis avec écart et/ou dérogation Plan Secteur / norme GRU",
            },
            {"id": "inconnu", "title": u"Inconnu"},
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
            {
                "id": "div_40_alinea_2_dash_1",
                "title": u"D.IV.40 Alinéa 2/1",
                "extraValue": u"D.IV.40 Alinéa 2/1",
                "description": u"""<p>Les demandes visant à implanter un commerce au sens de l'article D.IV.4, alinéa 1er, 8°, sont soumises à enquête publique, sauf lorsque la demande porte sur l'implantation d'un commerce de quatre-cents mètres carrés et moins soumis à permis en exécution de l'article D.IV.4, alinéa 4. </p>""",
                "startValidity": codt_2024_start_validity_date,
            }
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {
                "id": "annexe4",
                "title": u"D.IV.15. alinéa 1, 1° commune décentralisée",
            },
            {
                "id": "annexe5",
                "title": u"D.IV.15. alinéa 1, 2° SOL",
            },
            {
                "id": "annexe6",
                "title": u"D.IV.15. alinéa 1, 3° permis d'urbanisation non périmé",
            },
            {
                "id": "annexe7",
                "title": u"D.IV.15. alinéa 2, 1° zone d'enjeu communal",
            },
            {
                "id": "annexe8",
                "title": u"D.IV.15. alinéa 2, 2° enseigne, logement, abattage, travaux d'impact limité",
            },
            {
                "id": "annexe9",
                "title": u"Annexe 9 - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
        ],
    },
    "CODT_Article127": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "60j", "title": u"60 jours", "deadLineDelay": 60, "alertDelay": 20},
            {"id": "90j", "title": u"90 jours", "deadLineDelay": 90, "alertDelay": 20},
            {
                "id": "120j",
                "title": u"120 jours",
                "deadLineDelay": 120,
                "alertDelay": 20,
            },
            {
                "id": "130j",
                "title": u"130 jours",
                "deadLineDelay": 130,
                "alertDelay": 20,
            },
            {
                "id": "160j",
                "title": u"160 jours",
                "deadLineDelay": 160,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "foldercategories": [
            "UrbanVocabularyTerm",
            {
                "id": "art127",
                "title": u"UCP permis d'urbanisme à caractère public (article 127) SANS ENQUETE ",
            },
            {
                "id": "art127-e",
                "title": u"UCP permis d'urbanisme à caractère public (article 127) AVEC ENQUETE ",
            },
            {"id": "inconnu", "title": u"Inconnu"},
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
            {
                "id": "div_40_alinea_2_dash_1",
                "title": u"D.IV.40 Alinéa 2/1",
                "extraValue": u"D.IV.40 Alinéa 2/1",
                "description": u"""<p>Les demandes visant à implanter un commerce au sens de l'article D.IV.4, alinéa 1er, 8°, sont soumises à enquête publique, sauf lorsque la demande porte sur l'implantation d'un commerce de quatre-cents mètres carrés et moins soumis à permis en exécution de l'article D.IV.4, alinéa 4. </p>""",
                "startValidity": codt_2024_start_validity_date,
            }
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {
                "id": "annexe4",
                "title": u"Annexe 4 - Demande de permis avec concours d'un architecte",
            },
            {
                "id": "annexe5",
                "title": u"Annexe 5 - Modification de la destination ou modification de la répartition des surfaces de vente",
            },
            {
                "id": "annexe6",
                "title": u"Annexe 6 - Modification sensible du relief du sol - dépôt de véhicules, de mitrailles, de matériaux ou de déchets - installations mobiles - travaux d'aménagement au sol aux abords d'une construction autorisée",
            },
            {
                "id": "annexe7",
                "title": u"Annexe 7 - Boisement - déboisement - abattage - culture de sapins de Noël - modification de l'aspect d'un ou plusieurs arbres ou haies remarquables - défrichement - modification de la végétation",
            },
            {"id": "annexe8", "title": u"Annexe 8 - Travaux techniques"},
            {
                "id": "annexe9",
                "title": u"Annexe 9 - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
        ],
    },
    "CODT_IntegratedLicence": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "90j", "title": u"90 jours", "deadLineDelay": 90, "alertDelay": 20},
            {
                "id": "120j",
                "title": u"120 jours",
                "deadLineDelay": 120,
                "alertDelay": 20,
            },
            {
                "id": "140j",
                "title": u"140 jours",
                "deadLineDelay": 140,
                "alertDelay": 20,
            },
            {
                "id": "170j",
                "title": u"170 jours",
                "deadLineDelay": 170,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "authority": [
            "UrbanVocabularyTerm",
            {
                "id": "fc_fd_ft",
                "title": u"Fonctionnaire des implantations commerciales, le Fonctionnaire technique et le Fonctionnaire délégué",
            },
            {
                "id": "fc_fd",
                "title": u"Fonctionnaire des implantations commerciales et le Fonctionnaire délégué ",
            },
            {
                "id": "fc_fT",
                "title": u"Fonctionnaire des implantations commerciales et le Fonctionnaire technique",
            },
            {"id": "college", "title": u"Collège"},
            {"id": "ft", "title": u"Fonctionnaire technique"},
        ],
    },
    "CODT_CommercialLicence": {
        "folderdelays": [
            "UrbanDelay",
            {
                "id": "100j",
                "title": u"100 jours",
                "deadLineDelay": 100,
                "alertDelay": 20,
            },
            {
                "id": "130j",
                "title": u"130 jours",
                "deadLineDelay": 130,
                "alertDelay": 20,
            },
            {
                "id": "140j",
                "title": u"140 jours",
                "deadLineDelay": 140,
                "alertDelay": 20,
            },
            {
                "id": "170j",
                "title": u"170 jours",
                "deadLineDelay": 170,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
        ],
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "dic", "title": u"Déclaration d'implantation commerciale"},
            {"id": "pic", "title": u"Permis d'implantation commerciale"},
            {"id": "inc", "title": u"Inconnu"},
        ],
        "authority": [
            "UrbanVocabularyTerm",
            {"id": "fic", "title": u"Fonctionnaire des Implantations Commerciales"},
            {"id": "college", "title": u"Collège"},
        ],
    },
    "CODT_UniqueLicence": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "90j", "title": u"90 jours", "deadLineDelay": 90, "alertDelay": 20},
            {
                "id": "120j",
                "title": u"120 jours",
                "deadLineDelay": 120,
                "alertDelay": 20,
            },
            {
                "id": "140j",
                "title": u"140 jours",
                "deadLineDelay": 140,
                "alertDelay": 20,
            },
            {
                "id": "170j",
                "title": u"170 jours",
                "deadLineDelay": 170,
                "alertDelay": 20,
            },
            {"id": "50j", "title": u"50 jours", "deadLineDelay": 50, "alertDelay": 20},
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {
                "id": "annexe4",
                "title": u"Annexe 4 - Demande de permis avec concours d'un architecte",
            },
            {
                "id": "annexe5",
                "title": u"Annexe 5 - Modification de la destination ou modification de la répartition des surfaces de vente",
            },
            {
                "id": "annexe6",
                "title": u"Annexe 6 - Modification sensible du relief du sol - dépôt de véhicules, de mitrailles, de matériaux ou de déchets - installations mobiles - travaux d'aménagement au sol aux abords d'une construction autorisée",
            },
            {
                "id": "annexe7",
                "title": u"Annexe 7 - Boisement - déboisement - abattage - culture de sapins de Noël - modification de l'aspect d'un ou plusieurs arbres ou haies remarquables - défrichement - modification de la végétation",
            },
            {"id": "annexe8", "title": u"Annexe 8 - Travaux techniques"},
            {
                "id": "annexe9",
                "title": u"Annexe 9 - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
        ],
        "authority": [
            "UrbanVocabularyTerm",
            {
                "id": "fd_ft",
                "title": u"Fonctionnaire délégué et le Fonctionnaire technique",
            },
            {"id": "college", "title": u"Collège"},
            {"id": "ft", "title": u"Fonctionnaire technique"},
        ],
    },
    "CODT_UrbanCertificateTwo": {
        "folderdelays": [
            "UrbanDelay",
            {"id": "30j", "title": u"30 jours", "deadLineDelay": 30, "alertDelay": 20},
            {"id": "60j", "title": u"60 jours", "deadLineDelay": 60, "alertDelay": 20},
            {"id": "75j", "title": u"75 jours", "deadLineDelay": 75, "alertDelay": 20},
            {
                "id": "105j",
                "title": u"105 jours",
                "deadLineDelay": 105,
                "alertDelay": 20,
            },
            {
                "id": "115j",
                "title": u"115 jours",
                "deadLineDelay": 115,
                "alertDelay": 20,
            },
            {
                "id": "145j",
                "title": u"145 jours",
                "deadLineDelay": 145,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "investigationarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "enquete-derogation",
                "title": u"Article D.IV.40 - Dérogation à un plan ou aux normes d'un guide régional",
                "description": u"<p>Application de l'article D.IV.40 : Les demandes impliquant une ou plusieurs dérogations au plan de secteur ou aux normes du guide régional sont soumises à enquête publique.</p> ",
            },
            {
                "id": "enquete-derogation-facultative",
                "title": u'Article D.VIII.13 - Procédure d\'enquête publique "facultative"',
                "description": u"<p>Application de l'article D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p>",
            },
            {
                "id": "R.IV.40-1.1.1",
                "title": u"R.IV.40-1.§1-1° - Hauteur des constructions",
                "description": u"<p> Article R.IV.40-1.§1-1° du CoDT : 1° la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins six niveaux ou dix-huit mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions ;</p>",
            },
            {
                "id": "R.IV.40-1.1.2",
                "title": u"R.IV.40-1.§1-2°- Magasin de plus de 400m2",
                "description": u"<p>Article R.IV.40-1.§1-2° du CoDT : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est supérieure à quatre cents mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.3",
                "title": u"R.IV.40-1.§1.3° - Usage destiné aux bureaux de plus de 650m2",
                "description": u"<p>Article R.IV.40-1.§1.3° du CoDT: «&nbsp;la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à sixccent cinquante mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.4",
                "title": u"R.IV.40-1.§1.4° - Destination à usage de stockage supérieur à 400m2",
                "description": u"<p>Article R.IV.40-1.§1.4° du CoDT : «&nbsp;la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à quatre cents mètres carrés, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-1.1.5",
                "title": u"R.IV.40-1.§1.5° - Utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets",
                "description": u"<p>Article R.IV.40-1.§1.5° du CoDT : «&nbsp;l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets&nbsp;»</p> ",
            },
            {
                "id": "R.IV.40-1.1.6",
                "title": u"R.IV.40-1.§1.6° - Les demandes de permis d'urbanisation et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment inscrit sur la liste de sauvegarde ou classés",
                "description": u"<p>Article R.IV.40-1.§1.6° du CoDT : «&nbsp;la construction, la reconstruction ou la transformation d'un bâtiment qui se rapporte à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protectioon visée à l'article 209 du Code wallon du Patrimoine ou localisés dans un site repris à l'inventaire du patrimoine archéologique visé à l'article 233 du Code wallon du Patrimoine »</p> ",
            },
            {
                "id": "R.IV.40-1.1.7",
                "title": u"R.IV.40-1.§1.7° - Ouverture ou modification de la voirie communale",
                "description": u"i<p>Article R.IV.40-1.§1.7° du CoDT« les demande de permis d'urbanisation, de permis d'urbanisme ou de certificats d'urbanisme n°2 visées à l'article D.IV.41 »</p> ",
            },
            {
                "id": "R.IV.40-1.1.8",
                "title": u"R.IV.40-1.§1.8° - Voiries régionales",
                "description": u'<p>Article R.IV.40-1.§1.8° du CoD - " les voiries visées à l\'article R.II.21-1,1° pour autant que les actes et travaux impliquent une modification de leur gabarit"</p>',
            },
            {
                "id": "div_40_alinea_2_dash_1",
                "title": u"D.IV.40 Alinéa 2/1",
                "extraValue": u"D.IV.40 Alinéa 2/1",
                "description": u"""<p>Les demandes visant à implanter un commerce au sens de l'article D.IV.4, alinéa 1er, 8°, sont soumises à enquête publique, sauf lorsque la demande porte sur l'implantation d'un commerce de quatre-cents mètres carrés et moins soumis à permis en exécution de l'article D.IV.4, alinéa 4. </p>""",
                "startValidity": codt_2024_start_validity_date,
            }
        ],
        "announcementarticles": [
            "UrbanVocabularyTerm",
            {
                "id": "ecarts",
                "title": u"Article D.IV.40 - Écarts à un schéma, à un guide ou à un permis d'urbanisation",
                "description": u"<p>Application de l'article D.IV.40. : Les demandes impliquant un ou plusieurs écarts aux plans communaux d’aménagement adoptés avant l’entrée en vigueur du Code et devenus schémas d’orientation locaux, aux règlements adoptés avant l’entrée en vigueur du Code et devenus guides et aux permis d’urbanisation sont soumises à annonce de projet, et ce, jusqu’à la révision ou à l’abrogation du schéma ou du guide.</p> ",
            },
            {
                "id": "ecarts-facultatifs",
                "title": u'Article D.VIII.13 - Procédure d\'annonce de projet "facultative"',
                "description": u"<p>Art. D.VIII.13. L’autorité compétente pour adopter le plan, périmètre, schéma ou le guide et pour délivrer les<br /> permis et certificats d’urbanisme no 2, ainsi que les collèges communaux des communes organisant l’annonce de projet<br /> ou l’enquête publique, peuvent procéder à toute forme supplémentaire de publicité et d’information dans le respect des<br /> délais de décision qui sont impartis à l’autorité compétente.</p> ",
            },
            {
                "id": "R.IV.40-2-1-1",
                "title": u"R.IV.40-2.§1.1° - Hauteur des constructions",
                "description": u"<p>Article R.IV.40-2.§1-1°du CoDT : «&nbsp;la construction ou la reconstruction de bâtiments dont la hauteur est d’au moins trois niveaux ou neuf mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu’à cinquante mètres de part et d’autre de la construction projetée; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions;»</p> ",
            },
            {
                "id": "R.IV.40-2-1-2",
                "title": u"R.IV.40-2 § 2° - Profondeur de bâtisse",
                "description": u"<p>Article R.IV.40-2.§1-2°: «&nbsp;la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës, la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
            {
                "id": "R.IV.40-2-1-3",
                "title": u"R.IV.40-2.§1-3° - Magasin de moins de 400m2",
                "description": u"<p>Article R.IV.40-2.§1-3 : «&nbsp;la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface commerciale nette est inférieure à quatre cent mètres carrés ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions&nbsp;»</p>",
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            {"id": "dero-ps", "title": u"au plan de secteur"},
            {
                "id": "dero-gru",
                "title": u"à une ou des norme(s) du Guide Régional d'Urbanisme ",
            },
        ],
        "divergences": [
            "UrbanVocabularyTerm",
            {"id": "ecart-purba", "title": u"au permis d'urbanisation"},
            {"id": "ecart-gcu", "title": u"au Guide Communal d'Urbanisme"},
            {"id": "ecart-gru", "title": u"au Guide Régional d'Urbanisme"},
            {"id": "ecart-sol", "title": u"au Schéma d'Orientation Local"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {
                "id": "annexe4",
                "title": u"Annexe 4 - Demande de permis avec concours d'un architecte",
            },
            {
                "id": "annexe5",
                "title": u"Annexe 5 - Modification de la destination ou modification de la répartition des surfaces de vente",
            },
            {
                "id": "annexe6",
                "title": u"Annexe 6 - Modification sensible du relief du sol - dépôt de véhicules, de mitrailles, de matériaux ou de déchets - installations mobiles - travaux d'aménagement au sol aux abords d'une construction autorisée",
            },
            {
                "id": "annexe7",
                "title": u"Annexe 7 - Boisement - déboisement - abattage - culture de sapins de Noël - modification de l'aspect d'un ou plusieurs arbres ou haies remarquables - défrichement - modification de la végétation",
            },
            {"id": "annexe8", "title": u"Annexe 8 - Travaux techniques"},
            {
                "id": "annexe9",
                "title": u"Annexe 9 - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
        ],
    },
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
            {
                "id": "upp",
                "title": u"UPP (petit permis délivré directement par le Collège)",
            },
            {"id": "pu", "title": u"PU (demande de PERMIS UNIQUE)"},
            {"id": "inconnu", "title": u"Inconnue"},
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "plan_travaux", "title": u"Plan des travaux en 4 exemplaires"},
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 4 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable d'incidences environnement en 4 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {"id": "peb", "title": u"Formulaire d'engagement PEB en 4 exemplaires"},
        ],
        "roadmissingparts": [
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable incid'ences environnement (annexe 1C) en 2 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {
                "id": "isolation",
                "title": u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires",
            },
            {
                "id": "peb",
                "title": u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires",
            },
        ],
        "locationmissingparts": [
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {
                "id": "isolation",
                "title": u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires",
            },
            {
                "id": "peb",
                "title": u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires",
            },
        ],
        "exemptfdarticle": [
            "UrbanVocabularyTerm",
            {"id": "145", "title": "alinéa 145"},
            {"id": "232", "title": "alinéa 232"},
        ],
    },
    "Article127": {
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {
                "id": "isolation",
                "title": u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires",
            },
            {
                "id": "peb",
                "title": u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires",
            },
        ],
        "roadmissingparts": [
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable incid'ences environnement (annexe 1C) en 2 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {
                "id": "isolation",
                "title": u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires",
            },
            {
                "id": "peb",
                "title": u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires",
            },
        ],
        "locationmissingparts": [
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
            {
                "id": "attestation_ordre_archi",
                "title": u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires",
            },
            {
                "id": "photos",
                "title": u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires",
            },
            {
                "id": "notice_environnement",
                "title": u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires",
            },
            {"id": "plan_secteur", "title": u"Une copie du plan de secteur"},
            {
                "id": "isolation",
                "title": u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires",
            },
            {
                "id": "peb",
                "title": u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires",
            },
        ],
    },
    "ParcelOutLicence": {
        "foldercategories": [
            "UrbanVocabularyTerm",
            {"id": "lap", "title": u"LAP (permis de lotir avec avis préalable du FD)"},
            {
                "id": "lapm",
                "title": u"LAP/M (modification du permis de lotir avec avis du FD)",
            },
            {
                "id": "ldc",
                "title": u"LDC (permis de lotir dans un PCA, 'lotissement ou en décentralisation)",
            },
            {
                "id": "ldcm",
                "title": u"LDC/M (modification du permis de lotir dans un PCA, 'RCU, 'LOTISSEMENT)",
            },
        ],
        "lotusages": [
            "UrbanVocabularyTerm",
            {"id": "buildable", "title": u"Lot bâtissable"},
            {"id": "greenzone", "title": u"Espace vert"},
            {"id": "tosurrendertotown", "title": u"Lot à rétrocéder à la commune"},
            {"id": "autre", "title": u"Autre"},
        ],
        "equipmenttypes": [
            "UrbanVocabularyTerm",
            {"id": "telecom", "title": u"Télécomunication"},
            {"id": "electricity", "title": u"Electricité"},
            {"id": "gas", "title": u"Gaz"},
            {"id": "teledistribution", "title": u"Télédistribution"},
            {"id": "sewers", "title": u"Egouttage"},
            {"id": "water", "title": u"Eau"},
            {"id": "autre", "title": u"Autre"},
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
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
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
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {
                "id": "form_demande",
                "title": u"Formulaire de demande (formulaire 1A) en 3 exemplaires",
            },
            {"id": "extrait_cadastral", "title": u"Extrait cadastral en 3 exemplaires"},
        ],
    },
    "EnvClassOne": {
        "decisions": [
            "UrbanVocabularyTerm",
            {"id": "octroi", "title": u"Octroi", "extraValue": "Recevable"},
            {"id": "refus", "title": u"Refus", "extraValue": "Irrecevable"},
        ],
        "folderdelays": [
            "UrbanDelay",
            {"id": "40j", "title": u"40 jours", "deadLineDelay": 40, "alertDelay": 20},
            {"id": "50j", "title": u"50 jours", "deadLineDelay": 50, "alertDelay": 20},
            {"id": "70j", "title": u"70 jours", "deadLineDelay": 70, "alertDelay": 20},
            {"id": "80j", "title": u"80 jours", "deadLineDelay": 80, "alertDelay": 20},
            {
                "id": "140j",
                "title": u"140 jours",
                "deadLineDelay": 140,
                "alertDelay": 20,
            },
            {
                "id": "170j",
                "title": u"170 jours",
                "deadLineDelay": 170,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
    },
    "EnvClassTwo": {
        "decisions": [
            "UrbanVocabularyTerm",
            {"id": "octroi", "title": u"Octroi", "extraValue": "Recevable"},
            {"id": "refus", "title": u"Refus", "extraValue": "Irrecevable"},
        ],
        "folderdelays": [
            "UrbanDelay",
            {"id": "40j", "title": u"40 jours", "deadLineDelay": 40, "alertDelay": 20},
            {"id": "50j", "title": u"50 jours", "deadLineDelay": 50, "alertDelay": 20},
            {"id": "70j", "title": u"70 jours", "deadLineDelay": 70, "alertDelay": 20},
            {"id": "80j", "title": u"80 jours", "deadLineDelay": 80, "alertDelay": 20},
            {"id": "90j", "title": u"90 jours", "deadLineDelay": 90, "alertDelay": 20},
            {
                "id": "120j",
                "title": u"120 jours",
                "deadLineDelay": 120,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
    },
    "EnvClassThree": {
        "missingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
            {"id": "plan", "title": u"Plans"},
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
            {"id": "plan", "title": u"Plans"},
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            {"id": "form_demande", "title": u"Formulaire de demande en 4 exemplaires"},
            {"id": "plan", "title": u"Plans"},
        ],
        "folderdelays": [
            "UrbanDelay",
            {"id": "15j", "title": u"15 jours", "deadLineDelay": 15, "alertDelay": 0},
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "deposittype": [
            "UrbanVocabularyTerm",
            {"id": "papier", "title": u"Papier"},
            {"id": "soumission", "title": u"Soumission"},
        ],
    },
    "EnvClassBordering": {
        "decisions": [
            "UrbanVocabularyTerm",
            {"id": "octroi", "title": u"Octroi", "extraValue": "Recevable"},
            {"id": "refus", "title": u"Refus", "extraValue": "Irrecevable"},
        ],
        "folderdelays": [
            "UrbanDelay",
            {"id": "40j", "title": u"40 jours", "deadLineDelay": 40, "alertDelay": 20},
            {
                "id": "140j",
                "title": u"140 jours",
                "deadLineDelay": 140,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "authority": [
            "UrbanVocabularyTerm",
            {"id": "fd", "title": u"Fonctionnaire délégué"},
            {"id": "college", "title": u"Collège"},
            {"id": "ft", "title": u"Fonctionnaire technique"},
            {"id": "fc", "title": u"Fonctionnaire des implantations commerciales"},
            {
                "id": "fc_fd_ft",
                "title": u"Fonctionnaire des implantations commerciales, le Fonctionnaire technique et le Fonctionnaire délégué",
            },
            {
                "id": "fc_fd",
                "title": u"Fonctionnaire des implantations commerciales et le Fonctionnaire délégué ",
            },
            {
                "id": "fc_fT",
                "title": u"Fonctionnaire des implantations commerciales et le Fonctionnaire technique",
            },
            {
                "id": "fd_ft",
                "title": u"Fonctionnaire délégué et le Fonctionnaire technique",
            },
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
            {"id": "appu", "title": u"Avis préalable permis d'urbanisation"},
            {"id": "apd", "title": u"Avis préalable de division"},
            {"id": "dre", "title": u"Demande de raccordement à l'égout"},
            {"id": "div", "title": u"Divers"},
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
            {
                "id": "263_1_2",
                "title": u"article 263 §1er 2° la pose ou l'enlèvement d'un car-port <30m²",
                "extraValue": "263 §1er 2°",
                "description": "« article 263 §1er 2° par propriété, la pose ou l’enlèvement d’un car port d’une superficie maximale de 30, 00 m² qui ne respecte pas les conditions visées à l’article 262, 5°, f; »",
            },
            {
                "id": "263_1_3",
                "title": u"article 263 §1er 3° l'ouverture ou la modification de baies",
                "extraValue": "263 §1er 3°",
                "description": "« article 263 §1er 3° l’ouverture ou la modification de baies autres que celles visées à l’article 262, 9° et 10°, de même aspect architectural que les baies existantes; »",
            },
            {
                "id": "263_1_4",
                "title": u"article 263 §1er 4° le remplacement de parements d'élévation/couverture de toiture par plus isolants",
                "extraValue": "263 §1er 4°",
                "description": "« article 263 §1er 4° le remplacement de parements d’élévation et de couvertures de toiture par des parements et couvertures isolants visés à l’article 262, 11°, qui n’en remplissent pas les conditions; »",
            },
            {
                "id": "263_1_5a",
                "title": u"article 263 §1er 5° a}, la construction d'un volume secondaire en contiguïté <30m²",
                "extraValue": "263 §1er 5° a)",
                "description": "« article 263 §1er 5° a}, par propriété, la construction ou le remplacement d’un volume secondaire par un volume secondaire, sans étage s’il est érigé en contiguïté avec un bâtiment existant, à l’arrière de ce bâtiment ou en recul d’au moins 4, 00 m de l’alignement ou raccordé à ce bâtiment par un volume à toiture plate; »",
            },
            {
                "id": "263_1_5b",
                "title": u"article 263 §1er 5° b}, la construction d'un volume secondaire isolé <30m²",
                "extraValue": "263 §1er 5° b)",
                "description": "« article 263 §1er 5° b}, par propriété, la construction ou le remplacement d’un volume secondaire par un volume secondaire, sans étage s’il est isolé et érigé à l’arrière d’un bâtiment existant; »",
            },
            {
                "id": "263_1_6a",
                "title": u"article 263 §1er 6° a}, la construction d'un abri pour un ou des animaux",
                "extraValue": "263 §1er 6° a)",
                "description": "« article 263 §1er 6° a}, dans les cours et jardins, les abris pour un ou des animaux; »",
            },
            {
                "id": "263_1_6b",
                "title": u"article 263 §1er 6° b}, la pose d'un rucher",
                "extraValue": "263 §1er 6° b)",
                "description": "« article 263 §1er 6° b}, dans les cours et jardins, un rucher, sans préjudice de l’application des dispositions visées au Code rural; »",
            },
            {
                "id": "263_1_6c",
                "title": u"article 263 §1er 6° c}, Clôtures/portiques/portillons",
                "extraValue": "263 §1er 6° c)",
                "description": "« article 263 §1er 6° c}, dans les cours et jardins, la pose de clôtures, de portiques ou de portillons autres que ceux visés à l’article 262, 5°, e; »",
            },
            {
                "id": "263_1_6d",
                "title": u"article 263 §1er 6° d}, Etang/piscine non couverte < 75m²",
                "extraValue": "263 §1er 6° d)",
                "description": "« article 263 §1er 6° d}, dans les cours et jardins, par propriété, pour autant qu’ils soient situés à l’arrière de l’habitation, la création d’un étang ou d’une piscine non couverte n’excédant pas 75, 00 m² pour autant que les déblais nécessaires à ces aménagements n’entraînent aucune modification sensible du relief naturel du sol sur le reste de la propriété; »",
            },
            {
                "id": "263_1_7",
                "title": u"article 263 §1er 7° Démolition <30 m²",
                "extraValue": "263 §1er 7°",
                "description": "« article 263 §1er 7° la démolition de constructions sans étage ni sous-sol;",
            },
            {
                "id": "263_1_8a",
                "title": u"article 263 §1er 8° a}, les silos de stockage",
                "extraValue": "263 §1er 8° a)",
                "description": "« article 263 §1er 8° a}, pour les exploitations agricoles, la construction de silos de stockage en tout ou en partie enterrés, pour autant que le niveau supérieur des murs de soutènement n’excède pas de 1, 50 m le niveau du relief naturel du sol; »",
            },
            {
                "id": "263_1_8b",
                "title": u"article 263 §1er 8° b}, les dalles de fumière",
                "extraValue": "263 §1er 8° b)",
                "description": "« article 263 §1er 8° b}, pour les exploitations agricoles, l’établissement d’une dalle de fumière; »",
            },
            {
                "id": "263_1_8c",
                "title": u"article 263 §1er 8° c}, les citernes de récolte ou de stockage d'eau/effluents d'élevage",
                "extraValue": "263 §1er 8° c)",
                "description": "« article 263 §1er 8° c}, pour les exploitations agricoles, la pose de citernes de récolte ou de stockage d’eau ou d’effluents d’élevage, en tout ou en partie enterrées, pour autant que le niveau supérieur du mur de soutènement n’excède pas 0, 50 m et que les citernes soient implantées à 10, 00 m minimum de tout cours d’eau navigable ou non navigable, à 3, 00 m minimum du domaine public et à 20, 00 m minimum de toute habitation autre que celle de l’exploitant; »",
            },
            {
                "id": "263_1_9",
                "title": u"article 263 §1er 9° la culture de sapins de Noël",
                "extraValue": "263 §1er 9°",
                "description": "« article 263 §1er 9° la culture de sapins de Noël pour une période ne dépassant pas douze ans; »",
            },
            {
                "id": "263_1_10",
                "title": u"article 263 §1er 10° les miradors",
                "extraValue": "263 §1er 10°",
                "description": "« article 263 §1er 10° dans la zone contiguë à la zone forestière, les miradors en bois visés à l’article 1er, § 1er, 9°, de la loi du 28 février 1882 sur la chasse; »",
            },
        ],
    },
    "shared_vocabularies": {
        "decisions": [
            "UrbanVocabularyTerm",
            URBAN_TYPES,
            {"id": "favorable", "title": u"Octroi", "extraValue": "Recevable"},
            {"id": "defavorable", "title": u"Refus", "extraValue": "Irrecevable"},
        ],
        "collegeopinions": [
            "UrbanVocabularyTerm",
            URBAN_TYPES,
            {"id": "favorable", "title": u"Favorable", "extraValue": "Recevable"},
            {"id": "defavorable", "title": u"Défavorable", "extraValue": "Irrecevable"},
            {
                "id": "favorable-cond",
                "title": u"Favorable conditionné à",
                "extraValue": "Recevable sous conditions",
            },
        ],
        "foldertendencies": [
            "UrbanVocabularyTerm",
            ["UniqueLicence", "CODT_UniqueLicence"],
            {"id": "env", "title": u"Environnementale"},
            {"id": "urb", "title": u"Urbanistique"},
        ],
        "pebcategories": [
            "UrbanVocabularyTerm",
            [
                "BuildLicence",
                "Article127",
                "CODT_BuildLicence",
                "CODT_ParcelOutLicence",
                "CODT_Article127",
                "CODT_IntegratedLicence",
                "CODT_CommercialLicence",
            ],
            {"id": "not_applicable", "title": "Non applicable"},
            {"id": "complete_process", "title": "Procédure complète"},
            {"id": "form1_process", "title": "Déclaration simplifiée"},
            {"id": "form2_process", "title": "Engagement PEB"},
        ],
        "townshipfoldercategories": [
            "UrbanVocabularyTerm",
            URBAN_TYPES,
            {"id": "abattre", "title": u"Abattre"},
            {"id": "abri-animaux", "title": u"Abri pour animaux"},
            {"id": "abri-jardin", "title": u"Abri de jardin"},
            {"id": "car-port", "title": u"Car-port"},
            {"id": "changement-de-destination", "title": u"Changement de destination"},
            {"id": "clotures-murs", "title": u"Clôtures et murs"},
            {"id": "commerce", "title": u"Commerce"},
            {"id": "demolition", "title": u"Démolition"},
            {"id": "divers", "title": u"Divers"},
            {"id": "enseigne", "title": u"Enseigne"},
            {
                "id": "EXT_COMMERCE",
                "title": u"Extension d'un commerce de détail ou d'un ensemble commercial",
                "extraValue": "EXT_COMMERCE",
                "startValidity": codt_2024_start_validity_date,
            },
            {"id": "immeuble-appartements", "title": u"Immeuble à appartements"},
            {"id": "modification-relief", "title": u"Modification du relief du sol"},
            {
                "id": "module-electrite",
                "title": u"Modules de production d'électricité ou de chaleur",
            },
            {"id": "nouvelle-habitation", "title": u"Nouvelle habitation"},
            {
                "id": "nouveau-logement",
                "title": u"Nouveau logement dans un bâtiment existant",
            },
            {"id": "parking", "title": u"Parking"},
            {"id": "piscine", "title": u"Piscine"},
            {
                "id": "recouvrement-toiture",
                "title": u"Remplacement de parement de façade ou de recouvrement de toiture",
            },
            {
                "id": "transformation",
                "title": u"Transformation d'une habitation existante",
            },
            {"id": "transformation-facade", "title": u"Transformation d'une façade"},
            {"id": "veranda", "title": u"Véranda"},
        ],
        "ftSolicitOpinionsTo": [
            "UrbanVocabularyTerm",
            [
                "CODT_IntegratedLicence",
                "CODT_UniqueLicence",
                "EnvClassOne",
                "EnvClassTwo",
                "EnvClassBordering",
            ],
            {
                "id": "spw-dgo1",
                "title": "SPW-DGO1",
                "description": "<p>Direction Générale opérationnelle<br />Département du réseau de Namur et du Luxembourg<br />District 131.12 - SPY<br />37, Route de Saussin<br />5190 Spy</p>",
            },
            {
                "id": "dgrne",
                "title": "DGRNE",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "dnf",
                "title": "DNF",
                "description": "<p>39, Avenue Reine Astrid<br />5000 Namur</p>",
            },
            {
                "id": "stp",
                "title": "Service Technique Provincial",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "pi",
                "title": "Prévention Incendie",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "svp",
                "title": "Service Voyer Principal",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "agriculture",
                "title": "Agriculture",
                "description": "<p>Direction Générale opérationnelle<br />Agriculture, Ressources naturelles et Environnement<br />Service extérieur de Wavre<br />4, Avenue Pasteur<br />1300 Wavre</p>",
            },
            {
                "id": "pn",
                "title": "Parc Naturel",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "crmsf",
                "title": "Commission Royale des Monuments, Sites et Fouilles",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "swde",
                "title": "SWDE",
                "description": "<p>14, Rue Joseph Saintraint<br />5000 Namur</p>",
            },
            {
                "id": "ccatm",
                "title": "CCATM",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "inasep",
                "title": "INASEP",
                "description": "<p>1b, Rue des Viaux<br />5100 Naninne</p>",
            },
            {
                "id": "belgacom",
                "title": "Belgacom",
                "description": "<p>60, Rue Marie Henriette<br />5000 Namur</p>",
            },
            {
                "id": "spge",
                "title": "SPGE",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "cibe",
                "title": "CIBE/Vivaqua",
                "description": "<p>70, Rue aux Laines<br />1000 Bruxelles</p>",
            },
            {
                "id": "sncb",
                "title": "SNCB",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
            {
                "id": "infrabel",
                "title": "Infrabel",
                "description": "<p>Infrastructure ferroviaire<br />2/003, Place des Guillemins<br />4000 Liège</p>",
            },
            {
                "id": "voo",
                "title": "VOO",
                "description": "<p>1, Rue xxx<br />xxxx Commune</p>",
            },
        ],
        "missingparts": [
            "UrbanVocabularyTerm",
            [
                "NotaryLetter",
                "CODT_NotaryLetter",
                "MiscDemand",
                "Division",
                "Declaration",
                "RoadDecree",
            ],
        ],
        "roadmissingparts": [
            "UrbanVocabularyTerm",
            [
                "NotaryLetter",
                "CODT_NotaryLetter",
                "MiscDemand",
                "Division",
                "Declaration",
            ],
        ],
        "locationmissingparts": [
            "UrbanVocabularyTerm",
            [
                "NotaryLetter",
                "CODT_NotaryLetter",
                "MiscDemand",
                "Division",
                "Declaration",
                "RoadDecree",
            ],
        ],
        "authority": [
            "UrbanVocabularyTerm",
            [
                "EnvClassOne",
                "EnvClassTwo",
                "UniqueLicence",
            ],
            {"id": "college", "title": u"Collège"},
            {"id": "ft", "title": u"Fonctionnaire technique"},
        ],
        "inadmissibilityreasons": [
            "UrbanVocabularyTerm",
            ["EnvClassOne", "EnvClassTwo", "EnvClassThree", "EnvClassBordering"],
            {"id": "missing_parts", "title": u"Pièces/renseignements manquants"},
            {
                "id": "no_deposit_receipt",
                "title": u"Le dossier n'a pas été déposé contre récipissé",
            },
            {
                "id": "no_recommanded_deposit",
                "title": u"Le dossier n'a pas été envoyé par recommandé",
            },
        ],
        "applicationreasons": [
            "UrbanVocabularyTerm",
            [
                "EnvClassOne",
                "EnvClassTwo",
                "EnvClassThree",
                "EnvClassBordering",
                "CODT_IntegratedLicence",
            ],
            {
                "id": "new_business",
                "title": u"Mise en activité d'un établissement nouveau",
            },
            {
                "id": "class_change",
                "title": u"Maintien en activité d'un établissement qui vient d'être rangé en classe 3 suite à une modification de la liste des installations et activités classées",
            },
            {
                "id": "licence_expiration",
                "title": u"Maintien en activité d’un établissement dont la durée de validité de la déclaration est arrivée à expiration",
            },
            {
                "id": "restart_old_business",
                "title": u"Remise en activité d’un établissement existant",
            },
            {
                "id": "transformation",
                "title": u"Extension ou de la transformation d’un établissement ancien",
            },
            {"id": "location_move", "title": u"Déplacement de l’établissement"},
            {"id": "regularisation", "title": u"Régularisation"},
        ],
        "specificfeatures": [
            "SpecificFeatureTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "schema-developpement-espace-regional",
                "title": u"Option particulière du schéma de développement de l'espace régional",
                "description": "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>",
            },
            {
                "id": "situe-en-zone",
                "title": u"Situé en Zone [...]",
                "description": "<p>est situé en [[object.folderZone]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                "relatedFields": ["folderZone", ""],
            },
            {
                "id": "plan-de-secteur",
                "title": u"Plan de secteur",
                "description": "<p>est situé - dans un périmètre ... - en [[object.folderZone]] au projet - de révision du - de - plan de secteur de ... adopté par ... du ...;</p>",
                "relatedFields": ["folderZone", ""],
            },
            {
                "id": "plan-communal-ammenagement",
                "title": u"En Plan Communal d'Aménagement",
                "description": "<p>est situé en [[object.folderZone]] dans le périmètre du plan communal d'aménagement [[voc_term('pca').label]] approuvé par [[voc_term('pca').decreeType]] du [[format_date(voc_term('pca').decreeDate)]] et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                "relatedFields": ["folderZone", "isInPCA", "pca", ""],
            },
            {
                "id": "plan-communal-ammenagement-revision",
                "title": u"En Plan Communal d'Aménagement (révision),",
                "description": "<p>est situé en [[object.folderZone]] dans le périmètre du projet - de révision du - de - plan communal d'aménagement [[voc_term('pca').label]] approuvé par [[voc_term('pca').decreeType]] du [[format_date(voc_term('pca').decreeDate)]];</p>",
                "relatedFields": ["folderZone", "isInPCA", "pca", ""],
            },
            {
                "id": "perimetre-lotissement",
                "title": u"Dans un lot dans le périmètre d'un lotissement",
                "description": "<p>est situé sur le(s), lot(s) n° [[object.subdivisionDetails]] dans le périmètre du lotissement [[object.getParcellings().label]]non périmé autorisé du [[format_date(object.getParcellings().getAuthorizationDate()) ]];</p>",
            },
            {
                "id": "ssc",
                "title": u"Schéma de structure communal",
                "description": "<p> est situé en [[object.SSC]] au schéma de structure communal adopté par [[voc_term('SSC').extraValue ]];</p>",
                "relatedFields": ["SSC", ""],
            },
            {
                "id": "ssc-revision",
                "title": u"Schéma de structure communal (révision),",
                "description": "<p> est situé en [[object.SSC]] au projet de - révision du - de - schéma de structure communal adopté par [[voc_term('SSC').extraValue ]];</p>",
                "relatedFields": ["SSC", ""],
            },
            {
                "id": "rcu",
                "title": u"Règlement communal d'urbanisme",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement régional d'urbanisme [[object.folderZone]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-approuve",
                "title": u"Règlement communal d'urbanisme (approuvé),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par [[voc_term('RCU').extraValue,]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-revision",
                "title": u"Règlement communal d'urbanisme (révision),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal visé(e), par le projet - de révision du - de - règlement communal d'urbanisme approuvé par [[voc_term('RCU').extraValue]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-approuve-provisoirement",
                "title": u"Règlement communal d'urbanisme (approuvé provisoirement),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par [[', '.join(object.getValuesForTemplate('RCU', subfield='extraValue')) ]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-unite-paysagere-urbaine",
                "title": u"Règlement communal d'urbanisme (Unité paysagère urbaine),",
                "description": "<p>est situé en unité paysagère urbaine de bâtisse en ordre continu Art.15 au règlement communal d'urbanisme en vigueur;</p>",
            },
            {
                "id": "natura-2000",
                "title": u"Site Natura 2000",
                "description": "<p>est situé dans le périmètre d'un site Natura 2000 visé par l'article 1bis alinéa unique 18° de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                "id": "natura-2000-art6",
                "title": u"Natura 2000 (article 6 de la loi du 12 juillet 1973),",
                "description": "<p>est situé dans le périmètre d'un territoire désigné en vertu de l'article 6 de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                "id": "zone-prise-eau",
                "title": u"Zone de prise d'eau",
                "description": "<p>est situé dans une zone de prise d'eau, de prévention ou de surveillance au sens du décret du 30 avril 1990 relatif à la protection et l'exploitation des eaux souterraines et des eaux potabilisables modifié la dernière fois par le décret du 15 avril 1999 relatif au cycle de l'eau et instituant une société publique de gestion de l'eau;</p>",
            },
            {
                "id": "plan-expropriation",
                "title": u"Plan d'expropriation",
                "description": "<p> est situé dans les limites d'un plan d'expropriation approuvé par ... du ... ; le pouvoir expropriant est : ...;</p>",
            },
            {
                "id": "droit-de-preemption",
                "title": u"Droit de préemption",
                "description": "<p>est situé dans un périmètre d'application du droit de préemption arrêté par ... du ...; le(s}, bénéficiaires(s) du droit de préemption est (sont) : ...;</p>",
            },
            {
                "id": "perimetre-site-desaffecte",
                "title": u"Périmètre site désaffecté",
                "description": "<p>est situé dans le périmètre du site d'activité économique désaffecté suivant : ...;</p>",
            },
            {
                "id": "revitalisation-urbaine",
                "title": u"Revitalisation urbaine",
                "description": "<p>est situé dans un périmètre de revitalisation urbaine;</p>",
            },
            {
                "id": "renovation-urbaine",
                "title": u"Rénovation urbaine",
                "description": "<p>est situé dans un périmètre de rénovation urbaine;</p>",
            },
            {
                "id": "classe",
                "title": u"Classé (article 196 du CWATUPE),",
                "description": "<p>est - inscrit sur la liste de sauvegarde visée à l'article 193 - classé en application de l'article 196 - situé dans une zone de protection visée à l'article 209 - localisé dans un site repris à l'inventaire des sites archéologiques visés à l'article 233 - du Code précité;</p>",
            },
            {
                "id": "raccordable-egout",
                "title": u"Raccordable à l'égout",
                "description": "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>",
            },
            {
                "id": "raccordable-egout-prevision",
                "title": u"Raccordable à l'égout (prévision),",
                "description": "<p>sera raccordable à l'égout selon les prévisions actuelles;</p>",
            },
            {
                "id": "zone-faiblement-habitee",
                "title": u"Zone faiblement habitée (épuration individuelle),",
                "description": "<p>est situé dans une des zones faiblement habitée qui ne seront pas pourvue d'égout et qui feront l'objet d'une épuration individuelle;</p>",
            },
            {
                "id": "voirie-suffisamment-equipee",
                "title": u"Voirie suffisamment équipée",
                "description": "<p>bénéficie d'un accès à une voirie suffisamment équipée en eau, électricité, pourvue d'un revêtement solide et d'une largeur suffisante compte tenu de la situation des lieux;</p>",
            },
        ],
        "roadspecificfeatures": [
            "SpecificFeatureTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "raccordable-egout",
                "title": u"Raccordable à l'égout",
                "description": "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>",
            },
            {
                "id": "raccordable-egout-prevision",
                "title": u"Raccordable à l'égout (prévision),",
                "description": "<p>sera raccordable àl'égout selon les prévisions actuelles;</p>",
            },
            {
                "id": "zone-faiblement-habitee",
                "title": u"Zone faiblement habitée (épuration individuelle),",
                "description": "<p>est situé dans une des zones faiblement habitée qui ne seront pas pourvue d'égout et qui feront l'objet d'une épuration individuelle;</p>",
            },
            {
                "id": "voirie-suffisamment-equipee",
                "title": u"Voirie suffisamment équipée",
                "description": "<p>bénéficie d'un accès à une voirie suffisamment équipée en eau, électricité, pourvue d'un revêtement solide et d'une largeur suffisante compte tenu de la situation des lieux;</p>",
            },
        ],
        "locationspecificfeatures": [
            "SpecificFeatureTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "schema-developpement-espace-regional",
                "title": u"Option particulière du schéma de développement de l'espace régional",
                "description": "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>",
            },
            {
                "id": "situe-en-zone",
                "title": u"Situé en Zone [...]",
                "description": "<p>est situé en [[object.folderZone]] au plan de secteur de ... adopté par ... du ... et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                "relatedFields": ["folderZone", ""],
            },
            {
                "id": "plan-de-secteur",
                "title": u"Plan de secteur",
                "description": "<p>est situé - dans un périmètre ... - en [[object.folderZone]] au projet - de révision du - de - plan de secteur de ... adopté par ... du ...;</p>",
                "relatedFields": ["folderZone", ""],
            },
            {
                "id": "plan-communal-ammenagement",
                "title": u"En Plan Communal d'Aménagement",
                "description": "<p>est situé en [[object.folderZone]] dans le périmètre du plan communal d'aménagement [[voc_term('pca').label]] approuvé par [[voc_term('pca').decreeType]] du [[format_date(voc_term('pca').decreeDate)]] et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                "relatedFields": ["folderZone", "isInPCA", "pca", ""],
            },
            {
                "id": "plan-communal-ammenagement-revision",
                "title": u"En Plan Communal d'Aménagement (révision),",
                "description": "<p>est situé en [[object.folderZone]] dans le périmètre du projet - de révision du - de - plan communal d'aménagement [[voc_term('pca').label]] approuvé par [[voc_term('pca').decreeType]] du [[format_date(voc_term('pca').decreeDate)]];</p>",
                "relatedFields": ["folderZone", "isInPCA", "pca", ""],
            },
            {
                "id": "perimetre-lotissement",
                "title": u"Dans un lot dans le périmètre d'un lotissement",
                "description": "<p>est situé sur le(s}, lot(s) n° [[object.subdivisionDetails]] dans le périmètre du lotissement [[object.getParcellings().label]] non périmé autorisé du [[format_date(object.getParcellings().getAuthorizationDate()) ]];</p>",
            },
            {
                "id": "ssc",
                "title": u"Schéma de structure communal",
                "description": "<p> est situé en [[object.SSC]] au schéma de structure communal adopté par [[voc_term('SSC').extraValue ]];</p>",
                "relatedFields": ["SSC", ""],
            },
            {
                "id": "ssc-revision",
                "title": u"Schéma de structure communal (révision),",
                "description": "<p> est situé en [[object.SSC]] au projet de - révision du - de - schéma de structure communal adopté par [[voc_term('SSC').extraValue ]];</p>",
                "relatedFields": ["SSC", ""],
            },
            {
                "id": "rcu",
                "title": u"Règlement communal d'urbanisme",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement régional d'urbanisme [[object.folderZone]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-approuve",
                "title": u"Règlement communal d'urbanisme (approuvé),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par [[voc_term('RCU').extraValue,]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-revision",
                "title": u"Règlement communal d'urbanisme (révision),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal visé(e), par le projet - de révision du - de - règlement communal d'urbanisme approuvé par [[voc_term('RCU').extraValue]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-approuve-provisoirement",
                "title": u"Règlement communal d'urbanisme (approuvé provisoirement),",
                "description": "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par [[', '.join(object.getValuesForTemplate('RCU', subfield='extraValue')) ]] est applicable;</p>",
                "relatedFields": ["RCU", ""],
            },
            {
                "id": "rcu-unite-paysagere-urbaine",
                "title": u"Règlement communal d'urbanisme (Unité paysagère urbaine),",
                "description": "<p>est situé en unité paysagère urbaine de bâtisse en ordre continu Art.15 au règlement communal d'urbanisme en vigueur;</p>",
            },
            {
                "id": "natura-2000",
                "title": u"Site Natura 2000",
                "description": "<p>est situé dans le périmètre d'un site Natura 2000 visé par l'article 1bis alinéa unique 18° de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                "id": "natura-2000-art6",
                "title": u"Natura 2000 (article 6 de la loi du 12 juillet 1973),",
                "description": "<p>est situé dans le périmètre d'un territoire désigné en vertu de l'article 6 de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                "id": "zone-prise-eau",
                "title": u"Zone de prise d'eau",
                "description": "<p>est situé dans une zone de prise d'eau, de prévention ou de surveillance au sens du décret du 30 avril 1990 relatif à la protection et l'exploitation des eaux souterraines et des eaux potabilisables modifié la dernière fois par le décret du 15 avril 1999 relatif au cycle de l'eau et instituant une société publique de gestion de l'eau;</p>",
            },
            {
                "id": "plan-expropriation",
                "title": u"Plan d'expropriation",
                "description": "<p> est situé dans les limites d'un plan d'expropriation approuvé par ... du ... ; le pouvoir expropriant est : ...;</p>",
            },
            {
                "id": "droit-de-preemption",
                "title": u"Droit de préemption",
                "description": "<p>est situé dans un périmètre d'application du droit de préemption arrêté par ... du ...; le(s}, bénéficiaires(s) du droit de préemption est (sont) : ...;</p>",
            },
            {
                "id": "perimetre-site-desaffecte",
                "title": u"Périmètre site désaffecté",
                "description": "<p>est situé dans le périmètre du site d'activité économique désaffecté suivant : ...;</p>",
            },
            {
                "id": "revitalisation-urbaine",
                "title": u"Revitalisation urbaine",
                "description": "<p>est situé dans un périmètre de revitalisation urbaine;</p>",
            },
            {
                "id": "classe",
                "title": u"Classé (article 196 du CWATUPE),",
                "description": "<p>est - inscrit sur la liste de sauvegarde visée à l'article 193 - classé en application de l'article 196 - situé dans une zone de protection visée à l'article 209 - localisé dans un site repris à l'inventaire des sites archéologiques visés à l'article 233 - du Code précité;</p>",
            },
        ],
        "townshipspecificfeatures": [
            "SpecificFeatureTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "zone-a-risque",
                "title": u"Se trouve dans une zone à risque",
                "description": "<p>se trouve dans une zone à risque (faible moyen élevé}, dans la cartographie Aléa d'inondation par débordement de cours d'eau - dressée dans le cadre du plan P.L.U.I.E.S et annexée à l'arrêté du Gouvernement Wallon, adopté en date du 13 juillet 2008;</p>",
                "relatedFields": ["floodingLevel", ""],
            },
            {
                "id": "insalubrite",
                "title": u"Est frappé d'un Arrêté d'insalubrité",
                "description": "<p>est frappé d'un Arrêté d'insalubrité OU d'un permis de location datant du [...] - Le futur acquéreur est invité à prendre contact avec le Service Logement Salubrité (tél. : [...]}, pour de plus amples informations;</p>",
            },
            {
                "id": "infraction-urbanistique",
                "title": u"Infraction urbanistique",
                "description": "<p>fait l'objet d'une infraction urbanistique reconnue par notre Administration communale portant sur [...];</p>",
            },
            {
                "id": "cu1",
                "title": u"Certificat d'Urbanisme 1 dans les deux ans",
                "description": "<p>a fait l'objet, dans les deux dernières années, d'un Certificat d'Urbanisme n°1 datant du [...] et portant la référence [...];</p>",
            },
            {
                "id": "permis-urbanisme",
                "title": u"Permis d'Urbanisme depuis 1976",
                "description": "<p>a fait l'objet depuis 1976 d'un permis d'urbanisme daté de [...] pour [...] - REFUS/ACCEPTE - Réf.: [...];</p>",
            },
            {
                "id": "reconnaissance-economique",
                "title": u"Périmètre de reconnaissance économique",
                "description": "<p>est repris dans un périmètre de reconnaissance économique;</p>",
            },
            {
                "id": "site-seveso",
                "title": u"A moins de 2000m d'un site SEVESO",
                "description": "<p>est situé à moins de 2000m d'un site classé SEVESO à savoir [...];</p>",
            },
            {
                "id": "gestion-des-sols",
                "title": u"Gestion des sols",
                "description": "<p>état des sols, nous ne sommes pas en mesure de déterminer si le bien est ou pas inscrit dans la banque de données au sens de l'article 10 du décret du 5 décembre 2008 relatif à la gestion des sols (Décret du 05 décembre 2008, art.89, al.2},</p>",
            },
            {
                "id": "galeries-minieres",
                "title": u"Galeries minières",
                "description": "<p>est situé dans une région traversée par de nombreuses galeries minières et nous ne sommes pas en mesure de déterminer l'état de celle-ci, veuillez donc prendre vos renseignements auprès du SPW - Département de l'Environnement et de l'Eau - Direction des risques industriels, géologique et miniers - Cellules sous-sol/géologique - Avenue Prince de Liège, 15 à 5100 Jambes;  Le bien est situé sur une zone de consultation en liaison avec les gisements et puits de mine;</p>",
            },
        ],
        "opinionstoaskifworks": [
            "UrbanVocabularyTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "ores-gaz-electricite",
                "title": u"ORES - Gaz-Electricité",
                "description": u"<p>Adresse</p>",
            },
            {
                "id": "ores-eclairage-public",
                "title": u"ORES - Service Eclairage public",
                "description": u"<p>Adresse</p>",
            },
            {"id": "belgacom", "title": u"Belgacom", "description": u"<p>Adresse</p>"},
            {"id": "fluxsys", "title": u"Fluxsys", "description": u"<p>Adresse</p>"},
            {
                "id": "air-liquide",
                "title": u"Air Liquide - Div. Belge - Service des Canalisations",
                "description": u"<p>Adresse</p>",
            },
            {
                "id": "elia-asset-sud",
                "title": u"Elia Asset Sud",
                "description": u"<p>Adresse</p>",
            },
            {
                "id": "swde",
                "title": u"SWDE (Société Wallone de Distribution d'Eau),",
                "description": u"<p>Adresse</p>",
            },
            {"id": "voo", "title": u"Voo", "description": u"<p>Adresse</p>"},
        ],
        "basement": [
            "UrbanVocabularyTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
            {
                "id": "zone-carriere",
                "title": u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les carrières souterraines",
            },
            {
                "id": "zone-karstique",
                "title": u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les phénomènes karstiques",
            },
            {
                "id": "zone-gisement-et-puit",
                "title": u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les gisements et puits de mine",
            },
            {
                "id": "zone-miniere",
                "title": u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les minières de fer",
            },
        ],
        "zip": [
            "UrbanVocabularyTerm",
            [
                "UrbanCertificateOne",
                "CODT_UrbanCertificateOne",
                "UrbanCertificateTwo",
                "NotaryLetter",
                "CODT_NotaryLetter",
            ],
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
            [
                "BuildLicence",
                "Article127",
                "UniqueLicence",
                "IntegratedLicence",
                "ParcelOutLicence",
                "UrbanCertificateTwo",
            ],
            {
                "id": "330-1",
                "title": u"330 1° - « [...] bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et [...] »",
                "description": "<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu'à cinquante mètres de part et d'autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 1°",
            },
            {
                "id": "330-2",
                "title": u"330 2° - « [...] bâtiment dont la profondeur, mesurée [...] est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments [...] »",
                "description": "<p>« la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës (AGW du 23 décembre 1998, art 1er), la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 2°",
            },
            {
                "id": "330-3",
                "title": u"330 3° - « [...] un magasin [...] dont la surface nette de vente est supérieure à 400 m² [...] »",
                "description": "<p>« la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface nette de vente est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 3°",
            },
            {
                "id": "330-4",
                "title": u"330 4° - « [...] de bureaux [...] dont la superficie des planchers est supérieure à 650 m² [...] »",
                "description": "<p>« la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à 650 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 4°",
            },
            {
                "id": "330-5",
                "title": u"330 5° - « [...] bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² [...] »",
                "description": "<p>« la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>",
                "extraValue": "330 5°",
            },
            {
                "id": "330-6",
                "title": u"330 6° - « l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »",
                "description": "<p>« l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »</p>",
                "extraValue": "330 6°",
            },
            {
                "id": "330-7",
                "title": u"330 7° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »",
                "description": "<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »</p>",
                "extraValue": "330 7°",
            },
            {
                "id": "330-8",
                "title": u"330 8° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »",
                "description": "<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »</p>",
                "extraValue": "330 8°",
            },
            {
                "id": "330-9",
                "title": u"330 9° - « les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »",
                "description": "<p>« les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »</p>",
                "extraValue": "330 9°",
            },
            {
                "id": "330-10",
                "title": u"330 10° - « les demandes de permis de lotir visées à l'article 97 »",
                "description": "<p>« les demandes de permis de lotir visées à l'article 97 »</p>",
                "extraValue": "330 10°",
            },
            {
                "id": "330-11",
                "title": u"330 11° - « les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »",
                "description": "<p>« les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »</p>",
                "extraValue": "330 11°",
            },
            {
                "id": "330-12",
                "title": u"330 12° - « [...] permis de lotir et les demandes de permis d'urbanisme [...] d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde [...] »",
                "description": "<p>« les demandes de permis de lotir et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protection visée à l'article 205 (lire article 209) ou localisés dans un site mentionné à l'atlas visé à l'article 215 (lire article 233) »</p>",
                "extraValue": "330 12°",
            },
            {
                "id": "330-13",
                "title": u"330 13° - « les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »",
                "description": "<p>« les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »</p>",
                "extraValue": "330 13°",
            },
            {
                "id": "334-2",
                "title": u"334 2° - « Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique [...]»",
                "description": "<p>« Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique, le demandeur est tenu d'afficher sur le terrain faisant l'objet de la demande : 2° dans les cas visés à l'article 330, 1° à 5°, et 12°, ou lorsque la dérogation porte sur le gabarit d'un bâtiment, une vue axonométrique du projet et des bâtiments contigus »</p>",
                "extraValue": "334 2°",
            },
        ],
        "roadanalysis": [
            "UrbanVocabularyTerm",
            [
                "BuildLicence",
                "Article127",
                "UniqueLicence",
                "IntegratedLicence",
                "ParcelOutLicence",
                "UrbanCertificateTwo",
                "CODT_UniqueLicence",
                "CODT_IntegratedLicence",
                "CODT_CommercialLicence",
                "RoadDecree",
            ],
            {"id": "deficient-equipment", "title": u"Voire insuffisamment équipée"},
            {
                "id": "transformation",
                "title": u"Transformation sans nouveau raccordement à l'égout",
            },
            {"id": "extension", "title": u"Extension de réseau"},
            {"id": "fallback-zone", "title": u"Zone de recul supérieure à 5 m"},
            {
                "id": "built-surface",
                "title": u"Surface bâtie supérieure au 1/4 de la parcelle",
            },
            {"id": "aide-opinion", "title": u"Avis AIDE sollicité"},
        ],
        "townroaddecree": [
            "UrbanVocabularyTerm",
            ["RoadDecree"],
            {"id": "commune", "title": u"Commune"},
        ],
        "folderdelays": [
            "UrbanDelay",
            ["BuildLicence", "ParcelOutLicence", "UrbanCertificateTwo"],
            {"id": "30j", "title": u"30 jours", "deadLineDelay": 30, "alertDelay": 20},
            {"id": "70j", "title": u"70 jours", "deadLineDelay": 70, "alertDelay": 20},
            {"id": "75j", "title": u"75 jours", "deadLineDelay": 75, "alertDelay": 20},
            {
                "id": "115j",
                "title": u"115 jours",
                "deadLineDelay": 115,
                "alertDelay": 20,
            },
            {
                "id": "230j",
                "title": u"230 jours",
                "deadLineDelay": 230,
                "alertDelay": 20,
            },
            {
                "id": "inconnu",
                "title": u"Inconnu",
                "deadLineDelay": 0,
                "alertDelay": 20,
            },
        ],
        "derogations": [
            "UrbanVocabularyTerm",
            [
                "BuildLicence",
                "Article127",
                "UniqueLicence",
                "IntegratedLicence",
                "ParcelOutLicence",
                "UrbanCertificateTwo",
                "CODT_UniqueLicence",
                "CODT_IntegratedLicence",
                "CODT_CommercialLicence",
            ],
            {"id": "dero-ps", "title": u"au Plan de secteur"},
            {"id": "dero-pca", "title": u"au Plan Communal d'Aménagement"},
            {"id": "dero-rru", "title": u"au Règlement Régional d'Urbanisme"},
            {"id": "dero-rcu", "title": u"au Règlement Communal d'Urbanisme"},
            {"id": "dero-lot", "title": u"au Lotissement"},
        ],
        "folderbuildworktypes": [
            "UrbanVocabularyTerm",
            [
                "BuildLicence",
                "Article127",
                "UniqueLicence",
                "IntegratedLicence",
                "ParcelOutLicence",
                "UrbanCertificateTwo",
                "CODT_BuildLicence",
                "CODT_ParcelOutLicence",
                "CODT_UrbanCertificateTwo",
                "CODT_UniqueLicence",
                "CODT_IntegratedLicence",
                "CODT_CommercialLicence",
            ],
            {"id": "AUTRE", "title": u"Autres", "extraValue": "AUTRE"},
            {"id": "DEM", "title": u"Démolition", "extraValue": "DEM"},
            {
                "id": "DOM_PUB",
                "title": u"Intégration dans voirie publique",
                "extraValue": "DOM_PUB",
            },
            {
                "id": "GRONDPUBL",
                "title": u"Transformation non-bâti - Terrain pour installations publicitaires",
                "extraValue": "GRONDPUBL",
            },
            {
                "id": "INT",
                "title": u"Intégration dans voirie publique",
                "extraValue": "INT",
            },
            {
                "id": "LEASING",
                "title": u"Leasing (pour mémoire SPF Finances),",
                "extraValue": "LEASING",
            },
            {"id": "LOT", "title": u"Lotissement - Général", "extraValue": "LOT"},
            {
                "id": "N_APPART",
                "title": u"Nouvelle construction - Immeuble appartements",
                "extraValue": "N_APPART",
            },
            {
                "id": "N_AUT",
                "title": u"Nouvelle construction - Autres",
                "extraValue": "N_AUT",
            },
            {
                "id": "N_BIJ",
                "title": u"Nouvelle construction - Annexe",
                "extraValue": "N_BIJ",
            },
            {
                "id": "N_HANDEL",
                "title": u"Nouvelle construction - Commerce, horeca, services",
                "extraValue": "N_HANDEL",
            },
            {
                "id": "N_INDUS",
                "title": u"Nouvelle construction - Industrie, artisanat",
                "extraValue": "N_INDUS",
            },
            {
                "id": "N_INFRA",
                "title": u"Nouvelle construction - Infrastructures",
                "extraValue": "N_INFRA",
            },
            {
                "id": "N_KANTOOR",
                "title": u"Nouvelle construction - Bureaux",
                "extraValue": "N_KANTOOR",
            },
            {
                "id": "N_LANDTUIN",
                "title": u"Nouvelle construction - Agriculture et horticulture",
                "extraValue": "N_LANDTUIN",
            },
            {
                "id": "N_OPENBAAR",
                "title": u"Nouvelle construction - Équipement communautaire ou d'ordre public",
                "extraValue": "N_OPENBAAR",
            },
            {
                "id": "N_TOERISME",
                "title": u"Nouvelle construction - Tourisme et récréation",
                "extraValue": "N_TOERISME",
            },
            {
                "id": "N_UNI",
                "title": u"Nouvelle construction unifamiliale",
                "extraValue": "N_UNI",
            },
            {
                "id": "ONTBOSSEN",
                "title": u"Transformation non-bâti - Déboisement",
                "extraValue": "ONTBOSSEN",
            },
            {
                "id": "OPSLAFVAL",
                "title": u"Transformation non-bâti - Terrain pour entreposage",
                "extraValue": "OPSLAFVAL",
            },
            {
                "id": "PARKING",
                "title": u"Transformation non-bâti - Terrain pour parking",
                "extraValue": "PARKING",
            },
            {
                "id": "PUBLICIT",
                "title": u"Autres - Installations ou enseignes publicitaires",
                "extraValue": "PUBLICIT",
            },
            {"id": "RUINE", "title": u"Ruine", "extraValue": "RUINE"},
            {"id": "S_BIJ", "title": u"Démolition - Annexe", "extraValue": "S_BIJ"},
            {
                "id": "S_EEN",
                "title": u"Démolition - Maison unifamiliale",
                "extraValue": "S_EEN",
            },
            {
                "id": "S_HANDEL",
                "title": u"Démolition - Commerce, horeca, services",
                "extraValue": "S_HANDEL",
            },
            {
                "id": "S_INDUS",
                "title": u"Démolition - Industrie, artisanat",
                "extraValue": "S_INDUS",
            },
            {
                "id": "S_INFRA",
                "title": u"Démolition - Infrastructures",
                "extraValue": "S_INFRA",
            },
            {
                "id": "S_KANTOOR",
                "title": u"Démolition - Bureaux",
                "extraValue": "S_KANTOOR",
            },
            {
                "id": "S_LANDTUIN",
                "title": u"Démolition - Agriculture et horticulture",
                "extraValue": "S_LANDTUIN",
            },
            {
                "id": "S_MEER",
                "title": u"Démolition - Immeuble appartements",
                "extraValue": "S_MEER",
            },
            {
                "id": "S_OPENBAAR",
                "title": u"Démolition - Équipement communautaire ou d'ordre public",
                "extraValue": "S_OPENBAAR",
            },
            {
                "id": "S_TOERISME",
                "title": u"Démolition - Tourisme et récréation",
                "extraValue": "S_TOERISME",
            },
            {
                "id": "T_APPART",
                "title": u"Transformation - immeuble appartements",
                "extraValue": "T_APPART",
            },
            {
                "id": "T_AUT",
                "title": u"Transformation - autre bâtiment",
                "extraValue": "T_AUT",
            },
            {
                "id": "T_NBAT",
                "title": u"Transformation parcelle non bâtie",
                "extraValue": "T_NBAT",
            },
            {
                "id": "T_UNI",
                "title": u"Transformation habitation unifamiliale",
                "extraValue": "T_UNI",
            },
            {"id": "TAUDIS", "title": u"Taudis", "extraValue": "TAUDIS"},
            {
                "id": "V_BIJ",
                "title": u"Transformation - annexe bâtie",
                "extraValue": "V_BIJ",
            },
            {
                "id": "V_INDUS",
                "title": u"Transformation - industrie, artisanat",
                "extraValue": "V_INDUS",
            },
            {
                "id": "V_INFRA",
                "title": u"Transformation - infrastructures",
                "extraValue": "V_INFRA",
            },
            {
                "id": "V_KANTOOR",
                "title": u"Transformation - bureaux",
                "extraValue": "V_KANTOOR",
            },
            {
                "id": "V_LANDTUIN",
                "title": u"Transformation - agriculture et horticulture",
                "extraValue": "V_LANDTUIN",
            },
            {
                "id": "V_OPENBAAR",
                "title": u"Transformation - équipement communautaire ou d'ordre public",
                "extraValue": "V_OPENBAAR",
            },
            {
                "id": "V_TOERISME",
                "title": u"Transformation - tourisme et récréation",
                "extraValue": "V_TOERISME",
            },
            {
                "id": "VELHOOGST",
                "title": u"Transformation non-bâti - Abbattre arbres de haute tige",
                "extraValue": "VELHOOGST",
            },
            {
                "id": "VERNIETG",
                "title": u"Lotissement - annulation",
                "extraValue": "VERNIETG",
            },
            {
                "id": "WIJZAANTAL",
                "title": u"Transformation - Changement du nombre d'habitations",
                "extraValue": "WIJZAANTAL",
            },
            {
                "id": "WIJZIG",
                "title": u"Lotissement - changement de lotissement",
                "extraValue": "WIJZIG",
            },
            {
                "id": "WIJZRELIEF",
                "title": u"Transformation non-bâti - Transformation relief",
                "extraValue": "WIJZRELIEF",
            },
        ],
        "tax": [
            "UrbanVocabularyTerm",
            URBAN_TYPES,
            {"id": "150", "title": u"150"},
            {"id": "180", "title": u"180"},
            {"id": "other", "title": u"Autre"},
        ],
        "offense_articles": [
            "UrbanVocabularyTerm",
            ["Ticket", "Inspection"],
            {
                "id": "art1",
                "title": u"1° exécution sans permis préalable ou non conformément au permis Puisque non-respect de l’ (des)article(s) Art. DIV.4",
            },
            {"id": "art1.1", "title": u"construire", "numbering": u"... "},
            {"id": "art1.2", "title": u"enseignes / pub", "numbering": u"... "},
            {"id": "art1.3", "title": u"démolir", "numbering": u"... "},
            {"id": "art1.4", "title": u"reconstruire", "numbering": u"... "},
            {"id": "art1.5", "title": u"transformer", "numbering": u"... "},
            {
                "id": "art1.6",
                "title": u"créer un nouveau logement",
                "numbering": u"... ",
            },
            {
                "id": "art1.7",
                "title": u"modifier la destination ",
                "numbering": u"... ",
            },
            {"id": "art1.8", "title": u"modifier surf. vente", "numbering": u"... "},
            {"id": "art1.9", "title": u"relief du sol", "numbering": u"... "},
            {"id": "art1.10", "title": u"boiser ou déboiser", "numbering": u"... "},
            {
                "id": "art1.11",
                "title": u"abattre a) arbres isolés à haute tige dans espaces verts",
                "numbering": u"... ",
            },
            {
                "id": "art1.11",
                "title": u"abattre b) haies ou allées (R.IV.4-6)",
                "numbering": u"... ",
            },
            {
                "id": "art1.12",
                "title": u"abattre arbre/haie remarquable",
                "numbering": u"... ",
            },
            {"id": "art1.13", "title": u"défricher", "numbering": u"... "},
            {"id": "art1.14", "title": u"sapins de Noël", "numbering": u"... "},
            {
                "id": "art1.15",
                "title": u"a) dépôt véhicules, mitrailles...",
                "numbering": u"... ",
            },
            {
                "id": "art1.16",
                "title": u"b) installations mobiles",
                "numbering": u"... ",
            },
            {
                "id": "art1.17",
                "title": u"itravaux de restauration CoPat / liste de sauvegarde, classé ou assimilé",
                "numbering": u"... ",
            },
            {
                "id": "art2",
                "title": u"2° poursuite sans permis préalable ou postérieurement à l’acte ou à l’arrêt de suspension du permis",
            },
            {
                "id": "art3",
                "title": u"3° maintien des travaux exécutés après le 21 avril 1962 sans le permis qui était requis",
            },
            {"id": "art4", "title": u"4° non-respect PS et GRU"},
            {"id": "art5", "title": u"5° le non-respect affichage du permis"},
            {"id": "art6", "title": u"6° absence de notif début travaux"},
            {"id": "art7", "title": u"7° non-respect du CoPat"},
        ],
    },
    "global": {
        "deposittype": [
            "UrbanVocabularyTerm",
            {"id": "recommande", "title": u"Par recommandé postal"},
            {"id": "surplace", "title": u"Déposé à l'administration communale"},
        ],
        "recoursedecisions": [
            "UrbanVocabularyTerm",
            {"id": "confirme", "title": u"Confirmé"},
            {"id": "infirme", "title": u"Infirmé"},
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
            {
                "id": "pca2",
                "label": u"Plan communal d'aménagement 2",
                "number": "2",
                "decreeDate": "2008/06/23",
                "decreeType": "royal",
            },
            {
                "id": "pca3",
                "label": u"Plan communal d'aménagement 3",
                "number": "3",
                "decreeDate": "2001/12/13",
                "decreeType": "departmental",
            },
        ],
        "pcazones": [
            "UrbanVocabularyTerm",
            {
                "id": "zone-de-construction-d-habitation-fermee",
                "title": u"Zone de construction d'habitation fermée",
            },
            {
                "id": "zone-de-construction-d-habitation-semi-ouverte",
                "title": u"Zone de construction d'habitation semi ouverte",
            },
            {
                "id": "zone-de-construction-d-habitation-ouverte",
                "title": u"Zone de construction d'habitation ouverte",
            },
            {
                "id": "zone-de-construction-en-annexe",
                "title": u"Zone de construction en annexe",
            },
            {"id": "zone-de-recul", "title": u"Zone de recul"},
            {"id": "zone-artisanale", "title": u"Zone artisanale"},
            {"id": "zone-de-voirie", "title": u"Zone de voirie"},
            {"id": "zone-affectee-a-l-eau", "title": u"Zone affectée à l'eau"},
            {
                "id": "zone-de-construction-a-destination-publique-indifferenciee",
                "title": u"Zone de construction à destination publique indifférenciée",
            },
            {
                "id": "zone-agricole-indiferenciee",
                "title": u"Zone agricole indifférenciée",
            },
        ],
        "sols": [
            "PcaTerm",
            {
                "id": "sol1",
                "title": "Schéma d'orientation local 1",
                "label": u"Schéma d'orientation local 1",
                "number": "1",
                "decreeDate": "2009/01/01",
                "decreeType": "royal",
            },
            {
                "id": "sol2",
                "title": "Schéma d'orientation local 2",
                "label": u"Schéma d'orientation local 2",
                "number": "2",
                "decreeDate": "2008/06/23",
                "decreeType": "royal",
            },
            {
                "id": "sol3",
                "title": "Schéma d'orientation local 3",
                "label": u"Schéma d'orientation local 3",
                "number": "3",
                "decreeDate": "2001/12/13",
                "decreeType": "departmental",
            },
        ],
        "solzones": [
            "UrbanVocabularyTerm",
            {
                "id": "zone-de-construction-d-habitation-fermee",
                "title": u"Zone de construction d'habitation fermée",
            },
            {
                "id": "zone-de-construction-d-habitation-semi-ouverte",
                "title": u"Zone de construction d'habitation semi ouverte",
            },
            {
                "id": "zone-de-construction-d-habitation-ouverte",
                "title": u"Zone de construction d'habitation ouverte",
            },
            {
                "id": "zone-de-construction-en-annexe",
                "title": u"Zone de construction en annexe",
            },
            {"id": "zone-de-recul", "title": u"Zone de recul"},
            {"id": "zone-artisanale", "title": u"Zone artisanale"},
            {"id": "zone-de-voirie", "title": u"Zone de voirie"},
            {"id": "zone-affectee-a-l-eau", "title": u"Zone affectée à l'eau"},
            {
                "id": "zone-de-construction-a-destination-publique-indifferenciee",
                "title": u"Zone de construction à destination publique indifférenciée",
            },
            {
                "id": "zone-agricole-indiferenciee",
                "title": u"Zone agricole indiférenciée",
            },
        ],
        "pashs": [
            "UrbanVocabularyTerm",
            {
                "id": "zone-epuration-collective",
                "title": u"Zone d'assainissement collectif",
            },
            {"id": "zone-transitoire", "title": u"Zone d'assainissement transitoire"},
            {
                "id": "zone-epuration-individuelle",
                "title": u"Zone d'assainissement individuel",
            },
        ],
        "sewers": [
            "UrbanVocabularyTerm",
            {"id": "unitaire", "title": u"Unitaire"},
            {"id": "separatoire", "title": u"Séparatoire"},
            {"id": "inexistant", "title": u"Inexistant"},
        ],
        "folderroadtypes": [
            "UrbanVocabularyTerm",
            {"id": "com", "title": u"Communale"},
            {"id": "priv", "title": u"Privée"},
            {"id": "reg", "title": u"Régionale"},
        ],
        "folderprotectedbuildings": [
            "UrbanVocabularyTerm",
            {"id": "classe", "title": u"classé ou assimilé"},
            {
                "id": "certificatpatrimoine",
                "title": u"certificat de patrimoine délivré",
            },
            {"id": "zoneprotection", "title": u"zone de protection"},
            {"id": "reprisinventaire", "title": u"repris à l'inventaire"},
            {"id": "archeologique", "title": u"à l'Atlas archéologique"},
        ],
        "folderroadequipments": [
            "UrbanVocabularyTerm",
            {"id": "eau", "title": u"distribution d'eau"},
            {"id": "electricite", "title": u"distribution électrique"},
            {
                "id": "epuration",
                "title": u"canalisation reliée à une station d'épuration publique",
            },
            {
                "id": "nonepuration",
                "title": u"canalisation non-reliée à une station d'épuration publique",
            },
            {"id": "egoutsep", "title": u"réseau d'égouttage séparatif"},
            {
                "id": "pascollecteeaux",
                "title": u"pas de canalisation de collecte des eaux",
            },
            {"id": "fosse", "title": u"fossé"},
        ],
        "folderroadcoatings": [
            "UrbanVocabularyTerm",
            {"id": "filetseau", "title": u"Filets d'eau"},
            {"id": "bordures", "title": u"Bordures"},
        ],
        "folderzones": [
            "UrbanVocabularyTerm",
            {"id": "zh", "title": u"zone d'habitat"},
            {"id": "zhcr", "title": u"zone d'habitat à caractère rural"},
            {
                "id": "zhcrza",
                "title": u"zone d’habitat à caractère rural sur +/- 50 m et le surplus en zone agricole",
            },
            {
                "id": "zspec",
                "title": u"zone de services publics et d'équipements communautaires",
            },
            {"id": "zcet", "title": u"zone de centre d'enfouissement technique"},
            {"id": "zl", "title": u"zone de loisirs"},
            {"id": "zaem", "title": u"zones d'activité économique mixte"},
            {"id": "zaei", "title": u"zones d'activité économique industrielle"},
            {
                "id": "zaesae",
                "title": u"zones d'activité économique spécifique agro-économique",
            },
            {
                "id": "zaesgd",
                "title": u"zones d'activité économique spécifique grande distribution",
            },
            {"id": "ze", "title": u"zone d'extraction"},
            {
                "id": "zadci",
                "title": u"zone d'aménagement différé à caractère industriel",
            },
            {"id": "za", "title": u"zone agricole"},
            {"id": "zf", "title": u"zone forestière"},
            {"id": "zev", "title": u"zone d'espaces verts"},
            {"id": "zn", "title": u"zone naturelle"},
            {"id": "zp", "title": u"zone de parc"},
            {"id": "zacc", "title": u"zone d'aménagement communal concerté"},
        ],
        "rcu": [
            "UrbanVocabularyTerm",
            {"id": "rcu-aire-a", "title": u"Aire A habitat centre des villages"},
            {"id": "rcu-aire-b", "title": u"Aire B habitat hors centre des villages"},
            {"id": "rcu-aire-c", "title": u"Aire C rives des habitats"},
            {"id": "rcu-aire-d", "title": u"Aire D activités économiques"},
            {"id": "rcu-aire-e", "title": u"Aire E dominante rurale"},
        ],
        "township_guide": [
            "UrbanVocabularyTerm",
            {"id": "rcu-aire-a", "title": u"Aire A habitat centre des villages"},
            {"id": "rcu-aire-b", "title": u"Aire B habitat hors centre des villages"},
            {"id": "rcu-aire-c", "title": u"Aire C rives des habitats"},
            {"id": "rcu-aire-d", "title": u"Aire D activités économiques"},
            {"id": "rcu-aire-e", "title": u"Aire E dominante rurale"},
        ],
        "ssc": [
            "UrbanVocabularyTerm",
            {
                "id": "ssc-centre-ville",
                "title": u"Zone d'habitat urbain de centre-ville",
            },
            {"id": "ssc-suburbain", "title": u"Zone d'habitat suburbain"},
            {
                "id": "ssc-services-publics",
                "title": u"Zone de services publics et d'équipements communautaires",
            },
            {"id": "ssc-industrielle", "title": u"Zone industrielle"},
            {"id": "ssc-industrielle-verte", "title": u"Zone industrielle verte"},
            {"id": "ssc-militaire", "title": u"Zone militaire"},
            {
                "id": "ssc-habitat-urban-differe",
                "title": u"Zone d'habitat urbain à aménagement différé",
            },
            {"id": "ssc-extraction", "title": u"Zone d'extraction"},
            {"id": "ssc-loisirs", "title": u"Zone de loisirs et de séjours"},
            {"id": "ssc-agricole", "title": u"Zone agricole"},
            {"id": "ssc-vert-social", "title": u"Zone d'espace vert social"},
            {"id": "ssc-vert-eco", "title": u"Zone d'espace vert ecologique"},
            {"id": "ssc-vert-mixte", "title": u"Zone d'espace vert mixte"},
            {"id": "ssc-naturelle", "title": u"Zone naturelle"},
            {"id": "ssc-forestiere", "title": u"Zone forestière"},
            {"id": "ssc-forestiere-mixte", "title": u"Zone forestière mixte"},
            {
                "id": "ssc-activites-economiques-mixtes",
                "title": u"Zone d'activités économiques mixtes",
            },
            {
                "id": "ssc-activites-economiques-tertiaires",
                "title": u"Zone d'activités économiques tertiaires",
            },
        ],
        "sct": [
            "UrbanVocabularyTerm",
            {
                "id": "sct-zone-urbaine-de-centre-ville-de-grande-mixite",
                "title": u"Zone urbaine de centre ville de grande mixité (minimum 50 log/ha)",
            },
            {"id": "sct-zone-urbaine", "title": u"Zone urbaine (de 40 à 60 log/ha)"},
            {
                "id": "sct-zone-de-village-et-ou-peri-urbaine",
                "title": u"Zone de village et/ou péri-urbaine (de 20 à 40 log/ha)",
            },
            {
                "id": "sct-zone-residentielle",
                "title": u"Zone résidentielle (de 12 à 20 log/ha)",
            },
            {
                "id": "sct-zone-paysagere-de-tres-faible-densite",
                "title": u"Zone paysagère de très faible densité (maximum 5 log/ha)",
            },
            {"id": "sct-zone-ecologique", "title": u"Zone écologique"},
            {
                "id": "sct-perimetre-de-protection-paysagere",
                "title": u"Périmètre de protection paysagère",
            },
            {
                "id": "sct-activite-economique-mixte",
                "title": u"Activité économique mixte",
            },
            {
                "id": "sct-activite-economique-industrielle",
                "title": u"Activité économique industrielle",
            },
        ],
        "sdc": [
            "UrbanVocabularyTerm",
            {
                "id": "sdc-centre-ville",
                "title": u"Zone d'habitat urbain de centre-ville",
            },
            {"id": "sdc-suburbain", "title": u"Zone d'habitat suburbain"},
            {
                "id": "sdc-services-publics",
                "title": u"Zone de services publics et d'équipements communautaires",
            },
            {"id": "sdc-industrielle", "title": u"Zone industrielle"},
            {"id": "sdc-industrielle-verte", "title": u"Zone industrielle verte"},
            {"id": "sdc-militaire", "title": u"Zone militaire"},
            {
                "id": "sdc-habitat-urban-differe",
                "title": u"Zone d'habitat urbain à aménagement différé",
            },
            {"id": "sdc-extraction", "title": u"Zone d'extraction"},
            {"id": "sdc-loisirs", "title": u"Zone de loisirs et de séjours"},
            {"id": "sdc-agricole", "title": u"Zone agricole"},
            {"id": "sdc-vert-social", "title": u"Zone d'espace vert social"},
            {"id": "sdc-vert-eco", "title": u"Zone d'espace vert ecologique"},
            {"id": "sdc-vert-mixte", "title": u"Zone d'espace vert mixte"},
            {"id": "sdc-naturelle", "title": u"Zone naturelle"},
            {"id": "sdc-forestiere", "title": u"Zone forestière"},
            {"id": "sdc-forestiere-mixte", "title": u"Zone forestière mixte"},
            {
                "id": "sdc-activites-economiques-mixtes",
                "title": u"Zone d'activités économiques mixtes",
            },
            {
                "id": "sdc-activites-economiques-tertiaires",
                "title": u"Zone d'activités économiques tertiaires",
            },
        ],
        "prenu": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Revitalisation urbaine de XXX"},
            {"id": "yyy", "title": u"Revitalisation urbaine de YYY"},
            {"id": "zzz", "title": u"Revitalisation urbaine de ZZZ"},
        ],
        "prevu": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Rénovation urbaine de XXX"},
            {"id": "yyy", "title": u"Rénovation urbaine de YYY"},
            {"id": "zzz", "title": u"Rénovation urbaine de ZZZ"},
        ],
        "reparcelling": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Remembrement XXX"},
            {"id": "yyy", "title": u"Remembrement YYY"},
            {"id": "zzz", "title": u"Remembrement ZZZ"},
        ],
        "rgbsr": [
            "UrbanVocabularyTerm",
            {
                "id": "limoneux-brabancon",
                "title": u"du Plateau Limoneux Brabançon (art. 322-15 (lire « article 420 »));",
            },
            {
                "id": "limoneux-hennuyer",
                "title": u"du Plateau Limoneux Hennuyer (art. 322-15 (lire « article 420 »));",
            },
            {
                "id": "hesbaye",
                "title": u"de la Hesbaye (art. 322-17 (lire « article 422 »));",
            },
            {
                "id": "herve",
                "title": u"du Pays de Herve (art. 322-18 (lire « article 423 »));",
            },
            {
                "id": "condroz",
                "title": u"du Condroz (art. 322,-19 (lire « article 424 »));",
            },
            {
                "id": "famenne",
                "title": u"de la Fagne-Famenne (art. 322-2 (lire « article 425 »));",
            },
            {
                "id": "ardenne",
                "title": u"de l’Ardenne (art. 322-21 (lire « article 426 »));",
            },
            {
                "id": "lorraine",
                "title": u"de la Lorraine (art. 322-22 (lire « article 427 »));",
            },
        ],
        "regional_guide": [
            "UrbanVocabularyTerm",
            {
                "id": "limoneux-brabancon",
                "title": u"du Plateau Limoneux Brabançon (art. 322-15 (lire « article 420 »));",
            },
            {
                "id": "limoneux-hennuyer",
                "title": u"du Plateau Limoneux Hennuyer (art. 322-15 (lire « article 420 »));",
            },
            {
                "id": "hesbaye",
                "title": u"de la Hesbaye (art. 322-17 (lire « article 422 »));",
            },
            {
                "id": "herve",
                "title": u"du Pays de Herve (art. 322-18 (lire « article 423 »));",
            },
            {
                "id": "condroz",
                "title": u"du Condroz (art. 322,-19 (lire « article 424 »));",
            },
            {
                "id": "famenne",
                "title": u"de la Fagne-Famenne (art. 322-2 (lire « article 425 »));",
            },
            {
                "id": "ardenne",
                "title": u"de l’Ardenne (art. 322-21 (lire « article 426 »));",
            },
            {
                "id": "lorraine",
                "title": u"de la Lorraine (art. 322-22 (lire « article 427 »));",
            },
        ],
        "airportnoisezone": [
            "UrbanVocabularyTerm",
            {"id": "zone-expo-a", "title": u"Zone A' au plan d'Exposition au bruit"},
            {
                "id": "zone-devel-a",
                "title": u"Zone A au plan de Développement à Long Terme",
            },
            {"id": "zone-expo-b", "title": u"Zone B' au plan d'Exposition au bruit"},
            {
                "id": "zone-devel-b",
                "title": u"Zone B au plan de Développement à Long Terme",
            },
        ],
        "noteworthytrees": [
            "UrbanVocabularyTerm",
            {"id": "arbres", "title": u"Arbres remarquables"},
            {
                "id": "alignement",
                "title": u"Alignement d'arbres ou de haies remarquables ",
            },
            {"id": "haies", "title": u"Zone Haie remarquable"},
        ],
        "inquiry_suspension": [
            "UrbanVocabularyTerm",
            {"id": "summer", "title": u"du 16 juillet au 15 août"},
            {"id": "winter", "title": u"du 24 décembre au 31 décembre"},
        ],
        "persons_titles": [
            "PersonTitleTerm",
            {
                "id": "notitle",
                "title": u"",
                "extraValue": "Madame, Monsieur",
                "abbreviation": "",
                "gender": "male",
                "multiplicity": "single",
                "reverseTitle": "Monsieur, Madame",
            },
            {
                "id": "madam",
                "title": u"Madame",
                "extraValue": "Madame",
                "abbreviation": "Mme",
                "gender": "female",
                "multiplicity": "single",
                "reverseTitle": "Madame",
            },
            {
                "id": "mister",
                "title": u"Monsieur",
                "extraValue": "Monsieur",
                "abbreviation": "M",
                "gender": "male",
                "multiplicity": "single",
                "reverseTitle": "Monsieur",
            },
            {
                "id": "madam_and_mister",
                "title": u"Monsieur et Madame",
                "extraValue": "Madame, Monsieur",
                "abbreviation": "M et Mme",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Monsieur, Madame",
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
            {
                "id": "madam_or_mister_couple",
                "title": u"Madame ou Monsieur",
                "extraValue": "Madame, Monsieur",
                "abbreviation": "Mme ou Mr",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Monsieur ou Madame",
            },
            {
                "id": "master",
                "title": u"Maître",
                "extraValue": "Maître",
                "abbreviation": "Me",
                "gender": "male",
                "multiplicity": "single",
                "reverseTitle": "Maître",
            },
            {
                "id": "masters",
                "title": u"Maîtres",
                "extraValue": "Maitres",
                "abbreviation": "Mes",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Maitres",
            },
            {
                "id": "misters",
                "title": u"Messieurs",
                "extraValue": "Messieurs",
                "abbreviation": "MM",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Messieurs",
            },
            {
                "id": "ladies",
                "title": u"Mesdames",
                "extraValue": "Mesdames",
                "abbreviation": "Mmes",
                "gender": "female",
                "multiplicity": "plural",
                "reverseTitle": "Mesdames",
            },
            {
                "id": "consorts",
                "title": u"Consorts",
                "extraValue": "Consorts",
                "abbreviation": "Crts",
                "gender": "male",
                "multiplicity": "plural",
                "reverseTitle": "Consorts",
            },
        ],
        "persons_grades": [
            "UrbanVocabularyTerm",
            {"id": "agent-accueil", "title": "Agent d'accueil"},
            {"id": "agent-administratif", "title": "Agent administratif"},
            {"id": "agent-technique", "title": "Agent technique"},
            {"id": "agent-traitant", "title": "Agent traitant"},
            {"id": "directeur-administratif", "title": "Directeur administratif"},
            {"id": "directeur-general", "title": "Directeur général"},
            {"id": "directeur-technique", "title": "Directeur technique"},
            {"id": "reponsable", "title": "Responsable du Service Urbanisme"},
            {"id": "responsable-accueil", "title": "Responsable d'accueil"},
            {"id": "responsable-administratif", "title": "Responsable administratif"},
            {"id": "responsable-technique", "title": "Responsable technique"},
        ],
        "country": [
            "UrbanVocabularyTerm",
            {"id": "germany", "title": "Allemagne"},
            {"id": "belgium", "title": "Belgique"},
            {"id": "france", "title": "France"},
            {"id": "luxembourg", "title": "Luxembourg"},
            {"id": "netherlands", "title": "Pays Bas"},
        ],
        "externaldecisions": [
            "UrbanVocabularyTerm",
            {"id": "favorable", "title": u"Favorable"},
            {"id": "favorable-conditionnel", "title": u"Favorable conditionnel"},
            {"id": "defavorable", "title": u"Défavorable"},
            {
                "id": "favorable-defaut",
                "title": u"Réputé favorable par défaut",
                "isDefaultValue": True,
            },
        ],
        "rubrics": [
            "Folder",
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
        "karst_constraints": [
            "UrbanVocabularyTerm",
            {"id": "no", "title": u"Sans"},
            {"id": "low", "title": u"Faible"},
            {"id": "moderate", "title": u"Modéré"},
            {"id": "high", "title": u"Fort"},
        ],
        "concentrated_runoff_s_risk": [
            "UrbanVocabularyTerm",
            {"id": "low", "title": u"Faible, bassin versant afférent entre 1 et 9 Ha"},
            {
                "id": "medium",
                "title": u"Moyen, bassin versant afférent entre 9 et 18 Ha",
            },
            {"id": "high", "title": u"Elevé, bassin versant afférent de plus de 18 Ha"},
        ],
        "seveso_site": [
            "UrbanVocabularyTerm",
            {"id": "seuil-bas", "title": u"Seuil bas"},
            {"id": "seuil-haut", "title": u"Seuil haut"},
        ],
        "pipelines": [
            "UrbanVocabularyTerm",
            {"id": "fluxys", "title": u"Fluxys"},
            {"id": "oxyduc", "title": u"Oxyduc"},
            {"id": "otan", "title": u"Otan"},
        ],
        "natura_2000": [
            "UrbanVocabularyTerm",
            {"id": "xxx", "title": u"Périmètre NATURA 2000 de XXX"},
            {"id": "yyy", "title": u"Périmètre NATURA 2000 de YYY"},
        ],
        "groundstatestatus": [
            "UrbanVocabularyTerm",
            {"id": "no", "title": u"Non repris"},
            {"id": "lavande", "title": u"Couleur bleu lavande (indicatif)"},
            {"id": "peche", "title": u"Couleur pêche (démarches faites ou à prévoir)"},
        ],
        "delegatesignatures": [
            "UrbanVocabularyTerm",
            {"id": "adam", "title": u"Adam Smith"},
        ],
        "mainsignatures": [
            "UrbanVocabularyTerm",
            {"id": "sig_echevin_urbanisme", "title": u"Échevin de l'urbanisme"},
            {"id": "sig_echevin_environnement", "title": u"Échevin de l'environnement"},
            {"id": "sig_dg", "title": u"Direction Générale"},
            {"id": "sig_dg_adjoint", "title": u"Direction Générale (Adjoint)"},
        ],
        "form_composition": [
            "UrbanVocabularyTerm",
            {
                "id": "4",
                "title": u"Annexe IV - Demande de permis avec concours d'un architecte",
            },
            {
                "id": "5",
                "title": u"Annexe V - Modification de la destination ou modification de la répartition des surfaces de vente",
            },
            {
                "id": "6",
                "title": u"Annexe VI - Modification sensible du relief du sol - dépôt de véhicules, de mitrailles, de matériaux ou de déchets - installations mobiles - travaux d'aménagement au sol aux abords d'une construction autorisée",
            },
            {
                "id": "7",
                "title": u"Annexe VII - Boisement - déboisement - abattage - culture de sapins de Noël - modification de l'aspect d'un ou plusieurs arbres ou haies remarquables - défrichement - modification de la végétation",
            },
            {"id": "8", "title": u"Annexe VIII - Travaux techniques"},
            {
                "id": "9",
                "title": u"Annexe IX - Permis d'urbanisme dispensé d'un architecte ou autre que les demandes visées aux annexes 5 à 8",
            },
        ],
        "classification_order_scope": [
            "UrbanVocabularyTerm",
            {
                "id": "ensemble_charpente",
                "title": u"Ensemble charpente",
                "extraValue": "Ensemble charpente",
            },
            {"id": "facade", "title": u"Façade", "extraValue": "Façade"},
            {"id": "immeuble", "title": u"Immeuble", "extraValue": "Immeuble"},
            {"id": "toiture", "title": u"Toiture", "extraValue": "Toiture"},
        ],
        "general_disposition": [
            "UrbanVocabularyTerm",
            {"id": "dispense", "title": u"Déclaration pour dispense de permis"},
            {"id": "d_4_14", "title": u"Permis D.IV.14 du collège communal"},
            {"id": "d_4_24", "title": u"Art D.IV.24 décision sur recours"},
            {"id": "d_4_25", "title": u"Permis D.IV.25"},
        ],
        "watercourses": [
            "UrbanVocabularyTerm",
            {
                "id": "watercourses_expl",
                "title": u"traversé par un cours d'eau de la commune",
            },
            {
                "id": "watercourses_expl2",
                "title": u"longé par un cours d'eau de la commune",
            },
        ],
        "trails": [
            "UrbanVocabularyTerm",
            {
                "id": "trail_expl",
                "title": u"traversé par un sentier ou chemin communal",
            },
            {"id": "trail_expl2", "title": u"longé par un sentier ou chemin communal"},
        ],
        "zoning": [
            "UrbanVocabularyTerm",
            {"id": "zoning1", "title": "Zoning 1"},
            {"id": "zoning2", "title": "Zoning 2"},
            {"id": "zoning3", "title": "Zoning 3"},
        ],
        "investigations_radius": [
            "UrbanVocabularyTerm",
            {"id": "50m", "title": u"50 m"},
            {"id": "100m", "title": u"100 m"},
            {"id": "150m", "title": u"150 m"},
            {"id": "200m", "title": u"200 m"},
        ],
    },
    "Inspection": {
        "inspectioncontexts": [
            "UrbanVocabularyTerm",
            {"id": "suite", "title": u"Suite permis"},
            {"id": "plainte", "title": u"Plainte"},
            {"id": "observation", "title": u"Observation"},
            {"id": "interne", "title": u"Demande interne"},
            {"id": "externe", "title": u"Demande externe"},
        ],
    },
}
