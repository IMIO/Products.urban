# -*- coding: utf-8 -*-
#
# File: RecipientCadastre.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
##/code-section module-header

schema = Schema((

    StringField(
        name='name',
        widget=StringField._properties['widget'](
            label='Name',
            label_msgid='urban_label_name',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='firstname',
        widget=StringField._properties['widget'](
            label='Firstname',
            label_msgid='urban_label_firstname',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='adr1',
        widget=StringField._properties['widget'](
            label='Adr1',
            label_msgid='urban_label_adr1',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='adr2',
        widget=StringField._properties['widget'](
            label='Adr2',
            label_msgid='urban_label_adr2',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='street',
        widget=StringField._properties['widget'](
            label='Street',
            label_msgid='urban_label_street',
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
    ),
    StringField(
        name='zipcode',
        widget=StringField._properties['widget'](
            label='Zipcode',
            label_msgid='urban_label_zipcode',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='city',
        widget=StringField._properties['widget'](
            label='City',
            label_msgid='urban_label_city',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='country',
        default="belgium",
        widget=SelectionWidget(
            label='Country',
            label_msgid='urban_label_country',
            i18n_domain='urban',
        ),
        vocabulary=UrbanVocabulary('country', vocType='UrbanVocabularyTerm', inUrbanConfig=False),
    ),
    StringField(
        name='capakey',
        widget=StringField._properties['widget'](
            label='Capakey',
            label_msgid='urban_label_capakey',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='parcel_nature',
        widget=StringField._properties['widget'](
            label='Parcel_nature',
            label_msgid='urban_label_parcel_nature',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='parcel_street',
        widget=StringField._properties['widget'](
            label='Parcel_street',
            label_msgid='urban_label_parcel_street',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='parcel_police_number',
        widget=StringField._properties['widget'](
            label='Parcel_police_number',
            label_msgid='urban_label_parcel_police_number',
            i18n_domain='urban',
        ),
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RecipientCadastre_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
RecipientCadastre_schema['title'].widget.visible = False
RecipientCadastre_schema['adr2'].widget.visible = False
##/code-section after-schema

class RecipientCadastre(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IRecipientCadastre)

    meta_type = 'RecipientCadastre'
    _at_rename_after_creation = True

    schema = RecipientCadastre_schema

    # Manually created methods

    def getRecipientAddress(self):
        return self.getAdr1()+' '+self.getAdr2()

    def Title(self):
        return '{} {}'.format(self.getName(), self.getFirstname())


registerType(RecipientCadastre, PROJECTNAME)
# end of class RecipientCadastre

##code-section module-footer #fill in your manual code here
##/code-section module-footer

