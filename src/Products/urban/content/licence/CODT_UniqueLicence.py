# -*- coding: utf-8 -*-
#
# File: CODT_UniqueLicence.py
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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.CODT_UniqueLicenceInquiry import CODT_UniqueLicenceInquiry
from Products.urban.content.CODT_UniqueLicenceInquiry import finalizeSchema as thirdBaseFinalizeSchema
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.urban.content.licence.CODT_BaseBuildLicence import finalizeSchema as firstBaseFinalizeSchema
from Products.urban.content.licence.CODT_BuildLicence import finalizeSchema as secondBaseFinalizeSchema
from Products.urban.content.licence.EnvironmentBase import EnvironmentBase
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForCODT_UniqueLicenceInquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
optional_fields = [
    'referenceSPE', 'referenceFT', 'environmentTechnicalRemarks',
    'claimsSynthesis', 'conclusions', 'commentsOnSPWOpinion',
]

slave_fields_ = (
    {
        'name': 'annoncedDelay',
        'action': 'value',
        'vocab_method': 'getProrogationDelays',
        'control_param': 'values',
    },
)
##/code-section module-header

schema = Schema((

    StringField(
        name='referenceSPE',
        widget=StringField._properties['widget'](
            size=30,
            label=_('urban_label_referenceSPE', default='Referencespe'),
        ),
        schemata='urban_description',
    ),

    StringField(
        name='referenceFT',
        widget=StringField._properties['widget'](
            size=30,
            label=_('urban_label_referenceFT', default='Referenceft'),
        ),
        schemata='urban_description',
    ),
    StringField(
        name='authority',
        widget=SelectionWidget(
            label=_('urban_label_authority', default='Authority'),
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('authority', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    StringField(
        name='folderTendency',
        widget=SelectionWidget(
            format='select',
            label=_('urban_label_folderTendency', default='Foldertendency'),
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        vocabulary=UrbanVocabulary('foldertendencies', with_empty_value=True),
        default_method='getDefaultValue',
    ),
    ReferenceField(
        name='rubrics',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory='portal_urban/rubrics',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            base_query='rubrics_base_query',
            label=_('urban_label_rubrics', default='Rubrics'),
        ),
        allowed_types=('EnvironmentRubricTerm',),
        schemata='urban_environment',
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
            label=_('urban_label_minimumLegalConditions', default='Minimumlegalconditions'),
        ),
        schemata="urban_environment",
        multiValued=True,
        relationship='minimumconditions',
    ),
    ReferenceField(
        name='additionalLegalConditions',
        widget=ReferenceBrowserWidget(
            allow_browse=True,
            allow_search=True,
            default_search_index='Title',
            startup_directory='portal_urban/exploitationconditions',
            restrict_browsing_to_startup_directory=True,
            wild_card_search=True,
            label=_('urban_label_additionalLegalConditions', default='Additionallegalconditions'),
        ),
        allowed_types=('UrbanVocabularyTerm',),
        schemata="urban_environment",
        multiValued=True,
        relationship='additionalconditions',
    ),
    TextField(
        name='locationTechnicalAdviceAfterInquiry',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_locationTechnicalAdviceAfterInquiry',
                    default='Environmenttechnicaladviceafterinquiry'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_analysis',
        default_output_type='text/html',
    ),
    TextField(
        name='claimsSynthesis',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_claimsSynthesis', default='Claimssynthesis'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='environmentTechnicalAdviceAfterInquiry',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_environmentTechnicalAdviceAfterInquiry',
                    default='Environmenttechnicaladviceafterinquiry'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='commentsOnSPWOpinion',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_commentsOnSPWOpinion',
                    default='Commentsonspwopinion'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='conclusions',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_conclusions', default='Conclusions'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='environmentTechnicalRemarks',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_environmentTechnicalRemarks',
                    default='Environmenttechnicalremarks'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_UniqueLicence_schema = BaseFolderSchema.copy() + \
    getattr(BaseBuildLicence, 'schema', Schema(())).copy() + \
    getattr(CODT_BaseBuildLicence, 'schema', Schema(())).copy() + \
    getattr(CODT_UniqueLicenceInquiry, 'schema', Schema(())).copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
CODT_UniqueLicence_schema['title'].required = False
CODT_UniqueLicence_schema.delField('rgbsr')
CODT_UniqueLicence_schema.delField('rgbsrDetails')
CODT_UniqueLicence_schema.delField('SSC')
CODT_UniqueLicence_schema.delField('sscDetails')
CODT_UniqueLicence_schema.delField('RCU')
CODT_UniqueLicence_schema.delField('rcuDetails')
CODT_UniqueLicence_schema.delField('composition')
setSchemataForCODT_UniqueLicenceInquiry(CODT_UniqueLicence_schema)
##/code-section after-schema


class CODT_UniqueLicence(BaseFolder, CODT_UniqueLicenceInquiry, CODT_BaseBuildLicence, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_UniqueLicence)

    meta_type = 'CODT_UniqueLicence'
    _at_rename_after_creation = True

    schema = CODT_UniqueLicence_schema

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('class_1', 'Classe 1'),
            ('class_2', 'Classe 2'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        delay = 90

        if unknown:
            return ''
        elif 'class_2' in selection:
            delay = 90
        elif 'class_1' in selection:
            delay = 140

        if self.prorogation:
            delay += 30

        return '{}j'.format(str(delay))

    def getLastTransmitToSPW(self):
        return self.getLastEvent(interfaces.ITransmitToSPWEvent)

    def getLastCollegeOpinionTransmitToSPW(self):
        return self.getLastEvent(interfaces.ICollegeOpinionTransmitToSPWEvent)

    def getLastDecisionProjectFromSPW(self):
        return self.getLastEvent(interfaces.IDecisionProjectFromSPWEvent)

    def getLastWalloonRegionDecisionEvent(self):
        return self.getLastEvent(interfaces.IWalloonRegionDecisionEvent)

    def getLastImpactStudyEvent(self):
        return self.getLastEvent(interfaces.IImpactStudyEvent)


registerType(CODT_UniqueLicence, PROJECTNAME)
# end of class CODT_UniqueLicence

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('referenceSPE', after='reference')
    schema.moveField('referenceFT', after='referenceDGATLP')
    schema.moveField('authority', before='folderCategory')
    schema.moveField('folderTendency', after='folderCategory')
    schema.moveField('rubrics', after='folderTendency')
    schema.moveField('rubricsDetails', after='rubrics')
    schema.moveField('minimumLegalConditions', after='rubricsDetails')
    schema.moveField('additionalLegalConditions', after='minimumLegalConditions')
    schema.moveField('description', after='impactStudy')
    schema.moveField('locationTechnicalAdviceAfterInquiry', after='locationTechnicalAdvice')

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
firstBaseFinalizeSchema(CODT_UniqueLicence_schema)
secondBaseFinalizeSchema(CODT_UniqueLicence_schema)
thirdBaseFinalizeSchema(CODT_UniqueLicence_schema)
finalizeSchema(CODT_UniqueLicence_schema)
##/code-section module-footer
