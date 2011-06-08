# -*- coding: utf-8 -*-
#
# File: Division.py
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
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.CMFCore.utils import getToolByName
from Products.urban.indexes import UrbanIndexes
from collective.referencedatagridfield import ReferenceDataGridField
from collective.referencedatagridfield import ReferenceDataGridWidget
from Products.urban.taskable import Taskable
from Products.urban.base import UrbanBase
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='notaryContact',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='urban/notaries',
            restrict_browsing_to_startup_directory=True,
            label='Notarycontact',
            label_msgid='urban_label_notaryContact',
            i18n_domain='urban',
        ),
        allowed_types= ('Notary',),
        relationship="notary",
        required=True,
    ),
    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        required=True,
        accessor="Title",
    ),
    StringField(
        name='reference',
        widget=StringField._properties['widget'](
            label='Reference',
            label_msgid='urban_label_reference',
            i18n_domain='urban',
        ),
        default_method="getDefaultReference",
    ),
    StringField(
        name='divisionSubject',
        widget=StringField._properties['widget'](
            label='Divisionsubject',
            label_msgid='urban_label_divisionSubject',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='comments',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            label='Comments',
            label_msgid='urban_label_comments',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
    ),
    StringField(
        name='folderZone',
        widget=SelectionWidget(
            label='Folderzone',
            label_msgid='urban_label_folderZone',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listZones',
    ),
    ReferenceDataGridField(
        name='workLocations',
        widget=ReferenceDataGridWidget(
            startup_directory='/portal_urban/streets',
            macro="street_referencedatagridwidget",
            visible={'edit' : 'visible', 'view' : 'visible'},
            label='street',
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        schemata='default',
        columns=('numero','title' ,'link' ,'uid'),
        relationship='Street',
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=True,
            allow_browse=True,
            allow_search=True,
            show_indexes=True,
            available_indexes={'Title': 'Nom'},
            startup_directory="portal_urban/division/foldermanagers",
            wild_card_search=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        allowed_types=('FolderManager',),
        multiValued=1,
        relationship='division_foldermanager',
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Division_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Division_schema['title'].searchable = True
Division_schema['title'].required = False
##/code-section after-schema

class Division(BaseFolder, UrbanIndexes,  UrbanBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IDivision)

    meta_type = 'Division'
    _at_rename_after_creation = True

    schema = Division_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('generateReference')
    def generateReference(self):
        """
        """
        pass

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
        if self.getProprietaries():
            proprietary = self.getProprietaries()[0].getName1() + " " + self.getProprietaries()[0].getName2()
        else:
            proprietary = "No proprietary defined"
        title = str(self.getReference())+ " - " +self.getDivisionSubject() + " - " + proprietary
        self.setTitle(str(title))
        self.reindexObject()

    security.declarePublic('constructPortalMessage')
    def constructPortalMessage(self):
        """
           Return a supplementary portal message
        """
        parcels = self.getParcels()
        proprietaries = self.getProprietaries()
        messages=[]
        parcel_message = "warning_add_a_parcel"
        proprietary_message = "warning_add_a_proprietary"
        if not parcels:
            #we warn the user that no parcel have been added...
            messages.append(parcel_message)
        if not proprietaries:
            #we warn the user that no applicant have been added...
            messages.append(proprietary_message)

        return messages

    security.declarePublic('getProprietaries')
    def getProprietaries(self):
        """
           Return the list of applicants for the Licence
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Proprietary':
                res.append(obj)
        return res

    security.declarePublic('getParcels')
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

    security.declarePublic('listZones')
    def listZones(self):
        """
          Return a list of zones from the config
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderzones', self))

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



registerType(Division, PROJECTNAME)
# end of class Division

##code-section module-footer #fill in your manual code here
##/code-section module-footer

