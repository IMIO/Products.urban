# -*- coding: utf-8 -*-

default_values = {
    'pcas': [
        'PcaTerm',
        {'id': "pca1", 'label': u"Plan communal d'aménagement 1", 'number': '1', 'decreeDate': "2009/01/01", 'decreeType': "royal"},
    ],

    'pashs': [
        'UrbanVocabularyTerm',
        {'id': "zone-epuration-collective", 'title': u"Zone d'assainissement collectif"},
    ],

    'folderroadtypes': [
        'UrbanVocabularyTerm',
        {'id': "com", 'title': u"Communale"},
    ],

    'folderprotectedbuildings': [
        'UrbanVocabularyTerm',
        {'id': "classe", 'title': u"classé ou assimilé"},
    ],

    'folderroadequipments': [
        'UrbanVocabularyTerm',
        {'id': "eau", 'title': u"distribution d'eau"},
    ],

    'folderroadcoatings': [
        'UrbanVocabularyTerm',
        {'id': "filetseau", 'title': u"Filets d'eau"},
    ],

    'folderzones': [
        'UrbanVocabularyTerm',
        {'id': "zh", 'title': u"zone d'habitat"},
    ],

    'rcu': [
        'UrbanVocabularyTerm',
        {'id': "rcu-aire-a", 'title': u"Aire A habitat centre des villages"},
    ],

    'ssc': [
        'UrbanVocabularyTerm',
        {'id': "ssc-centre-ville", 'title': u"Zone d'habitat urbain de centre-ville"},
    ],

    'persons_titles': [
        'PersonTitleTerm',
        {'id': "notitle", 'title': u"", 'extraValue': "Madame, Monsieur", 'abbreviation': "", 'gender': "male", 'multiplicity': "single"},
    ],

    'persons_grades': [
        'UrbanVocabularyTerm',
        {'id': 'agent-accueil', 'title': "Agent d'accueil"},
    ],

    'country': [
        'UrbanVocabularyTerm',
        {'id': 'germany', 'title': "Allemagne"},
    ],

    'decisions': [
        'UrbanVocabularyTerm',
        {'id': "favorable", 'title': u"Favorable", 'extraValue': "Recevable"},
    ],

    'externaldecisions': [
        'UrbanVocabularyTerm',
        {'id': "favorable", 'title': u"Favorable"},
    ],

    'townshipfoldercategories': [
        'UrbanVocabularyTerm',
        {'id': "abattre", 'title': u"Abattre"},
    ],

    'articles': [
        'UrbanVocabularyTerm',
        {'id': "263_1_1", 'title': u"article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins", 'extraValue': "263 §1er 1°",
         'description': "« article 263 §1er 1° les aménagements conformes à la destination normale des cours et jardins pour autant qu’ils relèvent des actes et travaux visés à l’article 262, 4°, b, d, e et g, mais n’en remplissent pas les conditions; »"},
    ],

    'lotusages': [
        'UrbanVocabularyTerm',
        {'id': "buildable", 'title': u"Lot bâtissable"},
    ],

    'equipmenttypes': [
        'UrbanVocabularyTerm',
        {'id': "telecom", 'title': u"Télécomunication"},
    ],

    'specificfeatures': [
        'UrbanVocabularyTerm',
        {'id': "schema-developpement-espace-regional",
        'title': u"Option particulière du schéma de développement de l'espace régional",
        'description': "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>"},
    ],

    'roadspecificfeatures': [
        'UrbanVocabularyTerm',
        {'id': "raccordable-egout", 'title': u"Raccordable à l'égout",
        'description': "<p>est actuellement raccordable à l'égout selon les normes fixées par le Service Technique Communal;</p>"},
    ],

    'locationspecificfeatures': [
        'UrbanVocabularyTerm',
        {'id': "schema-developpement-espace-regional",
        'title': u"Option particulière du schéma de développement de l'espace régional",
        'description': "<p>fait l'objet d'une option particulière du schéma de développement de l'espace régional, à savoir ...;</p>"},
    ],

    'townshipspecificfeatures': [
        'UrbanVocabularyTerm',
        {'id': "zone-a-risque", 'title': u"Se trouve dans une zone à risque", 'description': "<p>se trouve dans une zone à risque (faible moyen élevé}, dans la cartographie Aléa d'inondation par débordement de cours d'eau - dressée dans le cadre du plan P.L.U.I.E.S et annexée à l'arrêté du Gouvernement Wallon, adopté en date du 13 juillet 2008;</p>"},
    ],

    'opinionstoaskifworks': [
        'OrganisationTerm',
        {'id': "ores-gaz-electricite", 'title': u"ORES - Gaz-Electricité", 'description': u"<p>Adresse</p>"},
    ],

    'foldermakers': [
        'OrganisationTerm',
        {'id': "service-pop", 'title': u"Service population", 'description': u'<p>1, Rue xxx<br />xxxx Commune</p>'},
    ],

    'folderdelays': [
        'UrbanDelay',
        {'id': "30j", 'title': u"30 jours", 'deadLineDelay': 30, 'alertDelay': 20},
    ],

    'derogations': [
        'UrbanVocabularyTerm',
        {'id': "dero-ps", 'title': u"au Plan de secteur"},
    ],

    'folderbuildworktypes': [
'UrbanVocabularyTerm',
        {'id': "ncmu", 'title': u"Nouvelle construction - Maison unifamiliale", 'extraValue': 'N_UNI'},
    ],

    'inadmissibilityreasons': [
'UrbanVocabularyTerm',
        {'id': "missing_parts", 'title': u"Pièces/renseignements manquants"},
    ],

    'applicationreasons': [
'UrbanVocabularyTerm',
        {'id': "new_business", 'title': u"Mise en activité d'un établissement nouveau"},
    ],

}
