# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import *
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence
from Products.urban.widget.urbanreferencewidget import UrbanReferenceWidget


schema = Schema((
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
        name='road_decree_reference',
        widget=UrbanReferenceWidget(
            label=_('urban_label_road_decree_reference',
                    default='road_decree_reference'),
            portal_types=[
                'CODT_BuildLicence',
                'CODT_UniqueLicence',
                'CODT_IntegratedLicence',
                'CODT_Article127',
            ],
        ),
        required=False,
        schemata='urban_analysis',
        default_method='getDefaultText',
        validators=('isReference',),
    ),
    StringField(
        name='commune_choices',
        default='ukn',
        widget=MasterSelectWidget(
            label=_('urban_label_commune_choices', default='urban_commune'),
        ),
        schemata='urban_analysis',
        multiValued=1,
        vocabulary=UrbanVocabulary('townroaddecree', with_empty_value=False),
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


class RoadDecree(CODT_BuildLicence):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRoadDecree)

    meta_type = 'RoadDecree'
    RoadDecree_schema['roadAdaptation'].schemata = 'urban_road'
    schema = RoadDecree_schema

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
        municipality = getattr(self, 'commune_choices', 'ukn')
        external_municipality = municipality != 'commune'

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
    schema['locationTechnicalAdvice'].widget.label = _(
        'urban_label_technicalAdvice',
        default='technicaladvice',
    )
    schema['roadAdaptation'].schemata = 'urban_analysis'
    schema['decisional_delay'].widget.visible = {
        'view': 'visible',
        'edit': 'invisible',
    }
    return schema


finalize_schema(RoadDecree_schema)
