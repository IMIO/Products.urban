# -*- coding: utf-8 -*-
#
# File: UrbanEventInquiry.py
#
# Copyright (c) 2011 by CommunesPlone
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
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventInquiry_schema = BaseFolderSchema.copy() + \
    getattr(UrbanEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventInquiry(BaseFolder, UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanEventInquiry)

    meta_type = 'UrbanEventInquiry'
    _at_rename_after_creation = True

    schema = UrbanEventInquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(UrbanEventInquiry, PROJECTNAME)
# end of class UrbanEventInquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

