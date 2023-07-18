# -*- coding: utf-8 -*-
#
# File: UniqueLicence.py
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
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.licence.BaseBuildLicence import finalizeSchema as firstBaseFinalizeSchema
from Products.urban.content.licence.BuildLicence import finalizeSchema as secondBaseFinalizeSchema
from Products.urban.content.licence.EnvironmentBase import EnvironmentBase
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from Products.urban.widget.historizereferencewidget import HistorizeReferenceBrowserWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from plone import api
from DateTime import DateTime
from zope.i18n import translate

##code-section module-header #fill in your manual code here
optional_fields = [
    'referenceSPE', 'environmentTechnicalRemarks',
    'claimsSynthesis', 'conclusions', 'commentsOnSPWOpinion',
    'ftSolicitOpinionsTo'
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
        default_method='getDefaultSPEReference',
    ),
    StringField(
        name='authority',
        widget=SelectionWidget(
            format='select',
            label=_('urban_label_authority', default='Authority'),
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('authority', inUrbanConfig=True, with_empty_value=True),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='ftSolicitOpinionsTo',
        widget=MultiSelect2Widget(
            format='checkbox',
            label=_('urban_label_ftSolicitOpinionsTo', default='Ftsolicitopinionsto'),
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('ftSolicitOpinionsTo', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
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
        default_output_type='text/x-html-safe',
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
        widget=HistorizeReferenceBrowserWidget(
            allow_browse=True,
            allow_search=True,
            default_search_index='Title',
            startup_directory='portal_urban/exploitationconditions',
            restrict_browsing_to_startup_directory=True,
            wild_card_search=True,
            base_query='legalconditions_base_query',
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
        default_output_type='text/x-html-safe',
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
        default_output_type='text/x-html-safe',
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
        default_output_type='text/x-html-safe',
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
        default_output_type='text/x-html-safe',
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
        default_output_type='text/x-html-safe',
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
        default_output_type='text/x-html-safe',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UniqueLicence_schema = BaseFolderSchema.copy() + \
    getattr(BaseBuildLicence, 'schema', Schema(())).copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UniqueLicence_schema['title'].required = False
UniqueLicence_schema.delField('rgbsr')
UniqueLicence_schema.delField('rgbsrDetails')
UniqueLicence_schema.delField('SSC')
UniqueLicence_schema.delField('sscDetails')
UniqueLicence_schema.delField('RCU')
UniqueLicence_schema.delField('rcuDetails')
##/code-section after-schema


class UniqueLicence(BaseFolder, BaseBuildLicence, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUniqueLicence)

    meta_type = 'UniqueLicence'
    _at_rename_after_creation = True

    schema = UniqueLicence_schema

    # Methods

    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        if self.getApplicants():
            applicantTitle = self.getApplicants()[0].Title()
        else:
            applicantTitle = translate('no_applicant_defined', 'urban', context=self.REQUEST).encode('utf8')
        title = "%s - %s - %s - %s" % (
            self.getReferenceSPE(),
            self.getReference(),
            self.getLicenceSubject(),
            applicantTitle
        )
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('opinions', 'Sollicitation d\'avis (instance ou service interne/externe)'),
            ('inquiry', 'Enquête publique'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        opinions = 'opinions' in selection
        inquiry = 'inquiry' in selection

        if unknown:
            return ''
        elif opinions and inquiry:
            return '60j'
        elif opinions and not inquiry:
            return '30j'
        else:
            return '30j'

    def getLastWalloonRegionDecisionEvent(self):
        return self.getLastEvent(interfaces.IWalloonRegionDecisionEvent)

    security.declarePublic('getDefaultSPEReference')

    def getLastImpactStudyEvent(self):
        return self.getLastEvent(interfaces.IImpactStudyEvent)

    def getDefaultSPEReference(self):
        """
          Returns the reference for the new element
        """
        registry = api.portal.get_tool('portal_registry')

        tal_expression = registry['Products.urban.interfaces.ICODT_UniqueLicence_spe_reference_config.tal_expression']
        last_value = registry['Products.urban.interfaces.ICODT_UniqueLicence_spe_reference_config.numerotation']
        last_value = last_value + 1

        #evaluate the numerotationTALExpression and pass it obj, lastValue and self
        data = {
            'obj': self,
            'tool': api.portal.get_tool('portal_urban'),
            'numerotation': str(last_value),
            'portal': api.portal.getSite(),
            'date': DateTime(),
        }
        res = ''
        try:
            ctx = getEngine().getContext(data)
            res = Expression(tal_expression)(ctx)
        except Exception:
            pass
        return res


registerType(UniqueLicence, PROJECTNAME)
# end of class UniqueLicence

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('referenceSPE', after='reference')
    schema.moveField('referenceFT', after='referenceDGATLP')
    schema.moveField('authority', before='folderCategory')
    schema.moveField('rubrics', after='folderCategory')
    schema.moveField('rubricsDetails', after='rubrics')
    schema.moveField('minimumLegalConditions', after='rubricsDetails')
    schema.moveField('additionalLegalConditions', after='minimumLegalConditions')
    schema.moveField('ftSolicitOpinionsTo', after='impactStudy')
    schema.moveField('description', after='ftSolicitOpinionsTo')
    schema.moveField('locationTechnicalAdviceAfterInquiry', after='locationTechnicalAdvice')

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
firstBaseFinalizeSchema(UniqueLicence_schema)
secondBaseFinalizeSchema(UniqueLicence_schema)
finalizeSchema(UniqueLicence_schema)
##/code-section module-footer
