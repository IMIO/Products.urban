# -*- coding: utf-8 -*-
#
# File: Declaration.py
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
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

optional_fields = ["linkedCU2s"]
##/code-section module-header

schema = Schema(
    (
        LinesField(
            name="article",
            widget=MultiSelect2Widget(
                label=_("urban_label_article", default="Article"),
            ),
            schemata="urban_description",
            multiValued=1,
            vocabulary=UrbanVocabulary("articles", with_empty_value=False),
            default_method="getDefaultValue",
        ),
        ReferenceField(
            name="linkedCU2s",
            widget=ReferenceBrowserWidget(
                allow_browse=0,
                base_query="CU2BaseQuery",
                show_results_without_query=True,
                label=_("urban_label_linkedCU2s", default="Linkedcu2s"),
            ),
            allowed_types=("UrbanCertificateTwo",),
            schemata="urban_location",
            multiValued=1,
            relationship="parcelCU2s",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Declaration_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
Declaration_schema["title"].required = False
##/code-section after-schema


class Declaration(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IDeclaration)

    meta_type = "Declaration"
    _at_rename_after_creation = True

    schema = Declaration_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ["urban_description", "urban_road", "urban_location"]
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("getAdditionalLayers")

    def getAdditionalLayers(self):
        """
        Return a list of additional layers that will be used
        when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues("Layer")
        except AttributeError:
            return None

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    security.declarePublic("getReceivability")

    def getReceivability(self):
        """
        Returns a string specifying if self is receivable or not
        """
        # get the last college report and check the decision
        lastCollegeReport = self.getLastCollegeReport()
        if lastCollegeReport:
            decisionTerm = lastCollegeReport.getDecision(theObject=True)
            # we use the extra value field on the term where we store
            # the 'receivable' text
            if decisionTerm:
                if decisionTerm.getExtraValue():
                    return decisionTerm.getExtraValue()
                return (
                    "[No ExtraValue defined for the decision term '%s']"
                    % decisionTerm.Title()
                )
        return ""

    security.declarePublic("CU2BaseQuery")

    def CU2BaseQuery(self):
        """ """
        catalog = getToolByName(self, "portal_catalog")
        portal = getToolByName(self, "portal_url").getPortalObject()
        rootPath = "/".join(portal.getPhysicalPath())
        dict = {}
        dict["path"] = {"query": "%s/urban/urbancertificatetwos" % (rootPath)}
        brain = catalog(id=self.id)[0]
        dict["parcelInfosIndex"] = brain.parcelInfosIndex
        return dict


registerType(Declaration, PROJECTNAME)
# end of class Declaration

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("description", after="article")
    schema.moveField("foldermanagers", after="workLocations")
    return schema


finalizeSchema(Declaration_schema)
##/code-section module-footer
