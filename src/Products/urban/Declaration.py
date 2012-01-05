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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
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
        vocabulary=UrbanVocabulary('articles'),
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_browse=1,
            allow_search=1,
            show_indexes=1,
            available_indexes={'Title':'Nom'},
            startup_directory="portal_urban/declaration/foldermanagers",
            wild_card_search=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        required= True,
        schemata='urban_description',
        multiValued=1,
        relationship='declarationFolderManagers',
        allowed_types=('FolderManager',),
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

##/code-section after-schema

class Declaration(BaseFolder, UrbanIndexes,  UrbanBase, GenericLicence, BrowserDefaultMixin):
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

    security.declarePublic('getDefaultReference')
    def getDefaultReference(self):
        """
          Returns the reference for the new element
        """
        tool = getToolByName(self, 'portal_urban')
        return tool.generateReference(self)

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        tool = getToolByName(self,'portal_urban')
        tool.incrementNumerotation(self)
        #create a folder ADDITIONAL_LAYERS_FOLDER that will contain additional layers
        #used while creating the mapfile
        self.invokeFactory("Folder", id=ADDITIONAL_LAYERS_FOLDER, title=ADDITIONAL_LAYERS_FOLDER)
        additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
        #constrain the content of this folder to layers only...
        additionalLayersFolder.setConstrainTypesMode(1)
        additionalLayersFolder.setLocallyAllowedTypes(['Layer'])
        additionalLayersFolder.setImmediatelyAddableTypes(['Layer'])
        additionalLayersFolder.reindexObject()
        #there is no need for other users than Managers to List folder contents
        #set this permission here if we use the simple_publication_workflow...
        self.manage_permission('List folder contents', ['Manager', ], acquire=0)
        self.updateTitle()

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        if self.getApplicants():
            applicant = self.getApplicants()[0].getName1() + " " + self.getApplicants()[0].getName2()
        else:
            applicant = "No applicant defined"
        title = str(self.getReference())+ " - " +self.getLicenceSubject() + " - " + applicant
        self.setTitle(str(title))
        self.reindexObject()

    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')

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



registerType(Declaration, PROJECTNAME)
# end of class Declaration

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('description', after='foldermanagers')
    return schema

finalizeSchema(Declaration_schema)
##/code-section module-footer

