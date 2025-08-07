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
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban import UrbanMessage as _
from Products.Archetypes.atapi import StringField


Housing_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(CODT_BaseBuildLicence, "schema", Schema(())).copy()
    + getattr(Inspection, "schema", Schema(())).copy()
)
Housing_schema += Schema((
    StringField(
        name="taxation",
        widget=StringField._properties["widget"](
                label=_(
                    "urban_label_taxation",
                    default="taxation",
                ),
            ),
        schemata="urban_description",
    ),
))


class Housing(Inspection, CODT_BaseBuildLicence):
    meta_type = "Housing"
    portal_type = "Housing"
    _at_rename_after_creation = True
    schema = Housing_schema

    implements(interfaces.IHousing)

    def getLastObservationEvent(self):
        return self.getLastEvent(interfaces.IObservationEvent)

    def getFirstObservationEvent(self):
        return self.getFirstEvent(interfaces.IObservationEvent)

    def getNObservationEvent(self, n):
        events = self.getAllEvent(interfaces.IObservationEvent)
        if len(events) >= n:
            return events[n - 1]
        return None


registerType(Housing, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("description", after="inspection_context")
    schema.moveField("use_bound_licence_infos", after="bound_licences")
    schema["inspection_context"].schemata = "urban_inspection"

    FIELDS_TO_DELETE = ["usage", "policeTicketReference", "referenceProsecution"]

    for field in FIELDS_TO_DELETE:
        if field in Housing_schema:
            del Housing_schema[field]
    return schema


finalize_schema(Housing_schema)
