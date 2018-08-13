# -*- coding: utf-8 -*-
#
from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.config import *
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban.widget.urbanreferencewidget import UrbanReferenceWidget


##code-section module-header #fill in your manual code here
##/code-section module-header



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
            name='communechoices',
            default='ukn',
            widget=MasterSelectWidget(
                    label='Commune test',
                    label_msgid='urban_label_test',
                    i18n_domain='urban',
            ),
            schemata='urban_description',
            multiValued=1,
            vocabulary=UrbanVocabulary('town_roaddecree'),
    ),
    StringField(
            name='pe_reference',
            widget=UrbanReferenceWidget(
                    label=_('urban_label_pe_reference', default='PE Reference'),
                    portal_types=['CODT_BuildLicence', 'CODT_UniqueLicence', 'CODT_IntegratedLicence', 'CODT_Article127'],
            ),
            required=False,
            schemata='urban_description',
            default_method='getDefaultText',
            validators=('isReference', ),
    ),
),
)

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
    def listEnvClassChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('EnvClassOne', 'classe 1'),
            ('EnvClassTwo', 'classe 2'),

        )
        return DisplayList(vocab)


registerType(RoadDecree, PROJECTNAME)
# end of class EnvClassOne

##code-section module-footer #fill in your manual code here

##/code-section module-footer
