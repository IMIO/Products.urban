# -*- coding: utf-8 -*-
from Products.urban.config import GLOBAL_TEMPLATES

globalTemplates = GLOBAL_TEMPLATES

urbanEventTypes = {
                   'buildlicence':
                   (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande (récépissé - article 115)",
                    'eventDateLabel': "Date de dépôt",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'isKeyEvent': True,
                    'keyDates': ('eventDate',),
                    'podTemplates': (),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet (avec listing des pièces manquantes - article 116 § 1)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'eventTypeType': 'Products.urban.interfaces.IMissingPartEvent',
                    'isKeyEvent': True,
                    'keyDates': ('eventDate',),
                    'podTemplates': (
                                    ),
                    },
                    {
                    'id': "accuse-de-reception",
                    'title': "Accusé de réception (dossier complet - article 116 § 1)",
                    'activatedFields': ['transmitDate'],
                    'deadLineDelay': 15,
                    'eventTypeType': 'Products.urban.interfaces.IAcknowledgmentEvent',
                    'isKeyEvent': True,
                    'keyDates': ('eventDate',),
                    'podTemplates': (
                                    ),
                    },
                    {
                    'id': "avis-etude-incidence",
                    'title': "Avis sur l'étude d'incidence",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'TALCondition': "python: here.getImpactStudy()",
                    'podTemplates': (
                                    ),
                    },
                    {
                    'id': "enquete-publique",
                    'title': "Enquête publique",
                    'activatedFields': ['claimsDate', 'explanationsDate', 'claimsText'],
                    'deadLineDelay': 15,
                    'TALCondition': "here/mayAddInquiryEvent",
                    'specialFunctionName': "Rechercher les propriétaires situés dans un rayon de 50m",
                    'specialFunctionUrl': "addInvestigationPO",
                    'podTemplates': (
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IInquiryEvent',
                    },
                    {
                    'id': "config-opinion-request",
                    'title': "*** Demande d'avis CONFIG ***",
                    'activatedFields': [],
                    'TALCondition': "python: False",
                    'podTemplates': ({'id': "urb-avis", 'title': "Courrier de demande d'avis"},),
                    'eventTypeType': 'Products.urban.interfaces.IOpinionRequestEvent',
                    },
                    {
                    'id': "rapport-du-college",
                    'title': "Rapport du Collège",
                    'activatedFields': ['decisionDate', 'decision', 'decisionText'],
                    'deadLineDelay': 15,
                    'isKeyEvent': True,
                    'keyDates': ('eventDate',),
                    'podTemplates': (
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ICollegeReportEvent',
                    },
                    {
                    'id': "delivrance-du-permis-octroi-ou-refus",
                    'title': "Délivrance du permis (octroi ou refus)",
                    'activatedFields': ['decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'eventDateLabel': "Date de notification",
                    'isKeyEvent': True,
                    'keyDates': ('eventDate',),
                    'podTemplates': (
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITheLicenceEvent',
                    },
                   ),
                  }
