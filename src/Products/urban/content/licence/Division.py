# -*- coding: utf-8 -*-
#
# File: Division.py
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

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.urban.utils import setOptionalAttributes
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

optional_fields = []
##/code-section module-header


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
            allow_search=True,
            only_for_review_states='enabled',
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='urban/notaries',
            restrict_browsing_to_startup_directory=True,
            label=_('urban_label_notaryContact', default='Notary(ies)'),
            popup_name='contact_reference_popup'
        ),
        required=False,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types= ('Notary',),
    ),
    StringField(
        name='patrimony',
        default='none',
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
),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Division_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Division_schema['title'].required = False
##/code-section after-schema


class Division(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IDivision)

    meta_type = 'Division'
    _at_rename_after_creation = True

    schema = Division_schema

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

    security.declarePublic('updateTitle')

    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        notaries = ''
        proprietaries = ''
        if self.getProprietaries:
            proprietaries = ', '.join([prop.Title() for prop in self.getProprietaries()])
        else:
            proprietaries = translate('no_proprietary_defined', 'urban', context=self.REQUEST).encode('utf8')
        if self.getNotaryContact():
            notaries = ', '.join([notar.Title() for notar in self.getNotaryContact()])
        else:
            notaries = translate('no_notary_defined', 'urban', context=self.REQUEST).encode('utf8')

        if proprietaries and notaries:
            title = "%s - %s - %s" % (self.getReference(), proprietaries, notaries)
        elif proprietaries:
            title = "%s - %s" % (self.getReference(), proprietaries)
        elif notaries:
            title = "%s - %s" % (self.getReference(), notaries)
        else:
            title = self.getReference()
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)


    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)

    def list_patrimony_types(self):
        """
        """
        vocabulary = (
                ('none', 'aucune incidence'),
                ('patrimonial', 'incidence patrimoniale'),
                ('classified', 'bien classé'),
        )
        return DisplayList(vocabulary)


registerType(Division, PROJECTNAME)
# end of class Division


##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('description', after='notaryContact')
    schema.moveField('foldermanagers', after='workLocations')
    schema['parcellings'].widget.label = _('urban_label_parceloutlicences')
    schema['isInSubdivision'].widget.label = _('urban_label_is_in_parceloutlicences')
    schema['subdivisionDetails'].widget.label = _('urban_label_parceloutlicences_details')
    schema['pca'].vocabulary = UrbanVocabulary('sols', vocType="PcaTerm", inUrbanConfig=False)
    schema['pca'].widget.label = _('urban_label_sol')
    schema['pcaZone'].vocabulary_factory = 'urban.vocabulary.SOLZones'
    schema['pcaZone'].widget.label = _('urban_label_solZone')
    schema['isInPCA'].widget.label = _('urban_label_is_in_sol')
    schema['pcaDetails'].widget.label = _('urban_label_sol_details')
    return schema


finalizeSchema(Division_schema)
##/code-section module-footer
