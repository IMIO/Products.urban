# encoding: utf-8
from plone import api


def update_reference(obj, event):
    if obj.getReference() and obj.road_decree_reference:
        brains = api.content.find(
            getReference=obj.road_decree_reference,
            portal_type=[
                'CODT_BuildLicence',
                'CODT_UniqueLicence',
                'CODT_IntegratedLicence',
                'CODT_Article127',
            ],
        )
        if brains:
            referenced_obj = brains[0].getObject()
            referenced_obj.road_decree_reference = obj.getReference()
