# -*- coding: utf-8 -*-
#
# File: PcaTerm.py
#
# Copyright (c) 2014 by CommunesPlone
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
from Products.urban.config.UrbanConfigurationValue import UrbanConfigurationValue
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible=False,
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
        accessor="Title",
    ),
    StringField(
        name='label',
        widget=StringField._properties['widget'](
            label='Label',
            label_msgid='urban_label_label',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='number',
        widget=StringField._properties['widget'](
            label='Number',
            label_msgid='urban_label_number',
            i18n_domain='urban',
        ),
        required=True,
    ),
    DateTimeField(
        name='decreeDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            starting_year=1940,
            future_years=False,
            label='Decreedate',
            label_msgid='urban_label_decreeDate',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='decreeType',
        widget=SelectionWidget(
            label='Decreetype',
            label_msgid='urban_label_decreeType',
            i18n_domain='urban',
        ),
        vocabulary='listDecreeTypes',
    ),
    TextField(
        name='changes',
        allowable_content_types="('text/plain',)",
        widget=TextAreaWidget(
            label='Changes',
            label_msgid='urban_label_changes',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/plain',
    ),
    TextField(
        name='comment',
        allowable_content_types="('text/plain',)",
        widget=TextAreaWidget(
            label='Comment',
            label_msgid='urban_label_comment',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        default_content_type='text/plain',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PcaTerm_schema = BaseSchema.copy() + \
    getattr(UrbanConfigurationValue, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PcaTerm(BaseContent, UrbanConfigurationValue, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IPcaTerm)

    meta_type = 'PcaTerm'
    _at_rename_after_creation = True

    schema = PcaTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic('listDecreeTypes')
    def listDecreeTypes(self):
        """
        """
        pass

registerType(PcaTerm, PROJECTNAME)
# end of class PcaTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

