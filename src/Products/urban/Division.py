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
from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

optional_fields = []
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        required=True,
        schemata='urban_description',
        accessor="Title",
    ),
    StringField(
        name='divisionSubject',
        widget=StringField._properties['widget'](
            label='Divisionsubject',
            label_msgid='urban_label_divisionSubject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='reference',
        widget=StringField._properties['widget'](
            label='Reference',
            label_msgid='urban_label_reference',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method="getDefaultReference",
    ),
    DataGridField(
        name='workLocations',
        schemata='urban_description',
        widget=DataGridWidget(
            columns={'number' : Column("Number"), 'street' : SelectColumn("Street", UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", inUrbanConfig=False)),},
            label='Worklocations',
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
    ),
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
        required=True,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types= ('Notary',),
    ),
    LinesField(
        name='folderZone',
        widget=MultiSelectionWidget(
            size=10,
            label='Folderzone',
            label_msgid='urban_label_folderZone',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary('folderzones', inUrbanConfig=False),
    ),
    TextField(
        name='folderZoneDetails',
        allowable_content_types=('text/plain',),
        default_content_type='text/plain',
        widget=TextAreaWidget(
            label='Folderzonedetails',
            label_msgid='urban_label_folderZoneDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        schemata='urban_description',
    ),
    TextField(
        name='comments',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Comments',
            label_msgid='urban_label_comments',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_description',
        default_output_type='text/html',
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
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Division_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Division_schema['title'].searchable = True
Division_schema['title'].required = False
Division_schema['title'].widget.visible = False
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
        return ''

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
        notary = ''
        applicant = ''
        if self.getApplicants():
            applicant = unicode(self.getApplicants()[0].Title(), 'utf-8')
        else:
            applicant = translate('no_applicant_defined', 'urban', context=self.REQUEST)
        if self.getNotaryContact():
            notary = unicode(self.getNotaryContact()[0].Title(), 'utf-8')
        else:
            notary = translate('no_notary_defined', 'urban', context=self.REQUEST)

        #do not use '%s - %s - %s' type notation as it could raise UnicodeDecodeErrors...
        if applicant and notary:
            title = str(self.getReference())+ " - " + applicant + " - " + notary
        elif applicant:
            title = str(self.getReference())+ " - " + applicant
        elif notary:
            title = str(self.getReference())+ " - " + notary
        else:
            title = str(self.getReference())
        self.setTitle(title)
        self.reindexObject()

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of applicants for the Division
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Applicant':
                res.append(obj)
        return res

    security.declarePublic('getParcels')
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

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)



registerType(Division, PROJECTNAME)
# end of class Division

##code-section module-footer #fill in your manual code here
##/code-section module-footer

