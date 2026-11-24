# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.urban import interfaces
from Products.urban.config import *
from Products.urban.content.licence.MiscDemand import finalizeSchema
from Products.urban.content.licence.MiscDemand import MiscDemand

##code-section module-header #fill in your manual code here
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForInquiry
from zope.interface import implements


optional_fields = [
    "architects",
    "patrimony",
    "archeological_site",
    "protection_zone",
    "regional_inventory_building",
    "small_popular_patrimony",
    "communal_inventory",
    "regional_inventory",
    "patrimony_analysis",
    "patrimony_architectural_complex",
    "patrimony_site",
    "patrimony_archaeological_map",
    "patrimony_project_gtoret_1ha",
    "patrimony_monument",
    "patrimony_observation",
    "classification_order_scope",
    "general_disposition",
    "noApplication",
    "shouldNumerotateBuildings",
    "habitationsBeforeLicence",
    "additionalHabitationsAsked",
    "additionalHabitationsGiven",
    "habitationsAfterLicence",
    "mayNeedLocationLicence",
]
##/code-section module-header


schema = Schema(
    (),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

MiscDemandEnvironment_schema = (
    BaseFolderSchema.copy()
    + getattr(MiscDemand, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# put the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(MiscDemandEnvironment_schema)
##/code-section after-schema


class MiscDemandEnvironment(BaseFolder, MiscDemand, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IMiscDemandEnvironment)

    meta_type = "MiscDemandEnvironment"
    _at_rename_after_creation = True

    schema = MiscDemandEnvironment_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ["urban_description", "urban_road", "urban_location"]
    ##/code-section class-header

    # Methods

    security.declarePublic("getRepresentatives")


registerType(MiscDemandEnvironment, PROJECTNAME)
# end of class MiscDemandEnvironment


##code-section module-footer
finalizeSchema(MiscDemandEnvironment_schema)
##/code-section module-footer
