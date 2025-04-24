# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import *
from Products.urban.content.licence.Inspection import Inspection
from zope.interface import implements

from Products.urban import interfaces
from Products.urban.config import PROJECTNAME
from Products.urban.content.licence.GenericLicence import GenericLicence

schema = Schema((

))

EmptyBuilding_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(Inspection, "schema", Schema(())).copy()
    # + schema.copy()
)

class EmptyBuilding(Inspection):
    meta_type = "EmptyBuilding"
    portal_type = "EmptyBuilding"
    _at_rename_after_creation = True
    schema = EmptyBuilding_schema

    implements(interfaces.IEmptyBuilding)

registerType(EmptyBuilding, PROJECTNAME)