# -*- coding: utf-8 -*-

def table(table):
    header = table['header']
    del table['header']
    for key, line in table.iteritems():
        table[key] = dict([(header[i], line[i],) for i in range(len(header))])
    return table

TYPE_map = table({
'header': ['portal_type',         'foldercategory', 'abreviation'],
'0'     : ['BuildLicence',        'uap',            'PU'],
'1'     : ['BuildLicence',        'upp',            'PU'],
'2'     : ['BuildLicence',        '',               'PU'],
'20'    : ['UrbanCertificateOne', 'cu1',            'CU1'],
'21'    : ['UrbanCertificateTwo', 'cu2',            'CU2'],
'22'    : ['NotaryLetter',        '',               'Not'],
'30'    : ['ParcelOutLicence',    '',               'PL'],
'40'    : ['MiscDemand',          'apct',           'DD'],
'50'    : ['BuildLicence',        'art127',         'PU'],
'80'    : ['BuildLicence',        'pu',             'PU'],
'82'    : ['Declaration',         'dup',            'Decl'],
'100'   : ['MiscDemand',          'apct',           'Decl'],
})


eventtype_id_map = table({
'header'             : ['decision_event',                       'folder_complete',     'deposit_event'],
'BuildLicence'       : ['delivrance-du-permis-octroi-ou-refus', 'accuse-de-reception', 'depot-de-la-demande'],
'UrbanCertificateOne': ['octroi-cu1',                           '',                    'depot-de-la-demande'],
'UrbanCertificateTwo': ['octroi-cu2',                           '',                    'depot-de-la-demande'],
'NotaryLetter'       : ['octroi-lettre-notaire',                '',                    'depot-de-la-demande'],
'ParcelOutLicence'   : ['delivrance-du-permis-octroi-ou-refus', 'accuse-de-reception', 'depot-de-la-demande'],
'Declaration'        : ['deliberation-college',                 '',                    'depot-de-la-demande'],
'MiscDemand'         : ['deliberation-college',                 '',                    'depot-de-la-demande'],
'Division'           : ['decision-octroi-refus',                '',                    'depot-de-la-demande'],
})

Titre_map = {
    'monsieur': 'mister',
    'm': 'mister',
    'm.': 'mister',
    'messieurs': 'misters',
    'mrs.': 'misters',
    'mrs': 'misters',
    'madame': 'madam',
    'mme': 'madam',
    'mme.': 'madam',
    'mesdames': 'ladies',
    'mademoiselle': 'miss',
    'monsieur et madame': 'madam_and_mister',
    'm et mme': 'madam_and_mister',
    'mr et mme': 'madam_and_mister',
    'm. et mme': 'madam_and_mister',
    'm et mme.': 'madam_and_mister',
    'm. et mme.': 'madam_and_mister',
    'notaire': 'master',
    'monsieur le notaire': 'master',
    'notaires': 'masters',
    'ma\xc3\xaetre': 'master',
    'ma\xc3\xaetres': 'masters',
}

country_map = {
    'belgique': 'belgium',
    'france': 'france',
    'allemagne': 'germany',
    'luxembourg': 'luxembourg',
    'pays bas': 'netherlands',
}


def normalizeDate(date):
    if not date:
        return ''
    parts = date.split()[0].split('/')
    century = parts[2] > '40' and '19' or '20'
    return '%s/%s/%s%s' % (parts[1], parts[0], century, parts[2])


def cleanAndSplitWord(word):
    clean_word = word.replace('\'', ' ').replace(',', ' ').replace('-', ' ').replace('.', ' ').replace(';', ' ').replace('(', ' ').replace(')', ' ').split()
    return clean_word
