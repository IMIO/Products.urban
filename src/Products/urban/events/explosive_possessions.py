# -*- coding: utf-8 -*-

from plone import api


def update_reference(obj, event):
    if obj.getReference() and obj.pe_reference:
        brains = api.content.find(
            getReference=obj.pe_reference,
            portal_type=['EnvClassOne', 'EnvClassTwo'],
        )
        if brains:
            referenced_obj = brains[0].getObject()
            referenced_obj.explosive_possession_reference = obj.getReference()
