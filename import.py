# -*- coding: utf-8 -*-
from Products.urban.profiles.dataMigration.AIHM_migration.AIHM_import import importAIHM
from Products.urban.profiles.dataMigration.AIHM_migration.AIHM_misc import table


def importLalouviereAIHM(context):
    """ Just calls the default AIHM import from La Louvière AIHM profile """
    if context.readDataFile('lalouviere_aihm_marker.txt') is None:
        return

    # !!!!! dirty override, but im just too fuckin lazy.. !!!!!
    custom_mapping = {
        'TYPE_map' : table({
        'header': ['portal_type',         'foldercategory', 'abreviation'],
        '0'     : ['BuildLicence',        'uap',            'PU'],
        '1'     : ['BuildLicence',        'upp',            'PU'],
        '2'     : ['UrbanCertificateOne', 'cu1',            'CU1'],
        '3'     : ['UrbanCertificateTwo', 'cu2',            'CU2'],
        '4'     : ['ParcelOutLicence',    '',               'PL'],
        '5'     : ['NotaryLetter',        '',               'Not'],
        '7'     : ['MiscDemand',          'apct',           'AP'],
        '8'     : [None,                  '',               'INF'],
        '9'     : ['BuildLicence',        'uap',            'FR'],
        '10'    : ['Declaration',         'dup',            'Decl'],
        '11'    : ['MiscDemand',          'rendez-vous',    'RV'],
        })
    }

    # !!!!! dirty override end !!!!!

    importAIHM(context, aihm_filename='export.csv', custom_mapping=custom_mapping)
