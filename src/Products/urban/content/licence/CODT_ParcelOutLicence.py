# -*- coding: utf-8 -*-
#
# File: CODT_ParcelOutLicence.py
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
from Products.urban import interfaces
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFCore.utils import getToolByName
from dateutil.relativedelta import relativedelta
from plone import api
##/code-section module-header

schema = Schema((

    BooleanField(
        name='isModification',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_isModification', default='Ismodification'),
        ),
        schemata='urban_description',
    ),
    ReferenceField(
        name='geometricians',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            only_for_review_states='enabled',
            allow_browse=1,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title': 'Nom'},
            startup_directory="urban/geometricians",
            wild_card_search=True,
            restrict_browsing_to_startup_directory=1,
            label=_('urban_label_geometricians', default='Geometrician(s)'),
            popup_name='contact_reference_popup',
            visible=False,
        ),
        required=False,
        schemata='urban_description',
        multiValued=1,
        relationship='parcelOutGeometricians',
        allowed_types=('Geometrician',),
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_ParcelOutLicence_schema = BaseFolderSchema.copy() + \
    getattr(CODT_BaseBuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
CODT_ParcelOutLicence_schema['title'].required = False
# CODT_ParcelOutLicence is almost the same as BuildLicence but with some fields are useless so remove them
del CODT_ParcelOutLicence_schema['pebType']
del CODT_ParcelOutLicence_schema['pebDetails']
del CODT_ParcelOutLicence_schema['pebStudy']
del CODT_ParcelOutLicence_schema['pebTechnicalAdvice']
del CODT_ParcelOutLicence_schema['usage']
##/code-section after-schema

class CODT_ParcelOutLicence(BaseFolder, CODT_BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_ParcelOutLicence)

    meta_type = 'CODT_ParcelOutLicence'
    _at_rename_after_creation = True

    schema = CODT_ParcelOutLicence_schema

    ##code-section class-header #fill in your manual code here
    archetype_name = 'CODT_ParcelOutLicence'
    schemata_order = ['urban_description', 'urban_road', 'urban_location',
                      'urban_investigation_and_advices']
    ##/code-section class-header

    # Methods

    # Manually created methods

    # Backward compatibility for pod template
    security.declarePublic('getGeometricians')
    def getGeometricians(self):
        """
        """
        return self.getRepresentativeContacts()

    security.declarePublic('generateReference')
    def generateReference(self):
        """
        """
        pass

    security.declarePublic('geometriciansBaseQuery')
    def geometriciansBaseQuery(self):
        """
          Do add some details for the base query
          Here, we want to be sure that geometricians are alphabetically sorted
        """
        portal = api.portal.get()
        rootPath = '/'.join(portal.getPhysicalPath())
        dict = {}
        dict['path'] = {'query': '%s/urban/geometricians' % rootPath, 'depth': 1}
        dict['sort_on'] = 'sortable_title'
        return dict

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastMissingPart(self):
        return self.getLastEvent(interfaces.IMissingPartEvent)

    def getLastMissingPartDeposit(self):
        return self.getLastEvent(interfaces.IMissingPartDepositEvent)

    def getLastWalloonRegionPrimo(self):
        return self.getLastEvent(interfaces.IWalloonRegionPrimoEvent)

    def getLastWalloonRegionOpinionRequest(self):
        return self.getLastEvent(interfaces.IWalloonRegionOpinionRequestEvent)

    def getFirstAcknowledgment(self):
        return self.getFirstEvent(interfaces.IAcknowledgmentEvent)

    def getLastAcknowledgment(self):
        return self.getLastEvent(interfaces.IAcknowledgmentEvent)

    def getLastCommunalCouncil(self):
        return self.getLastEvent(interfaces.ICommunalCouncilEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    def getLastWorkBeginning(self):
        return self.getLastEvent(interfaces.IWorkBeginningEvent)

    def getLastWorkEnd(self):
        return self.getLastEvent(interfaces.IWorkEndEvent)

    def getLastProrogation(self):
        return self.getLastEvent(interfaces.IProrogationEvent)

    def getAllMissingPartDeposits(self):
        return self.getAllEvents(interfaces.IMissingPartDepositEvent)

    def getProrogatedToDate(self, prorogation):
        """
          This method will calculate the 'prorogated to' date
        """
        lastTheLicenceDecisionDate = self.getLastTheLicence().getDecisionDate()
        if not lastTheLicenceDecisionDate:
            return ''
        else:
            #the prorogation gives one year more to the applicant
            tool = getToolByName(self, 'portal_urban')
            #relativedelta does not work with DateTime so use datetime
            return tool.formatDate(lastTheLicenceDecisionDate.asdatetime() + relativedelta(years=+prorogation))


registerType(CODT_ParcelOutLicence, PROJECTNAME)
# end of class CODT_ParcelOutLicence

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('isModification', after='folderCategory')
    schema.moveField('description', after='impactStudy')
    schema.moveField('representativeContacts', after='workLocations')
    return schema

finalizeSchema(CODT_ParcelOutLicence_schema)
##/code-section module-footer

