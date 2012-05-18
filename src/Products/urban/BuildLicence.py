# -*- coding: utf-8 -*-
#
# File: BuildLicence.py
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
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate as _
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from dateutil.relativedelta import relativedelta

optional_fields = ['implantation','roadAdaptation','pebDetails',
                   'roadTechnicalAdvice','locationTechnicalAdvice','locationTechnicalConditions',
                   'pebTechnicalAdvice','locationDgrneUnderground', 'roadDgrneUnderground', 'workType']
##/code-section module-header

schema = Schema((

    LinesField(
        name='workType',
        widget=MultiSelectionWidget(
            label='Worktype',
            label_msgid='urban_label_workType',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary(path='folderbuildworktypes', sort_on='sortable_title'),
    ),
    StringField(
        name='usage',
        widget=SelectionWidget(
            label='Usage',
            label_msgid='urban_label_usage',
            i18n_domain='urban',
        ),
        required=True,
        schemata='urban_description',
        vocabulary='listUsages',
    ),
    StringField(
        name='roadAdaptation',
        default='no',
        widget=SelectionWidget(
            label='Roadadaptation',
            label_msgid='urban_label_roadAdaptation',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary='listRoadAdaptations',
    ),
    BooleanField(
        name='implantation',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Implantation',
            label_msgid='urban_label_implantation',
            i18n_domain='urban',
        ),
        schemata='urban_road',
    ),
    StringField(
        name='pebType',
        widget=SelectionWidget(
            label='Pebtype',
            label_msgid='urban_label_pebType',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_peb',
        vocabulary='listPebTypes',
    ),
    TextField(
        name='pebDetails',
        allowable_content_types="('text/plain',)",
        default_content_type='text/plain',
        widget=TextAreaWidget(
            label='Pebdetails',
            label_msgid='urban_label_pebDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        schemata='urban_peb',
    ),
    BooleanField(
        name='pebStudy',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Pebstudy',
            label_msgid='urban_label_pebStudy',
            i18n_domain='urban',
        ),
        schemata='urban_peb',
    ),
    BooleanField(
        name='roadDgrneUnderground',
        default=False,
        widget=BooleanField._properties['widget'](
            description="If checked, an additional paragraph will be added in the licence document",
            label='Roaddgrneunderground',
            label_msgid='urban_label_roadDgrneUnderground',
            description_msgid='urban_help_roadDgrneUnderground',
            i18n_domain='urban',
        ),
        schemata='urban_road',
    ),
    TextField(
        name='roadTechnicalAdvice',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Roadtechnicaladvice',
            label_msgid='urban_label_roadTechnicalAdvice',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_road',
        default_output_type='text/html',
    ),
    BooleanField(
        name='locationDgrneUnderground',
        default=False,
        widget=BooleanField._properties['widget'](
            description="If checked, an additional paragraph will be added in the licence document",
            label='Locationdgrneunderground',
            label_msgid='urban_label_locationDgrneUnderground',
            description_msgid='urban_help_locationDgrneUnderground',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='locationTechnicalAdvice',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Locationtechnicaladvice',
            label_msgid='urban_label_locationTechnicalAdvice',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    TextField(
        name='locationTechnicalConditions',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Locationtechnicalconditions',
            label_msgid='urban_label_locationTechnicalConditions',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    TextField(
        name='pebTechnicalAdvice',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pebtechnicaladvice',
            label_msgid='urban_label_pebTechnicalAdvice',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        schemata='urban_peb',
        default_output_type='text/html',
    ),
    ReferenceField(
        name='architects',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=1,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title':'Nom'},
            startup_directory="urban/architects",
            wild_card_search=True,
            restrict_browsing_to_startup_directory=1,
            label='Architects',
            label_msgid='urban_label_architects',
            i18n_domain='urban',
        ),
        allowed_types=('Architect',),
        schemata='urban_description',
        multiValued=1,
        relationship='licenceArchitects',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

BuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
BuildLicence_schema['title'].required = False
#put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(BuildLicence_schema)
##/code-section after-schema

class BuildLicence(BaseFolder, Inquiry, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IBuildLicence)

    meta_type = 'BuildLicence'
    _at_rename_after_creation = True

    schema = BuildLicence_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location',\
                      'urban_investigation_and_advices', 'urban_peb']
    #implements(interfacesToImplement)
    archetype_name = 'BuildLicence'

    ##/code-section class-header

    # Methods

    security.declarePublic('listRoadAdaptations')
    def listRoadAdaptations(self):
        """
          This vocabulary for field roadAdaptation returns a list of
          road adaptations : no, yes modify, yes create
        """
        lst=[
             ['no', _('road_adaptation_no', 'urban', context=self.REQUEST)],
             ['modify', _('road_adaptation_modify', 'urban', context=self.REQUEST)],
             ['create', _('road_adaptation_create', 'urban', context=self.REQUEST)],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('listUsages')
    def listUsages(self):
        """
          This vocabulary for field usage returns a list of
          building usage : for habitation, not for habitation
        """
        lst=[
             ['for_habitation', _('usage_for_habitation', 'urban', context=self.REQUEST)],
             ['not_for_habitation', _('usage_not_for_habitation', 'urban', context=self.REQUEST)],
             ['not_applicable', _('usage_not_applicable', 'urban', context=self.REQUEST)],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    # Manually created methods

    def listPebTypes(self):
        """
          Vocabulary for field 'pebType'
        """
        lst=[
             ['not_applicable', _('peb_not_applicable', 'urban', context=self.REQUEST, default="Not applicable")],
             ['complete_process', _('peb_complete_process', 'urban', context=self.REQUEST, default="Complete process")],
             ['form1_process', _('peb_form1_process', 'urban', context=self.REQUEST, default="Form 1 process")],
             ['form2_process', _('peb_form2_process', 'urban', context=self.REQUEST, default="Form 2 process")],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('askFD')
    def askFD(self):
        """
        """
        if self.getFolderCategory() in ['udc', 'uap', 'cu2', 'lap', 'lapm']:
            return True
        else:
            return False

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

    def getProrogatedToDate(self):
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
            return tool.formatDate(lastTheLicenceDecisionDate.asdatetime() + relativedelta(years=+1))



registerType(BuildLicence, PROJECTNAME)
# end of class BuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('roadAdaptation', before='roadTechnicalAdvice')
    schema.moveField('licenceSubject', after='title')
    schema.moveField('reference', after='licenceSubject')
    schema.moveField('workLocations', after='reference')
    schema.moveField('architects', after='workLocations')
    schema.moveField('referenceDGATLP', after='reference')
    schema.moveField('foldermanagers', after='architects')
    schema.moveField('workType', after='folderCategory')
    schema.moveField('folderZoneDetails', after='folderZone')
    schema.moveField('isInPCA', after='folderZoneDetails')
    schema.moveField('pca', after='isInPCA')
    schema.moveField('isInSubdivision', after='pca')
    schema.moveField('parcellings', after='isInSubdivision')
    schema.moveField('subdivisionDetails', after='parcellings')
    schema.moveField('description', after='usage')
    schema.moveField('pash', after='roadEquipments')
    schema.moveField('pashDetails', after='pash')
    schema.moveField('folderCategoryTownship', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('derogation', after='areParcelsVerified')
    schema.moveField('derogationDetails', after='derogation')
    schema.moveField('investigationArticles', after='derogationDetails')
    schema.moveField('investigationStart', after='investigationArticles')
    schema.moveField('investigationEnd', after='investigationStart')
    schema.moveField('investigationDetails', after='investigationEnd')
    schema.moveField('investigationReasons', after='investigationDetails')
    schema.moveField('solicitOpinionsTo', after='investigationReasons')
    schema.moveField('investigationOralReclamationNumber', after='solicitOpinionsTo')
    schema.moveField('investigationWriteReclamationNumber', after='investigationOralReclamationNumber')
    return schema

finalizeSchema(BuildLicence_schema)
##/code-section module-footer

