# -*- coding: utf-8 -*-
#
# File: CODT_Article127.py
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
from Products.urban.content.licence.BuildLicence import finalizeSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_Article127_schema = BaseFolderSchema.copy() + \
    getattr(CODT_BaseBuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class CODT_Article127(BaseFolder, CODT_BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_Article127)

    meta_type = 'CODT_Article127'
    _at_rename_after_creation = True

    schema = CODT_Article127_schema

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

        if unknown:
            return ''
        elif opinions and inquiry:
            return '70j'
        elif opinions and not inquiry:
            return '30j'
        else:
            return '30j'

    def getLastWalloonRegionDecisionEvent(self, use_catalog=True):
        return self._getLastEvent(interfaces.IWalloonRegionDecisionEvent, use_catalog)


registerType(CODT_Article127, PROJECTNAME)
# end of class CODT_Article127

##code-section module-footer #fill in your manual code here

#finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
finalizeSchema(CODT_Article127_schema)
##/code-section module-footer
