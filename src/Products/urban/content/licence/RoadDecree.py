# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import *
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence

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
                'CODT_UrbanCertificateOne'
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
    BooleanField(
        name='IsAlignment_plan',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_IsAlignment_plan',
                    default='IsAlignment_plan'),
        ),
        schemata='urban_analysis',
    ),
    StringField(
        name='townships',
        default='ukn',
        widget=MasterSelectWidget(
            label=_('urban_label_townships', default='Townships'),
        ),
        schemata='urban_analysis',
        multiValued=1,
        vocabulary=UrbanVocabulary('townships', with_empty_value=True),
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


class RoadDecree(CODT_BuildLicence):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRoadDecree)

    meta_type = 'RoadDecree'
    RoadDecree_schema['roadAdaptation'].schemata = 'urban_road'
    schema = RoadDecree_schema

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

    def getDecisional_delay(self, *values):
        alignment = getattr(self, 'IsAlignment_plan', False)
        municipality = getattr(self, 'townships', 'ukn')
        external_municipality = municipality != 'township'

        if external_municipality and alignment:
            return '210j'
        if alignment:
            return '150j'
        if external_municipality:
            return '105j'
        return '75j'


registerType(RoadDecree, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('bound_licence', before='workLocations')
    schema.moveField('use_bound_licence_infos', after='bound_licence')
    schema.moveField('IsAlignment_plan', after='missingPartsDetails')
    schema.moveField('townships', after='IsAlignment_plan')
    schema.moveField('decisional_delay', after='townships')
    schema['locationTechnicalAdvice'].widget.label = _(
        'urban_label_technicalAdvice',
        default='technicaladvice',
    )
    schema['roadAdaptation'].schemata = 'urban_analysis'
    return schema


finalize_schema(RoadDecree_schema)
