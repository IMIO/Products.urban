# -*- coding: utf-8 -*-
from Products.urban.profiles.dataMigration.AIHM_migration.AIHM_import import importAIHM


def importMonsAIHM(context):
    """ Just calls the default AIHM import from Mons AIHM profile """
    if context.readDataFile('mons_aihm_marker.txt') is None:
        return

    importAIHM(context)
