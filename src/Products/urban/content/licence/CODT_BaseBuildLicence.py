# -*- coding: utf-8 -*-
#
# File: CODT_BaseBuildLicence.py
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
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.CODT_Inquiry import CODT_Inquiry
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setSchemataForCODT_Inquiry
##/code-section module-header

schema = Schema((
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_BaseBuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(BaseBuildLicence, 'schema', Schema(())).copy() + \
    getattr(CODT_Inquiry, 'schema', Schema(())).copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
CODT_BaseBuildLicence_schema['title'].required = False
#put the the fields coming from Inquiry in a specific schemata
setSchemataForCODT_Inquiry(CODT_BaseBuildLicence_schema)
##/code-section after-schema


class CODT_BaseBuildLicence(BaseFolder, CODT_Inquiry,  BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_BaseBuildLicence)

    _at_rename_after_creation = True

    schema = CODT_BaseBuildLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('internal_opinions', 'Sollicitation d\'avis internes'),
            ('external_opinions', 'Sollicitation d\'avis externes'),
            ('light_inquiry', 'Instruction d\'une annonce de projet'),
            ('inquiry', 'Instruction d\'une enquête publique'),
            ('FD', 'Sollicitation du fonctionnaire délégué'),
        )
        return DisplayList(vocab)

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        unknown = 'ukn' in selection
        opinions = 'external_opinions' in selection
        inquiry = 'inquiry' in selection or 'light_inquiry' in selection
        FD = 'FD' in selection

        if unknown:
            return ''
        elif (opinions or inquiry) and FD:
            return '115j'
        elif not opinions and not inquiry and not FD:
            return '30j'
        else:
            return '75j'


# end of class CODT_BaseBuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized


def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('roadAdaptation', before='roadTechnicalAdvice')
    schema.moveField('architects', after='workLocations')
    schema.moveField('foldermanagers', after='architects')
    schema.moveField('workType', after='folderCategory')
    schema.moveField('parcellings', after='isInSubdivision')
    schema.moveField('description', after='usage')
    schema.moveField('roadMiscDescription', after='roadEquipments')
    schema.moveField('locationTechnicalRemarks', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('requirementFromFD', before='annoncedDelay')
    schema.moveField('townshipCouncilFolder', after='futureRoadCoating')
    schema.moveField('annoncedDelayDetails', after='annoncedDelay')
    schema.moveField('impactStudy', after='annoncedDelayDetails')
    schema.moveField('procedureChoice', before='description')
    schema.moveField('exemptFDArticle', after='procedureChoice')
    schema.moveField('water', after='futureRoadCoating')
    schema.moveField('electricity', before='water')
    schema.moveField('composition', before='missingParts')
    schema.moveField('announcementArticlesText', before='derogation')
    schema.moveField('announcementArticles', before='announcementArticlesText')
    schema.moveField('divergenceDetails', before='announcementArticles')
    schema.moveField('divergence', before='divergenceDetails')
    schema.moveField('inquiry_type', before='divergence')
    schema['missingParts'].widget.format = None
    return schema

finalizeSchema(CODT_BaseBuildLicence_schema)
##/code-section module-footer
