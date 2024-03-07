# -*- coding: utf-8 -*-
#
# File: Article127.py
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
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.licence.BuildLicence import finalizeSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Article127_schema = (
    BaseFolderSchema.copy()
    + getattr(BaseBuildLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class Article127(BaseFolder, BaseBuildLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IArticle127)

    meta_type = "Article127"
    _at_rename_after_creation = True

    schema = Article127_schema

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ("ukn", "Non determiné"),
            ("opinions", "Sollicitation d'avis (instance ou service interne/externe)"),
            ("inquiry", "Enquête publique"),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v["val"] for v in values if v["selected"]]
        unknown = "ukn" in selection
        opinions = "opinions" in selection
        inquiry = "inquiry" in selection

        if unknown:
            return ""
        elif opinions and inquiry:
            return "60j"
        elif opinions and not inquiry:
            return "30j"
        else:
            return "30j"

    def getLastWalloonRegionDecisionEvent(self):
        return self.getLastEvent(interfaces.IWalloonRegionDecisionEvent)


registerType(Article127, PROJECTNAME)
# end of class Article127

##code-section module-footer #fill in your manual code here

# finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
finalizeSchema(Article127_schema)
##/code-section module-footer
