# -*- coding: utf-8 -*-
#
# File: Declaration.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

optional_fields = []
##/code-section module-header

schema = Schema((

    StringField(
        name='article',
        widget=SelectionWidget(
            label='Article',
            label_msgid='urban_label_article',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('articles', with_empty_value=True),
        default_method='getDefaultValue',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Declaration_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Declaration_schema['title'].required = False
Declaration_schema['title'].widget.visible = False
#remove the annoncedDelays for UrbanCertificates
del Declaration_schema['annoncedDelay']
del Declaration_schema['annoncedDelayDetails']
#remove the impactStudy field for UrbanCertificates
del Declaration_schema['impactStudy']
#hide the solicit opinions to fields for UrbanCertificateOne
Declaration_schema['solicitRoadOpinionsTo'].widget.visible=False
Declaration_schema['solicitLocationOpinionsTo'].widget.visible=False
#no need for missing parts as if it is not complete, it is decided not receivable
Declaration_schema['missingParts'].widget.visible=False
Declaration_schema['missingPartsDetails'].widget.visible=False
##/code-section after-schema

class Declaration(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IDeclaration)

    meta_type = 'Declaration'
    _at_rename_after_creation = True

    schema = Declaration_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_create_script(self)

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_edit_script(self)

    security.declarePublic('getAdditionalLayers')
    def getAdditionalLayers(self):
        """
          Return a list of additional layers that will be used
          when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues('Layer')
        except AttributeError:
            return None

    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self._getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)

    security.declarePublic('getArticle')
    def getArticle(self, theObject=False):
        """
          Returns the article value or the UrbanVocabularyTerm if theObject=True
        """
        res = self.getField('article').get(self)
        if res and theObject:
            tool = getToolByName(self, 'portal_urban')
            urbanConfig = tool.getUrbanConfig(self)
            res = getattr(urbanConfig.articles, res)
        return res

    security.declarePublic('getReceivability')
    def getReceivability(self):
        """
          Returns a string specifying if self is receivable or not
        """
        #get the last college report and check the decision
        lastCollegeReport = self.getLastCollegeReport()
        if lastCollegeReport:
            decisionTerm = lastCollegeReport.getDecision(theObject=True)
            #we use the extra value field on the term where we store
            #the 'receivable' text
            if decisionTerm:
                if decisionTerm.getExtraValue():
                    return decisionTerm.getExtraValue()
                return "[No ExtraValue defined for the decision term '%s']" % decisionTerm.Title()
        return ''



registerType(Declaration, PROJECTNAME)
# end of class Declaration

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('description', after='article')
    schema.moveField('foldermanagers', after='workLocations')
    return schema

finalizeSchema(Declaration_schema)
##/code-section module-footer

