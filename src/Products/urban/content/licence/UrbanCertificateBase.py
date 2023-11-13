# -*- coding: utf-8 -*-
#
# File: UrbanCertificateBase.py
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
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.DataGridField.FixedColumn import FixedColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.UrbanDataGridColumns.FormFocusColumn import FormFocusColumn
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget


optional_fields = [
    'specificFeatures', 'roadSpecificFeatures', 'locationSpecificFeatures',
    'customSpecificFeatures', 'townshipSpecificFeatures', 'opinionsToAskIfWorks',
    'basement', 'ZIP', 'pollution', 'annoncedDelay', 'annoncedDelayDetails',
    'notaryContact', 'SCT', 'sctDetails', 'SDC', 'sdcDetails', 'regional_guide', 'regional_guide_details',
    'township_guide', 'township_guide_details'
]


full_patrimony_slave_fields = (
    {
        'name': 'patrimony_site',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'patrimony_architectural_complex',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'archeological_site',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'protection_zone',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'regional_inventory_building',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'small_popular_patrimony',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'communal_inventory',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'regional_inventory',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'patrimony_archaeological_map',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'patrimony_project_gtoret_1ha',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'observation',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'patrimony_monument',
        'action': 'hide',
        'hide_values': ('none', 'patrimonial'),
    },
    {
        'name': 'classification_order_scope',
        'action': 'hide',
        'hide_values': ('none', 'patrimonial'),
    },
    {
        'name': 'patrimony_analysis',
        'action': 'hide',
        'hide_values': ('none',),
    },
    {
        'name': 'patrimony_observation',
        'action': 'hide',
        'hide_values': ('none',),
    },
)

schema = Schema((

    ReferenceField(
        name='notaryContact',
        widget=ReferenceBrowserWidget(
            allow_search=1,
            only_for_review_states='enabled',
            allow_browse=1,
            force_close_on_insert=1,
            startup_directory='urban/notaries',
            restrict_browsing_to_startup_directory=1,
            popup_name='contact_reference_popup',
            wild_card_search=True,
            label=_('urban_label_notaryContact', default='Notary(ies)'),
        ),
        required=False,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types=('Notary',),
    ),
    DataGridField(
        name='specificFeatures',
        widget=DataGridWidget(
            columns={'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label=_('urban_label_specificFeatures', default='Specificfeatures'),
        ),
        fixed_rows='getSpecificFeaturesRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=False,
        schemata='urban_description',
        columns=('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='roadSpecificFeatures',
        widget=DataGridWidget(
            columns={'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label=_('urban_label_roadSpecificFeatures', default='Roadspecificfeatures'),
        ),
        fixed_rows='getRoadFeaturesRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=False,
        schemata='urban_road',
        columns=('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='locationSpecificFeatures',
        widget=DataGridWidget(
            columns={'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label=_('urban_label_locationSpecificFeatures', default='Locationspecificfeatures'),
        ),
        fixed_rows='getLocationFeaturesRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=False,
        schemata='urban_location',
        columns=('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='customSpecificFeatures',
        widget=DataGridWidget(
            columns={'text': TextAreaColumn("Feature", rows=1, cols=50)},
            label=_('urban_label_customSpecificFeatures', default='Customspecificfeatures'),
        ),
        schemata='urban_description',
        columns=('text',),
    ),
    DataGridField(
        name='townshipSpecificFeatures',
        widget=DataGridWidget(
            columns={'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label=_('urban_label_townshipSpecificFeatures', default='Townshipspecificfeatures'),
        ),
        fixed_rows='getTownshipFeaturesRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=False,
        schemata='urban_description',
        columns=('id', 'check', 'value', 'text',),
    ),
    LinesField(
        name='opinionsToAskIfWorks',
        widget=MultiSelect2Widget(
            format='checkbox',
            label=_('urban_label_opinionsToAskIfWorks', default='Opinionstoaskifworks'),
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('opinionstoaskifworks', vocType='OrganisationTerm'),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='basement',
        widget=MultiSelect2Widget(
            format='checkbox',
            label=_('urban_label_basement', default='Basement'),
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('basement'),
        default_method='getDefaultValue',
    ),
    BooleanField(
        name='pollution',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_pollution', default='Pollution'),
        ),
        schemata='urban_location',
    ),
    LinesField(
        name='ZIP',
        widget=MultiSelect2Widget(
            format='checkbox',
            label=_('urban_label_ZIP', default='Zip'),
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('zip'),
        default_method='getDefaultValue',
    ),
    StringField(
        name='annoncedDelay',
        widget=SelectionWidget(
            label=_('urban_label_annoncedDelay', default='Annonceddelay'),
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('folderdelays', vocType='UrbanDelay', with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='annoncedDelayDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_annoncedDelayDetails', default='Annonceddelaydetails'),
        ),
        schemata='urban_description',
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
    ),
    LinesField(
        name='SCT',
        widget=MultiSelect2Widget(
            size=15,
            label=_('urban_label_SCT', default='Sct'),
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('sct', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='sctDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_sctDetails', default='Sctdetails'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/x-html-safe',
    ),
    LinesField(
        name='SDC',
        widget=MultiSelect2Widget(
            size=15,
            label=_('urban_label_SDC', default='Sdc'),
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('sdc', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='sdcDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_sdcDetails', default='Sdcdetails'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/x-html-safe',
    ),
    LinesField(
        name='township_guide',
        widget=MultiSelect2Widget(
            size=10,
            label=_('urban_label_township_guide', default='Township_guide'),
        ),
        schemata='urban_location',
        multiValued=1,
        vocabulary=UrbanVocabulary('township_guide', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='township_guide_details',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_township_guide_details',
                    default='Township_guide_details'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/x-html-safe',
    ),
    LinesField(
        name='regional_guide',
        widget=MultiSelect2Widget(
            label=_('urban_label_regional_guide', default='Regional_guide'),
        ),
        schemata='urban_location',
        vocabulary=UrbanVocabulary('regional_guide', inUrbanConfig=False, with_empty_value=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='regional_guide_details',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_regional_guide_details',
                    default='Regional_guide_details'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/x-html-safe',
    ),
    TextField(
        name='patrimony_analysis',
        widget=RichWidget(
            label=_('urban_label_patrimony_analysis', default='Patrimony_analysis'),
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_patrimony',
        default_method='getDefaultText',
        default_output_type='text/x-html-safe',
        accessor="PatrimonyAnalysis",
    ),
    BooleanField(
        name='patrimony_architectural_complex',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_patrimony_architectural_complex', default='Patrimony_architectural_complex'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='patrimony_site',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_patrimony_site', default='Patrimony_site'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='patrimony_archaeological_map',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_patrimony_archaeological_map', default='Patrimony_archaeological_map'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='patrimony_project_gtoret_1ha',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_patrimony_project_gtoret_1ha', default='Patrimony_project_gtoret_1ha'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='patrimony_monument',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_patrimony_monument', default='Patrimony_monument'),
        ),
        schemata='urban_patrimony',
    ),
    TextField(
        name='patrimony_observation',
        widget=RichWidget(
            label=_('urban_label_patrimony_observation', default='Patrimony_observation'),
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_patrimony',
        default_method='getDefaultText',
        default_output_type='text/x-html-safe',
        accessor="PatrimonyObservation",
    ),
    LinesField(
        name='classification_order_scope',
        widget=MultiSelect2Widget(
            format='checkbox',
            label=_('urban_label_classification_order_scope', default='Classification_order_scope'),
        ),
        schemata='urban_patrimony',
        multiValued=1,
        vocabulary=UrbanVocabulary('classification_order_scope', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    StringField(
        name='general_disposition',
        widget=SelectionWidget(
            label=_('urban_label_general_disposition', default='General_disposition'),
        ),
        schemata='urban_patrimony',
        vocabulary=UrbanVocabulary('general_disposition', inUrbanConfig=False, with_empty_value=True),
    ),
    StringField(
        name='patrimony',
        widget=MasterSelectWidget(
            slave_fields=full_patrimony_slave_fields,
            label=_('urban_label_patrimony', default='Patrimony'),
        ),
        vocabulary='list_patrimony_types',
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='archeological_site',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_archeological_site', default='Archeological_site'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='protection_zone',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_protection_zone', default='Protection_zone'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='regional_inventory_building',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_regional_inventory_building', default='Regional_inventory_building'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='small_popular_patrimony',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_small_popular_patrimony', default='Small_popular_patrimony'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='communal_inventory',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_communal_inventory', default='Communal_inventory'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='regional_inventory',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_regional_inventory', default='Regional_inventory'),
        ),
        schemata='urban_patrimony',
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

    security.declarePublic('getRepresentatives')
    def getRepresentatives(self):
        """
        """
        return self.getNotaryContact()

    security.declarePublic('attributeIsUsed')
    def attributeIsUsed(self, name):
        """
         Override the GenericLicence attributeIsUsed method to always return true.
         This is because we want to delegate the display of the field to licence edit view
         and not to archetype so we can hide the widget in a <div hidden=True> tag.
         This is needed for the specificFeature edit shortcut.
        """
        return True

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
        dict['path'] = {'query': '%s%s' % (rootPath, folderManagersPath)}
        dict['sort_on'] = 'sortable_title'
        return dict

    security.declarePublic('getSpecificFeaturesRows')
    def getSpecificFeaturesRows(self):
        return self._getSpecificFeaturesRows()

    security.declarePublic('getRoadFeaturesRows')
    def getRoadFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='road')

    security.declarePublic('getLocationFeaturesRows')
    def getLocationFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='location')

    security.declarePublic('getTownshipFeaturesRows')
    def getTownshipFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='township')

    def _getSpecificFeaturesRows(self, location=''):
        portal_urban = getToolByName(self, 'portal_urban')
        vocname = '%sspecificfeatures' % location
        vocterms = [brain.getObject() for brain in portal_urban.listVocabularyBrains(vocToReturn=vocname, vocType=['SpecificFeatureTerm'], context=self)]

        rows = []
        for vocterm in vocterms:
            numbering = vocterm.getNumbering() and '%s - ' % vocterm.getNumbering() or ''
            value = '%s%s' % (numbering, vocterm.Title())
            row_data = {
                'check': vocterm.getIsDefaultValue() and '1' or '',
                'id': vocterm.id,
                'value': value,
                'text': vocterm.Description(),
            }
            row = FixedRow(keyColumn='id', initialData=row_data)
            rows.append(row)

        return rows

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        notary = ''
        proprietary = ''
        proprietaries = self.getProprietaries() or self.getApplicants()
        if proprietaries:
            proprietary = ', '.join([prop.Title() for prop in proprietaries])
        else:
            proprietary = translate('no_proprietary_defined', 'urban', context=self.REQUEST).encode('utf8')
        if self.getNotaryContact():
            notary = ', '.join([notar.Title() for notar in self.getNotaryContact()])
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

    security.declarePublic('getOpinionsToAskForWorks')
    def getOpinionsToAskForWorks(self, theObjects=False):
        """
          Returns the opinionsToAskIfWorks values or the OrganisationTerms if theObject=True
        """
        res = self.getField('opinionsToAskIfWorks').get(self)
        if res and theObjects:
            urbanConfig = self.getLicenceConfig()
            opinionsToAskIfWorksConfigFolder = urbanConfig.opinionstoaskifworks
            elts = res
            res = []
            for elt in elts:
                res.append(getattr(opinionsToAskIfWorksConfigFolder, elt))
        return res

    security.declarePublic('getFirstAcknowledgment')
    def getFirstAcknowledgment(self):
        return self.getFirstEvent(interfaces.IAcknowledgmentEvent)

    security.declarePublic('getLastAcknowledgment')
    def getLastAcknowledgment(self):
        return self.getLastEvent(interfaces.IAcknowledgmentEvent)

    security.declarePublic('getLastDeposit')
    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    security.declarePublic('getLastTheLicence')
    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    security.declarePublic('getSpecificFeaturesForTemplate')
    def getSpecificFeaturesForTemplate(self, where=[''], active_style='', inactive_style='striked'):
        """
          Return formatted specific features (striked or not)
          Helper method used in templates
        """
        tool = getToolByName(self, 'portal_urban')
        #get all the specificfeatures vocabular terms from each config
        res=[]
        for location in where:
            specificfeature_accessor = "get%sSpecificFeatures" % location.capitalize()
            specificFeatures = getattr(self, specificfeature_accessor)()
            for specificfeature in specificFeatures:
                if specificfeature['check']:
                    #render the expressions
                    render = tool.renderText(text=specificfeature['text'], context=self)
                    if active_style:
                        render = tool.decorateHTML(active_style, render)
                    res.append(render)
                else:
                    #replace the expressions by a null value, aka "..."
                    render = tool.renderText(text=specificfeature['text'], context=self, renderToNull=True)
                    if inactive_style:
                        render = tool.decorateHTML(inactive_style, render)
                    res.append(render)
            #add customSpecificFeatures
            if location == '':
                for csf in self.getCustomSpecificFeatures():
                    res.append("<p>%s</p>" % csf['text'])
        return res

    security.declarePublic('getApplicantsSignaletic')
    def getProprietariesSignaletic(self, withaddress=False):
        """
          Returns a string representing the signaletic of every proprietaries
        """
        proprietaries = self.getProprietaries()
        signaletic = ''
        for proprietary in proprietaries:
            #if the signaletic is not empty, we are adding several applicants
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += proprietary.getSignaletic(withaddress=withaddress)
        return signaletic

    def list_patrimony_types(self):
        """
        """
        vocabulary = (
                ('none', 'aucune incidence'),
                ('patrimonial', 'incidence patrimoniale'),
                ('classified', 'bien classé'),
        )
        return DisplayList(vocabulary)


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
    schema.moveField('basement', after='RCU')
    schema.moveField('ZIP', after='basement')
    schema.moveField('pollution', after='ZIP')
    schema.moveField('folderCategoryTownship', after='pollution')
    schema.moveField('SDC', after='protectedBuildingDetails')
    schema.moveField('sdcDetails', after='SDC')
    schema.moveField('regional_guide', after='reparcellingDetails')
    schema.moveField('regional_guide_details', after='regional_guide')
    schema.moveField('township_guide', after='sdcDetails')
    schema.moveField('township_guide_details', after='township_guide')
    schema.moveField('patrimony', pos='top')
    schema.moveField('regional_inventory_building', after='patrimony')
    schema.moveField('patrimony_archaeological_map', after='regional_inventory_building')
    schema.moveField('patrimony_architectural_complex', after='patrimony_archaeological_map')
    schema.moveField('communal_inventory', after='patrimony_architectural_complex')
    schema.moveField('regional_inventory', after='communal_inventory')
    schema.moveField('patrimony_monument', after='regional_inventory')
    schema.moveField('small_popular_patrimony', after='patrimony_monument')
    schema.moveField('patrimony_project_gtoret_1ha', after='small_popular_patrimony')
    schema.moveField('patrimony_site', after='patrimony_project_gtoret_1ha')
    schema.moveField('archeological_site', after='patrimony_site')
    schema.moveField('protection_zone', after='archeological_site')
    schema.moveField('classification_order_scope', after='protection_zone')
    schema.moveField('general_disposition', after='classification_order_scope')
    schema.moveField('protectedBuilding', after='general_disposition')
    schema.moveField('protectedBuildingDetails', after='protectedBuilding')
    schema.moveField('patrimony_analysis', after='protectedBuildingDetails')
    schema.moveField('patrimony_observation', after='patrimony_analysis')
    schema['referenceDGATLP'].widget.label = _('urban_label_notaryReference')
    return schema

finalizeSchema(UrbanCertificateBase_schema)
##/code-section module-footer

