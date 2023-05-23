# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from zope.interface import implements

from plone import api

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import *
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence

import copy

slave_fields_bound_licence = (
    {
        'name': 'workLocations',
        'action': 'hide',
        'hide_values': (True, ),
    },
    {
        'name': 'architects',
        'action': 'hide',
        'hide_values': (True, ),
    },
)
slave_fields_townships = (
    {
        'name': 'decisional_delay',
        'action': 'value',
        'vocab_method': 'get_decisional_delays',
        'control_param': 'values',
    },
)

class TownshipVocabulary(UrbanVocabulary):

    def get_raw_voc(self, context, licence_type):
        voc = super(TownshipVocabulary, self).get_raw_voc(context, licence_type)
        new_terms = copy.deepcopy(voc)
        for term in new_terms:
            term['id'] = term['id'] + '_alignement'
            term['title'] = term['title'] + " (Modification plan d'alignement)"
        new_voc = voc + new_terms
        return new_voc

schema = Schema((
    ReferenceField(
        name='bound_licence',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=False,
            force_close_on_insert=True,
            startup_directory='urban',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            label=_('urban_label_bound_licence', default='Bound licence'),
        ),
        allowed_types=[
            t for t in URBAN_TYPES
            if t not in [
                'Inspection',
                'Ticket',
                'ProjectMeeting',
                'PatrimonyCertificate',
                'CODT_NotaryLetter',
                'CODT_UrbanCertificateOne',
                'NotaryLetter',
                'UrbanCertificateOne',
                'EnvClassThree',
                'RoadDecree',
            ]
        ],
        schemata='urban_description',
        multiValued=False,
        relationship="bound_licence",
    ),
    BooleanField(
        name='use_bound_licence_infos',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_bound_licence,
            label=_('urban_label_use_bound_licence_infos', default='Use_bound_licence_infos'),
        ),
        schemata='urban_description',
    ),
    StringField(
        name='townships_and_alignment',
        default='ukn',
        widget=MasterSelectWidget(
            slave_fields=slave_fields_townships,
            label=_('urban_label_townships_and_alignment', default='Townships_and_alignment'),
        ),
        schemata='urban_analysis',
        multiValued=1,
        vocabulary=TownshipVocabulary('townships', with_empty_value=True),
    ),
    StringField(
        name='decisional_delay',
        widget=SelectionWidget(
            label=_('urban_label_decisional_delay',
                    default='DecisionalDelay'),
        ),
        schemata='urban_analysis',
        vocabulary='list_decisional_delay',
        default_method='getDefaultValue',
    ),
),
)
RoadDecree_schema = CODT_BuildLicence.schema.copy() + schema.copy()
del RoadDecree_schema['usage']
del RoadDecree_schema['form_composition']
del RoadDecree_schema['annoncedDelay']
del RoadDecree_schema['annoncedDelayDetails']
del RoadDecree_schema['delayAfterModifiedBlueprints']
del RoadDecree_schema['delayAfterModifiedBlueprintsDetails']
del RoadDecree_schema['financial_caution']
del RoadDecree_schema['exemptFDArticle']
del RoadDecree_schema['requirementFromFD']


class RoadDecree(CODT_BuildLicence):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRoadDecree)

    meta_type = 'RoadDecree'
    RoadDecree_schema['roadAdaptation'].schemata = 'urban_road'
    schema = RoadDecree_schema


    security.declarePublic('getReferenceDGATLP')

    def getReferenceDGATLP(self):
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                return bound_licence.getReferenceDGATLP()

        field = self.getField('referenceDGATLP')
        reference = field.get(self)
        return reference

    security.declarePublic('getImpactStudy')

    def getImpactStudy(self):
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                return bound_licence.getImpactStudy()

        field = self.getField('impactStudy')
        impact_study = field.get(self)
        return impact_study

    security.declarePublic('getWorkLocations')

    def getWorkLocations(self):
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                return bound_licence.getWorkLocations()

        field = self.getField('workLocations')
        worklocations = field.get(self)
        return worklocations

    security.declarePublic('getParcels')

    def getParcels(self):
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                return bound_licence.getParcels()

        return super(RoadDecree, self).getParcels()

    security.declarePublic('getOfficialParcels')

    def getOfficialParcels(self):
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                return bound_licence.getOfficialParcels()

        return super(RoadDecree, self).getOfficialParcels()

    security.declarePublic('getApplicants')

    def getApplicants(self):
        """
        """
        applicants = super(RoadDecree, self).getApplicants()
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                applicants.extend(bound_licence.getApplicants())
        return list(set(applicants))

    security.declarePublic('get_applicants_history')

    def get_applicants_history(self):
        applicants = super(RoadDecree, self).get_applicants_history()
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                applicants.extend(bound_licence.get_applicants_history())
        return list(set(applicants))

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'enabled']
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                corporations.extend(bound_licence.getCorporations())
        return list(set(corporations))

    security.declarePublic('get_corporations_history')

    def get_corporations_history(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'disabled']
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                corporations.extend(bound_licence.get_corporations_history())
        return list(set(corporations))

    security.declarePublic('getArchitects')

    def getArchitects(self):
        architects = RoadDecree_schema['architects'].get(self)
        if self.getUse_bound_licence_infos():
            bound_licence = self.getBound_licence()
            if bound_licence:
                architects = bound_licence.getArchitects()
        return architects

    def list_inquiry_types(self):
        """
        """
        vocabulary = (
            ('inquiry', 'Enquête publique'),
        )
        return DisplayList(vocabulary)

    security.declarePublic('listProcedureChoices')

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('internal_opinions', 'Sollicitation d\'avis internes'),
            ('external_opinions', 'Sollicitation d\'avis externes'),
            ('inquiry', 'Enquête publique'),
        )
        return DisplayList(vocab)

    security.declarePublic('list_decisional_delay')

    def list_decisional_delay(self):
        vocabulary = (
            ('ukn', _('unknown')),
            ('75j', _('75 days')),
            ('105j', _('105 days')),
            ('150j', _('150 days')),
            ('210j', _('210 days')),
        )
        return DisplayList(vocabulary)

    def get_decisional_delays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        municipality = selection and selection[0] or 'ukn'
        external_municipality = not municipality.startswith('township')
        alignment = municipality.endswith('_alignement')

        if external_municipality and alignment:
            return '210j'
        if alignment:
            return '150j'
        if external_municipality:
            return '105j'
        return '75j'

    def getLastDisplayingTheDecision(self):
        return self.getLastEvent(interfaces.IDisplayingTheDecisionEvent)


registerType(RoadDecree, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('bound_licence', before='workLocations')
    schema.moveField('use_bound_licence_infos', after='bound_licence')
    schema.moveField('townships_and_alignment', after='missingPartsDetails')
    schema.moveField('decisional_delay', after='townships_and_alignment')
    schema['locationTechnicalAdvice'].widget.label = _(
        'urban_label_technicalAdvice',
        default='technicaladvice',
    )
    schema['roadAdaptation'].schemata = 'urban_analysis'
    schema['inquiry_type'].default = 'inquiry'
    RoadDecree_schema['prorogation'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    RoadDecree_schema['prorogationModifiedBp'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    RoadDecree_schema['announcementArticles'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    RoadDecree_schema['announcementArticlesText'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    return schema


finalize_schema(RoadDecree_schema)
