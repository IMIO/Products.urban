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
from Products.urban.Applicant import Applicant
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
    StringField(
        name='personRole',
        widget=StringField._properties['widget'](
            label='Personrole',
            label_msgid='urban_label_personRole',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Corporation_schema = BaseSchema.copy() + \
    getattr(Applicant, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Corporation_schema['society'].widget.visible = False
Corporation_schema['representedBySociety'].widget.visible = False
Corporation_schema['representedBy'].widget.visible = False
Corporation_schema['nationalRegister'].widget.visible = False
Corporation_schema['personTitle'].widget.visible = False
##/code-section after-schema

class Corporation(BaseContent, Applicant, BrowserDefaultMixin):
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

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
        Generate the title...
        """
        return self.getDenomination()



registerType(Corporation, PROJECTNAME)
# end of class Corporation

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField('denomination', before='personTitle')
    schema.moveField('legalForm', after='denomination')
    schema.moveField('tvaNumber', after='fax')
    schema.moveField('bceNumber', after='tvaNumber')
    schema.moveField('personTitle', after='bceNumber')
    schema.moveField('personRole', after='personTitle')
    schema.moveField('name1', after='personRole')
    schema.moveField('name2', after='name1')

finalizeSchema(Corporation_schema)
##/code-section module-footer

