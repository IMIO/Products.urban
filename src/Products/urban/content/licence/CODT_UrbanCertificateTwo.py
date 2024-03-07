# -*- coding: utf-8 -*-
#
# File: CODT_UrbanCertificateTwo.py
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
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence
from Products.urban.content.licence.CODT_BuildLicence import finalizeSchema
from Products.urban.content.licence.CODT_BuildLicence import finalizeSpecificSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import UrbanMessage as _
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.urban.utils import setOptionalAttributes
from plone import api


optional_fields = ["geometricians", "notaryContact"]
##/code-section module-header

schema = Schema(
    (
        ReferenceField(
            name="geometricians",
            widget=ReferenceBrowserWidget(
                force_close_on_insert=1,
                allow_search=1,
                only_for_review_states="enabled",
                allow_browse=1,
                show_indexes=1,
                show_index_selector=1,
                startup_directory="urban/geometricians",
                available_indexes={"Title": "Nom"},
                base_query="geometriciansBaseQuery",
                wild_card_search=True,
                show_results_without_query=True,
                restrict_browsing_to_startup_directory=1,
                label=_("urban_label_geometricians", default="Geometrician(s)"),
                popup_name="contact_reference_popup",
            ),
            required=False,
            schemata="urban_description",
            multiValued=1,
            relationship="parcelOutGeometricians",
            allowed_types=("Geometrician",),
        ),
        ReferenceField(
            name="notaryContact",
            widget=ReferenceBrowserWidget(
                allow_search=1,
                only_for_review_states="enabled",
                allow_browse=1,
                force_close_on_insert=1,
                startup_directory="urban/notaries",
                restrict_browsing_to_startup_directory=1,
                popup_name="contact_reference_popup",
                wild_card_search=True,
                label=_("urban_label_notaryContact", default="Notary(ies)"),
            ),
            required=False,
            schemata="urban_description",
            multiValued=True,
            relationship="notary",
            allowed_types=("Notary",),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_UrbanCertificateTwo_schema = (
    BaseFolderSchema.copy()
    + getattr(CODT_BuildLicence, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
# put the the fields coming from Inquiry in a specific schemata
##/code-section after-schema


class CODT_UrbanCertificateTwo(BaseFolder, CODT_BuildLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_UrbanCertificateTwo)

    meta_type = "CODT_UrbanCertificateTwo"
    _at_rename_after_creation = True

    schema = CODT_UrbanCertificateTwo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    security.declarePublic("geometriciansBaseQuery")

    def geometriciansBaseQuery(self):
        """
        Do add some details for the base query
        Here, we want to be sure that geometricians are alphabetically sorted
        """
        portal = api.portal.get()
        rootPath = "/".join(portal.getPhysicalPath())
        dict = {}
        dict["path"] = {"query": "%s/urban/geometricians" % rootPath, "depth": 1}
        dict["sort_on"] = "sortable_title"
        return dict


registerType(CODT_UrbanCertificateTwo, PROJECTNAME)
# end of class CODT_UrbanCertificateTwo

##code-section module-footer #fill in your manual code here

# finalizeSchema comes from BuildLicence to be sure to have the same changes reflected
finalizeSchema(CODT_UrbanCertificateTwo_schema)
finalizeSpecificSchema(CODT_UrbanCertificateTwo_schema)


def cu2FinalizeSchema(schema):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("representativeContacts", after="workLocations")
    schema.moveField("notaryContact", after="representativeContacts")


cu2FinalizeSchema(CODT_UrbanCertificateTwo_schema)
##/code-section module-footer
