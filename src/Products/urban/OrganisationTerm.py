# -*- coding: utf-8 -*-
#
# File: OrganisationTerm.py
#
# Copyright (c) 2011 by CommunesPlone
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
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
import UrbanEventType
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OrganisationTerm_schema = BaseSchema.copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class OrganisationTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IOrganisationTerm)

    meta_type = 'OrganisationTerm'
    _at_rename_after_creation = True

    schema = OrganisationTerm_schema

    ##code-section class-header #fill in your manual code here
    
    ##/code-section class-header

    # Methods


registerType(OrganisationTerm, PROJECTNAME)
# end of class OrganisationTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

