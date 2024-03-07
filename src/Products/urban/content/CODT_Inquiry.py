# -*- coding: utf-8 -*-
#
# File: CODT_Inquiry.py
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
from Products.urban import interfaces
from Products.urban import utils

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.content.Inquiry import Inquiry
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

##code-section module-header #fill in your manual code here
from zope.i18n import translate

optional_fields = ["divergence", "divergenceDetails", "announcementArticlesText"]

full_inquiry_slave_fields = (
    {
        "name": "divergence",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "divergenceDetails",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "announcementArticles",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "announcementArticlesText",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "investigationDetails",
        "action": "hide",
        "hide_values": ("none",),
    },
    {
        "name": "derogation",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "derogationDetails",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "investigationArticles",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "investigationArticlesText",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "roadModificationSubject",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "demandDisplay",
        "action": "hide",
        "hide_values": (
            "none",
            "announcement",
        ),
    },
    {
        "name": "investigationReasons",
        "action": "hide",
        "hide_values": ("none",),
    },
)
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="inquiry_type",
            widget=MasterSelectWidget(
                slave_fields=full_inquiry_slave_fields,
                label=_("urban_label_inquiry_type", default="Inquiry_type"),
            ),
            vocabulary="list_inquiry_types",
            schemata="urban_inquiry",
        ),
        LinesField(
            name="divergence",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_divergence", default="Divergence"),
            ),
            multiValued=1,
            vocabulary=UrbanVocabulary("divergences"),
            default_method="getDefaultValue",
            schemata="urban_inquiry",
        ),
        TextField(
            name="divergenceDetails",
            allowable_content_types=("text/plain",),
            widget=TextAreaWidget(
                label=_("urban_label_divergenceDetails", default="Divergencedetails"),
            ),
            default_output_type="text/plain",
            default_content_type="text/plain",
            default_method="getDefaultText",
            schemata="urban_inquiry",
        ),
        LinesField(
            name="announcementArticles",
            widget=MultiSelect2Widget(
                size=10,
                label=_(
                    "urban_label_announcementArticles", default="Announcementarticles"
                ),
            ),
            multiValued=True,
            vocabulary=UrbanVocabulary("announcementarticles"),
            default_method="getDefaultValue",
            schemata="urban_inquiry",
        ),
        TextField(
            name="announcementArticlesText",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_announcementArticlesText",
                    default="Announcementarticlestext",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            schemata="urban_inquiry",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_Inquiry_schema = (
    BaseSchema.copy() + getattr(Inquiry, "schema", Schema(())).copy() + schema.copy()
)

##code-section after-schema #fill in your manual code here
CODT_Inquiry_schema["title"].widget.visible = False
##/code-section after-schema


class CODT_Inquiry(BaseContent, Inquiry, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_Inquiry)

    meta_type = "CODT_Inquiry"
    _at_rename_after_creation = True

    schema = CODT_Inquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic("getLinkedUrbanEventInquiry")

    def getLinkedUrbanEventInquiry(self):
        """
        Return the linked UrbanEventInquiry object if exists
        """
        brefs = self.getBRefs("linkedInquiry")
        if brefs:
            # linkedInquiry may come from a UrbanEventInquiry or an UrbanEventOpinionRequest
            for bref in brefs:
                if bref and bref.portal_type in [
                    "UrbanEventAnnouncement",
                    "UrbanEventInquiry",
                ]:
                    return bref
        else:
            return None

    def list_inquiry_types(self):
        """ """
        vocabulary = (
            ("none", "Aucune"),
            ("announcement", "Annonce de projet"),
            ("inquiry", "Enquête publique"),
        )
        return DisplayList(vocabulary)

    security.declarePublic("mayAddOpinionRequestEvent")

    def mayAddOpinionRequestEvent(self, organisation):
        """
        This is used as TALExpression for the UrbanEventOpinionRequest
        We may add an OpinionRequest if we asked one in an inquiry on the licence
        We may add another if another inquiry defined on the licence ask for it and so on
        """
        opinions = self.getSolicitOpinionsTo()
        opinions += self.getSolicitOpinionsToOptional()
        limit = organisation in opinions and 1 or 0
        inquiries = [inq for inq in self.getInquiriesAndAnnouncements() if inq != self]
        for inquiry in inquiries:
            if (
                organisation in inquiry.getSolicitOpinionsTo()
                or organisation in inquiry.getSolicitOpinionsToOptional()
            ):
                limit += 1
        limit = limit - len(self.getOpinionRequests(organisation))
        return limit > 0

    security.declarePublic("getInquiriesAndAnnouncements")

    def getInquiriesAndAnnouncements(self):
        """
        Returns the existing inquiries
        """
        inqs = [inq for inq in self._get_inquiry_objs(all_=False)]
        return inqs

    security.declarePublic("getAllInquiriesAndAnnouncements")

    def getAllInquiriesAndAnnouncements(self):
        """
        Returns the existing inquiries
        """
        inqs = [inq for inq in self._get_inquiry_objs(all_=True)]
        return inqs

    security.declarePublic("getInquiries")

    def getInquiries(self):
        """
        Returns the existing inquiries
        """
        inqs = [
            inq
            for inq in self._get_inquiry_objs(all_=False)
            if "inquiry" in inq.getInquiry_type()
        ]
        return inqs

    security.declarePublic("getAllInquiries")

    def getAllInquiries(self):
        """
        Returns the existing inquiries
        """
        inqs = [
            inq
            for inq in self._get_inquiry_objs(all_=True)
            if "inquiry" in inq.getInquiry_type()
        ]
        return inqs

    def _get_inquiry_objs(self, all_=False, portal_type="CODT_Inquiry"):
        """
        Returns the existing inquiries or announcements
        """
        all_inquiries = super(CODT_Inquiry, self)._get_inquiry_objs(
            all_=all_, portal_type=portal_type
        )
        return all_inquiries

    security.declarePublic("getAnnouncements")

    def getAnnouncements(self):
        """
        Returns the existing announcements
        """
        inqs = [
            inq
            for inq in self._get_inquiry_objs(all_=False)
            if "announcement" in inq.getInquiry_type()
        ]
        return inqs

    security.declarePublic("getAllAnnouncements")

    def getAllAnnouncements(self):
        """
        Returns the existing announcements
        """
        inqs = [
            inq
            for inq in self._get_inquiry_objs(all_=True)
            if "announcement" in inq.getInquiry_type()
        ]
        return inqs

    security.declarePublic("getUrbanEventAnnouncements")

    def getUrbanEventAnnouncements(self):
        """
        Returns the existing UrbanEventAnnouncements
        """
        return self.listFolderContents({"portal_type": "UrbanEventAnnouncement"})

    security.declarePublic("mayAddAnnouncementEvent")

    def mayAddAnnouncementEvent(self):
        """
        This is used as TALExpression for the UrbanEventInquiry
        We may add an inquiry if we defined one on the licence
        We may add another if another is defined on the licence and so on
        """
        # first of all, we can add an InquiryEvent if an inquiry is defined on the licence at least
        announcements = self.getAllAnnouncements()
        urbanEventAnnouncements = self.getUrbanEventAnnouncements()
        if len(urbanEventAnnouncements) >= len(announcements):
            return False
        return True

    security.declarePublic("mayAddInquiryEvent")

    def mayAddInquiryEvent(self):
        """
        This is used as TALExpression for the UrbanEventInquiry
        We may add an inquiry if we defined one on the licence
        We may add another if another is defined on the licence and so on
        """
        # first of all, we can add an InquiryEvent if an inquiry is defined on the licence at least
        inquiries = self.getAllInquiries()
        urbanEventInquiries = self.getUrbanEventInquiries()
        if len(urbanEventInquiries) >= len(inquiries):
            return False
        return True

    def get_inquiry_fields_to_display(self, exclude=[]):
        """
        Depending on the value selected on 'inquiry_type', we hide/show some fields
        """
        licence_config = self.getLicenceConfig()
        displayed_fields = licence_config.getUsedAttributes()
        all_fields = utils.getSchemataFields(
            self, displayed_fields, "urban_inquiry", exclude
        )
        inquiry_type = self.getInquiry_type()
        fields_to_hide = [
            slave["name"]
            for slave in full_inquiry_slave_fields
            if slave["action"] == "hide" and inquiry_type in slave["hide_values"]
        ]
        fields_to_display = [f for f in all_fields if f.getName() not in fields_to_hide]
        return fields_to_display


registerType(CODT_Inquiry, PROJECTNAME)
# end of class Inquiry

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("derogationDetails", after="derogation")
    schema.moveField("announcementArticlesText", before="derogation")
    schema.moveField("announcementArticles", before="announcementArticlesText")
    schema.moveField("divergenceDetails", before="announcementArticles")
    schema.moveField("divergence", before="divergenceDetails")
    schema.moveField("inquiry_type", before="divergence")
    return schema


finalizeSchema(CODT_Inquiry_schema)
##/code-section module-footer
