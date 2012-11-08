# -*- coding: utf-8 -*-
#
# File: EnvironmentBase.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.6
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
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setOptionalAttributes

optional_fields =[]
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentBase_schema['title'].required = False
EnvironmentBase_schema['title'].widget.visible = False
#remove the annoncedDelays for Environments
del EnvironmentBase_schema['annoncedDelay']
del EnvironmentBase_schema['annoncedDelayDetails']
#remove the impactStudy field for Environments
del EnvironmentBase_schema['impactStudy']
#hide the solicit opinions to fields for EnvironmentOne
EnvironmentBase_schema['solicitRoadOpinionsTo'].widget.visible=False
EnvironmentBase_schema['solicitLocationOpinionsTo'].widget.visible=False
##/code-section after-schema

class EnvironmentBase(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvironmentBase)

    meta_type = 'EnvironmentBase'
    _at_rename_after_creation = True

    schema = EnvironmentBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
    ##/code-section class-header

    # Methods


registerType(EnvironmentBase, PROJECTNAME)
# end of class EnvironmentBase

##code-section module-footer #fill in your manual code here
##/code-section module-footer

