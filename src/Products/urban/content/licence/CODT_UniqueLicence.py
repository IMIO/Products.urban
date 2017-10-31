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
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.urban.content.licence.CODT_BuildLicence import finalizeSchema as baseFinalizeSchema
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
optional_fields = [
    'referenceSPE', 'referenceFT'
]
##/code-section module-header

schema = Schema((

    StringField(
        name='referenceSPE',
        widget=StringField._properties['widget'](
            size=30,
            label='Referencespe',
            label_msgid='urban_label_referenceSPE',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),

    StringField(
        name='referenceFT',
        widget=StringField._properties['widget'](
            size=30,
            label='Referenceft',
            label_msgid='urban_label_referenceFT',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    StringField(
        name='authority',
        widget=SelectionWidget(
            label='Authority',
            label_msgid='urban_label_authority',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('authority', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    StringField(
        name='folderTendency',
        widget=SelectionWidget(
            format='select',
            label='Foldertendency',
            label_msgid='urban_label_folderTendency',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        vocabulary=UrbanVocabulary('foldertendencies', with_empty_value=True),
        default_method='getDefaultValue',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_UniqueLicence_schema = BaseFolderSchema.copy() + \
    getattr(CODT_BaseBuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class CODT_UniqueLicence(BaseFolder, CODT_BaseBuildLicence, BrowserDefaultMixin):
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
            ('internal_opinions', 'Sollicitation d\'avis internes'),
            ('external_opinions', 'Sollicitation d\'avis externes'),
            ('light_inquiry', 'Instruction d\'une annonce de projet'),
            ('inquiry', 'Instruction d\'une enquête publique'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        opinions = 'external_opinions' in selection
        inquiry = 'inquiry' in selection or 'light_inquiry' in selection
        delay = 30

        if unknown:
            return ''
        elif opinions and inquiry:
            delay = 70
        elif opinions and not inquiry:
            delay = 70

        if self.prorogation:
            delay += 30

        return '{}j'.format(str(delay))

    def getLastWalloonRegionDecisionEvent(self):
        return self.getLastEvent(interfaces.IWalloonRegionDecisionEvent)


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

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
baseFinalizeSchema(CODT_UniqueLicence_schema)
finalizeSchema(CODT_UniqueLicence_schema)
##/code-section module-footer
