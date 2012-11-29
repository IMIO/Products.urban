# -*- coding: utf-8 -*-
#
# File: EnvironmentRubricTerm.py
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
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='exploitationCondition',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory_method='getExploitationConditionsPath',
            show_indexes=False,
            wild_card_search=True,
            label='Exploitationcondition',
            label_msgid='urban_label_exploitationCondition',
            i18n_domain='urban',
        ),
        relationship='exploitationConditions',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvironmentRubricTerm_schema = BaseSchema.copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvironmentRubricTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvironmentRubricTerm)

    meta_type = 'EnvironmentRubricTerm'
    _at_rename_after_creation = True

    schema = EnvironmentRubricTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getExploitationConditionsPath(self):
        portal_urban = getToolByName(self, 'portal_urban')
        return '/'.join(portal_urban.exploitationconditions.getPhysicalPath())


registerType(EnvironmentRubricTerm, PROJECTNAME)
# end of class EnvironmentRubricTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

