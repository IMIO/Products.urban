# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.urban import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.config import *
from Products.urban.content.licence.EnvironmentLicence import EnvironmentLicence
from Products.urban.utils import setOptionalAttributes
from Products.urban.widget.urbanreferencewidget import UrbanBackReferenceWidget
from zope.interface import implements


##code-section module-header #fill in your manual code here
##/code-section module-header

optional_fields = [
    "roadTechnicalAdvice",
    "locationTechnicalAdvice",
    "additionalLegalConditions",
    "businessOldLocation",
    "applicationReasons",
    "validityDelay",
    "environmentTechnicalRemarks",
    "rubricsDetails",
    "referenceFT",
    "referenceFT_PM",
    "divergences",
    "divergenceDetails",
    "prorogation",
]

schema = Schema(
    (
        StringField(
            name="explosive_possession_reference",
            widget=UrbanBackReferenceWidget(
                label=_(
                    "urban_label_explosive_reference",
                    default="Explosive Possession Reference",
                ),
                portal_types=["ExplosivesPossession"],
            ),
            required=False,
            schemata="urban_description",
            default_method="getDefaultText",
            validators=("isReference",),
        ),
    )
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

setOptionalAttributes(schema, optional_fields)

Article65_schema = (
    BaseFolderSchema.copy()
    + getattr(EnvironmentLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class Article65(BaseFolder, EnvironmentLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IArticle65)

    meta_type = "Article65"
    _at_rename_after_creation = True

    schema = Article65_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def rubrics_base_query(self):
        base_query = super(Article65, self).rubrics_base_query().copy()
        base_query["extraValue"] = ["0", "1", "2", "3"]
        return base_query

    def getProcedureDelays(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        if "simple" in selection:
            return "140j"
        elif "temporary" in selection:
            return "40j"
        elif "article65" in selection:
            return "50j"
        return ""

    def showBoundLicenceIfArticle65(self, *values):
        return True


registerType(Article65, PROJECTNAME)
# end of class Article65

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema["procedureChoice"].widget.visible = False
    schema["folderCategory"].widget.visible = False
    schema["referenceFT_PM"].widget.visible = False
    schema.moveField("businessOldLocation", after="workLocations")
    schema.moveField("foldermanagers", after="businessOldLocation")
    # schema.moveField("rubrics", after="folderCategory")
    schema.moveField("description", after="additionalLegalConditions")
    return schema


finalizeSchema(Article65_schema)
##/code-section module-footer
