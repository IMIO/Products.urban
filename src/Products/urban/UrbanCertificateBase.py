# -*- coding: utf-8 -*-
#
# File: UrbanCertificateBase.py
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
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate as _
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.LinesColumn import LinesColumn
from Products.urban.base import UrbanBase
from Products.urban.indexes import UrbanIndexes
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

optional_fields = []
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
    StringField(
        name='specificFeatures',
        widget=InAndOutWidget(
            size=15,
            description_msgid="certificateone_specificfeatures_descr",
            description='Select the specific features from the left box and drop them in the right box to select them',
            label='Specificfeatures',
            label_msgid='urban_label_specificFeatures',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary('specificfeatures'),
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
    StringField(
        name='townshipSpecificFeatures',
        widget=InAndOutWidget(
            size=15,
            description_msgid="certificateone_townshipspecificfeatures_descr",
            description='Select the specific features from the left box and drop them in the right box to select them',
            label='Townshipspecificfeatures',
            label_msgid='urban_label_townshipSpecificFeatures',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary('townshipspecificfeatures'),
    ),
    ReferenceField(
        name='foldermanagers',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=0,
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            available_indexes= {'Title':'Nom'},
            base_query="getSelectableFolderManagersBaseQuery",
            wild_card_search=True,
            label='Foldermanagers',
            label_msgid='urban_label_foldermanagers',
            i18n_domain='urban',
        ),
        required= False,
        schemata='urban_description',
        multiValued=1,
        relationship='certificateFolderManagers',
        default_method="getDefaultFolderManagers",
        allowed_types=('FolderManager',),
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
#remove the annoncedDelays for UrbanCertificateOne
del UrbanCertificateBase_schema['annoncedDelay']
del UrbanCertificateBase_schema['annoncedDelayDetails']
#hide the solicit opinions to fields for UrbanCertificateOne
del UrbanCertificateBase_schema['solicitRoadOpinionsTo']
del UrbanCertificateBase_schema['solicitLocationOpinionsTo']
##/code-section after-schema

class UrbanCertificateBase(BaseFolder, UrbanIndexes,  UrbanBase, GenericLicence, BrowserDefaultMixin):
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
        notary = ''
        applicant = ''
        if self.getApplicants():
            applicant = unicode(self.getApplicants()[0].Title(), 'utf-8')
        else:
            applicant = _('no_applicant_defined', 'urban', context=self.REQUEST)
        if self.getNotaryContact():
            notary = unicode(self.getNotaryContact()[0].Title(), 'utf-8')
        else:
            notary = _('no_notary_defined', 'urban', context=self.REQUEST)

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

    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)

    def getCustomSpecificFeaturesAsList(self):
        """
          To display custom specific features easily, get it as a list of features
        """
        res = []
        for csf in self.getCustomSpecificFeatures():
            if csf['feature']:
                res.append(csf['feature'])
        return res


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
    schema.moveField('description', after='townshipSpecificFeatures')
    schema.moveField('folderCategoryTownship', after='folderCategory')
    return schema

finalizeSchema(UrbanCertificateBase_schema)
##/code-section module-footer

