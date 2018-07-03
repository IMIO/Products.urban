# -*- coding: utf-8 -*-
#
# File: CODT_BaseBuildLicence.py
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
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban import interfaces
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.CODT_Inquiry import CODT_Inquiry
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForCODT_Inquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
##/code-section module-header

optional_fields = [
    'SCT', 'sctDetails', 'SDC', 'sdcDetails', 'regional_guide', 'regional_guide_details',
    'township_guide', 'township_guide_details', 'prorogation',
]

slave_fields_prorogation = (
    {
        'name': 'annoncedDelay',
        'action': 'value',
        'vocab_method': 'getProrogationDelays',
        'control_param': 'values',
    },
)


slave_fields_form_composition = (
    {
        'name': 'missingParts',
        'action': 'vocabulary',
        'vocab_method': 'getCompositionMissingParts',
        'control_param': 'values',
    },
)
schema = Schema((
    BooleanField(
        name='prorogation',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_prorogation,
            label=_('urban_label_prorogation', default='Prorogation'),
        ),
        schemata='urban_analysis',
    ),
    LinesField(
        name='form_composition',
        widget=MasterMultiSelectWidget(
            format='checkbox',
            slave_fields=slave_fields_form_composition,
            label=_('urban_label_form_composition', default='Form_composition'),
        ),
        schemata='urban_analysis',
        multiValued=1,
        vocabulary=UrbanVocabulary('form_composition', inUrbanConfig=False),
    ),
    LinesField(
        name='SCT',
        widget=MultiSelectionWidget(
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
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label=_('urban_label_sctDetails', default='Sctdetails'),
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='SDC',
        widget=MultiSelectionWidget(
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
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label=_('urban_label_sdcDetails', default='Sdcdetails'),
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='township_guide',
        widget=MultiSelectionWidget(
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
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label=_('urban_label_township_guide_details',
                    default='Township_guide_details'),
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
    LinesField(
        name='regional_guide',
        widget=MultiSelectionWidget(
            label=_('urban_label_regional_guide', default='Regional_guide'),
        ),
        schemata='urban_location',
        vocabulary=UrbanVocabulary('regional_guide', inUrbanConfig=False, with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='regional_guide_details',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label=_('urban_label_regional_guide_details',
                    default='Regional_guide_details'),
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/plain',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_BaseBuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(BaseBuildLicence, 'schema', Schema(())).copy() + \
    getattr(CODT_Inquiry, 'schema', Schema(())).copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
CODT_BaseBuildLicence_schema['title'].required = False
CODT_BaseBuildLicence_schema.delField('rgbsr')
CODT_BaseBuildLicence_schema.delField('rgbsrDetails')
CODT_BaseBuildLicence_schema.delField('SSC')
CODT_BaseBuildLicence_schema.delField('sscDetails')
CODT_BaseBuildLicence_schema.delField('RCU')
CODT_BaseBuildLicence_schema.delField('rcuDetails')
CODT_BaseBuildLicence_schema.delField('composition')
#put the the fields coming from Inquiry in a specific schemata
setSchemataForCODT_Inquiry(CODT_BaseBuildLicence_schema)
##/code-section after-schema


class CODT_BaseBuildLicence(BaseFolder, CODT_Inquiry,  BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_BaseBuildLicence)

    _at_rename_after_creation = True

    schema = CODT_BaseBuildLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('internal_opinions', 'Sollicitation d\'avis internes'),
            ('external_opinions', 'Sollicitation d\'avis externes'),
            ('light_inquiry', 'Annonce de projet'),
            ('initiative_light_inquiry', 'Annonce de projet d\'initiative'),
            ('inquiry', 'Enquête publique'),
            ('initiative_inquiry', 'Enquête publique d\'initiative'),
            ('FD', 'Sollicitation du fonctionnaire délégué'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        opinions = 'external_opinions' in selection
        inquiry = 'inquiry' in selection or 'light_inquiry' in selection
        FD = 'FD' in selection
        delay = 75

        if unknown:
            return ''
        elif (opinions or inquiry) and FD:
            delay = 115
        elif not opinions and not inquiry and not FD:
            delay = 30

        if self.prorogation:
            delay += 30

        return '{}j'.format(str(delay))

    def getProrogationDelays(self, *values):
        procedure_choice = [{'val': v, 'selected': True} for v in self.getProcedureChoice()]
        base_delay = self.getProcedureDelays(*procedure_choice)
        if self.prorogation:
            base_delay = '{}j'.format(str(int(base_delay[:-1]) - 30))

        if False in values:
            return base_delay

        prorogated_delay = ''
        if base_delay:
            prorogated_delay = '{}j'.format(str(int(base_delay[:-1]) + 30))

        return prorogated_delay

    security.declarePublic('listRequirementsFromFD')

    def listRequirementsFromFD(self):
        """
          This vocabulary for field requirementsFromFD returns this list: decision, opinion
        """
        vocab = (
            ('opinion', 'location_fdrequirement_opinion'),
            ('decision', 'location_fdrequirement_decision'),
            ('optional', 'location_fdrequirement_optional'),
        )
        return DisplayList(vocab)

    def getCompositionMissingParts(self, *values):
        """
        """
        selection = [v['val'] for v in values if v['selected']]
        urban_voc = self.schema['missingParts'].vocabulary
        all_terms = urban_voc.listAllVocTerms(self)

        display_values = []

        for term in all_terms:
            for composition in selection:
                if str(composition) in term.getExtraValue() or not term.getExtraValue():
                    display_values.append((term.id, term.Title().decode('utf-8')))
                    break

        return DisplayList(display_values)

    def getLastProcedureChoiceNotification(self):
        return self.getLastEvent(interfaces.ICODTProcedureChoiceNotified)

    def getLastDefaultAcknowledgment(self):
        return self.getLastEvent(interfaces.IDefaultCODTAcknowledgmentEvent)


# end of class CODT_BaseBuildLicence

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
    schema.moveField('prorogation', after='annoncedDelayDetails')
    schema.moveField('impactStudy', after='prorogation')
    schema.moveField('procedureChoice', before='description')
    schema.moveField('exemptFDArticle', after='procedureChoice')
    schema.moveField('water', after='futureRoadCoating')
    schema.moveField('electricity', before='water')
    schema.moveField('derogationDetails', after='derogation')
    schema.moveField('announcementArticlesText', before='derogation')
    schema.moveField('announcementArticles', before='announcementArticlesText')
    schema.moveField('divergenceDetails', before='announcementArticles')
    schema.moveField('divergence', before='divergenceDetails')
    schema.moveField('inquiry_type', before='divergence')
    schema.moveField('SDC', after='protectedBuildingDetails')
    schema.moveField('sdcDetails', after='SDC')
    schema.moveField('regional_guide', after='reparcellingDetails')
    schema.moveField('regional_guide_details', after='regional_guide')
    schema.moveField('township_guide', after='sdcDetails')
    schema.moveField('township_guide_details', after='township_guide')
    schema.moveField('form_composition', before='missingParts')
    schema['missingParts'].widget.format = None
    schema['parcellings'].widget.label = _('urban_label_parceloutlicences')
    schema['isInSubdivision'].widget.label = _('urban_label_is_in_parceloutlicences')
    schema['subdivisionDetails'].widget.label = _('urban_label_parceloutlicences_details')
    schema['pca'].widget.label = _('urban_label_sol')
    schema['pcaZone'].widget.label = _('urban_label_solZone')
    schema['isInPCA'].widget.label = _('urban_label_is_in_sol')
    schema['pcaDetails'].widget.label = _('urban_label_sol_details')
    schema['exemptFDArticle'].widget.label = _('urban_label_exemptFDArticleCODT')
    schema['implantation'].widget.label = _('urban_label_implantationCODT')
    schema['pca'].vocabulary = UrbanVocabulary('sols', vocType="PcaTerm", inUrbanConfig=False)
    schema['pcaZone'].vocabulary_factory = 'urban.vocabulary.SOLZones'
    return schema

finalizeSchema(CODT_BaseBuildLicence_schema)
##/code-section module-footer
