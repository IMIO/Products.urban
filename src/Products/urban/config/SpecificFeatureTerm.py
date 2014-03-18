# -*- coding: utf-8 -*-
#
# File: SpecificFeatureTerm.py
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
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    LinesField(
        name='relatedFields',
        widget=InAndOutWidget(
            label='Relatedfields',
            label_msgid='urban_label_relatedFields',
            i18n_domain='urban',
        ),
        multiValued=1,
        vocabulary='listSpecificfeatureRelatedFields',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SpecificFeatureTerm_schema = BaseSchema.copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class SpecificFeatureTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ISpecificFeatureTerm)

    meta_type = 'SpecificFeatureTerm'
    _at_rename_after_creation = True

    schema = SpecificFeatureTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(SpecificFeatureTerm, PROJECTNAME)
# end of class SpecificFeatureTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer

