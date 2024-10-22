# -*- coding: utf-8 -*-
#
# File: CODT_CommercialLicence.py
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
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.urban.content.licence.CODT_BuildLicence import finalizeSchema
from Products.urban.utils import setOptionalAttributes
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
optional_fields = ["limitedImpact", "SDC_divergence"]
##/code-section module-header

schema = Schema(
    (
        IntegerField(
            name="surfaceFoodBusiness",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_surfaceFoodBusiness",
                    default="surfaceFoodBusiness",
                ),
            ),
            schemata="urban_location",
        ),
        IntegerField(
            name="surfaceLightBusiness",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_surfaceLightBusiness",
                    default="surfaceLightBusiness",
                ),
            ),
            schemata="urban_location",
        ),
        IntegerField(
            name="surfaceHeavyBusiness",
            default=0,
            widget=IntegerField._properties["widget"](
                label=_(
                    "urban_label_surfaceHeavyBusiness",
                    default="surfaceHeavyBusiness",
                ),
            ),
            schemata="urban_location",
        ),
    ),

)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_CommercialLicence_schema = (
    BaseFolderSchema.copy()
    + getattr(CODT_BaseBuildLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class CODT_CommercialLicence(BaseFolder, CODT_BaseBuildLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_CommercialLicence)

    meta_type = "CODT_CommercialLicence"
    _at_rename_after_creation = True

    schema = CODT_CommercialLicence_schema

    def listProcedureChoices(self):
        vocab = (
            ("ukn", "Non determiné"),
            ("internal_opinions", "Sollicitation d'avis internes"),
            ("external_opinions", "Sollicitation d'avis externes"),
            ("inquiry", "Enquête publique"),
            ("big", "Superficie >= 2500m²"),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        unknown = "ukn" in selection
        big = "big" in selection
        delay = 30

        if unknown:
            return ""
        elif big:
            delay = 140
        else:
            delay = 100

        if self.prorogation:
            delay += 30

        return "{}j".format(str(delay))


registerType(CODT_CommercialLicence, PROJECTNAME)
# end of class CODT_CommercialLicence

##code-section module-footer #fill in your manual code here
finalizeSchema(CODT_CommercialLicence_schema)
del CODT_CommercialLicence_schema["usage"]
CODT_CommercialLicence_schema["referenceDGATLP"].widget.label = _(
    "urban_label_referenceDGO6"
)
##/code-section module-footer
