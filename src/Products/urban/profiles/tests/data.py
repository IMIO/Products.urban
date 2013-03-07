# -*- coding: utf-8 -*-
from Products.urban.config import GLOBAL_TEMPLATES

globalTemplates = GLOBAL_TEMPLATES

default_texts = {
    'claimsTextDefaultValue':
    """
    <p>Je réclame le port obligatoire de la mini jupe à l'unif</p>
    """
}

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
                    'id': "recepisse-art15-complement",
                    'title': "Récépissé d'un complément à une demande de permis (article 115)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': (),
                    'eventTypeType': 'Products.urban.interfaces.IMissingPartDepositEvent',
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
                                     {'id': "urb-accuse", 'title': "Accusé de réception"},
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
                    'textDefaultValues': [{'text': default_texts['claimsTextDefaultValue'], 'fieldname': 'claimsText'}],
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
                                     {'id': "urb-rapp-service", 'title': "Rapport du Service"},
                                     {'id': "urb-rapp-college", 'title': "Rapport du Collège"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ICollegeReportEvent',
                    },
                    {
                    'id': "transmis-2eme-dossier-rw",
                    'title': "Transmis 2eme dossier RW",
                    'eventDateLabel': "Date de transmis",
                    'activatedFields': ['decisionDate', 'decision', 'receiptDate'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IWalloonRegionOpinionRequestEvent',
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
                    {
                    'id': "debut-des-travaux",
                    'title': "Début des travaux",
                    'deadLineDelay': 15,
                    'activatedFields': [],
                    'podTemplates': (),
                    'eventTypeType': 'Products.urban.interfaces.IWorkBeginningEvent',
                    },
                    {
                    'id': "prorogation",
                    'title': "Prorogation du permis",
                    'deadLineDelay': 15,
                    'activatedFields': ['decisionDate', 'decision', 'receiptDate', ],
                    'podTemplates': (
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IProrogationEvent',
                    },
                   ),
                  }
