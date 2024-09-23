# -*- coding: utf-8 -*-
#
# File: PatrimonyCertificate.py
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
from Products.urban import interfaces
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setOptionalAttributes
from Products.urban.utils import setSchemataForInquiry
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)

optional_fields = ["architects"]
##/code-section module-header

schema = Schema(
    (
        ReferenceField(
            name="architects",
            widget=ReferenceBrowserWidget(
                allow_search=True,
                only_for_review_states="enabled",
                allow_browse=True,
                force_close_on_insert=True,
                startup_directory="urban/architects",
                restrict_browsing_to_startup_directory=True,
                wild_card_search=True,
                show_index_selector=True,
                label=_("urban_label_architects", default="Architect(s)"),
                popup_name="contact_reference_popup",
            ),
            required=False,
            schemata="urban_description",
            multiValued=True,
            relationship="miscdemandarchitects",
            allowed_types="Architect",
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

PatrimonyCertificate_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + getattr(Inquiry, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(PatrimonyCertificate_schema)
##/code-section after-schema


class PatrimonyCertificate(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IPatrimonyCertificate)

    meta_type = "PatrimonyCertificate"
    _at_rename_after_creation = True

    schema = PatrimonyCertificate_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ["urban_description", "urban_road", "urban_location"]
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("getRepresentatives")

    def getRepresentatives(self):
        """ """
        return self.getArchitects()

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastCollegeReport(self):
        return self.getLastEvent(interfaces.ICollegeReportEvent)

    def getLastTheLicence(self):
        return self.getLastEvent(interfaces.ITheLicenceEvent)


registerType(PatrimonyCertificate, PROJECTNAME)
# end of class PatrimonyCertificate

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("description", after="architects")
    return schema


finalizeSchema(PatrimonyCertificate_schema)
##/code-section module-footer
