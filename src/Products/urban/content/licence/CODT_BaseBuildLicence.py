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
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban import interfaces
from Products.urban.content.licence.BaseBuildLicence import BaseBuildLicence
from Products.urban.content.CODT_Inquiry import CODT_Inquiry
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setSchemataForCODT_Inquiry
##/code-section module-header

slave_fields_prorogation = (
    {
        'name': 'annoncedDelay',
        'action': 'value',
        'vocab_method': 'getProrogationDelays',
        'control_param': 'values',
    },
)

schema = Schema((
    BooleanField(
        name='prorogation',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_prorogation,
            label='Prorogation',
            label_msgid='urban_label_prorogation',
            i18n_domain='urban',
        ),
        schemata='urban_analysis',
    ),
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

    def getProrogationDelays(self, *values):
        procedure_choice = [{'val': v, 'selected': True} for v in self.getProcedureChoice()]
        base_delay = self.getProcedureDelays(*procedure_choice)
        if False in values:
            return base_delay

        prorogated_delay = ''
        if base_delay:
            prorogated_delay = '{}j'.format(str(int(base_delay[:-1]) + 30))

        return prorogated_delay

    security.declarePublic('listRequirementsFromFD')

    def listRequirementsFromFD(self):
        """
          This vocabulary for field requirementsFromFD returns this list: decision, opinion
        """
        vocab = (
            ('opinion', 'location_fdrequirement_opinion'),
            ('decision', 'location_fdrequirement_decision'),
            ('optional', 'location_fdrequirement_optional'),
        )
        return DisplayList(vocab)


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
    schema.moveField('prorogation', after='annoncedDelayDetails')
    schema.moveField('impactStudy', after='prorogation')
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
    schema['parcellings'].widget.label_msgid = 'urban_label_parceloutlicences'
    schema['isInSubdivision'].widget.label_msgid = 'urban_label_is_in_parceloutlicences'
    schema['subdivisionDetails'].widget.label_msgid = 'urban_label_parceloutlicences_details'
    schema['pca'].widget.label_msgid = 'urban_label_sol'
    schema['isInPCA'].widget.label_msgid = 'urban_label_is_in_sol'
    schema['pcaDetails'].widget.label_msgid = 'urban_label_sol_details'
    return schema

finalizeSchema(CODT_BaseBuildLicence_schema)
##/code-section module-footer
