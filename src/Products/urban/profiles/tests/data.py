# -*- coding: utf-8 -*-
urbanEventTypes = {
                    'buildlicence':
                    (
                    {
                    'id': "procedure-erronee-art127",
                    'title': "Procédure erronée (article 127)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: here.getFolderCategory() == 'art127'",
                    'podTemplates': (
                                     {'id': "urb-procedure-erronee-art127", 'title': "Procédure erronée (article 127 - courrier au demandeur)"},
                                     {'id': "urb-procedure-erronee-art127-rw", 'title': "Procédure erronée (article 127 - courrier à la RW)"},
                                    ),
                    },
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande (récépissé - article 115)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse", 'title': "Récépissé de la demande (article 115)"},),
                    },
                    {
                    'id': "recepisse-art15-complement",
                    'title': "Récépissé d'un complément à une demande de permis (article 115)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse-art115-complement", 'title': "Récépissé d'un complément à une demande de permis (article 115)"},),
                    },
                    {
                    'id': "recepisse-article-116",
                    'title': "Récépissé d'un modificatif à une demande de permis (article 116 - 6)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse-art116", 'title': "Récépissé d'un modificatif à une demande de permis (article 116 - 6)"},),
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet (avec listing des pièces manquantes - article 116 § 1)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-dossier-incomplet-demandeur", 'title': "Dossier incomplet (lettre demandeur)"},
                                     {'id': "urb-dossier-incomplet-archi", 'title': "Dossier incomplet (lettre architecte)"},
                                    ),
                    },
                    {
                    'id': "accuse-de-reception",
                    'title': "Accusé de réception (dossier complet - article 116 § 1)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-accuse", 'title': "Accusé de réception"},),
                    },
                    {
                    'id': "avis-etude-incidence",
                    'title': "Avis sur l'étude d'incidence",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: here.getImpactStudy()",
                    'podTemplates': (
                                     {'id': "urb-avis-etude-incidence", 'title': "Avis sur l'étude d'incidence"},
                                    ),
                    },
                    {
                    'id': "demande-avis-ccatm",
                    'title': "Demande d'avis (CCATM)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'ccatm' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-ccatm", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "demande-avis-belgacom",
                    'title': "Demande d'avis (Belgacom)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'belgacom' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-belgacom", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "demande-avis-dgrne",
                    'title': "Demande d'avis (DGRNE)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'dgrne' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-dgrne", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "demande-avis-dnf",
                    'title': "Demande d'avis (DNF)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'dnf' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-dnf", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "demande-avis-spw-dgo1",
                    'title': "Demande d'avis (SPW-DGO1)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'spw-dgo1' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-spw-dgo1", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "demande-avis-swde",
                    'title': "Demande d'avis (SWDE)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'TALCondition' : "python: 'swde' in here.getSolicitOpinionsTo()",
                    'podTemplates': ({'id': "urb-avis-swde", 'title': "Courrier de demande d'avis"},),
                    },
                    {
                    'id': "transmis-1er-dossier-rw",
                    'title': "Transmis 1er dossier RW",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-envoi-premier-dossier-rw", 'title': "Lettre d'envoi du premier dossier à la RW"},
                                     {'id': "urb-envoi-premier-dossier-art127-rw", 'title': "Lettre d'envoi du dossier (article 127) à la RW"},
                                    ),
                    },
                    {
                    'id': "enquete-publique",
                    'title': "Enquête publique",
                    'activatedFields': ['eventDate', 'claimsDate', 'explanationsDate', 'claimsText'],
                    'deadLineDelay': 15,
                    'specialFunctionName': "Rechercher les propriétaires situés dans un rayon de 50m",
                    'specialFunctionUrl': "addInvestigationPO",
                    'podTemplates': (
                                     {'id': "urb-enq-avis-riverains-annexe26", 'title': "Avis enquête (annexe 26 - lettre riverains)"},
                                     {'id': "urb-enq-certif-aff-annexe26", 'title': "Certificat d'affichage (annexe 26)"},
                                     {'id': "urb-enq-copie-rw-annexe26", 'title': "Avis enquête (annexe 26 - copie RW)"},
                                     {'id': "urb-enq-annexe25-dem", 'title': "Affiche (annexe 25 - lettre au demandeur)"},
                                     {'id': "urb-enq-annexe25", 'title': "Affiche (annexe 25)"},
                                     {'id': "urb-enq-pv-clot", 'title': "PV de clôture enquête"},
                                     {'id': "urb-enq-frais", 'title': "Frais d'enquête"},
                                     {'id': "urb-enq-recommandes", 'title': "Recommandés aux riverains (étiquette Poste)"},
                                    ),
                    },
                    {
                    'id': "rapport-du-college",
                    'title': "Rapport du Collège",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision', 'decisionText'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-rapp-service", 'title': "Rapport du Service"},
                                     {'id': "urb-rapp-college", 'title': "Rapport du Collège"},
                                    ),
                    },
                    {
                    'id': "transmis-2eme-dossier-rw",
                    'title': "Transmis 2eme dossier RW",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-envoi-second-dossier-rw", 'title': "Lettre envoi deuxième dossier à la RW"},
                                     {'id': "urb-envoi-second-dossier-demandeur", 'title': "Information au demandeur envoi second dossier"},
                                    ),
                    },
                    {
                    'id': "passage-conseil-communal",
                    'title': "Passage au Conseil Communal",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     #{'id': "urb-conseil-communal", 'title': "Délibération passée au Conseil Communal"},
                                    ),
                    },
                    {
                    'id': "delivrance-du-permis-octroi-ou-refus",
                    'title': "Délivrance du permis (octroi ou refus)",
                    'activatedFields': ['eventDate', 'decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-decision-octroi-dem", 'title': "Octroi du permis (lettre au demandeur)"},
                                     {'id': "urb-decision-octroi-rw", 'title': "Octroi du permis (lettre à l'Urbanisme)"},
                                     {'id': "urb-decision-stats-mod3", 'title': "Statistiques modèle 3"},
                                     {'id': "urb-decision-formulaire-a", 'title': "Annexe 30 - Formulaire A"},
                                     {'id': "urb-decision-egout-travaux", 'title': "Demande de raccordement aux égouts avec travaux (formulaire à remplir par le demandeur)"},
                                     {'id': "urb-decision-frais", 'title': "Ventilation des frais"},
                                     {'id': "urb-debut-travaux", 'title': "Début des travaux (formulaire à remplir par le demandeur)"},
                                    ),
                    },
                    {
                    'id': "demande-raccordement-egout",
                    'title': "Demande de raccordement à l'égout",
                    'deadLineDelay': 15,
                    'activatedFields': ['eventDate', 'decisionDate', ],
                    'podTemplates': (
                                     {'id': "urb-racc-egout-devis-egouttage", 'title': "Devis raccordement égouttage"},
                                     {'id': "urb-racc-egout-delib-college-avec-traversee-voirie", 'title': "Délibération du Collège Communal AVEC traversée de voirie"},
                                     {'id': "urb-racc-egout-delib-college-sans-traversee-voirie", 'title': "Délibération du Collège Communal SANS traversée de voirie"},
                                     {'id': "urb-racc-egout-delib-college-lotissement", 'title': "Délibération du Collège raccordement égout dans un lotissement"},
                                    ),
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
                    {
                    'id': "prorogation",
                    'title': "Prorogation du permis",
                    'deadLineDelay': 15,
                    'activatedFields': ['eventDate', 'decisionDate', 'decision', ],
                    'podTemplates': (
                                     {'id': "urb-prorogation", 'title': "Délibération du Collège Communal concernant la prorogation du permis"},
                                    ),
                    },
                    {
                    'id': "suspension-du-permis",
                    'title': "Suspension du permis",
                    'deadLineDelay': 15,
                    'activatedFields': ['eventDate', ],
                    'podTemplates': (
                                     {'id': "urb-suspension-retrait-refus-dem", 'title': "Retrait et refus du permis d'urbanisme (lettre au demandeur)"},
                                     {'id': "urb-suspension-retrait-refus-rw", 'title': "Retrait et refus du permis d'urbanisme (lettre à la RW)"},
                                     {'id': "urb-suspension-retrait-refus-rw-recours", 'title': "Retrait et refus du permis d'urbanisme (lettre à la RW - direction des recours)"},
                                    ),
                    },
                    {
                    'id': "enveloppes",
                    'title': "Enveloppes",
                    'deadLineDelay': 0,
                    'activatedFields': ['eventDate', ],
                    'podTemplates': (
                                     {'id': "urb-enveloppes-dem", 'title': "Enveloppes demandeurs"},
                                     {'id': "urb-enveloppes-archi", 'title': "Enveloppes architectes"},
                                    ),
                    },
                    {
                    'id': "fiche-recap",
                    'title': "Fiche récapitulative",
                    'deadLineDelay': 0,
                    'activatedFields': ['eventDate', ],
                    'podTemplates': (
                                     {'id': "urb-fiche-recap", 'title': "Fiche récapitulative"},
                                    ),
                    },
                   ),
                   'declaration':
                   (),
                   'urbancertificateone':
                   (
                    {
                    'id': "depot-de-la-demande",
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
