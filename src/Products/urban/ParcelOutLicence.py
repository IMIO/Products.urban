# -*- coding: utf-8 -*-
#
# File: ParcelOutLicence.py
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
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from GenericLicence import GenericLicence
from GenericLicence import GenericLicence_schema
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
import appy.pod.renderer
import os
import psycopg2
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry

optional_fields = []
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='geometricians',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title':'Nom'},
            base_query="geometriciansBaseQuery",
            wild_card_search=True,
            label='Geometricians',
            label_msgid='urban_label_geometricians',
            i18n_domain='urban',
            show_results_without_query=True
        ),
        allowed_types=('Geometrician',),
        multiValued=1,
        relationship='parcelOutGeometricians',
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

ParcelOutLicence_schema = GenericLicence_schema.copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
ParcelOutLicence_schema['title'].required = False
#put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(ParcelOutLicence_schema)
##/code-section after-schema

class ParcelOutLicence(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IParcelOutLicence)

    meta_type = 'ParcelOutLicence'
    _at_rename_after_creation = True

    schema = ParcelOutLicence_schema

    ##code-section class-header #fill in your manual code here
    archetype_name = 'ParcelOutLicence'
    schemata_order = ['urban_description', 'urban_road', 'urban_location',\
                      'urban_investigation_and_advices']
    ##/code-section class-header

    # Methods

    security.declarePublic('generateReference')
    def generateReference(self):
        """
        """
        pass

    # Manually created methods

    security.declarePublic('geometriciansBaseQuery')
    def geometriciansBaseQuery(self):
        """
          Do add some details for the base query
          Here, we want to be sure that geometricians are alphabetically sorted
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        dict = {}
        dict['path'] = {'query':'%s/urban/geometricians' % (rootPath), 'depth':1}
        dict['sort_on'] = 'sortable_title'
        return dict

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_create_script(self)

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_edit_script(self)

    security.declarePublic('mayAddOpinionRequestEvent')
    def mayAddOpinionRequestEvent(self, organisation):
        """
           This is used as TALExpression for the UrbanEventOpinionRequest
           We may add an OpinionRequest if we asked one in an inquiry on the licence
           We may add another if another inquiry defined on the licence ask for it and so on
        """
        limit = 0
        inquiries = self.getInquiries()
        for inquiry in inquiries:
            if organisation in inquiry.getSolicitOpinionsTo():
                limit += 1
        limit = limit - len(self.getOpinionRequests(organisation))
        return limit > 0

    security.declarePublic('mayAddInquiryEvent')
    def mayAddInquiryEvent(self):
        """
           This is used as TALExpression for the UrbanEventInquiry
           We may add an inquiry if we defined one on the licence
           We may add another if another is defined on the licence and so on
        """
        #first of all, we can add an InquiryEvent if an inquiry is defined on the licence at least
        inquiries = self.getInquiries()
        urbanEventInquiries = self.getUrbanEventInquiries()
        #if we have only the inquiry defined on the licence and no start date is defined
        #it means that no inquiryEvent can be added because no inquiry is defined...
        #or if every UrbanEventInquiry have already been added
        if (len(inquiries) == 1 and not self.getInvestigationStart()) or \
           (len(urbanEventInquiries) >= len(inquiries)):
            return False
        return True

    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    def getLastMissingPart(self):
        return self._getLastEvent(interfaces.IMissingPartEvent)

    def getLastMissingPartDeposit(self):
        return self._getLastEvent(interfaces.IMissingPartDepositEvent)

    def getLastWalloonRegionPrimo(self):
        return self._getLastEvent(interfaces.IWalloonRegionPrimoEvent)

    def getLastWalloonRegionOpinionRequest(self):
        return self._getLastEvent(interfaces.IWalloonRegionOpinionRequestEvent)

    def getLastAcknowledgment(self):
        return self._getLastEvent(interfaces.IAcknowledgmentEvent)

    def getLastInquiry(self):
        return self._getLastEvent(interfaces.IInquiryEvent)

    def getLastCommunalCouncil(self):
        return self._getLastEvent(interfaces.ICommunalCouncilEvent)

    def getLastCollegeReport(self):
        return self._getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)

    def getLastWorkBeginning(self):
        return self._getLastEvent(interfaces.IWorkBeginningEvent)

    def getLastProrogation(self):
        return self._getLastEvent(interfaces.IProrogationEvent)

    def getLastOpinionRequest(self):
        return self._getLastEvent(interfaces.IOpinionRequestEvent)

    def getAllMissingPartDeposits(self):
        return self._getAllEvents(interfaces.IMissingPartDepositEvent)

    def getAllTechnicalServiceOpinionRequests(self):
        return self._getAllEvents(interfaces.ITechnicalServiceOpinionRequestEvent)

    def getAllTechnicalServiceOpinionRequestsNoDup(self):
        allOpinions = self.getAllTechnicalServiceOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor]=opinion
        return allOpinionsNoDup.values()

    def getAllOpinionRequests(self, organisation=""):
        if organisation == "":
            return self._getAllEvents(interfaces.IOpinionRequestEvent)
        catalog = getToolByName(self, 'portal_catalog')
        currentPath = '/'.join(self.getPhysicalPath())
        query = {'path': {'query': currentPath,
                          'depth': 1},
                 'meta_type': ['UrbanEvent', 'UrbanEventInquiry'],
                 'sort_on': 'getObjPositionInParent',
                 'id' : organisation.lower()}
        return [brain.getObject() for brain in catalog(**query)]

    def getAllOpinionRequestsNoDup(self):
        allOpinions = self.getAllOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor]=opinion
        return allOpinionsNoDup.values()

    def getAllInquiries(self):
        return self._getAllEvents(interfaces.IInquiryEvent)

    def getAllClaimsTexts(self):
        claimsTexts = []
        for inquiry in self.getAllInquiries():
            text = inquiry.getClaimsText()
            if text is not "":
                claimsTexts.append(text)
        return claimsTexts


registerType(ParcelOutLicence, PROJECTNAME)
# end of class ParcelOutLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

