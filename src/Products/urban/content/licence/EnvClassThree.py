# -*- coding: utf-8 -*-
#
# File: EnvClassThree.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.EnvironmentBase import EnvironmentBase
from Products.urban.utils import (
    setOptionalAttributes,
    setSchemataForCODT_UniqueLicenceInquiry,
)
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

slave_fields_additionalconditions = (
    {
        "name": "additionalConditions",
        "action": "show",
        "hide_values": (True,),
    },
)

optional_fields = [
    "depositType",
    "submissionNumber",
    "inadmissibilityReasons",
    "inadmissibilityreasonsDetails",
    "annoncedDelay",
    "annoncedDelayDetails",
]

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="depositType",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_depositType", default="Deposittype"),
            ),
            vocabulary=UrbanVocabulary("deposittype", inUrbanConfig=True),
            default_method="getDefaultValue",
            schemata="urban_description",
        ),
        StringField(
            name="submissionNumber",
            widget=StringField._properties["widget"](
                label=_("urban_label_submissionNumber", default="Submissionnumber"),
            ),
            schemata="urban_description",
        ),
        BooleanField(
            name="hasAdditionalConditions",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_additionalconditions,
                label=_(
                    "urban_label_hasAdditionalConditions",
                    default="Hasadditionalconditions",
                ),
            ),
            schemata="urban_description",
        ),
        FileField(
            name="additionalConditions",
            schemata="urban_description",
            widget=FileField._properties["widget"](
                label=_(
                    "urban_label_additionalConditions", default="Additionalconditions"
                ),
            ),
            storage=AnnotationStorage(),
        ),
        LinesField(
            name="inadmissibilityReasons",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_(
                    "urban_label_inadmissibilityReasons",
                    default="Inadmissibilityreasons",
                ),
            ),
            schemata="urban_description",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                path="inadmissibilityreasons", sort_on="getObjPositionInParent"
            ),
            default_method="getDefaultValue",
        ),
        TextField(
            name="inadmissibilityreasonsDetails",
            widget=RichWidget(
                label=_(
                    "urban_label_inadmissibilityreasonsDetails",
                    default="Inadmissibilityreasonsdetails",
                ),
            ),
            default_content_type="text/html",
            allowable_content_types=("text/html",),
            schemata="urban_description",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassThree_schema = (
    BaseFolderSchema.copy()
    + getattr(EnvironmentBase, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# must be done after schema extension to be sure to make fields
# of parents schema optional
setOptionalAttributes(EnvClassThree_schema, optional_fields)
##/code-section after-schema


class EnvClassThree(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassThree)

    meta_type = "EnvClassThree"
    _at_rename_after_creation = True

    schema = EnvClassThree_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getValidityDelay(self):
        return 10

    def rubrics_base_query(self):
        base_query = super(EnvClassThree, self).rubrics_base_query().copy()
        base_query["extraValue"] = ["0", "3"]
        return base_query

    def getProcedureDelays(self, *values):
        return "15j"


registerType(EnvClassThree, PROJECTNAME)
# end of class EnvClassThree

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("businessOldLocation", after="workLocations")
    schema.moveField("foldermanagers", after="businessOldLocation")
    schema.moveField("depositType", after="folderCategory")
    schema.moveField("submissionNumber", after="depositType")
    schema.moveField("rubrics", after="submissionNumber")
    schema.moveField("description", after="additionalLegalConditions")
    schema.moveField("missingParts", after="inadmissibilityReasons")
    schema.moveField("missingPartsDetails", after="missingParts")
    schema["validityDelay"].default = 10
    return schema


finalizeSchema(EnvClassThree_schema)
##/code-section module-footer
