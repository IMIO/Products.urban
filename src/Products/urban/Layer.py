# -*- coding: utf-8 -*-
#
# File: Layer.py
#
# Copyright (c) 2013 by CommunesPlone
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='WMSUrl',
        widget=StringField._properties['widget'](
            label='Wmsurl',
            label_msgid='urban_label_WMSUrl',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='layers',
        widget=StringField._properties['widget'](
            label='Layers',
            label_msgid='urban_label_layers',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='styles',
        widget=StringField._properties['widget'](
            label='Styles',
            label_msgid='urban_label_styles',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='SRS',
        widget=StringField._properties['widget'](
            label='Srs',
            label_msgid='urban_label_SRS',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='layerFormat',
        widget=StringField._properties['widget'](
            description="Enter the layer image mimetype, for example 'image/jpeg' or 'image/png'",
            label='Layerformat',
            label_msgid='urban_label_layerFormat',
            description_msgid='urban_help_layerFormat',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='baseLayer',
        widget=BooleanField._properties['widget'](
            label='Baselayer',
            label_msgid='urban_label_baseLayer',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='visibility',
        widget=BooleanField._properties['widget'](
            label='Visibility',
            label_msgid='urban_label_visibility',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='transparency',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Transparency',
            label_msgid='urban_label_transparency',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='queryable',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Queryable',
            label_msgid='urban_label_queryable',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Layer_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Layer(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ILayer)

    meta_type = 'Layer'
    _at_rename_after_creation = True

    schema = Layer_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(Layer, PROJECTNAME)
# end of class Layer

##code-section module-footer #fill in your manual code here
##/code-section module-footer

