# -*- coding: utf-8 -*-
urbanEventTypes = {
                    'buildlicence':
                    (
                    {
                    'id': "fiche-technique-voirie",
                    'title': "Fiche technique voirie",
                    'activatedFields': ['decision', ],
                    'deadLineDelay': 0,
                    'TALCondition' : "",
                    'podTemplates': (
                                     {'id': "urb-avis-technique-voirie", 'title': "Avis technique"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITechnicalServiceOpinionRequestEvent',
                    },
                    {
                    'id': "fiche-technique-energie",
                    'title': "Fiche technique conseiller en énergie",
                    'activatedFields': ['decision', ],
                    'deadLineDelay': 0,
                    'TALCondition' : "",
                    'podTemplates': (
                                     {'id': "urb-avis-technique-energie", 'title': "Avis technique"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITechnicalServiceOpinionRequestEvent',
                    },
                    {
                    'id': "fiche-technique-urbanisme",
                    'title': "Fiche technique urbanisme",
                    'activatedFields': ['decision', ],
                    'deadLineDelay': 0,
                    'TALCondition' : "",
                    'podTemplates': (
                                     {'id': "urb-avis-technique-urbanisme", 'title': "Avis technique"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITechnicalServiceOpinionRequestEvent',
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet (avec documents 'Dossier à compléter' services techniques)",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'TALCondition' : "",
                    'podTemplates': (
                                     {'id': "urb-dossier-incomplet-demandeur", 'title': "Dossier incomplet (lettre demandeur)"},
                                     {'id': "urb-dossier-incomplet-technique-voirie", 'title': "Dossier incomplet (service voirie)"},
                                     {'id': "urb-dossier-incomplet-pieces-manquantes", 'title': "Dossier incomplet (relevé de pièces manquantes)"},
                                    ),
                    },
                   ),
                   }
