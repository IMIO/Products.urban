# -*- coding: utf-8 -*-
#
# File: MiscDemand.py
#
# Copyright (c) 2013 by CommunesPlone
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
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
optional_fields = ['subdivisionDetails','missingParts','missingPartsDetails','folderZoneDetails','folderZone',
                   'derogationDetails','isInPCA','annoncedDelayDetails','roadType','roadCoating','roadEquipments',
                   'investigationDetails','investigationReasons','isInSubdivision', 'solicitLocationOpinionsTo',
                   'folderCategoryTownship','protectedBuilding','protectedBuildingDetails',
                   'pash','pashDetails','catchmentArea', 'catchmentAreaDetails','equipmentAndRoadRequirements','technicalRemarks',
                   'pca','SSC','sscDetails','RCU','rcuDetails','floodingLevel','floodingLevelDetails','solicitRoadOpinionsTo',
                   'areParcelsVerified', 'locationFloodingLevel', 'architects']
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='architects',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='urban/architects',
            restrict_browsing_to_startup_directory=True,
            wild_card_search=True,
            show_index_selector=True,
            label='Architects',
            label_msgid='urban_label_architects',
            i18n_domain='urban',
        ),
        required=False,
        schemata='urban_description',
        multiValued=True,
        relationship="miscdemandarchitects",
        allowed_types='Architect',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

MiscDemand_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
del MiscDemand_schema['annoncedDelay']
del MiscDemand_schema['annoncedDelayDetails']
del MiscDemand_schema['impactStudy']
del MiscDemand_schema['referenceDGATLP']
MiscDemand_schema['folderCategory'].widget.label_msgid='urban_label_category'
MiscDemand_schema['missingParts'].widget.visible=False
MiscDemand_schema['missingPartsDetails'].widget.visible=False
##/code-section after-schema

class MiscDemand(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IMiscDemand)

    meta_type = 'MiscDemand'
    _at_rename_after_creation = True

    schema = MiscDemand_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self._getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)



registerType(MiscDemand, PROJECTNAME)
# end of class MiscDemand

##code-section module-footer #fill in your manual code here
##/code-section module-footer

