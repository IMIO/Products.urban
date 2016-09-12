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

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

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
    BooleanField(
        name='outOfTime',
        widget=BooleanWidget(
            label='OutOfTime',
            label_msgid='urban_label_outOfTime',
            i18n_domain='urban',
        ),
    ),
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

