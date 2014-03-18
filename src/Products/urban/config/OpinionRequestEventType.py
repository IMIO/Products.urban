# -*- coding: utf-8 -*-
#
# File: OpinionRequestEventType.py
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
from Products.urban.config.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.urban.config.UrbanEventType import UrbanEventType
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((


),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OpinionRequestEventType_schema = OrderedBaseFolderSchema.copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy() + \
    getattr(UrbanEventType, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class OpinionRequestEventType(OrderedBaseFolder, UrbanVocabularyTerm, UrbanEventType, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IOpinionRequestEventType)

    meta_type = 'OpinionRequestEventType'
    _at_rename_after_creation = True

    schema = OpinionRequestEventType_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(OpinionRequestEventType, PROJECTNAME)
# end of class OpinionRequestEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer

