# -*- coding: utf-8 -*-

from Products.Archetypes.atapi import *
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

from Products.DataGridField import DataGridField, DataGridWidget, FixedColumn
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

schema = Schema((
    
    DataGridField(
        name="dimensions",
        widget=DataGridWidget(
            columns={
                "type": SelectColumn("Type", "listDimensionType"),
                "value": Column("Value"),
                "unit": SelectColumn("Unit", "listDimensionUnit"),
                "details": TextAreaColumn("Details", rows=3, cols=40),
            },
            label="dimensions",
            label_msgid="urban_label_dimensions",
            i18n_domain="urban",
        ),
        # fixed_rows="getTabsConfigRows",
        allow_insert=True,
        allow_reorder=True,
        allow_oddeven=True,
        allow_delete=True,
        schemata="urban_description",
        columns=(
            "type",
            "value",
            "unit",
            "details"
        ),
    ),
    LinesField(
            name="observation_items",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_observation_items", default="Observation_items"),
            ),
            multiValued=True,
            schemata="urban_description",
            vocabulary="listObservationItems",
        ),
   
))

EmptyBuilding_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(CODT_BaseBuildLicence, "schema", Schema(())).copy()
    + getattr(Inspection, "schema", Schema(())).copy()
    + schema.copy()
)

class EmptyBuilding(Inspection, CODT_BaseBuildLicence):
    meta_type = "EmptyBuilding"
    portal_type = "EmptyBuilding"
    _at_rename_after_creation = True
    schema = EmptyBuilding_schema

    implements(interfaces.IEmptyBuilding)

    def listDimensionType(self):
        """ Return a list of dimension types """
        voc = UrbanVocabulary("dimensiontypes", inUrbanConfig=False)
        return voc.getDisplayList(self)

    def listDimensionUnit(self):
        """ Return a list of dimension types """
        voc = UrbanVocabulary("units", inUrbanConfig=False)
        return voc.getDisplayList(self)

    def getDimension(self, type):
        """ Return the dimension of the given type """
        for dimension in self.dimensions:
            if dimension["type"] == type:
                return dimension
        return None
    
    def listObservationItems(self):
       
        vocab = (
            ("opinion", "Avis simple"),
            ("decision", "Avis conforme"),
            ("optional", "Avis facultatif"),
        )
        return DisplayList(vocab)

registerType(EmptyBuilding, PROJECTNAME)