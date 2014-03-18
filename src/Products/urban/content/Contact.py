# -*- coding: utf-8 -*-
#
# File: Contact.py
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
        name='personTitle',
        widget=SelectionWidget(
            label='Persontitle',
            label_msgid='urban_label_personTitle',
            i18n_domain='urban',
        ),
        vocabulary=UrbanVocabulary('persons_titles', vocType='PersonTitleTerm', inUrbanConfig=False),
    ),
    StringField(
        name='name1',
        widget=StringField._properties['widget'](
            label='Name1',
            label_msgid='urban_label_name1',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='name2',
        widget=StringField._properties['widget'](
            label='Name2',
            label_msgid='urban_label_name2',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='society',
        widget=StringField._properties['widget'](
            label='Society',
            label_msgid='urban_label_society',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='representedBySociety',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_representedby,
            condition="python: here.portal_type == 'Applicant' or here.portal_type == 'Proprietary'",
            label='Representedbysociety',
            label_msgid='urban_label_representedBySociety',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='isSameAddressAsWorks',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_address,
            condition="python: here.portal_type == 'Applicant' or here.portal_type == 'Proprietary'",
            label='Issameaddressasworks',
            label_msgid='urban_label_isSameAddressAsWorks',
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
        name='email',
        widget=StringField._properties['widget'](
            label='Email',
            label_msgid='urban_label_email',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='phone',
        widget=StringField._properties['widget'](
            label='Phone',
            label_msgid='urban_label_phone',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='fax',
        widget=StringField._properties['widget'](
            label='Fax',
            label_msgid='urban_label_fax',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='registrationNumber',
        widget=StringField._properties['widget'](
            condition="python: here.portal_type == 'Architect'",
            label='Registrationnumber',
            label_msgid='urban_label_registrationNumber',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='nationalRegister',
        widget=StringField._properties['widget'](
            size=30,
            label='Nationalregister',
            label_msgid='urban_label_nationalRegister',
            i18n_domain='urban',
        ),
        validators=('isBelgianNR',),
    ),
    LinesField(
        name='representedBy',
        widget=MultiSelectionWidget(
            condition='python:here.showRepresentedByField()',
            format='checkbox',
            label='Representedby',
            label_msgid='urban_label_representedBy',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        multiValued=1,
        vocabulary='listRepresentedBys',
    ),
    TextField(
        name='claimingText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            condition="python: here.portal_type == 'Claimant'",
            label='Claimingtext',
            label_msgid='urban_label_claimingText',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Contact_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Contact(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IContact)

    meta_type = 'Contact'
    _at_rename_after_creation = True

    schema = Contact_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(Contact, PROJECTNAME)
# end of class Contact

##code-section module-footer #fill in your manual code here
##/code-section module-footer

