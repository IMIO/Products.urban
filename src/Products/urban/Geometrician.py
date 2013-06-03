# -*- coding: utf-8 -*-
#
# File: Geometrician.py
#
# Copyright (c) 2013 by CommunesPlone
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

    IntegerField(
        name='nationalRegister',
        widget=IntegerField._properties['widget'](
            label='Nationalregister',
            label_msgid='urban_label_nationalRegister',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Geometrician_schema = Contact.schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Geometrician(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IGeometrician)

    meta_type = 'Geometrician'
    _at_rename_after_creation = True

    schema = Geometrician_schema

    ##code-section class-header #fill in your manual code here
    del schema['title']
    archetype_name = 'Geometrician'
    aliases = {
        '(Default)'  : 'Geometrician_view',
        'view'       : '(Default)',
        'index.html' : '(Default)',
        'edit'       : 'Geometrician_edit',
        'properties' : 'base_metadata',
        'sharing'    : '',
        }
    ##/code-section class-header

    # Methods

    # Manually created methods

    def Title(self):
        return self.getName1() + " " + self.getName2()



registerType(Geometrician, PROJECTNAME)
# end of class Geometrician

##code-section module-footer #fill in your manual code here
##/code-section module-footer

