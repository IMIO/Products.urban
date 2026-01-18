# -*- coding: utf-8 -*-

from plone import api


SUBDIVIDER_NAME_PLACEHOLDER = "n/a"

def fix_subdividerName_field():
    parcellings = api.content.find(portal_type="Parcelling")
    for parcelling in parcellings:
        parcelling_obj = parcelling.getObject()
        parcelling_obj.subdividerName = SUBDIVIDER_NAME_PLACEHOLDER
