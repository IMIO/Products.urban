# -*- coding: utf-8 -*-
#
# File: Recipient.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Contact import Contact

##/code-section module-header

schema = Schema(
    (),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Recipient_schema = Contact.schema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class Recipient(BaseContent, Contact, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IRecipient)

    meta_type = "Recipient"
    _at_rename_after_creation = True

    schema = Recipient_schema

    ##code-section class-header #fill in your manual code here
    del schema["title"]
    ##/code-section class-header

    # Methods

    # Manually created methods

    def Title(self):
        return self.getName1() + " " + self.getName2()


registerType(Recipient, PROJECTNAME)
# end of class Recipient

##code-section module-footer #fill in your manual code here
##/code-section module-footer
