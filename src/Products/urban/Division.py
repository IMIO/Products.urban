# -*- coding: utf-8 -*-
#
# File: Division.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
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
from zope.i18n import translate
from Products.urban.utils import setOptionalAttributes
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

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

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Division_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Division_schema['title'].required = False
##/code-section after-schema

class Division(BaseFolder, GenericLicence, BrowserDefaultMixin):
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

    security.declarePublic('getRepresentatives')
    def getRepresentatives(self):
        """
        """
        return self.getNotaryContact()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        notary = ''
        proprietary = ''
        proprietaries = self.getProprietaries()
        if proprietaries:
            proprietary = proprietaries[0].Title()
        else:
            proprietary = translate('no_proprietary_defined', 'urban', context=self.REQUEST).encode('utf8')
        if self.getNotaryContact():
            notary = self.getNotaryContact()[0].Title()
        else:
            notary = translate('no_notary_defined', 'urban', context=self.REQUEST).encode('utf8')

        if proprietary and notary:
            title = "%s - %s - %s" % (self.getReference(), proprietary, notary)
        elif proprietary:
            title = "%s - %s" % (self.getReference(), proprietary)
        elif notary:
            title = "%s - %s" % (self.getReference(), notary)
        else:
            title = self.getReference()
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    def getLastDeposit(self, use_catalog=True):
        return self._getLastEvent(interfaces.IDepositEvent, use_catalog)

    def getLastCollegeReport(self, use_catalog=True):
        return self._getLastEvent(interfaces.ICollegeReportEvent, use_catalog)

    def getLastTheLicence(self, use_catalog=True):
        return self._getLastEvent(interfaces.ITheLicenceEvent, use_catalog)



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

