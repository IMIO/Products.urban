# -*- coding: utf-8 -*-
#
# File: Locality.py
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

# additional imports from tagged value 'import'
from Products.urban.Street import Street, Street_schema

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    TextField(
        name='alsoCalled',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            description='Enter the different kind of spelling for this locality',
            description_msgid="alsocalled_descr",
            label='Alsocalled',
            label_msgid='urban_label_alsoCalled',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Locality_schema = Street_schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Locality(Street, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ILocality)

    meta_type = 'Locality'
    _at_rename_after_creation = True

    schema = Locality_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Locality, PROJECTNAME)
# end of class Locality

##code-section module-footer #fill in your manual code here
##/code-section module-footer

