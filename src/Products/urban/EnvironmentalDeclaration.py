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
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.urban.indexes import UrbanIndexes
from Products.urban.MultipleStreets import MultipleStreets
from Products.urban.taskable import Taskable
from Products.urban.base import UrbanBase
from zope.i18n import translate as _
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
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
            popup_name='popup',
            wild_card_search=True
        ),
        allowed_types=('FolderManager',),
        multiValued=1,
        relationship='environmentalDeclarationFolderManagers',
        required=False,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvironmentalDeclaration_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentalDeclaration_schema['title'].required = False
EnvironmentalDeclaration_schema['title'].visible = False
##/code-section after-schema

class EnvironmentalDeclaration(BaseFolder, UrbanIndexes,  MultipleStreets,  Taskable,  UrbanBase, BrowserDefaultMixin):
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
        self.updateWorkLocation()

    security.declarePublic('at_post_edit_script')
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



registerType(EnvironmentalDeclaration, PROJECTNAME)
# end of class EnvironmentalDeclaration

##code-section module-footer #fill in your manual code here
##/code-section module-footer

