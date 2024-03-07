# -*- coding: utf-8 -*-
#
# File: SpecificFeatureTerm.py
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
from plone import api
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.urban.config import *
from Products.urban.utils import getLicenceSchema
from zope.i18n import translate

import interfaces

schema = Schema(
    (
        LinesField(
            name="relatedFields",
            widget=InAndOutWidget(
                label="Relatedfields",
                label_msgid="urban_label_relatedFields",
                i18n_domain="urban",
            ),
            multiValued=1,
            vocabulary="listSpecificfeatureRelatedFields",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

SpecificFeatureTerm_schema = (
    BaseSchema.copy()
    + getattr(UrbanVocabularyTerm, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class SpecificFeatureTerm(BaseContent, UrbanVocabularyTerm, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ISpecificFeatureTerm)

    meta_type = "SpecificFeatureTerm"
    _at_rename_after_creation = True

    schema = SpecificFeatureTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("hasRelatedFields")

    def hasRelatedFields(self):
        """
        return a DisplayList of fields wich are marked as optional
        """
        return self.getRelatedFields()

    security.declarePublic("listSpecificfeatureRelatedFields")

    def listSpecificfeatureRelatedFields(self):
        """
        return a DisplayList of fields wich are marked as optional
        """
        licence_type = self.aq_parent.getLicencePortalType()
        licence_schema = getLicenceSchema(licence_type)
        available_fieldtypes = [
            "Products.Archetypes.Field.StringField",
            "Products.Archetypes.Field.LinesField",
            "Products.Archetypes.Field.BooleanField",
        ]
        available_fields = [
            field
            for field in licence_schema.fields()
            if field.getType() in available_fieldtypes
            and field.schemata.startswith("urban")
        ]
        vocabulary_fields = [
            (
                field.getName(),
                translate(
                    getattr(field.widget, "label_msgid", field.widget.label),
                    "urban",
                    context=self.REQUEST,
                ),
            )
            for field in available_fields
        ]
        # return a vocabulary containing the names of all the text fields of the schema
        return DisplayList(sorted(vocabulary_fields, key=lambda name: name[1]))

    security.declarePublic("getRenderedDescription")

    def getRenderedDescription(self, obj, renderToNull=False):
        """
        see renderText method of UrbanTool
        """
        portal_urban = api.portal.get_tool("portal_urban")
        return portal_urban.renderText(
            text=self.Description(), context=obj, renderToNull=renderToNull
        )


registerType(SpecificFeatureTerm, PROJECTNAME)
# end of class SpecificFeatureTerm

##code-section module-footer #fill in your manual code here
##/code-section module-footer
