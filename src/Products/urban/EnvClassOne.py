# -*- coding: utf-8 -*-
#
# File: EnvClassOne.py
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


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassOne_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvClassOne(BaseFolder, EnvironmentLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassOne)

    meta_type = 'EnvClassOne'
    _at_rename_after_creation = True

    schema = EnvClassOne_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def rubrics_base_query(self):
        return {'extraValue': ['0', '1', '2', '3']}



registerType(EnvClassOne, PROJECTNAME)
# end of class EnvClassOne

##code-section module-footer #fill in your manual code here
##/code-section module-footer

