# -*- coding: utf-8 -*-
#
# File: EnvironmentalDeclaration.py
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
from zope.i18n import translate as _
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
        name='reference',
        widget=StringField._properties['widget'](
            size=30,
            label='Reference',
            label_msgid='urban_label_reference',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method="getDefaultReference",
    ),
    StringField(
        name='finality',
        widget=StringField._properties['widget'](
            size=60,
            label='Finality',
            label_msgid='urban_label_finality',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    TextField(
        name='subjects',
        widget=TextAreaWidget(
            description='Please enter one subject by line with the following format : xx.xx.xx.xx',
            description_msgid="envionmentaldeclaration_subjects_descr",
            label='Subjects',
            label_msgid='urban_label_subjects',
            i18n_domain='urban',
        ),
        schemata='urban_description',
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
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            available_indexes= {'Title':'Nom'},
            startup_directory="portal_urban/environmentaldeclaration/foldermanagers",
            wild_card_search=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        required=False,
        schemata='urban_description',
        multiValued=1,
        relationship='environmentalDeclarationFolderManagers',
        allowed_types=('FolderManager',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentalDeclaration_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentalDeclaration_schema['title'].required = False
EnvironmentalDeclaration_schema['title'].visible = False
##/code-section after-schema

class EnvironmentalDeclaration(BaseFolder, UrbanIndexes,  UrbanBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvironmentalDeclaration)

    meta_type = 'EnvironmentalDeclaration'
    _at_rename_after_creation = True

    schema = EnvironmentalDeclaration_schema

    ##code-section class-header #fill in your manual code here
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
        #update the last reference in the configuration
        tool.incrementNumerotation(self)
        #there is no need for other users than Managers to List folder contents
        #set this permission here if we use the simple_publication_workflow...
        self.manage_permission('List folder contents', ['Manager', ], acquire=0)
        self.updateTitle()

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to clearly identify the certificate
           Display the reference, the applicant and the notary
        """
        if self.getApplicants():
            applicant = self.getApplicants()[0].getName1() + " " + self.getApplicants()[0].getName2()
        else:
            applicant = _('no_applicant_defined', 'urban', context=self.REQUEST)
        title = self.getReference() + " - " + applicant + " - " + self.getFinality()
        self.setTitle(title)
        self.reindexObject()

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



registerType(EnvironmentalDeclaration, PROJECTNAME)
# end of class EnvironmentalDeclaration

##code-section module-footer #fill in your manual code here
##/code-section module-footer

