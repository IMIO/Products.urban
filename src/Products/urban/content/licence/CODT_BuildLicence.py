# -*- coding: utf-8 -*-
#
# File: CODT_BuildLicence.py
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
from Products.urban.content.licence.CODT_BaseCODT_BuildLicence import CODT_BaseCODT_BuildLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_BuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(CODT_BaseCODT_BuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class CODT_BuildLicence(BaseFolder, CODT_BaseCODT_BuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_BuildLicence)

    meta_type = 'CODT_BuildLicence'
    _at_rename_after_creation = True

    schema = CODT_BuildLicence_schema

    # Methods

    def listProcedureChoices(self):
        vocabulary = (
            ('ukn', 'Non determiné'),
            ('opinions', 'Sollicitation d\'avis (instance ou service interne/externe)'),
            ('inquiry', 'Instruction d\'une enquête publique'),
            ('FD', 'Sollicitation du fonctionnaire délégué'),
        )
        return DisplayList(vocabulary)


registerType(CODT_BuildLicence, PROJECTNAME)
# end of class CODT_BuildLicence

##code-section module-footer #fill in your manual code here


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
    schema['missingParts'].widget.format = None
    return schema

finalizeSchema(CODT_BuildLicence_schema)
##/code-section module-footer
