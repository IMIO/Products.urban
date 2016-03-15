# -*- coding: utf-8 -*-

from Products.urban.config import URBAN_TYPES

vocabularies_with_HTML_description = [
    'specificfeatures',
    'roadspecificfeatures',
    'locationspecificfeatures',
    'townshipspecificfeatures',
    'opinionstoaskifworks',
    'investigationarticles',
]

default_values = {
    'BuildLicence': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "uap", 'title': u"UAP (permis d'urbanisme avec avis préalable du FD)"},
            {'id': "udc", 'title': u"UDC (permis dans PCA, 'RCU, 'LOTISSEMENT, 'parfois avec demande de dérogation)"},
            {'id': "upp", 'title': u"UPP (petit permis délivré directement par le Collège)"},
            {'id': "pu", 'title': u"PU (demande de PERMIS UNIQUE)"},
            {'id': "inconnu", 'title': u"Inconnue"},
        ],

        'missingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable incid'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'pebcategories': [
            'UrbanVocabularyTerm',
            {'id': "not_applicable", 'title': 'peb_not_applicable'},
            {'id': "complete_process", 'title': 'peb_complete_process'},
            {'id': "form1_process", 'title': 'peb_form1_process'},
            {'id': "form2_process", 'title': 'peb_form2_process'},
        ],
    },
    'Article127': {
        'missingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable incid'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (annexe 20) en 2 exemplaires"},
            {'id': "plan_travaux", 'title': u"Plan des travaux en 4 exemplaires"},
            {'id': "attestation_archi", 'title': u"Attestation de l'architecte (annexe 21) en 2 exemplaires"},
            {'id': "attestation_ordre_archi", 'title': u"Attestation de l'architecte soumis au visa du conseil de l'ordre (annexe 22) en 2 exemplaires"},
            {'id': "photos", 'title': u"3 photos numérotées de la parcelle ou immeuble en 2 exemplaires"},
            {'id': "notice_environnement", 'title': u"Notice d'évaluation préalable inc'id'ences environnement (annexe 1C) en 2 exemplaires"},
            {'id': "plan_secteur", 'title': u"Une copie du plan de secteur"},
            {'id': "isolation", 'title': u"Notice relative aux exigences d'isolation thermique et de ventilation (formulaire K) en 2 exemplaires"},
            {'id': "peb", 'title': u"Formulaire d'engagement PEB (ou formulaire 1 ou formulaire 2) en 3 exemplaires"},
        ],

        'pebcategories': [
            'UrbanVocabularyTerm',
            {'id': "not_applicable", 'title': 'peb_not_applicable'},
            {'id': "complete_process", 'title': 'peb_complete_process'},
            {'id': "form1_process", 'title': 'peb_form1_process'},
            {'id': "form2_process", 'title': 'peb_form2_process'},
        ],
    },
    'ParcelOutLicence': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "lap", 'title': u"LAP (permis de lotir avec avis préalable du FD)"},
            {'id': "lapm", 'title': u"LAP/M (modification du permis de lotir avec avis du FD)"},
            {'id': "ldc", 'title': u"LDC (permis de lotir dans un PCA, 'lotissement ou en décentralisation)"},
            {'id': "ldcm", 'title': u"LDC/M (modification du permis de lotir dans un PCA, 'RCU, 'LOTISSEMENT)"},
        ],

        'lotusages': [
            'UrbanVocabularyTerm',
            {'id': "buildable", 'title': u"Lot bâtissable"},
            {'id': "greenzone", 'title': u"Espace vert"},
            {'id': "tosurrendertotown", 'title': u"Lot à rétrocéder à la commune"},
            {'id': "autre", 'title': u"Autre"},
        ],

        'equipmenttypes': [
            'UrbanVocabularyTerm',
            {'id': "telecom", 'title': u"Télécomunication"},
            {'id': "electricity", 'title': u"Electricité"},
            {'id': "gas", 'title': u"Gaz"},
            {'id': "teledistribution", 'title': u"Télédistribution"},
            {'id': "sewers", 'title': u"Egouttage"},
            {'id': "water", 'title': u"Eau"},
            {'id': "autre", 'title': u"Autre"},
        ],
    },
    'UrbanCertificateOne': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "cu1", 'title': u"CU1 (certificat d'urbanisme 1)"},
        ],

        'missingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],
    },
    'UrbanCertificateTwo': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "cu2", 'title': u"CU2 (certificat d'urbanisme 2)"},
        ],

        'missingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande (formulaire 1A) en 3 exemplaires"},
            {'id': "extrait_cadastral", 'title': u"Extrait cadastral en 3 exemplaires"},
        ],
    },

    'EnvClassOne': {
        'decisions': [
            'UrbanVocabularyTerm',
            {'id': "octroi", 'title': u"Octroi", 'extraValue': "Recevable"},
            {'id': "refus", 'title': u"Refus", 'extraValue': "Irrecevable"},
        ],
    },
    'EnvClassTwo': {
        'decisions': [
            'UrbanVocabularyTerm',
            {'id': "octroi", 'title': u"Octroi", 'extraValue': "Recevable"},
            {'id': "refus", 'title': u"Refus", 'extraValue': "Irrecevable"},
        ],
    },
    'EnvClassThree': {
        'missingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande en 4 exemplaires"},
            {'id': "plan", 'title': u"Plans"},
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande en 4 exemplaires"},
            {'id': "plan", 'title': u"Plans"},
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm',
            {'id': "form_demande", 'title': u"Formulaire de demande en 4 exemplaires"},
            {'id': "plan", 'title': u"Plans"},
        ],
    },
    'Division': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "dup", 'title': u"DIV (Division notariale)"},
        ],

    },
    'MiscDemand': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "apct", 'title': u"Avis préalable construction ou transformation"},
            {'id': "appu", 'title': u"Avis préalable permis d'urbanisation"},
            {'id': "apd", 'title': u"Avis préalable de division"},
            {'id': "dre", 'title': u"Demande de raccordement à l'égout"},
            {'id': "div", 'title': u"Divers"},
        ],

    },
    'Declaration': {
        'foldercategories': [
            'UrbanVocabularyTerm',
            {'id': "dup", 'title': u"DUP (Déclaration Urbanistique Préalable)"},
        ],

        'articles': [
            'UrbanVocabularyTerm',
            {'id': "263_1_1", 'title': u"article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins", 'extraValue': "263 §1er 1°",
            'description': "« article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins pour autant qu’ils relèvent des actes et travaux visés à l’article 262, 4°, b, d, e et g, mais n’en remplissent pas les conditions; »"},
            {'id': "263_1_2", 'title': u"article 263 §1er 2° la pose ou l'enlèvement d'un car-port <30m²", 'extraValue': "263 §1er 2°",
            'description': "« article 263 §1er 2° par propriété, la pose ou l’enlèvement d’un car port d’une superficie maximale de 30, 00 m² qui ne respecte pas les conditions visées à l’article 262, 5°, f; »"},
            {'id': "263_1_3", 'title': u"article 263 §1er 3° l'ouverture ou la modification de baies", 'extraValue': "263 §1er 3°",
            'description': "« article 263 §1er 3° l’ouverture ou la modification de baies autres que celles visées à l’article 262, 9° et 10°, de même aspect architectural que les baies existantes; »"},
            {'id': "263_1_4", 'title': u"article 263 §1er 4° le remplacement de parements d'élévation/couverture de toiture par plus isolants", 'extraValue': "263 §1er 4°",
            'description': "« article 263 §1er 4° le remplacement de parements d’élévation et de couvertures de toiture par des parements et couvertures isolants visés à l’article 262, 11°, qui n’en remplissent pas les conditions; »"},
            {'id': "263_1_5a", 'title': u"article 263 §1er 5° a}, la construction d'un volume secondaire en contiguïté <30m²", 'extraValue': "263 §1er 5° a)",
            'description': "« article 263 §1er 5° a}, par propriété, la construction ou le remplacement d’un volume secondaire par un volume secondaire, sans étage s’il est érigé en contiguïté avec un bâtiment existant, à l’arrière de ce bâtiment ou en recul d’au moins 4, 00 m de l’alignement ou raccordé à ce bâtiment par un volume à toiture plate; »"},
            {'id': "263_1_5b", 'title': u"article 263 §1er 5° b}, la construction d'un volume secondaire isolé <30m²", 'extraValue': "263 §1er 5° b)",
            'description': "« article 263 §1er 5° b}, par propriété, la construction ou le remplacement d’un volume secondaire par un volume secondaire, sans étage s’il est isolé et érigé à l’arrière d’un bâtiment existant; »"},
            {'id': "263_1_6a", 'title': u"article 263 §1er 6° a}, la construction d'un abri pour un ou des animaux", 'extraValue': "263 §1er 6° a)",
            'description': "« article 263 §1er 6° a}, dans les cours et jardins, les abris pour un ou des animaux; »"},
            {'id': "263_1_6b", 'title': u"article 263 §1er 6° b}, la pose d'un rucher", 'extraValue': "263 §1er 6° b)",
            'description': "« article 263 §1er 6° b}, dans les cours et jardins, un rucher, sans préjudice de l’application des dispositions visées au Code rural; »"},
            {'id': "263_1_6c", 'title': u"article 263 §1er 6° c}, Clôtures/portiques/portillons", 'extraValue': "263 §1er 6° c)",
            'description': "« article 263 §1er 6° c}, dans les cours et jardins, la pose de clôtures, de portiques ou de portillons autres que ceux visés à l’article 262, 5°, e; »"},
            {'id': "263_1_6d", 'title': u"article 263 §1er 6° d}, Etang/piscine non couverte < 75m²", 'extraValue': "263 §1er 6° d)",
            'description': "« article 263 §1er 6° d}, dans les cours et jardins, par propriété, pour autant qu’ils soient situés à l’arrière de l’habitation, la création d’un étang ou d’une piscine non couverte n’excédant pas 75, 00 m² pour autant que les déblais nécessaires à ces aménagements n’entraînent aucune modification sensible du relief naturel du sol sur le reste de la propriété; »"},
            {'id': "263_1_7", 'title': u"article 263 §1er 7° Démolition <30 m²", 'extraValue': "263 §1er 7°",
            'description': "« article 263 §1er 7° la démolition de constructions sans étage ni sous-sol;"},
            {'id': "263_1_8a", 'title': u"article 263 §1er 8° a}, les silos de stockage", 'extraValue': "263 §1er 8° a)",
            'description': "« article 263 §1er 8° a}, pour les exploitations agricoles, la construction de silos de stockage en tout ou en partie enterrés, pour autant que le niveau supérieur des murs de soutènement n’excède pas de 1, 50 m le niveau du relief naturel du sol; »"},
            {'id': "263_1_8b", 'title': u"article 263 §1er 8° b}, les dalles de fumière", 'extraValue': "263 §1er 8° b)",
            'description': "« article 263 §1er 8° b}, pour les exploitations agricoles, l’établissement d’une dalle de fumière; »"},
            {'id': "263_1_8c", 'title': u"article 263 §1er 8° c}, les citernes de récolte ou de stockage d'eau/effluents d'élevage", 'extraValue': "263 §1er 8° c)",
            'description': "« article 263 §1er 8° c}, pour les exploitations agricoles, la pose de citernes de récolte ou de stockage d’eau ou d’effluents d’élevage, en tout ou en partie enterrées, pour autant que le niveau supérieur du mur de soutènement n’excède pas 0, 50 m et que les citernes soient implantées à 10, 00 m minimum de tout cours d’eau navigable ou non navigable, à 3, 00 m minimum du domaine public et à 20, 00 m minimum de toute habitation autre que celle de l’exploitant; »"},
            {'id': "263_1_9", 'title': u"article 263 §1er 9° la culture de sapins de Noël", 'extraValue': "263 §1er 9°",
            'description': "« article 263 §1er 9° la culture de sapins de Noël pour une période ne dépassant pas douze ans; »"},
            {'id': "263_1_10", 'title': u"article 263 §1er 10° les miradors", 'extraValue': "263 §1er 10°",
            'description': "« article 263 §1er 10° dans la zone contiguë à la zone forestière, les miradors en bois visés à l’article 1er, § 1er, 9°, de la loi du 28 février 1882 sur la chasse; »"},
        ],
    },
    'shared_vocabularies': {

        'decisions': [
            'UrbanVocabularyTerm', [
                'BuildLicence', 'Article127', 'ParcelOutLicence', 'Declaration', 'Division', 'NotaryLetter',
                'UrbanCertificateOne', 'UrbanCertificateTwo', 'EnvClassThree', 'MiscDemand'
            ],
            {'id': "favorable", 'title': u"Favorable", 'extraValue': "Recevable"},
            {'id': "defavorable", 'title': u"Défavorable", 'extraValue': "Irrecevable"},
        ],

        'townshipfoldercategories': [
            'UrbanVocabularyTerm', URBAN_TYPES,
            {'id': "abattre", 'title': u"Abattre"},
            {'id': "abri-animaux", 'title': u"Abri pour animaux"},
            {'id': "abri-jardin", 'title': u"Abri de jardin"},
            {'id': "car-port", 'title': u"Car-port"},
            {'id': "changement-de-destination", 'title': u"Changement de destination"},
            {'id': "clotures-murs", 'title': u"Clôtures et murs"},
            {'id': "commerce", 'title': u"Commerce"},
            {'id': "demolition", 'title': u"Démolition"},
            {'id': "divers", 'title': u"Divers"},
            {'id': "enseigne", 'title': u"Enseigne"},
            {'id': "immeuble-appartements", 'title': u"Immeuble à appartements"},
            {'id': "modification-relief", 'title': u"Modification du relief du sol"},
            {'id': "module-electrite", 'title': u"Modules de production d'électricité ou de chaleur"},
            {'id': "nouvelle-habitation", 'title': u"Nouvelle habitation"},
            {'id': "nouveau-logement", 'title': u"Nouveau logement dans un bâtiment existant"},
            {'id': "parking", 'title': u"Parking"},
            {'id': "piscine", 'title': u"Piscine"},
            {'id': "recouvrement-toiture", 'title': u"Remplacement de parement de façade ou de recouvrement de toiture"},
            {'id': "transformation", 'title': u"Transformation d'une habitation existante"},
            {'id': "transformation-facade", 'title': u"Transformation d'une façade"},
            {'id': "veranda", 'title': u"Véranda"},
        ],

        'ftSolicitOpinionsTo': [
            'UrbanVocabularyTerm', ['EnvClassOne', 'EnvClassTwo'],
            {
                'id': 'spw-dgo1',
                'title': "SPW-DGO1",
                'description': '<p>Direction Générale opérationnelle<br />Département du réseau de Namur et du Luxembourg<br />District 131.12 - SPY<br />37, Route de Saussin<br />5190 Spy</p>',
            },
            {
                'id': 'dgrne',
                'title': "DGRNE",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'dnf',
                'title': "DNF",
                'description': '<p>39, Avenue Reine Astrid<br />5000 Namur</p>',
            },
            {
                'id': 'stp',
                'title': "Service Technique Provincial",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'pi',
                'title': "Prévention Incendie",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'svp',
                'title': "Service Voyer Principal",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'agriculture',
                'title': "Agriculture",
                'description': '<p>Direction Générale opérationnelle<br />Agriculture, Ressources naturelles et Environnement<br />Service extérieur de Wavre<br />4, Avenue Pasteur<br />1300 Wavre</p>',
            },
            {
                'id': 'pn',
                'title': "Parc Naturel",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'crmsf',
                'title': "Commission Royale des Monuments, Sites et Fouilles",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'swde',
                'title': "SWDE",
                'description': '<p>14, Rue Joseph Saintraint<br />5000 Namur</p>',
            },
            {
                'id': 'ccatm',
                'title': "CCATM",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'inasep',
                'title': "INASEP",
                'description': '<p>1b, Rue des Viaux<br />5100 Naninne</p>',
            },
            {
                'id': 'belgacom',
                'title': "Belgacom",
                'description': '<p>60, Rue Marie Henriette<br />5000 Namur</p>',
            },
            {
                'id': 'spge',
                'title': "SPGE",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'cibe',
                'title': "CIBE/Vivaqua",
                'description': '<p>70, Rue aux Laines<br />1000 Bruxelles</p>',
            },
            {
                'id': 'sncb',
                'title': "SNCB",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
            {
                'id': 'infrabel',
                'title': "Infrabel",
                'description': '<p>Infrastructure ferroviaire<br />2/003, Place des Guillemins<br />4000 Liège</p>',
            },
            {
                'id': 'voo',
                'title': "VOO",
                'description': '<p>1, Rue xxx<br />xxxx Commune</p>',
            },
        ],
        'missingparts': [
            'UrbanVocabularyTerm', ['NotaryLetter', 'MiscDemand', 'Division', 'Declaration'],
        ],

        'roadmissingparts': [
            'UrbanVocabularyTerm', ['NotaryLetter', 'MiscDemand', 'Division', 'Declaration'],
        ],

        'locationmissingparts': [
            'UrbanVocabularyTerm', ['NotaryLetter', 'MiscDemand', 'Division', 'Declaration'],
        ],

        'authority': [
            'UrbanVocabularyTerm', ['EnvClassOne', 'EnvClassTwo'],
            {'id': "college", 'title': u"Collège"},
            {'id': "ft", 'title': u"Fonctionnaire technique"},
        ],

        'inadmissibilityreasons': [
            'UrbanVocabularyTerm', ['EnvClassOne', 'EnvClassTwo', 'EnvClassThree'],
            {'id': "missing_parts", 'title': u"Pièces/renseignements manquants"},
            {'id': "no_deposit_receipt", 'title': u"Le dossier n'a pas été déposé contre récipissé"},
            {'id': "no_recommanded_deposit", 'title': u"Le dossier n'a pas été envoyé par recommandé"},
        ],

        'applicationreasons': [
            'UrbanVocabularyTerm', ['EnvClassOne', 'EnvClassTwo', 'EnvClassThree'],
            {'id': "new_business", 'title': u"Mise en activité d'un établissement nouveau"},
            {'id': "class_change", 'title': u"Maintien en activité d'un établissement qui vient d'être rangé en classe 3 suite à une modification de la liste des installations et activités classées"},
            {'id': "licence_expiration", 'title': u"Maintien en activité d’un établissement dont la durée de validité de la déclaration est arrivée à expiration"},
            {'id': "restart_old_business", 'title': u"Remise en activité d’un établissement existant"},
            {'id': "transformation", 'title': u"Extension ou de la transformation d’un établissement ancien"},
            {'id': "location_move", 'title': u"Déplacement de l’établissement"},
            {'id': "regularisation", 'title': u"Régularisation"},
        ],
        'specificfeatures': [
            'SpecificFeatureTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {
                'id': "schema-developpement-espace-regional",
                'title': u"Option particulière du schéma de développement de l'espace régional",
                'description': "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>"
            },
            {
                'id': "situe-en-zone",
                'title': u"Situé en Zone [...]",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                'relatedFields': ['folderZone', '']
            },
            {
                'id': "plan-de-secteur",
                'title': u"Plan de secteur",
                'description': "<p>est situé - dans un périmètre ... - en [[python: object.getValueForTemplate('folderZone'),]] au projet - de révision du - de - plan de secteur de ... adopté par ... du ...;</p>",
                'relatedFields': ['folderZone', '']
            },
            {
                'id': "plan-communal-ammenagement",
                'title': u"En Plan Communal d'Aménagement",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] dans le périmètre du plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]] et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                'relatedFields': ['folderZone', 'isInPCA', 'pca', '']
            },
            {
                'id': "plan-communal-ammenagement-revision",
                'title': u"En Plan Communal d'Aménagement (révision),",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] dans le périmètre du projet - de révision du - de - plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]];</p>",
                'relatedFields': ['folderZone', 'isInPCA', 'pca', '']
            },
            {
                'id': "perimetre-lotissement",
                'title': u"Dans un lot dans le périmètre d'un lotissement",
                'description': "<p>est situé sur le(s}, lot(s) n° [[python: object.getValueForTemplate('subdivisionDetails')]] dans le périmètre du lotissement [[python: object.getValueForTemplate('parcellings', subfield='label')]]non périmé autorisé du [[python: '/'.join(object.getValueForTemplate('parcellings', subfield='authorizationDate').split()[0].split('/')[::-1]) ]];</p>",
            },
            {
                'id': "ssc",
                'title': u"Schéma de structure communal",
                'description': "<p> est situé en [[python: object.getValueForTemplate('SSC'),]] au schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
                'relatedFields': ['SSC', '']
            },
            {
                'id': "ssc-revision",
                'title': u"Schéma de structure communal (révision),",
                'description': "<p> est situé en [[python: object.getValueForTemplate('SSC'),]] au projet de - révision du - de - schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
                'relatedFields': ['SSC', '']
            },
            {
                'id': "rcu",
                'title': u"Règlement communal d'urbanisme",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement régional d'urbanisme [[python: object.getValueForTemplate('folderZone'}, ]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-approuve",
                'title': u"Règlement communal d'urbanisme (approuvé),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue'),]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-revision",
                'title': u"Règlement communal d'urbanisme (révision),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal visé(e}, par le projet - de révision du - de - règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue')]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-approuve-provisoirement",
                'title': u"Règlement communal d'urbanisme (approuvé provisoirement),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par [[python: ', '.join(object.getValuesForTemplate('RCU', subfield='extraValue'},) ]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-unite-paysagere-urbaine",
                'title': u"Règlement communal d'urbanisme (Unité paysagère urbaine),",
                'description': "<p>est situé en unité paysagère urbaine de bâtisse en ordre continu Art.15 au règlement communal d'urbanisme en vigueur;</p>",
            },
            {
                'id': "natura-2000",
                'title': u"Site Natura 2000",
                'description': "<p>est situé dans le périmètre d'un site Natura 2000 visé par l'article 1bis alinéa unique 18° de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                'id': "natura-2000-art6",
                'title': u"Natura 2000 (article 6 de la loi du 12 juillet 1973),",
                'description': "<p>est situé dans le périmètre d'un territoire désigné en vertu de l'article 6 de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                'id': "zone-prise-eau",
                'title': u"Zone de prise d'eau",
                'description': "<p>est situé dans une zone de prise d'eau, de prévention ou de surveillance au sens du décret du 30 avril 1990 relatif à la protection et l'exploitation des eaux souterraines et des eaux potabilisables modifié la dernière fois par le décret du 15 avril 1999 relatif au cycle de l'eau et instituant une société publique de gestion de l'eau;</p>",
            },
            {
                'id': "plan-expropriation",
                'title': u"Plan d'expropriation",
                'description': "<p> est situé dans les limites d'un plan d'expropriation approuvé par ... du ... ; le pouvoir expropriant est : ...;</p>",
            },
            {
                'id': "droit-de-preemption",
                'title': u"Droit de préemption",
                'description': "<p>est situé dans un périmètre d'application du droit de préemption arrêté par ... du ...; le(s}, bénéficiaires(s) du droit de préemption est (sont) : ...;</p>",
            },
            {
                'id': "perimetre-site-desaffecte",
                'title': u"Périmètre site désaffecté",
                'description': "<p>est situé dans le périmètre du site d'activité économique désaffecté suivant : ...;</p>",
            },
            {
                'id': "revitalisation-urbaine",
                'title': u"Revitalisation urbaine",
                'description': "<p>est situé dans un périmètre de revitalisation urbaine;</p>",
            },
            {
                'id': "renovation-urbaine",
                'title': u"Rénovation urbaine",
                'description': "<p>est situé dans un périmètre de rénovation urbaine;</p>",
            },
            {
                'id': "classe",
                'title': u"Classé (article 196 du CWATUPE),",
                'description': "<p>est - inscrit sur la liste de sauvegarde visée à l'article 193 - classé en application de l'article 196 - situé dans une zone de protection visée à l'article 209 - localisé dans un site repris à l'inventaire des sites archéologiques visés à l'article 233 - du Code précité;</p>",
            },
            {
                'id': "raccordable-egout",
                'title': u"Raccordable à l'égout",
                'description': "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>",
            },
            {
                'id': "raccordable-egout-prevision",
                'title': u"Raccordable à l'égout (prévision),",
                'description': "<p>sera raccordable à l'égout selon les prévisions actuelles;</p>",
            },
            {
                'id': "zone-faiblement-habitee",
                'title': u"Zone faiblement habitée (épuration individuelle),",
                'description': "<p>est situé dans une des zones faiblement habitée qui ne seront pas pourvue d'égout et qui feront l'objet d'une épuration individuelle;</p>",
            },
            {
                'id': "voirie-suffisamment-equipee",
                'title': u"Voirie suffisamment équipée",
                'description': "<p>bénéficie d'un accès à une voirie suffisamment équipée en eau, électricité, pourvue d'un revêtement solide et d'une largeur suffisante compte tenu de la situation des lieux;</p>",
            },
        ],

        'roadspecificfeatures': [
            'SpecificFeatureTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {
                'id': "raccordable-egout",
                'title': u"Raccordable à l'égout",
                'description': "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>",
            },
            {
                'id': "raccordable-egout-prevision",
                'title': u"Raccordable à l'égout (prévision),",
                'description': "<p>sera raccordable àl'égout selon les prévisions actuelles;</p>",
            },
            {
                'id': "zone-faiblement-habitee",
                'title': u"Zone faiblement habitée (épuration individuelle),",
                'description': "<p>est situé dans une des zones faiblement habitée qui ne seront pas pourvue d'égout et qui feront l'objet d'une épuration individuelle;</p>",
            },
            {
                'id': "voirie-suffisamment-equipee",
                'title': u"Voirie suffisamment équipée",
                'description': "<p>bénéficie d'un accès à une voirie suffisamment équipée en eau, électricité, pourvue d'un revêtement solide et d'une largeur suffisante compte tenu de la situation des lieux;</p>",
            },
        ],

        'locationspecificfeatures': [
            'SpecificFeatureTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {
                'id': "schema-developpement-espace-regional",
                'title': u"Option particulière du schéma de développement de l'espace régional",
                'description': "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>",
            },
            {
                'id': "situe-en-zone",
                'title': u"Situé en Zone [...]",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] au plan de secteur de ... adopté par ... du ... et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                'relatedFields': ['folderZone', '']
            },
            {
                'id': "plan-de-secteur",
                'title': u"Plan de secteur",
                'description': "<p>est situé - dans un périmètre ... - en [[python: object.getValueForTemplate('folderZone'),]] au projet - de révision du - de - plan de secteur de ... adopté par ... du ...;</p>",
                'relatedFields': ['folderZone', '']
            },
            {
                'id': "plan-communal-ammenagement",
                'title': u"En Plan Communal d'Aménagement",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] dans le périmètre du plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]] et qui n'a pas cessé de produire ses effets pour le bien précité;</p>",
                'relatedFields': ['folderZone', 'isInPCA', 'pca', '']
            },
            {
                'id': "plan-communal-ammenagement-revision",
                'title': u"En Plan Communal d'Aménagement (révision),",
                'description': "<p>est situé en [[python: object.getValueForTemplate('folderZone'),]] dans le périmètre du projet - de révision du - de - plan communal d'aménagement [[python: object.getValueForTemplate('pca', subfield='label')]] approuvé par [[python: object.getValueForTemplate('pca', subfield='decreeType')]] du [[python: '/'.join(object.getValueForTemplate('pca', subfield='decreeDate').split()[0].split('/')[::-1]) ]];</p>",
                'relatedFields': ['folderZone', 'isInPCA', 'pca', '']
            },
            {
                'id': "perimetre-lotissement",
                'title': u"Dans un lot dans le périmètre d'un lotissement",
                'description': "<p>est situé sur le(s}, lot(s) n° [[python: object.getValueForTemplate('subdivisionDetails')]] dans le périmètre du lotissement [[python: object.getValueForTemplate('parcellings', subfield='label')]]non périmé autorisé du [[python: '/'.join(object.getValueForTemplate('parcellings', subfield='authorizationDate').split()[0].split('/')[::-1]) ]];</p>",
            },
            {
                'id': "ssc",
                'title': u"Schéma de structure communal",
                'description': "<p> est situé en [[python: object.getValueForTemplate('SSC'),]] au schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
                'relatedFields': ['SSC', '']
            },
            {
                'id': "ssc-revision",
                'title': u"Schéma de structure communal (révision),",
                'description': "<p> est situé en [[python: object.getValueForTemplate('SSC'),]] au projet de - révision du - de - schéma de structure communal adopté par [[python: object.getValueForTemplate('SSC', subfield='extraValue') ]];</p>",
                'relatedFields': ['SSC', '']
            },
            {
                'id': "rcu",
                'title': u"Règlement communal d'urbanisme",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement régional d'urbanisme [[python: object.getValueForTemplate('folderZone'}, ]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-approuve",
                'title': u"Règlement communal d'urbanisme (approuvé),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue'),]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-revision",
                'title': u"Règlement communal d'urbanisme (révision),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal visé(e}, par le projet - de révision du - de - règlement communal d'urbanisme approuvé par [[python: object.getValueForTemplate('RCU', subfield='extraValue')]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-approuve-provisoirement",
                'title': u"Règlement communal d'urbanisme (approuvé provisoirement),",
                'description': "<p>est situé sur le territoire ou la partie du territoire communal où le règlement communal d'urbanisme approuvé provisoirement par [[python: ', '.join(object.getValuesForTemplate('RCU', subfield='extraValue'},) ]] est applicable;</p>",
                'relatedFields': ['RCU', '']
            },
            {
                'id': "rcu-unite-paysagere-urbaine",
                'title': u"Règlement communal d'urbanisme (Unité paysagère urbaine),",
                'description': "<p>est situé en unité paysagère urbaine de bâtisse en ordre continu Art.15 au règlement communal d'urbanisme en vigueur;</p>",
            },
            {
                'id': "natura-2000",
                'title': u"Site Natura 2000",
                'description': "<p>est situé dans le périmètre d'un site Natura 2000 visé par l'article 1bis alinéa unique 18° de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                'id': "natura-2000-art6",
                'title': u"Natura 2000 (article 6 de la loi du 12 juillet 1973),",
                'description': "<p>est situé dans le périmètre d'un territoire désigné en vertu de l'article 6 de la loi du 12 juillet 1973 sur la conservation de la nature, modifié par le décret du 6 décembre 2001 relatif à la conservation des sites Natura 2000 ainsi que de la faune et de la flore sauvages;</p>",
            },
            {
                'id': "zone-prise-eau",
                'title': u"Zone de prise d'eau",
                'description': "<p>est situé dans une zone de prise d'eau, de prévention ou de surveillance au sens du décret du 30 avril 1990 relatif à la protection et l'exploitation des eaux souterraines et des eaux potabilisables modifié la dernière fois par le décret du 15 avril 1999 relatif au cycle de l'eau et instituant une société publique de gestion de l'eau;</p>",
            },
            {
                'id': "plan-expropriation",
                'title': u"Plan d'expropriation",
                'description': "<p> est situé dans les limites d'un plan d'expropriation approuvé par ... du ... ; le pouvoir expropriant est : ...;</p>",
            },
            {
                'id': "droit-de-preemption",
                'title': u"Droit de préemption",
                'description': "<p>est situé dans un périmètre d'application du droit de préemption arrêté par ... du ...; le(s}, bénéficiaires(s) du droit de préemption est (sont) : ...;</p>",
            },
            {
                'id': "perimetre-site-desaffecte",
                'title': u"Périmètre site désaffecté",
                'description': "<p>est situé dans le périmètre du site d'activité économique désaffecté suivant : ...;</p>",
            },
            {
                'id': "revitalisation-urbaine",
                'title': u"Revitalisation urbaine",
                'description': "<p>est situé dans un périmètre de revitalisation urbaine;</p>",
            },
            {
                'id': "classe",
                'title': u"Classé (article 196 du CWATUPE),",
                'description': "<p>est - inscrit sur la liste de sauvegarde visée à l'article 193 - classé en application de l'article 196 - situé dans une zone de protection visée à l'article 209 - localisé dans un site repris à l'inventaire des sites archéologiques visés à l'article 233 - du Code précité;</p>"
            },
        ],

        'townshipspecificfeatures': [
            'SpecificFeatureTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {
                'id': "zone-a-risque",
                'title': u"Se trouve dans une zone à risque",
                'description': "<p>se trouve dans une zone à risque (faible moyen élevé}, dans la cartographie Aléa d'inondation par débordement de cours d'eau - dressée dans le cadre du plan P.L.U.I.E.S et annexée à l'arrêté du Gouvernement Wallon, adopté en date du 13 juillet 2008;</p>",
                'relatedFields': ['floodingLevel', '']
            },
            {
                'id': "insalubrite",
                'title': u"Est frappé d'un Arrêté d'insalubrité",
                'description': "<p>est frappé d'un Arrêté d'insalubrité OU d'un permis de location datant du [...] - Le futur acquéreur est invité à prendre contact avec le Service Logement Salubrité (tél. : [...]}, pour de plus amples informations;</p>",
            },
            {
                'id': "infraction-urbanistique",
                'title': u"Infraction urbanistique",
                'description': "<p>fait l'objet d'une infraction urbanistique reconnue par notre Administration communale portant sur [...];</p>",
            },
            {
                'id': "cu1",
                'title': u"Certificat d'Urbanisme 1 dans les deux ans",
                'description': "<p>a fait l'objet, dans les deux dernières années, d'un Certificat d'Urbanisme n°1 datant du [...] et portant la référence [...];</p>",
            },
            {
                'id': "permis-urbanisme",
                'title': u"Permis d'Urbanisme depuis 1976",
                'description': "<p>a fait l'objet depuis 1976 d'un permis d'urbanisme daté de [...] pour [...] - REFUS/ACCEPTE - Réf.: [...];</p>",
            },
            {
                'id': "reconnaissance-economique",
                'title': u"Périmètre de reconnaissance économique",
                'description': "<p>est repris dans un périmètre de reconnaissance économique;</p>",
            },
            {
                'id': "site-seveso",
                'title': u"A moins de 2000m d'un site SEVESO",
                'description': "<p>est situé à moins de 2000m d'un site classé SEVESO à savoir [...];</p>",
            },
            {
                'id': "gestion-des-sols",
                'title': u"Gestion des sols",
                'description': "<p>état des sols, nous ne sommes pas en mesure de déterminer si le bien est ou pas inscrit dans la banque de données au sens de l'article 10 du décret du 5 décembre 2008 relatif à la gestion des sols (Décret du 05 décembre 2008, art.89, al.2},</p>",
            },
            {
                'id': "galeries-minieres",
                'title': u"Galeries minières",
                'description': "<p>est situé dans une région traversée par de nombreuses galeries minières et nous ne sommes pas en mesure de déterminer l'état de celle-ci, veuillez donc prendre vos renseignements auprès du SPW - Département de l'Environnement et de l'Eau - Direction des risques industriels, géologique et miniers - Cellules sous-sol/géologique - Avenue Prince de Liège, 15 à 5100 Jambes;  Le bien est situé sur une zone de consultation en liaison avec les gisements et puits de mine;</p>",
            },
        ],

        'opinionstoaskifworks': [
            'UrbanVocabularyTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {'id': "ores-gaz-electricite", 'title': u"ORES - Gaz-Electricité", 'description': u"<p>Adresse</p>"},
            {'id': "ores-eclairage-public", 'title': u"ORES - Service Eclairage public", 'description': u"<p>Adresse</p>"},
            {'id': "belgacom", 'title': u"Belgacom", 'description': u"<p>Adresse</p>"},
            {'id': "fluxsys", 'title': u"Fluxsys", 'description': u"<p>Adresse</p>"},
            {'id': "air-liquide", 'title': u"Air Liquide - Div. Belge - Service des Canalisations", 'description': u"<p>Adresse</p>"},
            {'id': "elia-asset-sud", 'title': u"Elia Asset Sud", 'description': u"<p>Adresse</p>"},
            {'id': "swde", 'title': u"SWDE (Société Wallone de Distribution d'Eau),", 'description': u"<p>Adresse</p>"},
            {'id': "voo", 'title': u"Voo", 'description': u"<p>Adresse</p>"},
        ],

        'basement': [
            'UrbanVocabularyTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {'id': "zone-carriere", 'title': u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les carrières souterraines"},
            {'id': "zone-karstique", 'title': u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les phénomènes karstiques"},
            {'id': "zone-gisement-et-puit", 'title': u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les gisements et puits de mine"},
            {'id': "zone-miniere", 'title': u"Le bien est situé à environ 50 m d'une zone de consultation en liaison avec les minières de fer"},
        ],

        'zip': [
            'UrbanVocabularyTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {'id': "type-1", 'title': u"Type 1: zone à forte pression foncière"},
            {'id': "type-2", 'title': u"Type 2: zone de requalification des noyaux d'habitat"},
            {'id': "type-3", 'title': u"Type 3: zons de développement global de quartier"},
            {'id': "type-4", 'title': u"Type 4: zones de cités sociales à requalifier"},
        ],

        'noteworthytrees': [
            'UrbanVocabularyTerm', ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'],
            {'id': "arbres", 'title': u"Arbres remarquables"},
            {'id': "alignement", 'title': u"Alignement d'arbres ou de haies remarquables "},
            {'id': "haies", 'title': u"Zone Haie remarquable"},
        ],

        'investigationarticles': [
            'UrbanVocabularyTerm', ['BuildLicence', 'Article127', 'ParcelOutLicence', 'UrbanCertificateTwo'],
            {'id': "330-1", 'title': u"330 1° - « [...] bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et [...] »", 'description': "<p>« la construction ou la reconstruction de bâtiments dont la hauteur est d'au moins quatre niveaux ou douze mètres sous corniche et dépasse de trois mètres ou plus la moyenne des hauteurs sous corniche des bâtiments situés dans la même rue jusqu'à cinquante mètres de part et d'autre de la construction projetée ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", 'extraValue': "330 1°"},
            {'id': "330-2", 'title': u"330 2° - « [...] bâtiment dont la profondeur, mesurée [...] est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments [...] »", 'description': "<p>« la construction ou la reconstruction de bâtiments dont la profondeur, mesurée à partir de l'alignement ou du front de bâtisse lorsque les constructions voisines ne sont pas implantées sur l'alignement, est supérieure à 15 mètres et dépasse de plus de 4 mètres les bâtiments situés sur les parcelles contiguës (AGW du 23 décembre 1998, art 1er), la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", 'extraValue': "330 2°"},
            {'id': "330-3", 'title': u"330 3° - « [...] un magasin [...] dont la surface nette de vente est supérieure à 400 m² [...] »", 'description': "<p>« la construction, la reconstruction d'un magasin ou la modification de la destination d'un bâtiment en magasin dont la surface nette de vente est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", 'extraValue': "330 3°"},
            {'id': "330-4", 'title': u"330 4° - « [...] de bureaux [...] dont la superficie des planchers est supérieure à 650 m² [...] »", 'description': "<p>« la construction, la reconstruction de bureaux ou la modification de la destination d'un bâtiment en bureaux dont la superficie des planchers est supérieure à 650 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", 'extraValue': "330 4°"},
            {'id': "330-5", 'title': u"330 5° - « [...] bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² [...] »", 'description': "<p>« la construction, la reconstruction ou la modification de la destination d'un bâtiment en atelier, entrepôt ou hall de stockage à caractère non agricole dont la superficie des planchers est supérieure à 400 m² ; la transformation de bâtiments ayant pour effet de placer ceux-ci dans les mêmes conditions »</p>", 'extraValue': "330 5°"},
            {'id': "330-6", 'title': u"330 6° - « l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »", 'description': "<p>« l'utilisation habituelle d'un terrain pour le dépôt d'un ou plusieurs véhicules usagés, de mitrailles, de matériaux ou de déchets »</p>", 'extraValue': "330 6°"},
            {'id': "330-7", 'title': u"330 7° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »", 'description': "<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui portent sur une superficie de 2 hectares et plus »</p>", 'extraValue': "330 7°"},
            {'id': "330-8", 'title': u"330 8° - « [...] permis de lotir ou de permis d'urbanisme [...] constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »", 'description': "<p>« les demandes de permis de lotir ou de permis d'urbanisme relatives à des constructions groupées visées à l'article 126 qui peuvent comporter un ou plusieurs bâtiments visés aux 1°, 2°, 3°, 4° et 5° »</p>", 'extraValue': "330 8°"},
            {'id': "330-9", 'title': u"330 9° - « les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »", 'description': "<p>« les demandes de permis de lotir ou de permis d'urbanisme visées à l'article 128 »</p>", 'extraValue': "330 9°"},
            {'id': "330-10", 'title': u"330 10° - « les demandes de permis de lotir visées à l'article 97 »", 'description': "<p>« les demandes de permis de lotir visées à l'article 97 »</p>", 'extraValue': "330 10°"},
            {'id': "330-11", 'title': u"330 11° - « les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »", 'description': "<p>« les demandes de permis de lotir ou de permis d'urbanisme impliquant l'application des articles 110 à 113 »</p>", 'extraValue': "330 11°"},
            {'id': "330-12", 'title': u"330 12° - « [...] permis de lotir et les demandes de permis d'urbanisme [...] d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde [...] »", 'description': "<p>« les demandes de permis de lotir et les demandes de permis d'urbanisme relatives à la construction, la reconstruction ou la transformation d'un bâtiment qui se rapportent à des biens immobiliers inscrits sur la liste de sauvegarde, classés, situés dans une zone de protection visée à l'article 205 (lire article 209) ou localisés dans un site mentionné à l'atlas visé à l'article 215 (lire article 233) »</p>", 'extraValue': "330 12°"},
            {'id': "330-13", 'title': u"330 13° - « les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »", 'description': "<p>« les voiries publiques de la Région classées en réseau interurbain (RESI) par l'arrêté ministériel du 11 août 1994 »</p>", 'extraValue': "330 13°"},
            {'id': "334-2", 'title': u"334 2° - « Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique [...]»", 'description': "<p>« Dès le lendemain du jour où il est en possession de l'accusé de réception et jusqu'au jour de la clôture de l'enquête publique, le demandeur est tenu d'afficher sur le terrain faisant l'objet de la demande : 2° dans les cas visés à l'article 330, 1° à 5°, et 12°, ou lorsque la dérogation porte sur le gabarit d'un bâtiment, une vue axonométrique du projet et des bâtiments contigus »</p>", 'extraValue': "334 2°"},
        ],

        'folderdelays': [
            'UrbanDelay', ['BuildLicence', 'ParcelOutLicence', 'UrbanCertificateTwo'],
            {'id': "30j", 'title': u"30 jours", 'deadLineDelay': 30, 'alertDelay': 20},
            {'id': "70j", 'title': u"70 jours", 'deadLineDelay': 70, 'alertDelay': 20},
            {'id': "75j", 'title': u"75 jours", 'deadLineDelay': 75, 'alertDelay': 20},
            {'id': "115j", 'title': u"115 jours", 'deadLineDelay': 115, 'alertDelay': 20},
            {'id': "230j", 'title': u"230 jours", 'deadLineDelay': 230, 'alertDelay': 20},
            {'id': "inconnu", 'title': u"Inconnu", 'deadLineDelay': 0, 'alertDelay': 20},
        ],

        'derogations': [
            'UrbanVocabularyTerm', ['BuildLicence', 'Article127', 'ParcelOutLicence', 'UrbanCertificateTwo'],
            {'id': "dero-ps", 'title': u"au Plan de secteur"},
            {'id': "dero-pca", 'title': u"au Plan Communal d'Aménagement"},
            {'id': "dero-rru", 'title': u"au Règlement Régional d'Urbanisme"},
            {'id': "dero-rcu", 'title': u"au Règlement Communal d'Urbanisme"},
            {'id': "dero-lot", 'title': u"au Lotissement"},
        ],

        'folderbuildworktypes': [
            'UrbanVocabularyTerm', ['BuildLicence', 'Article127', 'ParcelOutLicence', 'UrbanCertificateTwo'],
            {'id': "ncmu", 'title': u"Nouvelle construction - Maison unifamiliale", 'extraValue': 'N_UNI'},
            {'id': "ncia", 'title': u"Nouvelle construction - Immeuble appartements", 'extraValue': 'N_APPART'},
            {'id': "nca", 'title': u"Nouvelle construction - Autres", 'extraValue': 'N_AUT'},
            {'id': "tmu", 'title': u"Transformation - maison unifamiliale", 'extraValue': 'T_UNI'},
            {'id': "tia", 'title': u"Transformation - immeuble appartements", 'extraValue': 'T_APPART'},
            {'id': "tab", 'title': u"Transformation - autre bâtiment", 'extraValue': 'T_AUT'},
            {'id': "dg", 'title': u"Démolition - Général", 'extraValue': 'DEM'},
            {'id': "lg", 'title': u"Lotissement - Général", 'extraValue': 'LOT'},
            {'id': "tnbg", 'title': u"Transformation Non-bâti - Général", 'extraValue': 'T_NBAT'},
            {'id': "td", 'title': u"Taudis", 'extraValue': 'TAUDIS'},
            {'id': "integration", 'title': u"Intégration dans voirie publique", 'extraValue': 'INT'},
            {'id': "leasing", 'title': u"Leasing (pour mémoire SPF Finances),", 'extraValue': 'LEASING'},
            {'id': "autres", 'title': u"Autres", 'extraValue': 'AUTRE'},
        ],

    },
    'global': {

        'deposittype': [
            'UrbanVocabularyTerm',
            {'id': "recommande", 'title': u"Par recommandé postal"},
            {'id': "surplace", 'title': u"Déposé à l'administration communale"},
        ],

        'recoursedecisions': [
            'UrbanVocabularyTerm',
            {'id': "confirme", 'title': u"Confirmé"},
            {'id': "infirme", 'title': u"Infirmé"},
        ],

        'pcas': [
            'PcaTerm',
            {'id': "pca1", 'label': u"Plan communal d'aménagement 1", 'number': '1', 'decreeDate': "2009/01/01", 'decreeType': "royal"},
            {'id': "pca2", 'label': u"Plan communal d'aménagement 2", 'number': '2', 'decreeDate': "2008/06/23", 'decreeType': "royal"},
            {'id': "pca3", 'label': u"Plan communal d'aménagement 3", 'number': '3', 'decreeDate': "2001/12/13", 'decreeType': "departmental"},
        ],

        'pcazones': [
            'UrbanVocabularyTerm',
            {
                'id': "zone-de-construction-d-habitation-fermee",
                'title': u"Zone de construction d'habitation fermée"
            },
            {
                'id': "zone-de-construction-d-habitation-semi-ouverte",
                'title': u"Zone de construction d'habitation semi ouverte"
            },
            {
                'id': "zone-de-construction-d-habitation-ouverte",
                'title': u"Zone de construction d'habitation ouverte"
            },
            {
                'id': "zone-de-construction-en-annexe",
                'title': u"Zone de construction en annexe"
            },
            {
                'id': "zone-de-recul",
                'title': u"Zone de recul"
            },
            {
                'id': "zone-artisanale",
                'title': u"Zone artisanale"
            },
            {
                'id': "zone-de-voirie",
                'title': u"Zone de voirie"
            },
            {
                'id': "zone-affectee-a-l-eau",
                'title': u"Zone affectée à l'eau"
            },
            {
                'id': "zone-de-construction-a-destination-publique-indifferenciee",
                'title': u"Zone de construction à destination publique indifférenciée"
            },
            {
                'id': "zone-agricole-indiferenciee",
                'title': u"Zone agricole indiférenciée"
            },
        ],

        'pashs': [
            'UrbanVocabularyTerm',
            {'id': "zone-epuration-collective", 'title': u"Zone d'assainissement collectif"},
            {'id': "zone-transitoire", 'title': u"Zone d'assainissement transitoire"},
            {'id': "zone-epuration-individuelle", 'title': u"Zone d'assainissement individuel"},
        ],

        'folderroadtypes': [
            'UrbanVocabularyTerm',
            {'id': "com", 'title': u"Communale"},
            {'id': "priv", 'title': u"Privée"},
            {'id': "prov", 'title': u"Provinciale"},
            {'id': "reg", 'title': u"Régionale"},
            {'id': "vic", 'title': u"Vicinale"},
        ],

        'folderprotectedbuildings': [
            'UrbanVocabularyTerm',
            {'id': "classe", 'title': u"classé ou assimilé"},
            {'id': "certificatpatrimoine", 'title': u"certificat de patrimoine délivré"},
            {'id': "zoneprotection", 'title': u"zone de protection"},
            {'id': "reprisinventaire", 'title': u"repris à l'inventaire"},
            {'id': "archeologique", 'title': u"à l'Atlas archéologique"},
        ],

        'folderroadequipments': [
            'UrbanVocabularyTerm',
            {'id': "eau", 'title': u"distribution d'eau"},
            {'id': "electricite", 'title': u"distribution électrique"},
            {'id': "epuration", 'title': u"canalisation reliée à une station d'épuration publique"},
            {'id': "nonepuration", 'title': u"canalisation non-reliée à une station d'épuration publique"},
            {'id': "egoutsep", 'title': u"réseau d'égoutage séparatif"},
            {'id': "pascollecteeaux", 'title': u"pas de canalisation de collecte des eaux"},
            {'id': "fosse", 'title': u"fossé"},
        ],

        'folderroadcoatings': [
            'UrbanVocabularyTerm',
            {'id': "filetseau", 'title': u"Filets d'eau"},
            {'id': "bordures", 'title': u"Bordures"},
        ],

        'folderzones': [
            'UrbanVocabularyTerm',
            {'id': "zh", 'title': u"zone d'habitat"},
            {'id': "zhcr", 'title': u"zone d'habitat à caractère rural"},
            {'id': "zhcrza", 'title': u"zone d’habitat à caractère rural sur +/- 50 m et le surplus en zone agricole"},
            {'id': "zspec", 'title': u"zone de services publics et d'équipements communautaires"},
            {'id': "zcet", 'title': u"zone de centre d'enfouissement technique"},
            {'id': "zl", 'title': u"zone de loisirs"},
            {'id': "zaem", 'title': u"zones d'activité économique mixte"},
            {'id': "zaei", 'title': u"zones d'activité économique industrielle"},
            {'id': "zaesae", 'title': u"zones d'activité économique spécifique agro-économique"},
            {'id': "zaesgd", 'title': u"zones d'activité économique spécifique grande distribution"},
            {'id': "ze", 'title': u"zone d'extraction"},
            {'id': "zadci", 'title': u"zone d'aménagement différé à caractère industriel"},
            {'id': "za", 'title': u"zone agricole"},
            {'id': "zf", 'title': u"zone forestière"},
            {'id': "zev", 'title': u"zone d'espaces verts"},
            {'id': "zn", 'title': u"zone naturelle"},
            {'id': "zp", 'title': u"zone de parc"},
            {'id': "znatura2000", 'title': u"zone Natura 2000"},
        ],

        'rcu': [
            'UrbanVocabularyTerm',
            {'id': "rcu-aire-a", 'title': u"Aire A habitat centre des villages"},
            {'id': "rcu-aire-b", 'title': u"Aire B habitat hors centre des villages"},
            {'id': "rcu-aire-c", 'title': u"Aire C rives des habitats"},
            {'id': "rcu-aire-d", 'title': u"Aire D activités économiques"},
            {'id': "rcu-aire-e", 'title': u"Aire E dominante rurale"},
        ],

        'ssc': [
            'UrbanVocabularyTerm',
            {'id': "ssc-centre-ville", 'title': u"Zone d'habitat urbain de centre-ville"},
            {'id': "ssc-suburbain", 'title': u"Zone d'habitat suburbain"},
            {'id': "ssc-services-publics", 'title': u"Zone de services publics et d'équipements communautaires"},
            {'id': "ssc-industrielle", 'title': u"Zone industrielle"},
            {'id': "ssc-industrielle-verte", 'title': u"Zone industrielle verte"},
            {'id': "ssc-militaire", 'title': u"Zone militaire"},
            {'id': "ssc-habitat-urban-differe", 'title': u"Zone d'habitat urbain à aménagement différé"},
            {'id': "ssc-extraction", 'title': u"Zone d'extraction"},
            {'id': "ssc-loisirs", 'title': u"Zone de loisirs et de séjours"},
            {'id': "ssc-agricole", 'title': u"Zone agricole"},
            {'id': "ssc-vert-social", 'title': u"Zone d'espace vert social"},
            {'id': "ssc-vert-eco", 'title': u"Zone d'espace vert ecologique"},
            {'id': "ssc-vert-mixte", 'title': u"Zone d'espace vert mixte"},
            {'id': "ssc-naturelle", 'title': u"Zone naturelle"},
            {'id': "ssc-forestiere", 'title': u"Zone forestière"},
            {'id': "ssc-forestiere-mixte", 'title': u"Zone forestière mixte"},
            {'id': "ssc-activites-economiques-mixtes", 'title': u"Zone d'activités économiques mixtes"},
            {'id': "ssc-activites-economiques-tertiaires", 'title': u"Zone d'activités économiques tertiaires"},
        ],

        'prenu': [
            'UrbanVocabularyTerm',
            {'id': "xxx", 'title': u"Revitalisation urbaine de XXX"},
            {'id': "yyy", 'title': u"Revitalisation urbaine de YYY"},
            {'id': "zzz", 'title': u"Revitalisation urbaine de ZZZ"},
        ],

        'prevu': [
            'UrbanVocabularyTerm',
            {'id': "xxx", 'title': u"Rénovation urbaine de XXX"},
            {'id': "yyy", 'title': u"Rénovation urbaine de YYY"},
            {'id': "zzz", 'title': u"Rénovation urbaine de ZZZ"},
        ],

        'rgbsr': [
            'UrbanVocabularyTerm',
            {'id': "limoneux-brabancon", 'title': u"du Plateau Limoneux Brabançon (art. 322-15 (lire « article 420 »));"},
            {'id': "limoneux-hennuyer", 'title': u"du Plateau Limoneux Hennuyer (art. 322-15 (lire « article 420 »));"},
            {'id': "hesbaye", 'title': u"de la Hesbaye (art. 322-17 (lire « article 422 »));"},
            {'id': "herve", 'title': u"du Pays de Herve (art. 322-18 (lire « article 423 »));"},
            {'id': "condroz", 'title': u"du Condroz (art. 322,-19 (lire « article 424 »));"},
            {'id': "famenne", 'title': u"de la Fagne-Famenne (art. 322-2 (lire « article 425 »));"},
            {'id': "ardenne", 'title': u"de l’Ardenne (art. 322-21 (lire « article 426 »));"},
            {'id': "lorraine", 'title': u"de la Lorraine (art. 322-22 (lire « article 427 »));"},
        ],

        'airportnoisezone': [
            'UrbanVocabularyTerm',
            {'id': "zone-expo-a", 'title': u"Zone A au plan d'Exposition au bruit"},
            {'id': "zone-devel-a", 'title': u"Zone A au plan de Développement à Long Terme"},
            {'id': "zone-expo-b", 'title': u"Zone B au plan d'Exposition au bruit"},
            {'id': "zone-devel-b", 'title': u"Zone B au plan de Développement à Long Terme"},
        ],

        'persons_titles': [
            'PersonTitleTerm',
            {'id': "notitle", 'title': u"", 'extraValue': "Madame, Monsieur", 'abbreviation': "", 'gender': "male", 'multiplicity': "single"},
            {'id': "madam", 'title': u"Madame", 'extraValue': "Madame", 'abbreviation': "Mme", 'gender': "female", 'multiplicity': "single"},
            {'id': "miss", 'title': u"Mademoiselle", 'extraValue': "Mademoiselle", 'abbreviation': "Mlle", 'gender': "female", 'multiplicity': "single"},
            {'id': "mister", 'title': u"Monsieur", 'extraValue': "Monsieur", 'abbreviation': "M", 'gender': "male", 'multiplicity': "single"},
            {'id': "madam_and_mister", 'title': u"Monsieur et Madame", 'extraValue': "Madame, Monsieur", 'abbreviation': "M et Mme", 'gender': "male", 'multiplicity': "plural"},
            {'id': "master", 'title': u"Maître", 'extraValue': "Maître", 'abbreviation': "Me", 'gender': "male", 'multiplicity': "single"},
            {'id': "masters", 'title': u"Maîtres", 'extraValue': "Maitres", 'abbreviation': "Mes", 'gender': "male", 'multiplicity': "plural"},
            {'id': "misters", 'title': u"Messieurs", 'extraValue': "Messieurs", 'abbreviation': "MM", 'gender': "male", 'multiplicity': "plural"},
            {'id': "ladies", 'title': u"Mesdames", 'extraValue': "Mesdames", 'abbreviation': "Mmes", 'gender': "female", 'multiplicity': "plural"},
            {'id': "consorts", 'title': u"Consorts", 'extraValue': "Consorts", 'abbreviation': "Crts", 'gender': "male", 'multiplicity': "plural"},
        ],

        'persons_grades': [
            'UrbanVocabularyTerm',
            {'id': 'agent-accueil', 'title': "Agent d'accueil"},
            {'id': 'agent-administratif', 'title': "Agent administratif"},
            {'id': 'agent-technique', 'title': "Agent technique"},
            {'id': 'agent-traitant', 'title': "Agent traitant"},
            {'id': 'directeur-administratif', 'title': "Directeur administratif"},
            {'id': 'directeur-general', 'title': "Directeur général"},
            {'id': 'directeur-technique', 'title': "Directeur technique"},
            {'id': 'reponsable', 'title': "Responsable du Service Urbanisme"},
            {'id': 'responsable-accueil', 'title': "Responsable d'accueil"},
            {'id': 'responsable-administratif', 'title': "Responsable administratif"},
            {'id': 'responsable-technique', 'title': "Responsable technique"},
        ],

        'country': [
            'UrbanVocabularyTerm',
            {'id': 'germany', 'title': "Allemagne"},
            {'id': 'belgium', 'title': "Belgique"},
            {'id': 'france', 'title': "France"},
            {'id': 'luxembourg', 'title': "Luxembourg"},
            {'id': 'netherlands', 'title': "Pays Bas"},
        ],

        'externaldecisions': [
            'UrbanVocabularyTerm',
            {'id': "favorable", 'title': u"Favorable"},
            {'id': "favorable-conditionnel", 'title': u"Favorable conditionnel"},
            {'id': "defavorable", 'title': u"Défavorable"},
            {'id': "favorable-defaut", 'title': u"Réputé favorable par défaut"},
        ],

        'rubrics': [
            'Folder',
        ],

        'exploitationconditions': [
            'Folder',
        ],

        'foldermanagers': [
            'FolderManager',
        ],

        'streets': [
            'City',
        ],

        'karst_constraints': [
            'UrbanVocabularyTerm',
            {'id': "no", 'title': u"Sans"},
            {'id': "low", 'title': u"Faible"},
            {'id': "moderate", 'title': u"Modéré"},
            {'id': "high", 'title': u"Fort"},
        ],
    },
}
