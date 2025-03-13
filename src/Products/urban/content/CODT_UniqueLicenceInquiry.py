# -*- coding: utf-8 -*-
#
# File: CODT_UniqueLicenceInquiry.py
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
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from zope.interface import implements
from Products.urban import interfaces
from Products.urban import utils
from Products.urban import UrbanMessage as _

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban.content.CODT_Inquiry import CODT_Inquiry

slave_fields_inquiry_category = (
    {
        "name": "investigation_radius",
        "action": "value",
        "vocab_method": "get_inquiry_category_radius",
        "control_param": "enquiry_type",
    },
)
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="inquiry_category",
            widget=MasterSelectWidget(
                slave_fields=slave_fields_inquiry_category,
                label=_("urban_label_inquiry_category", default="Inquiry_category"),
            ),
            vocabulary="list_inquiry_category",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_UniqueLicenceInquiry_schema = (
    BaseSchema.copy()
    + getattr(CODT_Inquiry, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
CODT_UniqueLicenceInquiry_schema["title"].widget.visible = False
CODT_UniqueLicenceInquiry_schema["inquiry_type"].widget.visible = {
    "view": "invisible",
    "edit": "invisible",
}
CODT_UniqueLicenceInquiry_schema["inquiry_type"].default = "inquiry"
##/code-section after-schema


class CODT_UniqueLicenceInquiry(BaseContent, CODT_Inquiry, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_UniqueLicenceInquiry)

    meta_type = "CODT_UniqueLicenceInquiry"
    _at_rename_after_creation = True

    schema = CODT_UniqueLicenceInquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def list_inquiry_category(self):
        """ """
        vocabulary = (
            ("B", "Catégorie B, rayon 200m (attention publication)"),
            ("C", "Catégorie C, rayon 50m"),
        )
        return DisplayList(vocabulary)

    def _get_inquiry_objs(
        self, all_=False, portal_type=["Inquiry", "CODT_UniqueLicenceInquiry"]
    ):
        """
        Returns the existing inquiries or announcements
        """
        all_inquiries = super(CODT_UniqueLicenceInquiry, self)._get_inquiry_objs(
            all_=all_, portal_type=portal_type
        )
        return all_inquiries

    def get_inquiry_category_radius(self, enquiry_type):
        """ """
        if enquiry_type == "B":
            return "200m"
        return "50m"


registerType(CODT_UniqueLicenceInquiry, PROJECTNAME)
# end of class Inquiry

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.delField("announcementArticles")
    schema.delField("announcementArticlesText")
    schema.moveField("derogation", after="investigationArticlesText")
    schema.moveField("derogationDetails", after="derogation")
    schema.moveField("inquiry_category", after="derogationDetails")
    schema.moveField("investigationReasons", after="inquiry_category")
    schema.moveField("divergence", after="derogationDetails")
    schema.moveField("divergenceDetails", after="divergence")
    schema.moveField("demandDisplay", after="divergenceDetails")
    schema.moveField("investigationDetails", after="roadModificationSubject")
    return schema


finalizeSchema(CODT_UniqueLicenceInquiry_schema)
##/code-section module-footer
