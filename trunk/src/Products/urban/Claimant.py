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


registerType(Claimant, PROJECTNAME)
# end of class Claimant

##code-section module-footer #fill in your manual code here
##/code-section module-footer

