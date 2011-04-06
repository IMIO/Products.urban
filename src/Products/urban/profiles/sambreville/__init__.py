# -*- coding: utf-8 -*-
urbanEventTypes = (
                   {
                    'buildlicence':
                    (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse", 'title': "Récépissé de la demande"},),
                    },
                    {
                    'id': "avis-etude-incidence",
                    'title': "Dossier incomplet",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: here.getImpactStudy()",
                    'podTemplates': ({'id': "urb-avis-etude-incidence", 'title': "Avis sur l'étude d'incidence"},),
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-dossier-incomplet", 'title': "Dossier incomplet"},),
                    },
                    {
                    'id': "accuse-de-reception",
                    'title': "Accusé de réception",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-accuse", 'title': "Accusé de réception"},),
                    },
                    {
                    'id': "rapport-du-college",
                    'title': "Rapport du Collège",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision', 'decisionText'],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-rapp-college", 'title': "Rapport du Collège"},{'id': "urb-rapp-college-transmis-avec-pca", 'title': "Transmis de la décision avec PCA"},{'id': "urb-rapp-college-transmis-sans-pca", 'title': "Transmis de la décision sans PCA"},),
                    },
                    {
                    'id': "transmis-1er-dossier-rw",
                    'title': "Transmis 1er dossier RW",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-permisurb-transavis", 'title': "Transmis de l'avis du collège à la RW"},),
                    },
                    {
                    'id': "demande-davis",
                    'title': "Demande d'avis",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-avis-met", 'title': "Demande avis au MET"},),
                    },
                    {
                    'id': "enquete-publique",
                    'title': "Enquête publique",
                    'activatedFields': ['eventDate', 'claimsDate', 'explanationsDate', ],
                    'deadLineDelay': 15,
                    'specialFunctionName': "Rechercher les propriétaires situés dans un rayon de 50m",
                    'specialFunctionUrl': "addInvestigationPO",
                    'podTemplates': ({'id': "urb-enq-certif-aff", 'title': "Certificat d'affichage"},{'id': "urb-enq-pv-ouv", 'title': "PV ouverture enquête"},{'id': "urb-enq-pv-clot", 'title': "PV de clôture enquête"},{'id': "urb-enq-frais", 'title': "Frais d'enquête"},),
                    },
                    {
                    'id': "delivrance-du-permis-octroi-ou-refus",
                    'title': "Délivrance du permis (octroi ou refus)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-decision-octroi-dem", 'title': "Octroi du permis (lettre au demandeur)"},{'id': "urb-decision-octroi-urb", 'title': "Octroi du permis (lettre à l'Urbanisme)"},{'id': "urb-decision-formulaire-a", 'title': "Formulaire A"},),
                    },
                    {
                    'id': "debut-des-travaux",
                    'title': "Début des travaux",
                    'deadLineDelay': 15,
                    'activatedFields': ['eventDate', ],
                    'podTemplates': (),
                    },
                    {
                    'id': "fin-des-travaux",
                    'title': "Fin des travaux",
                    'deadLineDelay': 15,
                    'activatedFields': ['eventDate', ],
                    'podTemplates': (),
                    },
                   ),
                   'declaration':
                   (),
                   'urbancertificateone':
                   (
                    {
                    'id': "recepisse-cu1",
                    'title': "Récépissé",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                    ),
                    },
                    {
                    'id': "octroi-cu1",
                    'title': "Octroi du certificat",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "cu1-lettre-notaire", 'title': "Lettre au notaire (octroi)"},
                                     {'id': "cu1-certif", 'title': "Certificat d'urbanisme 1"},
                                    ),
                    },
                   ),
                   'environmentaldeclaration':
                   (
                    {
                    'id': "premier-envoi",
                    'title': "Premier envoi",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "declaenv-courrier-ft", 'title': "1er envoi (Fonctionnaire technique)"},),
                    },
                   ),
                   }
                )
