# -*- coding: utf-8 -*-
#
# File: FollowUpEventType.py
#
# Copyright (c) 2015 by CommunesPlone
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban.UrbanEventType import UrbanEventType
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import interfaces
from Products.urban.config import PROJECTNAME


schema = Schema((
),
)

FollowUpEventType_schema = OrderedBaseFolderSchema.copy() + schema.copy() + \
    getattr(UrbanEventType, 'schema', Schema(())).copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy()


class FollowUpEventType(OrderedBaseFolder, UrbanEventType, UrbanVocabularyTerm, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IFollowUpEventType)

    meta_type = 'FollowUpEventType'
    _at_rename_after_creation = True

    schema = FollowUpEventType_schema



registerType(FollowUpEventType, PROJECTNAME)