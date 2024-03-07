# -*- coding: utf-8 -*-
#
# File: OpinionRequestEventType.py
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
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanEventType import UrbanEventType
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

##code-section module-header #fill in your manual code here

slave_field_internal_service = (
    # applicant is either represented by a society or by another contact but not both at the same time
    {
        "name": "internal_service",
        "action": "show",
        "hide_values": (True,),
    },
)
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="recipientSName",
            widget=StringField._properties["widget"](
                label=_("urban_label_recipientSName", default="Recipientsname"),
            ),
        ),
        StringField(
            name="function_department",
            widget=StringField._properties["widget"](
                label=_(
                    "urban_label_function_department", default="Function_department"
                ),
            ),
        ),
        StringField(
            name="organization",
            widget=StringField._properties["widget"](
                label=_("urban_label_organization", default="Organization"),
            ),
        ),
        StringField(
            name="dispatchSInformation",
            widget=StringField._properties["widget"](
                label=_(
                    "urban_label_dispatchSInformation", default="Dispatchsinformation"
                ),
            ),
        ),
        StringField(
            name="typeAndStreetName_number_box",
            widget=StringField._properties["widget"](
                label=_(
                    "urban_label_typeAndStreetName_number_box",
                    default="Typeandstreetname_number_box",
                ),
            ),
        ),
        StringField(
            name="postcode_locality",
            widget=StringField._properties["widget"](
                label=_("urban_label_postcode_locality", default="Postcode_locality"),
            ),
        ),
        StringField(
            name="country",
            widget=StringField._properties["widget"](
                label=_("urban_label_country", default="Country"),
            ),
        ),
        BooleanField(
            name="is_internal_service",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_field_internal_service,
                label=_(
                    "urban_label_is_internal_service", default="Is_internal_service"
                ),
            ),
        ),
        StringField(
            name="internal_service",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_internal_service", default="Internal_service"),
            ),
            enforceVocabulary=True,
            vocabulary="listInternalServices",
        ),
        LinesField(
            name="concernedOutsideDirections",
            vocabulary="listConcernedOutsideDirections",
            widget=MultiSelect2Widget(
                label="ConcernedOutsideDirections",
                label_msgid="urban_label_concernedOutsideDirections",
                i18n_domain="urban",
            ),
            mode="r",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OpinionRequestEventType_schema = (
    OrderedBaseFolderSchema.copy()
    + schema.copy()
    + getattr(UrbanEventType, "schema", Schema(())).copy()
    + getattr(UrbanVocabularyTerm, "schema", Schema(())).copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class OpinionRequestEventType(
    OrderedBaseFolder, UrbanEventType, UrbanVocabularyTerm, BrowserDefaultMixin
):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IOpinionRequestEventType)

    meta_type = "OpinionRequestEventType"
    _at_rename_after_creation = True

    schema = OpinionRequestEventType_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("listInternalServices")

    def listInternalServices(self):
        registry = api.portal.get_tool("portal_registry")
        registry_field = (
            registry["Products.urban.interfaces.IInternalOpinionServices.services"]
            or {}
        )
        voc_terms = [
            (key, value["full_name"]) for key, value in registry_field.iteritems()
        ]
        vocabulary = DisplayList(voc_terms)
        return vocabulary

    security.declarePublic("getAddressCSV")

    def getAddressCSV(self):
        name = self.Title()
        lines = self.Description()[3:-4].split("<br />")
        description = lines[:-2]
        address = lines[-2:]
        return "%s|%s|%s|%s" % (name, " ".join(description), address[0], address[1])

    security.declarePublic("mayAddOpinionRequestEvent")

    def mayAddOpinionRequestEvent(self, inquiry):
        """
        This is used as TALExpression for the UrbanEventOpinionRequest
        We may add an OpinionRequest if we asked one in an inquiry on the licence
        We may add another if another inquiry defined on the licence ask for it and so on
        """
        may_add = inquiry.mayAddOpinionRequestEvent(self.id)
        return may_add

    security.declarePublic("listConcernedOutsideDirections")

    def listConcernedOutsideDirections(self):
        vocab = (
            ("brabant_wallon", "Brabant wallon"),
            ("eupen", "Eupen"),
            ("hainaut_1", "Hainaut 1"),
            ("hainaut_2", "Hainaut 2"),
            ("liege_1", "Liège 1"),
            ("liege_2", "Liège 2"),
            ("luxembourg", "Luxembourg"),
            ("namur", "Namur"),
        )
        return DisplayList(vocab)


registerType(OpinionRequestEventType, PROJECTNAME)
# end of class OpinionRequestEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer
