# -*- coding: utf-8 -*-
#
# File: Architect.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Contact import Contact
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Architect_schema = Contact.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Architect(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IArchitect)

    meta_type = 'Architect'
    _at_rename_after_creation = True

    schema = Architect_schema

    ##code-section class-header #fill in your manual code here
    del schema['title']
    archetype_name = 'Architect'
    aliases = {
        '(Default)'  : 'Architect_view',
        'view'       : '(Default)',
        'index.html' : '(Default)',
        'edit'       : 'Architect_edit',
        'properties' : 'base_metadata',
        'sharing'    : '',
        }
    ##/code-section class-header

    # Methods

    # Manually created methods

    def Title(self):
        return self.getName1() + " " + self.getName2()



registerType(Architect, PROJECTNAME)
# end of class Architect

##code-section module-footer #fill in your manual code here
##/code-section module-footer

