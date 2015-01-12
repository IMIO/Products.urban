# -*- coding: utf-8 -*-
#
# File: Corporation.py
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
from Products.urban.Contact import Contact
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='denomination',
        widget=StringField._properties['widget'](
            label='Denomination',
            label_msgid='urban_label_denomination',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='legalForm',
        widget=StringField._properties['widget'](
            label='Legalform',
            label_msgid='urban_label_legalForm',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='tvaNumber',
        widget=StringField._properties['widget'](
            label='Tvanumber',
            label_msgid='urban_label_tvaNumber',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='bceNumber',
        widget=StringField._properties['widget'](
            label='Bcenumber',
            label_msgid='urban_label_bceNumber',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Corporation_schema = BaseSchema.copy() + \
    getattr(Contact, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Corporation(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICorporation)

    meta_type = 'Corporation'
    _at_rename_after_creation = True

    schema = Corporation_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(Corporation, PROJECTNAME)
# end of class Corporation

##code-section module-footer #fill in your manual code here
##/code-section module-footer

