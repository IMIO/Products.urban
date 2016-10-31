# -*- coding: utf-8 -*-
#
# File: Article127.py
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
from Products.urban.BuildLicence import BuildLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Article127_schema = BaseFolderSchema.copy() + \
    getattr(BuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Article127(BaseFolder, BuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IArticle127)

    meta_type = 'Article127'
    _at_rename_after_creation = True

    schema = Article127_schema

    # Methods

    def listProcedureChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('opinions', 'Sollicitation d\'avis (instance ou service interne/externe)'),
            ('inquiry', 'Instruction d\'une enquête publique'),
        )
        return DisplayList(vocab)


registerType(Article127, PROJECTNAME)
# end of class Article127

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
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
    schema.moveField('folderCategoryTownship', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('requirementFromFD', after='locationDgrneUnderground')
    schema.moveField('townshipCouncilFolder', after='roadCoating')
    schema.moveField('annoncedDelay', after='missingPartsDetails')
    schema.moveField('annoncedDelayDetails', after='annoncedDelay')
    schema.moveField('impactStudy', after='annoncedDelayDetails')
    return schema

finalizeSchema(Article127_schema)
##/code-section module-footer

