# -*- coding: utf-8 -*-
from Products.urban.profiles.dataMigration.AIHM_migration.AIHM_import import importAIHM


def importLalouviereAIHM(context):
    """ Just calls the default AIHM import from La Louvière AIHM profile """
    if context.readDataFile('lalouviere_aihm_marker.txt') is None:
        return

    importAIHM(context)
