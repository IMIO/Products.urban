# -*- coding: utf-8 -*-
#
# File: CODT_UrbanCertificateBase.py
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
from Products.urban.content.licence.UrbanCertificateBase import UrbanCertificateBase
from Products.urban.content.licence.UrbanCertificateBase import (
    finalizeSchema as UrbanCertificateBase_finalizeSchema,
)
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName

schema = Schema()

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

CODT_UrbanCertificateBase_schema = (
    BaseFolderSchema.copy()
    + getattr(UrbanCertificateBase, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
CODT_UrbanCertificateBase_schema["title"].required = False
##/code-section after-schema


class CODT_UrbanCertificateBase(BaseFolder, UrbanCertificateBase, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICODT_UrbanCertificateBase)

    meta_type = "CODT_UrbanCertificateBase"
    _at_rename_after_creation = True

    schema = CODT_UrbanCertificateBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ["urban_description", "urban_road", "urban_location"]
    ##/code-section class-header

    # Methods

    # Manually created methods


registerType(CODT_UrbanCertificateBase, PROJECTNAME)
# end of class CODT_UrbanCertificateBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema = UrbanCertificateBase_finalizeSchema(schema, folderish, moveDiscussion)
    schema["parcellings"].widget.label = _("urban_label_parceloutlicences")
    schema["isInSubdivision"].widget.label = _("urban_label_is_in_parceloutlicences")
    schema["subdivisionDetails"].widget.label = _(
        "urban_label_parceloutlicences_details"
    )
    schema["pca"].vocabulary = UrbanVocabulary(
        "sols", vocType="PcaTerm", inUrbanConfig=False
    )
    schema["pca"].widget.label = _("urban_label_sol")
    schema["pcaZone"].vocabulary_factory = "urban.vocabulary.SOLZones"
    schema["pcaZone"].widget.label = _("urban_label_solZone")
    schema["isInPCA"].widget.label = _("urban_label_is_in_sol")
    schema["pcaDetails"].widget.label = _("urban_label_sol_details")
    return schema


finalizeSchema(CODT_UrbanCertificateBase_schema)
##/code-section module-footer
