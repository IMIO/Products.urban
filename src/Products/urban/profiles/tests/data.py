# -*- coding: utf-8 -*-
from Products.urban.config import GLOBAL_TEMPLATES

globalTemplates = GLOBAL_TEMPLATES

urbanEventTypes = {
                   'buildlicence':
                   (
                    {
                    'id': "procedure-erronee-art127",
                    'title': "Procédure erronée (article 127)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'TALCondition': "python: here.getFolderCategory() == 'art127'",
                    'podTemplates': (
                                     {'id': "urb-procedure-erronee-art127", 'title': "Procédure erronée (article 127 - courrier au demandeur)"},
                                     {'id': "urb-procedure-erronee-art127-rw", 'title': "Procédure erronée (article 127 - courrier à la RW)"},
                                    ),
                    },
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande (récépissé - article 115)",
                    'eventDateLabel': "Date de dépôt",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse", 'title': "Récépissé de la demande (article 115)"},),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': "avis-etude-incidence",
                    'title': "Avis sur l'étude d'incidence",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'TALCondition': "python: here.getImpactStudy()",
                    'podTemplates': (
                                     {'id': "urb-avis-etude-incidence", 'title': "Avis sur l'étude d'incidence"},
                                    ),
                    },
                    {
                    'id': "recepisse-art15-complement",
                    'title': "Récépissé d'un complément à une demande de permis (article 115)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse-art115-complement", 'title': "Récépissé d'un complément à une demande de permis (article 115)"},),
                    'eventTypeType': 'Products.urban.interfaces.IMissingPartDepositEvent',
                    },
                    {
                    'id': "recepisse-article-116",
                    'title': "Récépissé d'un modificatif à une demande de permis (article 116 - 6)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "urb-recepisse-art116", 'title': "Récépissé d'un modificatif à une demande de permis (article 116 - 6)"},),
                    'eventTypeType': 'Products.urban.interfaces.IModificationDepositEvent',
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet (avec listing des pièces manquantes - article 116 § 1)",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'eventTypeType': 'Products.urban.interfaces.IMissingPartEvent',
                    'podTemplates': (
                                     {'id': "urb-dossier-incomplet-demandeur", 'title': "Dossier incomplet (lettre demandeur)"},
                                     {'id': "urb-dossier-incomplet-archi", 'title': "Dossier incomplet (lettre architecte)"},
                                    ),
                    },
                    {
                    'id': "accuse-de-reception",
                    'title': "Accusé de réception (dossier complet - article 116 § 1)",
                    'activatedFields': ['transmitDate'],
                    'deadLineDelay': 15,
                    'eventTypeType': 'Products.urban.interfaces.IAcknowledgmentEvent',
                    'podTemplates': (
                                     {'id': "urb-accuse", 'title': "Accusé de réception"},
                                     {'id': "urb-accuse-demande-paiement", 'title': "Demande de paiement"},
                                    ),
                    },
                    {
                    'id': "dossier-irrecevable",
                    'title': "Dossier irrecevable",
                    'activatedFields':['decisionDate'],
                    'podTemplates': (
                                     {'id':"urb-regularisation-delib-college-refus", 'title':"Délibération refus de régularisation PU"},
                                    )
                    },
                    {
                    'id': "demande-complements-art116-6",
                    'title': "Demande de compléments (article 116§6)",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'TALCondition': "python: here.getLastAcknowledgment()",
                    'podTemplates': (
                                     {'id': "urb-demande-complements-art116-6", 'title': "Lettre au demandeur"},
                                    ),
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
                    'id': "transmis-1er-dossier-rw",
                    'title': "Transmis 1er dossier RW",
                    'eventDateLabel': "Date de transmis",
                    'activatedFields': ['decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-envoi-premier-dossier-rw", 'title': "Lettre d'envoi du premier dossier à la RW"},
                                     {'id': "urb-envoi-premier-dossier-art127-rw", 'title': "Lettre d'envoi du dossier (article 127) à la RW"},
                                     {'id': "urb-envoi-premier-dossier-form-rw", 'title': "Formulaire d'envoi d'un dossier à la RW"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IWalloonRegionPrimoEvent',
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
                                     {'id': "urb-enq-avis-riverains-annexe26", 'title': "Avis enquête (annexe 26 - lettre riverains)"},
                                     {'id': "urb-enq-certif-aff-annexe26", 'title': "Certificat d'affichage (annexe 26)"},
                                     {'id': "urb-enq-copie-rw-annexe26", 'title': "Avis enquête (annexe 26 - copie RW)"},
                                     {'id': "urb-enq-annexe25-dem", 'title': "Affiche (annexe 25 - lettre au demandeur)"},
                                     {'id': "urb-enq-annexe25", 'title': "Affiche (annexe 25)"},
                                     {'id': "urb-enq-ordre-mission", 'title': "Ordre de mission"},
                                     {'id': "urb-enq-accuse-reclamation", 'title': "Accusé de réception d'une réclamation"},
                                     {'id': "urb-enq-reunion-clot", 'title': "Réunion de clôture d'enquête"},
                                     {'id': "urb-enq-pv-clot", 'title': "PV de clôture enquête"},
                                     {'id': "urb-enq-frais", 'title': "Frais d'enquête"},
                                     {'id': "urb-enq-recommandes", 'title': "Recommandés aux riverains (étiquette Poste)"},
                                     {'id': "urb-enq-art341-invit", 'title': "Invitation séance de réclamation (article 341)"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IInquiryEvent',
                    },
                    {
                    'id': "rapport-du-college",
                    'title': "Rapport du Collège",
                    'activatedFields': ['decisionDate', 'decision', 'decisionText'],
                    'deadLineDelay': 15,
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
                    'activatedFields': ['decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-envoi-second-dossier-rw", 'title': "Lettre envoi deuxième dossier à la RW"},
                                     {'id': "urb-envoi-second-dossier-demandeur", 'title': "Information au demandeur envoi second dossier"},
                                     {'id': "urb-envoi-premier-dossier-form-rw", 'title': "Formulaire d'envoi d'un dossier à la RW"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IWalloonRegionOpinionRequestEvent',
                    },
                    {
                    'id': "passage-conseil-communal",
                    'title': "Passage au Conseil Communal",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-conseil-delib-college", 'title': "Délibération passée au collège"},
                                     {'id': "urb-conseil-delib-communale-creation", 'title': "Délibération du conseil communal (ouverture de voirie)"},
                                     {'id': "urb-conseil-delib-communale-modif", 'title': "Délibération du conseil communal (modification de voirie)"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ICommunalCouncilEvent',
                    },
                    {
                    'id': "delivrance-du-permis-octroi-ou-refus",
                    'title': "Délivrance du permis (octroi ou refus)",
                    'eventDateLabel': "Date de notification",
                    'activatedFields': ['decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "urb-decision-octroi-dem", 'title': "Octroi du permis (lettre au demandeur)"},
                                     {'id': "urb-decision-octroi-rw", 'title': "Octroi du permis (lettre à l'Urbanisme)"},
                                     {'id': "urb-decision-transmis-reclamants", 'title': "Décision du permis (transmis aux réclamants)"},
                                     {'id': "urb-decision-stats-mod3", 'title': "Statistiques modèle 3"},
                                     {'id': "urb-decision-formulaire-a", 'title': "Annexe 30 - Formulaire A"},
                                     {'id': "urb-decision-egout-travaux", 'title': "Demande de raccordement aux égouts avec travaux (formulaire à remplir par le demandeur)"},
                                     {'id': "urb-decision-frais", 'title': "Ventilation des frais"},
                                     {'id': "urb-debut-travaux", 'title': "Début des travaux (formulaire à remplir par le demandeur)"},
                                     {'id': "urb-decision-deliberation-college", 'title': "Delibération du collège d'octroi du permis"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITheLicenceEvent',
                    },
                    {
                    'id': "fiche-recap",
                    'title': "Fiche récapitulative",
                    'deadLineDelay': 0,
                    'activatedFields': [],
                    'podTemplates': (
                                     {'id': "urb-fiche-recap", 'title': "Fiche récapitulative"},
                                    ),
                    },
                    {
                    'id': "demande-raccordement-egout",
                    'title': "Demande de raccordement à l'égout",
                    'deadLineDelay': 15,
                    'activatedFields': ['decisionDate', ],
                    'podTemplates': (
                                     {'id': "urb-racc-egout-devis-egouttage", 'title': "Devis raccordement égouttage"},
                                     {'id': "urb-racc-egout-delib-college-avec-traversee-voirie", 'title': "Délibération du Collège Communal AVEC traversée de voirie"},
                                     {'id': "urb-racc-egout-delib-college-sans-traversee-voirie", 'title': "Délibération du Collège Communal SANS traversée de voirie"},
                                     {'id': "urb-racc-egout-delib-college-lotissement", 'title': "Délibération du Collège raccordement égout dans un lotissement"},
                                    ),
                    },
                    {
                    'id': "avis-technique-peb",
                    'title':"Avis technique PEB",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'podTemplates': ({'id': "avis-technique-peb", 'title': "Avis technique PEB"},)
                    },

                    {
                    'id': "peb-declaration-initiale",
                    'title': "PEB : déclaration initiale",
                    'activatedFields': ['receiptDate', ],
                    'deadLineDelay': 0,
                    'TALCondition' : "python: here.getPebType() == 'complete_process'",
                    'podTemplates': (),
                    },
                    {
                    'id': "indication-implantation",
                    'title': "Indication d'implantation",
                    'deadLineDelay': 0,
                    'activatedFields': ['receiptDate', ],
                    'TALCondition' : "python: here.getImplantation()",
                    'podTemplates': (),
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
                    'id': "fin-des-travaux",
                    'title': "Fin des travaux",
                    'deadLineDelay': 15,
                    'activatedFields': [],
                    'podTemplates': (),
                    },
                    {
                    'id': "peb-declaration-finale",
                    'title': "PEB : déclaration finale",
                    'activatedFields': ['receiptDate', ],
                    'deadLineDelay': 0,
                    'TALCondition' : "python: here.getPebType() == 'complete_process'",
                    'podTemplates': (
                                     {'id':"rapport-final-peb", 'title': "Rapport final PEB"},
                                    ),
                    },
                    {
                    'id': "prorogation",
                    'title': "Prorogation du permis",
                    'deadLineDelay': 15,
                    'activatedFields': ['decisionDate', 'decision', 'receiptDate', ],
                    'podTemplates': (
                                     {'id': "urb-prorogation", 'title': "Délibération du Collège Communal concernant la prorogation du permis"},
                                     {'id': "urb-prorogation-transmis-refus", 'title': "Refus de prorogation (lettre au demandeur)"},
                                     {'id': "urb-prorogation-transmis-accept", 'title': "Acceptation de prorogation (lettre au demandeur)"},
                                     {'id': "urb-prorogation-transmis-accept-fd", 'title': "Acceptation de prorogation (lettre au fonctionnaire délégué)"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IProrogationEvent',
                    },
                    {
                    'id': "suspension-du-permis",
                    'title': "Suspension du permis",
                    'deadLineDelay': 15,
                    'activatedFields': [],
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
                    'activatedFields': [],
                    'podTemplates': (
                                     {'id': "urb-enveloppes-dem", 'title': "Enveloppes demandeurs"},
                                     {'id': "urb-enveloppes-archi", 'title': "Enveloppes architectes"},
                                    ),
                    },
                    {
                    'id': "rappel-implantation",
                    'title':"Rappel implantation",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'podTemplates': ({'id': "urb-rappel-implantation", 'title': "Rappel implantation"},),
                    },
                    {
                    'id': "rappel-decl-init-peb",
                    'title':"Rappel déclaration initiale PEB",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'podTemplates': ({'id': "urb-rappel-decl-init-peb", 'title': "Rappel déclaration initiale PEB"},),
                    },
                    {
                    'id': "rappel-implantation-peb",
                    'title':"Rappel implantation et PEB",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'podTemplates': ({'id': "urb-rappel-implantation-peb", 'title': "Rappel implantation et PEB"},),
                    },
                    {
                    'id': "demande-irrecevable-art159",
                    'title':"Demande irrecevable (article 159 bis)",
                    'activatedFields': [],
                    'deadLineDelay': 0,
                    'podTemplates': ({'id': "urb-demande-irrecevable-art159", 'title': "Demande irrecevable (article 159 bis)"},),
                    },
                    {
                    'id': "recours-decision-au-conseil-etat",
                    'title':"Recours du demandeur contre la décision au conseil d'état",
                    'activatedFields': ['auditionDate', ],
                    'deadLineDelay': 0,
                    'podTemplates': (),
                    },
                    {
                    'id': "recours-decision-au-gouvernement",
                    'title':"Recours du demandeur contre la décision au gouvernement",
                    'activatedFields': ['decisionDate', 'decision', ],
                    'deadLineDelay': 0,
                    'podTemplates': (
                                     {'id': "urb-recours-GW-transmis-decision-FD-art127", 'title':"Transmis au réclamant de la décision du FD concernant recours au GW contre art 127"},),
                                     {'id': "urb-recours-GW-transmis-decision-FD-PU", 'title': 
                    }
                   ),
                   'declaration':
                   (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': [],
                    'eventDateLabel': "Date du dépôt de la demande",
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "decl-recepisse", 'title': "Récepissé de la déclaration"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': 'avis-technique',
                    'title': "Avis technique",
                    'activatedFields': ['transmitDate',],
                    'eventDateLabel': "Date de retour souhaitée",
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': 'decl-avis-technique', 'title': "Avis technique urbanisme"},
                                    ),
                    },
                    {
                    'id': 'deliberation-college',
                    'title': "Délibération collège",
                    'activatedFields': ['decision',],
                    'eventDateLabel': "Date de la séance collège",
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': 'decl-delib-college', 'title': "Délibération collège"},
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
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "cu1-recepisse", 'title': "Récépissé de la demande"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.IDepositEvent',
                    },
                    {
                    'id': "octroi-cu1",
                    'title': "Octroi du certificat",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "cu1-lettre-notaire", 'title': "Lettre au notaire (ou demandeur) (octroi)"},
                                     {'id': "cu1-certif", 'title': "Certificat d'urbanisme 1"},
                                    ),
                    'eventTypeType': 'Products.urban.interfaces.ITheLicenceEvent',
                    },
                   ),
                   'division':
                   (
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "div-recepisse", 'title': "Récépissé de la demande"},),
                    },
                    {
                    'id': "decision-octroi-refus",
                    'title': "Octroi/refus de la division",
                    'activatedFields': ['decisionDate', 'decision'],
                    'deadLineDelay': 15,
                    'podTemplates': (
                                     {'id': "div-decision-octroi", 'title': "Octroi de la division"},
                                     {'id': "div-transmis-decision", 'title': "Octroi de la division (transmis au notaire)"},
                                    ),
                    },
                   ),
                   'environmentaldeclaration':
                   (
                    {
                    'id': "premier-envoi",
                    'title': "Premier envoi",
                    'activatedFields': [],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "declaenv-courrier-ft", 'title': "1er envoi (Fonctionnaire technique)"},),
                    },
                   ),
                   }
