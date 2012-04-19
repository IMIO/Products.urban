# -*- coding: utf-8 -*-
#
# File: UrbanCertificateBase.py
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

from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.LinesColumn import LinesColumn
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

optional_fields = ['customSpecificFeatures', 'townshipSpecificFeatures', 'opinionsToAskIfWorks', ]
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='notaryContact',
        widget=ReferenceBrowserWidget(
            allow_search=1,
            allow_browse=1,
            force_close_on_insert=1,
            startup_directory='urban/notaries',
            restrict_browsing_to_startup_directory=1,
            popup_name='popup',
            wild_card_search=True,
            label='Notarycontact',
            label_msgid='urban_label_notaryContact',
            i18n_domain='urban',
        ),
        required=False,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types= ('Notary',),
    ),
    LinesField(
        name='specificFeatures',
        widget=MultiSelectionWidget(
            description_msgid="certificateone_specificfeatures_descr",
            description='Select the specific features from the left box and drop them in the right box to select them',
            format='checkbox',
            label='Specificfeatures',
            label_msgid='urban_label_specificFeatures',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary('specificfeatures'),
        enforceVocabulary=True,
    ),
    DataGridField(
        name='customSpecificFeatures',
        widget=DataGridWidget(
            columns={'feature' : LinesColumn("Feature")},
            label='Customspecificfeatures',
            label_msgid='urban_label_customSpecificFeatures',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('feature',),
    ),
    LinesField(
        name='townshipSpecificFeatures',
        widget=MultiSelectionWidget(
            description_msgid="certificateone_townshipspecificfeatures_descr",
            description='Select the specific features from the left box and drop them in the right box to select them',
            format='checkbox',
            label='Townshipspecificfeatures',
            label_msgid='urban_label_townshipSpecificFeatures',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary('townshipspecificfeatures'),
        enforceVocabulary=True,
    ),
    LinesField(
        name='opinionsToAskIfWorks',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Opinionstoaskifworks',
            label_msgid='urban_label_opinionsToAskIfWorks',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('opinionstoaskifworks', vocType="OrganisationTerm"),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanCertificateBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanCertificateBase_schema['title'].required = False
UrbanCertificateBase_schema['title'].widget.visible = False
#remove the annoncedDelays for UrbanCertificates
del UrbanCertificateBase_schema['annoncedDelay']
del UrbanCertificateBase_schema['annoncedDelayDetails']
#remove the impactStudy field for UrbanCertificates
del UrbanCertificateBase_schema['impactStudy']
#hide the solicit opinions to fields for UrbanCertificateOne
UrbanCertificateBase_schema['solicitRoadOpinionsTo'].widget.visible=False
UrbanCertificateBase_schema['solicitLocationOpinionsTo'].widget.visible=False
##/code-section after-schema

class UrbanCertificateBase(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanCertificateBase)

    meta_type = 'UrbanCertificateBase'
    _at_rename_after_creation = True

    schema = UrbanCertificateBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getWhoSubmitted')
    def getWhoSubmitted(self):
        """
          This method will find who submitted the request
        """
        #either the notary for an applicant, either the applicant, either a notary
        applicants = self.getApplicants()
        notaries = self.getNotaryContact()
        if notaries and applicants:
            #a notary submitted the request for the applicant
            return 'both'
        elif applicants:
            #an applicant submitted the request, without a notary
            return 'applicant'
        elif notaries:
            #a notary alone submitted the request (rare...)
            return 'notary'
        else:
            return ''

    security.declarePublic('getRealSubmitters')
    def getRealSubmitters(self, signaletic=False):
        """
          This method will return the real submitters depending on getWhoSubmitted
          We could return the objects or their signaletic
        """
        who = self.getWhoSubmitted()
        if who == 'both' or who == 'notary':
            if signaletic:
                return self.getNotariesSignaletic()
            else:
                return self.getNotaryContact()
        elif who == 'applicant':
            if signaletic:
                return self.getApplicantsSignaletic()
            else:
                return self.getApplicants()
        else:
            return ''

    security.declarePublic('getSelectableFolderManagersBaseQuery')
    def getSelectableFolderManagersBaseQuery(self):
        """
          Return the folder were are stored folder managers
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        folderManagersPath = '/portal_urban/%s/foldermanagers' % self.getPortalTypeName().lower()
        dict = {}
        dict['path'] = {'query':'%s%s' % (rootPath, folderManagersPath)}
        dict['sort_on'] = 'sortable_title'
        return dict

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
        self.reindexObject(idxs=('Title', 'applicantInfosIndex',))

    security.declarePublic('getOpinionsToAskForWorks')
    def getOpinionsToAskForWorks(self, theObjects=False):
        """
          Returns the opinionsToAskIfWorks values or the OrganisationTerms if theObject=True
        """
        res = self.getField('opinionsToAskIfWorks').get(self)
        if res and theObjects:
            tool = getToolByName(self, 'portal_urban')
            urbanConfig = tool.getUrbanConfig(self)
            opinionsToAskIfWorksConfigFolder = urbanConfig.opinionstoaskifworks
            elts = res
            res = []
            for elt in elts:
                res.append(getattr(opinionsToAskIfWorksConfigFolder, elt))
        return res

    security.declarePublic('getLastDeposit')
    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    security.declarePublic('getLastTheLicence')
    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)

    security.declarePublic('getCustomSpecificFeaturesAsList')
    def getCustomSpecificFeaturesAsList(self):
        """
          To display custom specific features easily, get it as a list of features
        """
        res = []
        for csf in self.getCustomSpecificFeatures():
            #in some case, DataGridField add an empty dict...
            if csf.has_key('feature') and csf['feature']:
                res.append(csf['feature'])
        return res

    security.declarePublic('getSpecificFeaturesForTemplate')
    def getSpecificFeaturesForTemplate(self, township=False):
        """
          Return formatted specific features (striked or not)
          Helper method used in templates
        """
        tool = getToolByName(self, 'portal_urban')
        portal_catalog = getToolByName(self, 'portal_catalog')
        config = tool.getUrbanConfig(self, urbanConfigId=self.portal_type.lower())
        if township:
            specificFeaturesPath = '/'.join(config.townshipspecificfeatures.getPhysicalPath())
        else:
            specificFeaturesPath = '/'.join(config.specificfeatures.getPhysicalPath())
        params = {
                  'path': specificFeaturesPath,
                  'review_state': 'enabled',
        }
        res=[]
        #get every enabled specific features from the config
        enabledSpecificFeatures = portal_catalog(**params)
        if township:
            specificFeatures = self.getTownshipSpecificFeatures()
        else:
            specificFeatures = self.getSpecificFeatures()
        for esf in enabledSpecificFeatures:
            obj = esf.getObject()
            if esf.id in specificFeatures:
                #render the expressions
                res.append(obj.getRenderedDescription(self))
            else:
                #replace the expressions by a null value, aka "..."
                res.append(tool.decorateHTML('striked', obj.getRenderedDescription(self, renderToNull=True)))

        #add customSpecificFeatures
        if not township:
            for csf in self.getCustomSpecificFeatures():
                res.append("<p>%s</p>" % "<br />".join(csf['feature']))
        return res

    security.declarePublic('getProprietaries')
    def getProprietaries(self):
        """
           Return the list of proprietaries for the certificate
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Proprietary':
                res.append(obj)
        return res

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of proprietaries for the certificate
        """
        return self.getProprietaries()

    security.declarePublic('getLicencesOfTheParcels')
    def getLicencesOfTheParcels(self, licence_type=''):
        history = []
        licence_uids = set([])
        for parcel in self.getParcels():
            for brain in parcel.getRelatedLicences(licence_type=licence_type):
                if brain.UID not in licence_uids:
                    history.extend(parcel.getRelatedLicences(licence_type=licence_type))
                    licence_uids.add(brain.UID)
        return history

    security.declarePublic('getBuildlicencesOfTheParcels')
    def getBuildlicencesOfTheParcels(self):
        limit_date = DateTime('1977/01/01')
        return self.getLicenceOfTheParcels('BuildLicence', limit_date)

    security.declarePublic('getUrbanCertificateOneOfTheParcels')
    def getUrbanCertificateOneOfTheParcels(self):
        #cu1 cannot be older than 2 years
        limit_date = self.getLastTheLicence().getEventDate() - 731
        return self.getLicenceOfTheParcels('UrbanCertificateOne', limit_date)

    security.declarePublic('getUrbanCertificateTwoOfTheParcels')
    def getUrbanCertificateTwoOfTheParcels(self):
        #cu2 cannot be older than 2 years
        limit_date = self.getLastTheLicence().getEventDate() - 731
        return self.getLicenceOfTheParcels('UrbanCertificateTwo', limit_date)

    security.declarePublic('getParceloutlicenceOfTheParcels')
    def getParceloutlicenceOfTheParcels(self):
        limit_date = DateTime('1977/01/01')
        return self.getLicenceOfTheParcels('ParcelOutLicence', limit_date)

    def getLicenceOfTheParcels(self, licence_type, limit_date):
        licences = []
        for brain in self.getLicencesOfTheParcels(licence_type=licence_type):
            licence = brain.getObject()
            delivered = licence.getLastTheLicence()
            if delivered and delivered.getDecisionDate() > limit_date:
                if delivered.getDecision() == 'favorable':
                    licences.append(licence)
                elif licence_type in ['UrbanCertificateTwo', 'UrbanCertificateOne']:
                    licences.append(licence)
        return licences

    security.declarePublic('hasEventNamed')
    def hasEventNamed(self, title):
        """
        Tells if the licence contains an urbanEvent named 'title'
        """
        catalog = getToolByName(self, 'portal_catalog')
        if catalog(portal_type='UrbanEvent', path=self.absolute_url_path(), Title=title):
            return True
        return False

    security.declarePublic('hasNoEventNamed')
    def hasNoEventNamed(self, title):
        """
        Tells if the licence does not contain any urbanEvent named 'title'
        """
        return not self.hasEventNamed(title)

registerType(UrbanCertificateBase, PROJECTNAME)
# end of class UrbanCertificateBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('referenceDGATLP', after='reference')
    schema.moveField('notaryContact', after='workLocations')
    schema.moveField('foldermanagers', after='notaryContact')
    schema.moveField('description', after='opinionsToAskIfWorks')
    schema.moveField('folderCategoryTownship', after='RCU')
    return schema

finalizeSchema(UrbanCertificateBase_schema)
##/code-section module-footer

