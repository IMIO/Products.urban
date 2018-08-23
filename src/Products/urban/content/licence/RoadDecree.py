# -*- coding: utf-8 -*-
#
from Products.Archetypes.atapi import *
from Products.MasterSelectWidget.MasterMultiSelectWidget import MasterMultiSelectWidget
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import *
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence
from Products.urban.widget.urbanreferencewidget import UrbanReferenceWidget
from zope.interface import implements

##code-section module-header #fill in your manual code here
##/code-section module-header

slave_fields_decisionalDelays = (
    {
        'name': 'decisionalDelays',
        'action': 'value',
        'vocab_method': 'getDecisionalDelays',
        'control_param': 'values',
    },
)

schema = Schema((
    BooleanField(
            name='IsAlignment_plan',
            default=False,
            widget=BooleanField._properties['widget'](
                    label=_('urban_label_IsAlignment_plan',
                            default='IsAlignment_plan'),
            ),
            schemata='urban_road',
    ),
    StringField(
            name='road_decree_reference',
            widget=UrbanReferenceWidget(
                    label=_('urban_label_pe_reference', default='road_decree_reference'),
                    portal_types=['CODT_BuildLicence', 'CODT_UniqueLicence', 'CODT_IntegratedLicence',
                                  'CODT_Article127'],
            ),
            required=False,
            schemata='urban_description',
            default_method='getDefaultText',
            validators=('isReference',),
    ),
    StringField(
            name='commune_choices',
            default='ukn',
            widget=MasterSelectWidget(
                    label='commune_choices',
                    label_msgid='urban_commune',
                    i18n_domain='urban',
            ),
            schemata='urban_road',
            multiValued=1,
            vocabulary=UrbanVocabulary('townroaddecree'),
    ),
    StringField(
            name='missing_piece_choices',
            default='ukn',
            widget=MasterSelectWidget(
                    label='missing_piece_choices',
                    label_msgid='urban_missing_piece_choices',
                    i18n_domain='urban',
            ),
            schemata='urban_road',
            multiValued=1,
            vocabulary=UrbanVocabulary('roadmissingpiece'),
    ),
    TextField(
            name='missing_piece_details',
            allowable_content_types=('text/html',),
            widget=RichWidget(
                    label=_('missing_piece_details', default='missing_piece_details'),
            ),
            default_content_type='text/html',
            default_method='getDefaultText',
            schemata='urban_road',
            default_output_type='text/html',
    ),
    LinesField(
            name='decisionalChoice',
            default='75j',
            widget=MasterMultiSelectWidget(
                    format='checkbox',
                    slave_fields=slave_fields_decisionalDelays,
                    label=_('urban_label_class', default='DecisionalMeeting'),
            ),
            required=True,
            schemata='urban_description',
            multiValued=1,
            vocabulary='decisionaldelay',
    ),
    StringField(
            name='decisionalDelays',
            widget=SelectionWidget(
                    label=_('urban_label_annoncedDelay', default='Annonceddelay'),
            ),
            schemata='urban_description',
            vocabulary='decisionaldelay',
            default_method='getDefaultValue',
    ),
),
)

# StringField(
#         name='decisionnaldelay',
#         widget=SelectionWidget(
#                 label=_('urban_label_class', default='Class'),
#         ),
#         vocabulary='decisionnaldelay',
#         required=True,
#         schemata='urban_description',
#         default_method='getDefaultValue',
# ),
##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RoadDecree_schema = CODT_BuildLicence.schema.copy() + schema.copy()


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RoadDecree(CODT_BuildLicence):
    """
    """
    implements(interfaces.IRoadDecree)

    meta_type = 'RoadDecree'

    RoadDecree_schema['roadAdaptation'].schemata = 'urban_road'

    schema = RoadDecree_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header
    def decisionaldelay(self):
        vocabulary = (
            ('75j', _('75 days')),
            ('105j', _('105 days')),
            ('150j', _('150 days')),
            ('210j', _('210 days')),
        )
        return DisplayList(vocabulary)


def getDecisionalDelays(self, *values):
    print "-------"
    # selection = [v['val'] for v in values if v['selected']]
    # unknown = 'ukn' in selection
    # opinions = 'IsAlignment_plan' in selection
    # inquiry = 'inquiry' in selection
    # FD = 'FD' in selection
    # print "fooo"
    #
    # if unknown:
    #     return ''
    # elif (opinions or inquiry) and FD:
    #     return '115j'
    # elif opinions and inquiry and not FD:
    #     return '70j'
    # elif opinions and not (inquiry or FD):
    #     return '70j'
    # elif inquiry and not (opinions or FD):
    #     return '70j'
    # elif FD and not (opinions or inquiry):
    #     return '75j'


registerType(RoadDecree, PROJECTNAME)
# end of class EnvClassOne

##code-section module-footer #fill in your manual code here

##/code-section module-footer
