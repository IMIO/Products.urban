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
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.BaseBuildLicence import BaseBuildLicence
from Products.urban.BuildLicence import finalizeSchema
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

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

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UniqueLicence_schema = BaseFolderSchema.copy() + \
    getattr(BaseBuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class UniqueLicence(BaseFolder, BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUniqueLicence)

    meta_type = 'UniqueLicence'
    _at_rename_after_creation = True

    schema = UniqueLicence_schema

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('opinions', 'Sollicitation d\'avis (instance ou service interne/externe)'),
            ('inquiry', 'Instruction d\'une enquête publique'),
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

    def getLastWalloonRegionDecisionEvent(self, use_catalog=True):
        return self._getLastEvent(interfaces.IWalloonRegionDecisionEvent, use_catalog)


registerType(UniqueLicence, PROJECTNAME)
# end of class UniqueLicence

##code-section module-footer #fill in your manual code here

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
finalizeSchema(UniqueLicence_schema)
UniqueLicence_schema.moveField('authority', after='referenceDGATLP')
##/code-section module-footer
