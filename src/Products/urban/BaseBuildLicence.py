# -*- coding: utf-8 -*-
#
# File: BaseBuildLicence.py
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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from dateutil.relativedelta import relativedelta
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

optional_fields = [
    'implantation', 'roadAdaptation', 'pebDetails', 'requirementFromFD',
    'roadTechnicalAdvice', 'locationTechnicalAdvice', 'locationTechnicalConditions',
    'pebTechnicalAdvice', 'locationDgrneUnderground', 'roadDgrneUnderground', 'workType',
    'townshipCouncilFolder', 'roadMiscDescription', 'procedureChoice', 'water', 'electricity',
    'shouldNumerotateBuildings', 'habitationsAfterLicence', 'habitationsBeforeLicence',
    'additionalHabitationsAsked', 'additionalHabitationsGiven', 'mayNeedLocationLicence',
    'impactStudy', 'exemptFDArticle'
]

slave_fields_habitation = (
    # if in a pca, display a selectbox
    {
        'name': 'shouldNumerotateBuildings',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'habitationsBeforeLicence',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'habitationsAfterLicence',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'additionalHabitationsAsked',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'additionalHabitationsGiven',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'mayNeedLocationLicence',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'habitationsBeforeLicence',
        'action': 'hide',
        'hide_values': (True, ),
    },
)

slave_fields_procedurechoice = (
    {
        'name': 'annoncedDelay',
        'action': 'value',
        'vocab_method': 'getProcedureDelays',
        'control_param': 'values',
    },
    {
        'name': 'exemptFDArticle',
        'action': 'show',
        'toggle_method': 'showExemptFDArticle',
        'control_param': 'values',
    },
    {
        'name': 'requirementFromFD',
        'action': 'show',
        'toggle_method': 'showRequirementFromFD',
        'control_param': 'values',
    },

)

slave_fields_composition = (
    {
        'name': 'missingParts',
        'action': 'vocabulary',
        'vocab_method': 'getCompositionMissingParts',
        'control_param': 'composition',
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
        schemata='urban_analysis',
        vocabulary='listUsages',
    ),
    StringField(
        name='annoncedDelay',
        widget=SelectionWidget(
            label='Annonceddelay',
            label_msgid='urban_label_annoncedDelay',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
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
        schemata='urban_analysis',
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
        schemata='urban_analysis',
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
        allowable_content_types=('text/plain',),
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
    BooleanField(
        name='noApplication',
        default=True,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_habitation,
            label='Noapplication',
            label_msgid='urban_label_noApplication',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    BooleanField(
        name='shouldNumerotateBuildings',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Shouldnumerotatebuildings',
            label_msgid='urban_label_shouldNumerotateBuilding',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    IntegerField(
        name='habitationsBeforeLicence',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Habitationsbeforelicence',
            label_msgid='urban_label_habitationsBeforeLicence',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    IntegerField(
        name='additionalHabitationsAsked',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Additionalhabitationsasked',
            label_msgid='urban_label_additionalHabitationsAsked',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    IntegerField(
        name='additionalHabitationsGiven',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Additionalhabitationsgiven',
            label_msgid='urban_label_additionalHabitationsGiven',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    IntegerField(
        name='habitationsAfterLicence',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Habitationsafterlicence',
            label_msgid='urban_label_habitationsAfterLicence',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    BooleanField(
        name='mayNeedLocationLicence',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Mayneedlocationlicence',
            label_msgid='urban_label_mayNeedLocationLicence',
            i18n_domain='urban',
        ),
        schemata='urban_habitation',
    ),
    StringField(
        name='roadAdaptation',
        default='no',
        widget=MultiSelectionWidget(
            format='checkbox',
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
        schemata='urban_analysis',
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
        default_method='getDefaultText',
        schemata='urban_analysis',
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
            available_indexes={'Title': 'Nom'},
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
    LinesField(
        name='procedureChoice',
        default='ukn',
        widget=MasterMultiSelectWidget(
            format='checkbox',
            slave_fields=slave_fields_procedurechoice,
            label='Procedurechoice',
            label_msgid='urban_label_procedureChoice',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
        validators=('isValidProcedureChoice',),
        multiValued=1,
        vocabulary='listProcedureChoices',
    ),
    LinesField(
        name='requirementFromFD',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Requirementfromfd',
            label_msgid='urban_label_requirementFromFD',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
        multiValued=1,
        vocabulary='listRequirementsFromFD',
    ),
    StringField(
        name='exemptFDArticle',
        widget=SelectionWidget(
            format='select',
            label='Exemptfdarticle',
            label_msgid='urban_label_exemptFDArticle',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
        vocabulary=UrbanVocabulary('exemptfdarticle', with_empty_value=True),
        default_method='getDefaultValue',
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
    StringField(
        name='composition',
        widget=MasterSelectWidget(
            slave_fields=slave_fields_composition,
            label='Composition',
            label_msgid='urban_label_composition',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
        vocabulary='listCompositions',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

BaseBuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
BaseBuildLicence_schema['title'].required = False
#put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(BaseBuildLicence_schema)
##/code-section after-schema


class BaseBuildLicence(BaseFolder, Inquiry, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IBaseBuildLicence)

    _at_rename_after_creation = True

    schema = BaseBuildLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('getApplicants')

    def getApplicants(self):
        """
        """
        applicants = self.getCorporations() or super(BaseBuildLicence, self).getApplicants()
        return applicants

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')]
        return corporations

    security.declarePublic('listRoadAdaptations')

    def listRoadAdaptations(self):
        """
          This vocabulary for field roadAdaptation returns a list of
          road adaptations : no, yes modify, yes create
        """
        vocab = (
            ('modify', 'road_adaptation_modify'),
            ('create', 'road_adaptation_create'),
            ('supress', 'road_adaptation_supress'),
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

    security.declarePublic('getRepresentatives')

    def getRepresentatives(self):
        """
        """
        return self.getArchitects()

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
        return 'FD' in self.getProcedureChoice()

    def getLastDeposit(self, use_catalog=True):
        return self._getLastEvent(interfaces.IDepositEvent, use_catalog)

    def getLastMissingPart(self, use_catalog=True):
        return self._getLastEvent(interfaces.IMissingPartEvent, use_catalog)

    def getLastMissingPartDeposit(self, use_catalog=True):
        return self._getLastEvent(interfaces.IMissingPartDepositEvent, use_catalog)

    def getLastWalloonRegionPrimo(self, use_catalog=True):
        return self._getLastEvent(interfaces.IWalloonRegionPrimoEvent, use_catalog)

    def getLastWalloonRegionOpinionRequest(self, use_catalog=True):
        return self._getLastEvent(interfaces.IWalloonRegionOpinionRequestEvent, use_catalog)

    def getLastAcknowledgment(self, use_catalog=True):
        return self._getLastEvent(interfaces.IAcknowledgmentEvent, use_catalog)

    def getLastCommunalCouncil(self, use_catalog=True):
        return self._getLastEvent(interfaces.ICommunalCouncilEvent, use_catalog)

    def getLastCollegeReport(self, use_catalog=True):
        return self._getLastEvent(interfaces.ICollegeReportEvent, use_catalog)

    def getLastTheLicence(self, use_catalog=True):
        return self._getLastEvent(interfaces.ITheLicenceEvent, use_catalog)

    def getLastWorkBeginning(self, use_catalog=True):
        return self._getLastEvent(interfaces.IWorkBeginningEvent, use_catalog)

    def getLastProrogation(self, use_catalog=True):
        return self._getLastEvent(interfaces.IProrogationEvent, use_catalog)

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

    def listProcedureChoices(self):
        vocabulary = (
            ('ukn', 'Non determiné'),
            ('opinions', 'Sollicitation d\'avis (instance ou service interne/externe)'),
            ('inquiry', 'Instruction d\'une enquête publique'),
            ('FD', 'Sollicitation du fonctionnaire délégué'),
        )
        return DisplayList(vocabulary)

    def listCompositions(self):
        vocabulary = (
            ('', 'Non déterminée'),
            ('285', 'Art. 285 - complet avec architecte'),
            ('288', 'Art. 288 - simplifié avec architecte'),
            ('291', 'Art. 291 - simplifié sans architecte'),
        )
        return DisplayList(vocabulary)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        opinions = 'opinions' in selection
        inquiry = 'inquiry' in selection
        FD = 'FD' in selection

        if unknown:
            return ''
        elif (opinions or inquiry) and FD:
            return '115j'
        elif opinions and inquiry and not FD:
            return '70j'
        elif opinions and not (inquiry or FD):
            return '70j'
        elif inquiry and not (opinions or FD):
            return '70j'
        elif FD and not (opinions or inquiry):
            return '75j'
        else:
            return '30j'

    def showExemptFDArticle(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        show = 'FD' not in selection and 'ukn' not in selection
        return show

    def showRequirementFromFD(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        show = 'FD' in selection and 'ukn' not in selection
        return show

    def getCompositionMissingParts(self, composition):
        """
        """
        urban_voc = self.schema['missingParts'].vocabulary
        all_terms = urban_voc.listAllVocTerms(self)

        display_values = [(term.Title().decode('utf-8'), term.id) for term in all_terms if str(composition) in term.getExtraValue()]

        return DisplayList(display_values)

    def costCalculation(self, base_price=0, FD_price=0, inquiry_price=0, opinions_price=0):
        cost = base_price
        if ('opinions' in self.getProcedureChoice()):
            cost += opinions_price
        if ('inquiry' in self.getProcedureChoice()):
            cost += inquiry_price
        if ('FD' in self.getProcedureChoice()):
            cost += FD_price
        return cost

# end of class BaseBuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized


def finalizeSchema(schema):
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
    schema.moveField('locationTechnicalRemarks', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('requirementFromFD', before='annoncedDelay')
    schema.moveField('townshipCouncilFolder', after='futureRoadCoating')
    schema.moveField('annoncedDelayDetails', after='annoncedDelay')
    schema.moveField('impactStudy', after='annoncedDelayDetails')
    schema.moveField('procedureChoice', before='description')
    schema.moveField('exemptFDArticle', after='procedureChoice')
    schema.moveField('water', after='futureRoadCoating')
    schema.moveField('electricity', before='water')
    schema.moveField('composition', before='missingParts')
    schema['missingParts'].widget.format = None
    return schema

finalizeSchema(BaseBuildLicence_schema)
##/code-section module-footer
