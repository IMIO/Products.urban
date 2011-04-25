# -*- coding: utf-8 -*-
#
# File: Declaration.py
#
# Copyright (c) 2011 by CommunesPlone
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFPlone.i18nl10n import utranslate
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.utils import getToolByName
from Products.urban.indexes import UrbanIndexes
from Products.urban.MultipleStreets import MultipleStreets
from Products.urban.base import UrbanBase
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        required= True,
        accessor="Title",
    ),
    StringField(
        name='reference',
        widget=StringField._properties['widget'](
            size=30,
            label='Reference',
            label_msgid='urban_label_reference',
            i18n_domain='urban',
        ),
        default_method="getDefaultReference",
    ),
    StringField(
        name='declarationSubject',
        widget=StringField._properties['widget'](
            label='Declarationsubject',
            label_msgid='urban_label_declarationSubject',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='description',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Description',
            label_msgid='urban_label_description',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
    ),
    StringField(
        name='article',
        widget=SelectionWidget(
            label='Article',
            label_msgid='urban_label_article',
            i18n_domain='urban',
        ),
        vocabulary='listArticles',
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_browse=True,
            allow_search=True,
            show_indexes=True,
            available_indexes={'Title':'Nom'},
            startup_directory="portal_urban/declaration/foldermanagers",
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
            popup_name='popup-urban',
            wild_card_search=True
        ),
        allowed_types=('FolderManager',),
        multiValued=1,
        relationship='declarationFolderManagers',
        required= True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Declaration_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Declaration_schema['title'].required = False
Declaration_schema['title'].searchable = True
##/code-section after-schema

class Declaration(BaseFolder, UrbanIndexes,  MultipleStreets,  UrbanBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IDeclaration)

    meta_type = 'Declaration'
    _at_rename_after_creation = True

    schema = Declaration_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('generateReference')
    def generateReference(self):
        """
        """
        pass

    security.declarePublic('listArticles')
    def listArticles(self):
        """
          Returns the list of available articles
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('articles', self))

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
        urbanTool = getToolByName(self,'portal_urban')
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
        self.updateWorkLocation()

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()
        self.updateWorkLocation()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        if self.getApplicants():
            applicant = self.getApplicants()[0].getName1() + " " + self.getApplicants()[0].getName2()
        else:
            applicant = "No applicant defined"
        title = str(self.getReference())+ " - " +self.getDeclarationSubject() + " - " + applicant
        self.setTitle(str(title))
        self.reindexObject()

    security.declarePublic('constructPortalMessage')
    def constructPortalMessage(self):
        """
           Return a supplementary portal message
        """
        parcels = self.getParcels()
        applicants = self.getApplicants()
        messages=[]
        parcel_message = "warning_add_a_parcel"
        applicant_message = "warning_add_an_applicant"
        if not parcels:
            #we warn the user that no parcel have been added...
            messages.append(parcel_message)
        if not applicants:
            #we warn the user that no applicant have been added...
            messages.append(applicant_message)

        return messages

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of applicants for the Licence
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Applicant':
                res.append(obj)
        return res

    def getParcels(self):
        """
           Return the list of parcels (portionOut) for the Licence
        """
        return self.objectValues('PortionOut')

    security.declarePublic('getUrbanEvents')
    def getUrbanEvents(self):
        """
          Return contained UrbanEvents...
        """
        return self.objectValues("UrbanEvent")

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

    security.declarePublic('getWorkLocationStreet')
    def getWorkLocationStreet(self):
        """
          Return the street name
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().getStreetName()
        return ''

    security.declarePublic('getWorkLocationZipCode')
    def getWorkLocationZipCode(self):
        """
          Return the zip code
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().aq_inner.aq_parent.getZipCode()
        return ''

    security.declarePublic('getWorkLocationCity')
    def getWorkLocationCity(self):
        """
          Return the city of the primary WorkLocation
          We take the Street defined in the WorkLocation and the
          parent of this street is the City
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().aq_inner.aq_parent.Title()
        return ''



registerType(Declaration, PROJECTNAME)
# end of class Declaration

##code-section module-footer #fill in your manual code here
##/code-section module-footer

