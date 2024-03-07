# -*- coding: utf-8 -*-
#
# File: PersonTitleTerm.py
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
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="abbreviation",
            widget=StringField._properties["widget"](
                label="Abbreviation",
                label_msgid="urban_label_abbreviation",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="gender",
            widget=SelectionWidget(
                label="Gender",
                label_msgid="urban_label_gender",
                i18n_domain="urban",
            ),
            vocabulary="listGender",
        ),
        StringField(
            name="multiplicity",
            widget=SelectionWidget(
                label="Multiplicity",
                label_msgid="urban_label_multiplicity",
                i18n_domain="urban",
            ),
            vocabulary="listMultiplicity",
        ),
        StringField(
            name="reverseTitle",
            widget=StringField._properties["widget"](
                label="Reversetitle",
                label_msgid="urban_label_reverseTitle",
                i18n_domain="urban",
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

PersonTitleTerm_schema = (
    BaseSchema.copy()
    + getattr(UrbanVocabularyTerm, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class PersonTitleTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IPersonTitleTerm)

    meta_type = "PersonTitleTerm"
    _at_rename_after_creation = True

    schema = PersonTitleTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("listGender")

    def listGender(self):
        lst = [
            ["male", translate("gender_male", "urban", context=self.REQUEST)],
            ["female", translate("gender_female", "urban", context=self.REQUEST)],
        ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic("listMultiplicity")

    def listMultiplicity(self):
        lst = [
            ["single", translate("multiplicity_single", "urban", context=self.REQUEST)],
            ["plural", translate("multiplicity_plural", "urban", context=self.REQUEST)],
        ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))


registerType(PersonTitleTerm, PROJECTNAME)
# end of class PersonTitleTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer
