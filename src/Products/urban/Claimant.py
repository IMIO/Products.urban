# -*- coding: utf-8 -*-
#
# File: Claimant.py
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
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from zope.i18n import translate
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
##/code-section module-header


slave_fields_signature_number = (
    # if petition ok : display signatures textfield
    {
        'name': 'signatureNumber',
        'action': 'show',
        'hide_values': (True, ),
    },
)

schema = Schema((

    StringField(
        name='claimType',
        widget=SelectionWidget(
            format='select',
            label='ClaimType',
            label_msgid='urban_label_claimType',
            i18n_domain='urban',
        ),
        vocabulary='listClaimTypeChoices',

    ),
    BooleanField(
        name='hasPetition',
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_signature_number,
            label='HasPetition',
            label_msgid='urban_label_hasPetition',
            i18n_domain='urban',
        ),
    ),
    IntegerField(
        name='signatureNumber',
        widget=IntegerWidget(
            label='signatureNumber',
            label_msgid='urban_label_signatureNumber',
            i18n_domain='urban',
        ),
        validators=('isInt', ),
    ),
    BooleanField(
        name='outOfTime',
        widget=BooleanWidget(
            label='OutOfTime',
            label_msgid='urban_label_outOfTime',
            i18n_domain='urban',
        ),
    ),
    DateTimeField(
        name='claimDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label='Claimdate',
            label_msgid='urban_label_claimDate',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='claimingText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
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

Claimant_schema = BaseSchema.copy() + \
    getattr(Contact, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Claimant(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IClaimant)

    meta_type = 'Claimant'
    _at_rename_after_creation = True

    schema = Claimant_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def validate_signatureNumber(self, value):
        if self['hasPetition'] and not value:
            return translate(_('error_signatureNumber', default=u"Nombre de signature obligatoire"))

    def listClaimTypeChoices(self):
        vocab = (
            ('writedClaim', 'Ecrite'),
            ('oralClaim', 'Orale'),
        )
        return DisplayList(vocab)

registerType(Claimant, PROJECTNAME)
# end of class Claimant

##code-section module-footer #fill in your manual code here
##/code-section module-footer

