# -*- coding: utf-8 -*-
#
# File: BuildLicence.py
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
from Products.urban.Inquiry import Inquiry
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from dateutil.relativedelta import relativedelta

optional_fields = [
    'implantation', 'roadAdaptation', 'pebDetails', 'requirementFromFD',
    'roadTechnicalAdvice', 'locationTechnicalAdvice', 'locationTechnicalConditions',
    'pebTechnicalAdvice', 'locationDgrneUnderground', 'roadDgrneUnderground', 'workType',
    'townshipCouncilFolder', 'roadMiscDescription', 'procedureChoice', 'water'
]

slave_fields_procedurechoice = (
    {
        'name': 'annoncedDelay',
        'action': 'value',
        'vocab_method': 'getProcedureDelays',
        'control_param': 'values',
    },
)
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
        default_method='getDefaultValue',
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
        name='annoncedDelay',
        widget=SelectionWidget(
            label='Annonceddelay',
            label_msgid='urban_label_annoncedDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('folderdelays', vocType='UrbanDelay', with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='annoncedDelayDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Annonceddelaydetails',
            label_msgid='urban_label_annoncedDelayDetails',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
    ),
    BooleanField(
        name='townshipCouncilFolder',
        default=False,
        widget=BooleanField._properties['widget'](
            description="If checked, an additional paragraph will be added in the licence document",
            label='Townshipcouncilfolder',
            label_msgid='urban_label_townshipCouncilFolder',
            description_msgid='urban_help_townshipCouncilFolder',
            i18n_domain='urban',
        ),
        schemata='urban_road',
    ),
    BooleanField(
        name='impactStudy',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Impactstudy',
            label_msgid='urban_label_impactStudy',
            i18n_domain='urban',
        ),
        schemata='urban_description',
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
        vocabulary=UrbanVocabulary(path='pebcategories'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='pebDetails',
        allowable_content_types= ('text/plain',),
        widget=TextAreaWidget(
            label='Pebdetails',
            label_msgid='urban_label_pebDetails',
            i18n_domain='urban',
        ),
        schemata='urban_peb',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
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
    TextField(
        name='roadMiscDescription',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Roadmiscdescription',
            label_msgid='urban_label_roadMiscDescription',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/html',
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
        default_method='getDefaultText',
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
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
    ),
    LinesField(
        name='requirementFromFD',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Requirementfromfd',
            label_msgid='urban_label_requirementFromFD',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary='listRequirementsFromFD',
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
        default_method='getDefaultText',
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
        default_method='getDefaultText',
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
    BooleanField(
        name='water',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Water',
            label_msgid='urban_label_water',
            i18n_domain='urban',
        ),
        schemata='urban_road',
    ),
    BooleanField(
        name='electricity',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Electricity',
            label_msgid='urban_label_electricity',
            i18n_domain='urban',
        ),
        schemata='urban_road',
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
        vocab = (
            ('no', 'road_adaptation_no'),
            ('modify', 'road_adaptation_modify'),
            ('create', 'road_adaptation_create'),
        )
        return DisplayList(vocab)

    security.declarePublic('listUsages')
    def listUsages(self):
        """
          This vocabulary for field usage returns a list of
          building usage : for habitation, not for habitation
        """
        vocab = (
            ('for_habitation', 'usage_for_habitation'),
            ('not_for_habitation', 'usage_not_for_habitation'),
            ('not_applicable', 'usage_not_applicable'),
        )
        return DisplayList(vocab)

    # Manually created methods

    security.declarePublic('listRequirementsFromFD')
    def listRequirementsFromFD(self):
        """
          This vocabulary for field requirementsFromFD returns this list: decision, opinion
        """
        vocab = (
            ('opinion', 'location_fdrequirement_opinion'),
            ('decision', 'location_fdrequirement_decision'),
        )
        return DisplayList(vocab)

    security.declarePublic('askFD')
    def askFD(self):
        """
        """
        return self.getFolderCategory() in ['udc', 'uap', 'cu2', 'lap', 'lapm']

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

    def getAllMissingPartDeposits(self):
        return self._getAllEvents(interfaces.IMissingPartDepositEvent)

    def getAllTechnicalServiceOpinionRequests(self):
        return self._getAllEvents(interfaces.ITechnicalServiceOpinionRequestEvent)

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
            return tool.formatDate(lastTheLicenceDecisionDate.asdatetime() + relativedelta(years=+3))



registerType(BuildLicence, PROJECTNAME)
# end of class BuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('roadAdaptation', before='roadTechnicalAdvice')
    schema.moveField('architects', after='workLocations')
    schema.moveField('foldermanagers', after='architects')
    schema.moveField('workType', after='folderCategory')
    schema.moveField('parcellings', after='isInSubdivision')
    schema.moveField('description', after='usage')
    schema.moveField('roadMiscDescription', after='roadEquipments')
    schema.moveField('folderCategoryTownship', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('requirementFromFD', after='locationDgrneUnderground')
    schema.moveField('townshipCouncilFolder', after='roadCoating')
    schema.moveField('annoncedDelay', after='missingPartsDetails')
    schema.moveField('annoncedDelayDetails', after='annoncedDelay')
    schema.moveField('impactStudy', after='annoncedDelayDetails')
    schema.moveField('water', after='roadCoating')
    schema.moveField('electricity', before='water')
    return schema

finalizeSchema(BuildLicence_schema)
##/code-section module-footer

