# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import registerType
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.urban.content.licence.Inspection import Inspection
from Products.urban.widget.select2widget import MultiSelect2Widget
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from zope.interface import implements

from Products.urban import interfaces
from Products.urban.config import PROJECTNAME
from Products.urban.content.licence.GenericLicence import GenericLicence

from Products.urban import UrbanMessage as _


Housing_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(CODT_BaseBuildLicence, "schema", Schema(())).copy()
    + getattr(Inspection, "schema", Schema(())).copy()
)


class Housing(Inspection, CODT_BaseBuildLicence):
    meta_type = "Housing"
    portal_type = "Housing"
    _at_rename_after_creation = True
    schema = Housing_schema

    implements(interfaces.IHousing)


registerType(Housing, PROJECTNAME)
