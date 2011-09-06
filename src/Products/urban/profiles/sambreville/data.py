# -*- coding: utf-8 -*-
urbanEventTypes = {
                   'declaration':
                   (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': [],
                    'eventDateLabel': "Date du dépôt de la demande",
                    'deadLineDelay': 15,
                    'podTemplates': (),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': "deliberation-college",
                    'title': "Délibération collège",
                    'activatedFields': ['decision', ],
                    'eventDateLabel': "Date de la séance collège",
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "decl-delib-college", 'title': "Délibération collège"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ICollegeReportEvent',
                    },
                    {
                    'id': "transmis-decision",
                    'title': "Transmis décision au FD et demandeur",
                    'activatedFields': [],
                    'eventDateLabel': "Date du transmis",
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "decl-transmis-decision-fd", 'title': "Transmis décision au FD"},
                                     {'id': "decl-transmis-decision-demandeur", 'title': "Transmis décision au demandeur"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITheLicenceEvent',
                    },
                   ),
                   'urbancertificateone':
                   (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': [],
                    'eventDateLabel': "Date du dépôt de la demande",
                    'deadLineDelay': 15,
                    'podTemplates': (),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': "octroi-cu1",
                    'title': "Octroi du certificat",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "cu1-lettre-notaire", 'title': "Lettre au notaire (octroi)"},
                                     {'id': "cu1-certif", 'title': "Certificat d'urbanisme 1"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITheLicenceEvent',
                    },
                   ),
                   }
