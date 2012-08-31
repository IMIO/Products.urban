# -*- coding: utf-8 -*-
from Products.urban.Extensions.AIHM_mapping import OBJECTS_STRUCTURE, fields_mapping
from Products.urban.Extensions.mappers import Migrator
import csv
import os


AIHM_FILENAME = 'urbanisme.csv'

def importAIHM(self):

    """
    minimal infos needed to reproduce a licence:
    -licence type
    -folder reference
    -subject
    -work locations
    -parcel reference
    -applicant
    -decision
    -decision date

    lets work on these one first, the rest of the data can be constructed later
    """

    """
    case 1: mapping '1 - +' the raw data of one cell have to be splitted and mapped to more than one urban field
    case 2: mapping '1 - 1' the raw data of one cell maps to one and only one urban field
    case 3: mapping '+ - 1' the raw data of several cells have to be aggregated to map one urban field
    """

    context = self.aq_inner
    db_name = 'Urbanisme.mdb'
    table_name = 'Urbanisme'
    path = './aihm_migration'
    AIHM_migrator = Migrator(context, db_name, table_name, OBJECTS_STRUCTURE, fields_mapping, path)

    aihm_file = open('temp_1', 'w')
    aihm_file.write(context.aihm_test.raw)
    aihm_file = open('temp_1', 'r')

    AIHM_migrator.migrate(aihm_file, key='CLEF')
    errors = AIHM_migrator.sorted_errors
    print errors.keys()
    import ipdb; ipdb.set_trace()
