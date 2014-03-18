# -*- coding: utf-8 -*-
#
# File: PortionOut.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='divisionCode',
        widget=StringField._properties['widget'](
            visible={'edit':'hidden', 'view':'visible'},
            label='Divisioncode',
            label_msgid='urban_label_divisionCode',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='division',
        widget=SelectionWidget(
            format='select',
            label='Division',
            label_msgid='urban_label_division',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        vocabulary='listDivisionNames',
    ),
    StringField(
        name='section',
        widget=StringField._properties['widget'](
            label='Section',
            label_msgid='urban_label_section',
            i18n_domain='urban',
        ),
        required=True,
        validators=('isValidSection',),
    ),
    StringField(
        name='radical',
        widget=StringField._properties['widget'](
            label='Radical',
            label_msgid='urban_label_radical',
            i18n_domain='urban',
        ),
        validators=('isValidRadical',),
    ),
    StringField(
        name='bis',
        widget=StringField._properties['widget'](
            label='Bis',
            label_msgid='urban_label_bis',
            i18n_domain='urban',
        ),
        validators=('isValidBis',),
    ),
    StringField(
        name='exposant',
        widget=StringField._properties['widget'](
            label='Exposant',
            label_msgid='urban_label_exposant',
            i18n_domain='urban',
        ),
        validators=('isValidExposant',),
    ),
    StringField(
        name='puissance',
        widget=StringField._properties['widget'](
            label='Puissance',
            label_msgid='urban_label_puissance',
            i18n_domain='urban',
        ),
        validators=('isValidPuissance',),
    ),
    BooleanField(
        name='partie',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Partie',
            label_msgid='urban_label_partie',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='isOfficialParcel',
        default=True,
        widget=BooleanField._properties['widget'](
            visible={'edit':'hidden', 'view':'visible'},
            label='Isofficialparcel',
            label_msgid='urban_label_isOfficialParcel',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='outdated',
        default=False,
        widget=BooleanField._properties['widget'](
            visible={'edit':'hidden', 'view':'visible'},
            label='Outdated',
            label_msgid='urban_label_outdated',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PortionOut_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class PortionOut(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IPortionOut)

    meta_type = 'PortionOut'
    _at_rename_after_creation = True

    schema = PortionOut_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(PortionOut, PROJECTNAME)
# end of class PortionOut

##code-section module-footer #fill in your manual code here
##/code-section module-footer

