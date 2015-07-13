# -*- coding: utf-8 -*-
#
# File: EnvClassTwo.py
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
from Products.urban.EnvironmentLicence import EnvironmentLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='temporaryExploitation',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Temporaryexploitation',
            label_msgid='urban_label_temporaryExploitation',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassTwo_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvClassTwo_schema['hasEnvironmentImpactStudy'].default = False
##/code-section after-schema

class EnvClassTwo(BaseFolder, EnvironmentLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassTwo)

    meta_type = 'EnvClassTwo'
    _at_rename_after_creation = True

    schema = EnvClassTwo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def rubrics_base_query(self):
        return {'extraValue': ['0', '2', '3']}



registerType(EnvClassTwo, PROJECTNAME)
# end of class EnvClassTwo

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('businessOldLocation', after='workLocations')
    schema.moveField('foldermanagers', after='businessOldLocation')
    schema.moveField('rubrics', after='folderCategory')
    schema.moveField('description', after='additionalLegalConditions')
    schema.moveField('temporaryExploitation', after='natura2000Details')
    return schema

finalizeSchema(EnvClassTwo_schema)
##/code-section module-footer

