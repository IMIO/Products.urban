urbanEventTypes = (
                   {
                    'buildlicence':
                    (
                    {
                    'id': "avis-etude-incidence",
                    'title': "Avis sur l'étude d'incidence",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "avis-etude-incidence", 'title': "Avis sur l'étude d'incidence"},),
                    },
                    {
                    'id': "delivrance-du-permis-octroi-ou-refus",
                    'title': "Délivrance du permis (octroi ou refus)",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "octroi-type", 'title': "Octroi type"},{'id': "envoi-pu-demandeur", 'title': "Envoi permis d'urbanisme au demandeur"},{'id': "envoi-pu-rw", 'title': "Envoi permis d'urbanisme à la RW"},{'id': "ventilation-des-frais", 'title': "Ventilation des frais"},{'id': "demande-racc-egout-avec-travaux", 'title': "Demande de raccordement aux égouts avec travaux"},{'id': "stats-mod-iii", 'title': "Statistiques modèle III"},{'id': "debut-des-travaux", 'title': "Début des travaux"},),
                    },
                    {
                    'id': "demande-avis",
                    'title': "Demande d'avis",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "demande-avis-belgacom", 'title': "Demande avis Belgacom"},{'id': "demande-avis-dga", 'title': "Demande avis D.G.A."},{'id': "demande-avis-inasep", 'title': "Demande avis INASEP"},{'id': "demande-avis-met", 'title': "Demande avis MET"},{'id': "demande-avis-police", 'title': "Demande avis Police"},{'id': "demande-avis-pompiers", 'title': "Demande avis Pompiers"},{'id': "demande-avis-swde", 'title': "Demande avis SWDE"},),
                    },
                    {
                    'id': "demande-raccordement-egout",
                    'title': "Demande de raccordement à l'égout",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "autorisation-racc-avec-traversee-voirie", 'title': "Autorisation de raccordement AVEC traversée de voirie"},{'id': "autorisation-racc-sans-traversee-voirie", 'title': "Autorisation de raccordement SANS traversée de voirie"},{'id': "autorisation-racc-dans-lotissement", 'title': "Autorisation de raccordement dans lotissement"},{'id': "devis-racc-avec-traversee-voirie", 'title': "Devis de raccordement AVEC traversée de voirie"},{'id': "devis-racc-sans-traversee-voirie", 'title': "Devis de raccordement SANS traversée de voirie"},{'id': "devis-type-racc", 'title': "Devis type de raccordement"},),
                    },
                    {
                    'id': "depot-de-la-demande",
                    'title': "Dépôt de la demande",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "recepisse-depot", 'title': "Récépissé de dépôt"},),
                    },
                    {
                    'id': "dossier-incomplet",
                    'title': "Dossier incomplet",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "notification-dossier-incomplet-demandeur", 'title': "Notification dossier incomplet au demandeur"},{'id': "notification-dossier-incomplet-architecte", 'title': "Notification dossier incomplet à l'architecte"},),
                    },
                    {
                    'id': "enquete-publique",
                    'title': "Enquête publique",
                    'activatedFields': ['eventDate', 'claimsDate', 'explanationsDate', ],
                    'deadLineDelay': 15,
                    'specialFunctionName': "Rechercher les propriétaires situés dans un rayon de 50m",
                    'specialFunctionUrl': "addInvestigationPO",
                    'podTemplates': ({'id': "annexe25-avis", 'title': "Annexe 25 - Avis"},{'id': "annexe-25-envoi-axono-et-annexe-demandeur", 'title': "Annexe 25 - Envoi axono et Annexe 25 au demandeur"},{'id': "annexe26-avis", 'title': "Annexe 26 - Avis"},{'id': "annexe26-lettre", 'title': "Annexe 26 - Lettre"},{'id': "art127-envoi-copie-annexe-26-rw", 'title': "Article 127 envoi copie annexe 26 RW"},),
                    },
                    {
                    'id': "enveloppes",
                    'title': "Enveloppes",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "enveloppe-architecte", 'title': "Enveloppe architecte"},{'id': "enveloppe-demandeur", 'title': "Enveloppe demandeur"},),
                    'podTemplates': (),
                    },
                    {
                    'id': "envoi-premier-dossier-rw",
                    'title': "Envoi 1er dossier à la RW",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "envoi-premier-dossier-rw", 'title': "Envoi 1er dossier à la RW"},),
                    },
                    {
                    'id': "envoi-deuxieme-dossier-rw",
                    'title': "Envoi 1er dossier à la RW",
                    'activatedFields': ['eventDate', ],
                    'deadLineDelay': 15,
                    'podTemplates': ({'id': "envoi-deuxieme-dossier-rw", 'title': "Envoi 2ème dossier à la RW"},),
                    },
                    {
                    'id': "fiche-recap",
                    'title': "Fiche récapitulative",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "fiche-pu", 'title': "Fiche récapitulative Permis d'Urbanisme"},),
                    },
                    {
                    'id': "info-demandeur-avis-fd",
                    'title': "Information au demandeur sur avis FD",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "info-demandeur-avis-fd", 'title': "Information au demandeur sur avis FD"},),
                    },
                    {
                    'id': "premier-passage-college",
                    'title': "Premier passage collège",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "rapport-service-pu", 'title': "Rapport du service"},{'id': "rapport-college-pu", 'title': "Rapport du Collège"},),
                    },
                    {
                    'id': "reception-de-la-demande",
                    'title': "Réception de la demande",
                    'activatedFields': ['eventDate', ],
                    'podTemplates': ({'id': "accuse-de-reception", 'title': "Accusé de réception de la demande"},),
                    },
                   ),
                   'declaration':
                   ()
                   }
                )
