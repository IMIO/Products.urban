# -*- coding: utf-8 -*-
#
# File: Division.py
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
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes

optional_fields = []
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
        required=True,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types= ('Notary',),
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
        required=True,
        schemata='urban_description',
        multiValued=1,
        relationship='division_foldermanager',
        allowed_types=('FolderManager',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Division_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Division_schema['title'].searchable = True
Division_schema['title'].required = False
Division_schema['title'].widget.visible = False
#remove the annoncedDelays for Divisons
del Division_schema['annoncedDelay']
del Division_schema['annoncedDelayDetails']
#remove the impactStudy field for Divisons
del Division_schema['impactStudy']
#hide the solicit opinions to fields for Divisons
Division_schema['solicitRoadOpinionsTo'].widget.visible=False
Division_schema['solicitLocationOpinionsTo'].widget.visible=False
#no need for missing parts as if it is not complete, it is decided not receivable
Division_schema['missingParts'].widget.visible=False
Division_schema['missingPartsDetails'].widget.visible=False
##/code-section after-schema

class Division(BaseFolder, UrbanIndexes,  UrbanBase, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IDivision)

    meta_type = 'Division'
    _at_rename_after_creation = True

    schema = Division_schema

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

    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self._getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)



registerType(Division, PROJECTNAME)
# end of class Division

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('description', after='notaryContact')
    schema.moveField('foldermanagers', after='workLocations')
    return schema

finalizeSchema(Division_schema)
##/code-section module-footer

