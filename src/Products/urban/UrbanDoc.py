# -*- coding: utf-8 -*-
#
# File: UrbanDoc.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.6
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

from plone.app.blob.content import ATBlob
from plone.app.blob.content import ATBlobSchema
from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanDoc_schema = ATBlobSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanDoc(ATBlob):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanDoc)

    meta_type = 'UrbanDoc'
    _at_rename_after_creation = True

    schema = UrbanDoc_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(UrbanDoc, PROJECTNAME)
# end of class UrbanDoc

##code-section module-footer #fill in your manual code here
##/code-section module-footer

