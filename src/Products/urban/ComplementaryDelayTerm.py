# -*- coding: utf-8 -*-
#
# File: complementary_delay_term.py
#
# Copyright (c) 2025 by CommunesPlone
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
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

from Products.urban import UrbanMessage as _

##/code-section module-header

schema = Schema(
    (
        IntegerField(
            name="delay",
            widget=IntegerField._properties["widget"](
                label=_("urban_label_delay", "Delay"),
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ComplementaryDelayTerm_schema = (
    BaseSchema.copy()
    + getattr(UrbanVocabularyTerm, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class ComplementaryDelayTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IComplementaryDelayTerm)

    meta_type = "ComplementaryDelayTerm"
    _at_rename_after_creation = True

    schema = ComplementaryDelayTerm_schema


registerType(ComplementaryDelayTerm, PROJECTNAME)
# end of class ComplementaryDelayTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer
