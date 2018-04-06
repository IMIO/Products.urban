# -*- coding: utf-8 -*-
#
# File: EnvironmentBase.py
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
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.CODT_UniqueLicenceInquiry import CODT_UniqueLicenceInquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from collective.delaycalculator import workday
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from datetime import date
from Products.urban.utils import setOptionalAttributes, setSchemataForCODT_UniqueLicenceInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.widget.historizereferencewidget import HistorizeReferenceBrowserWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget

optional_fields = [
    'roadTechnicalAdvice', 'locationTechnicalAdvice', 'additionalLegalConditions',
    'businessOldLocation', 'applicationReasons',
]

slave_fields_natura2000 = (
    {
        'name': 'natura2000Details',
        'action': 'show',
        'hide_values': (True,),
    },
    {
        'name': 'natura2000location',
        'action': 'show',
        'hide_values': (True,),
    },
)

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

    ReferenceField(
        name='rubrics',
        widget=HistorizeReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='portal_urban/rubrics',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            base_query='rubrics_base_query',
            label='Rubrics',
            label_msgid='urban_label_rubrics',
            i18n_domain='urban',
        ),
        allowed_types=('EnvironmentRubricTerm',),
        schemata='urban_description',
        multiValued=True,
        relationship="rubric",
    ),
    TextField(
        name='rubricsDetails',
        widget=RichWidget(
            label=_('urban_label_rubricsDetails', default='Rubricsdetails'),
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_environment',
        default_method='getDefaultText',
        default_output_type='text/html',
    ),
    ReferenceField(
        name='minimumLegalConditions',
        widget=ReferenceBrowserWidget(
            label='Minimumlegalconditions',
            label_msgid='urban_label_minimumLegalConditions',
            i18n_domain='urban',
        ),
        schemata="urban_description",
        multiValued=True,
        relationship='minimumconditions',
    ),
    ReferenceField(
        name='additionalLegalConditions',
        widget=HistorizeReferenceBrowserWidget(
            allow_browse=True,
            allow_search=True,
            default_search_index='Title',
            startup_directory='portal_urban/exploitationconditions',
            restrict_browsing_to_startup_directory=True,
            wild_card_search=True,
            label='Additionallegalconditions',
            label_msgid='urban_label_additionalLegalConditions',
            i18n_domain='urban',
        ),
        allowed_types=('UrbanVocabularyTerm',),
        schemata="urban_description",
        multiValued=True,
        relationship='additionalconditions',
    ),
    LinesField(
        name='applicationReasons',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Applicationreasons',
            label_msgid='urban_label_applicationReasons',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=True,
        vocabulary=UrbanVocabulary(path='applicationreasons', sort_on='getObjPositionInParent'),
        default_method='getDefaultValue',
    ),
    DataGridField(
        name='businessOldLocation',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number': Column("Number"), 'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',))},
            helper_js=('datagridwidget.js', 'datagridautocomplete.js'),
            label='Businessoldlocation',
            label_msgid='urban_label_businessOldLocation',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
        validators=('isValidStreetName',),
    ),
    TextField(
        name='businessDescription',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Businessdescription',
            label_msgid='urban_label_businessDescription',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    StringField(
        name='procedureChoice',
        default='ukn',
        widget=MasterSelectWidget(
            slave_fields=slave_fields_procedurechoice,
            label='Procedurechoice',
            label_msgid='urban_label_procedureChoice',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        validators=('isValidProcedureChoice',),
        multiValued=1,
        vocabulary='listProcedureChoices',
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
        schemata='urban_analysis',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
    ),
    BooleanField(
        name='natura2000',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_natura2000,
            label='Natura2000',
            label_msgid='urban_label_natura2000',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='natura2000location',
        widget=SelectionWidget(
            label='Natura2000location',
            label_msgid='urban_label_location',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary='listNatura2000Locations',
    ),
    TextField(
        name='natura2000Details',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Natura2000details',
            label_msgid='urban_label_natura2000Details',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    IntegerField(
        name='validityDelay',
        default=20,
        widget=IntegerField._properties['widget'](
            label='Validitydelay',
            label_msgid='urban_label_validityDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
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
    TextField(
        name='description',
        widget=RichWidget(
            label='Description',
            label_msgid='urban_label_description',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_description',
        default_method='getDefaultText',
        default_output_type='text/html',
        accessor="Description",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    getattr(CODT_UniqueLicenceInquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentBase_schema['title'].required = False
EnvironmentBase_schema['title'].widget.visible = False
setSchemataForCODT_UniqueLicenceInquiry(EnvironmentBase_schema)
# hide Inquiry fields but 'solicitOpinionsTo'
for field in EnvironmentBase_schema.filterFields(isMetadata=False):
    if field.schemata == 'urban_investigation_and_advices' and field.getName() not in ['solicitOpinionsTo',
                                                                                       'solicitOpinionsToOptional']:
        field.widget.visible = False

# change translation of some fields
EnvironmentBase_schema['referenceDGATLP'].widget.label = _('urban_label_referenceDGO3')
EnvironmentBase_schema['workLocations'].widget.label = _('urban_label_situation')


##/code-section after-schema

class EnvironmentBase(BaseFolder, GenericLicence, CODT_UniqueLicenceInquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentBase)

    meta_type = 'EnvironmentBase'
    _at_rename_after_creation = True

    schema = EnvironmentBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location', \
                      'urban_investigation_and_advices']
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listNatura2000Locations')

    def listNatura2000Locations(self):
        """
          This vocabulary for field location returns a list of
          Natura2000 locations
        """
        vocab = (
            ('inside', 'location_inside'),
            ('near', 'location_near'),
        )
        return DisplayList(vocab)

    def rubrics_base_query(self):
        """ to be overriden """
        return {}

    def listProcedureChoices(self):
        vocabulary = (
            ('ukn', 'Non determiné'),
            ('simple', 'Simple'),
            ('temporary', 'Temporaire'),
        )
        return DisplayList(vocabulary)

    def getProcedureDelays(self, *values):
        """
        To implements in subclasses
        """

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastDisplayingTheDecision(self):
        return self.getLastEvent(interfaces.IDisplayingTheDecisionEvent)

    def getLastRecourse(self):
        return self.getLastEvent(interfaces.IRecourseEvent)

    def getLicenceExpirationDate(self):
        return self.getLastEvent(interfaces.ILicenceExpirationEvent)

    security.declarePublic('getAdditionalLayers')

    def getAdditionalLayers(self):
        """
          Return a list of additional layers that will be used
          when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues('Layer')
        except AttributeError:
            return None

    def getRubricsConfigPath(self):
        config_path = '/'.join(self.getLicenceConfig().rubrics.getPhysicalPath())[1:]
        return config_path

    security.declarePrivate('_getConditions')

    def _getConditions(self, restrict=['CI/CS', 'CI', 'CS']):
        all_conditions = self.getMinimumLegalConditions()
        all_conditions.extend(self.getAdditionalLegalConditions())
        return [cond for cond in all_conditions if cond.getExtraValue() in restrict]

    security.declarePublic('getIntegralConditions')

    def getIntegralConditions(self):
        """
         Return all the integral conditions,
        """
        return self._getConditions(restrict=['CI'])

    security.declarePublic('getSectorialConditions')

    def getSectorialConditions(self):
        """
         Return all the sectorial conditions,
        """
        return self._getConditions(restrict=['CS'])

    security.declarePublic('getIandSConditions')

    def getIandSConditions(self):
        """
         Return all the integral & sectorial conditions,
        """
        return self._getConditions(restrict=['CI/CS'])

    security.declarePublic('getLicenceSEnforceableDate')

    def getLicenceSEnforceableDate(self, displayDay, periodForAppeal):
        return workday(date(displayDay.year(), displayDay.month(), displayDay.day()), periodForAppeal)


registerType(EnvironmentBase, PROJECTNAME)


# end of class EnvironmentBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('businessOldLocation', after='workLocations')
    schema.moveField('foldermanagers', after='businessOldLocation')
    schema.moveField('rubrics', after='folderCategory')
    schema.moveField('description', after='additionalLegalConditions')
    return schema


finalizeSchema(EnvironmentBase_schema)
##/code-section module-footer
