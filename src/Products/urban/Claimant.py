# -*- coding: utf-8 -*-
#
# File: Claimant.py
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
from Products.urban.Contact import Contact
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from zope.i18n import translate
from Products.urban import UrbanMessage as _
from Products.urban.utils import WIDGET_DATE_END_YEAR

##code-section module-header #fill in your manual code here
##/code-section module-header


slave_fields_signature_number = (
    # if petition ok : display signatures textfield
    {
        "name": "signatureNumber",
        "action": "show",
        "hide_values": (True,),
    },
)

schema = Schema(
    (
        StringField(
            name="claimType",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_claimType", default="ClaimType"),
            ),
            vocabulary="listClaimTypeChoices",
        ),
        BooleanField(
            name="hasPetition",
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_signature_number,
                label=_("urban_label_hasPetition", default="HasPetition"),
            ),
        ),
        IntegerField(
            name="signatureNumber",
            widget=IntegerWidget(
                label=_("urban_label_signatureNumber", default="signatureNumber"),
            ),
            validators=("isInt",),
        ),
        BooleanField(
            name="outOfTime",
            widget=BooleanWidget(
                label=_("urban_label_outOfTime", default="OutOfTime"),
            ),
        ),
        DateTimeField(
            name="claimDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_claimDate", default="Claimdate"),
            ),
        ),
        TextField(
            name="claimingText",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_claimingText", default="Claimingtext"),
            ),
            default_output_type="text/x-html-safe",
        ),
        BooleanField(
            name="wantDecisionCopy",
            widget=BooleanWidget(
                label=_("urban_label_Wantdecisioncopy", default="Wantdecisioncopy"),
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Claimant_schema = (
    BaseSchema.copy() + getattr(Contact, "schema", Schema(())).copy() + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class Claimant(BaseContent, Contact, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IClaimant)

    meta_type = "Claimant"
    _at_rename_after_creation = True

    schema = Claimant_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def validate_signatureNumber(self, value):
        if self["hasPetition"] and not value:
            return translate(
                _("error_signatureNumber", default=u"Nombre de signature obligatoire")
            )

    def listClaimTypeChoices(self):
        vocab = (
            ("writedClaim", "Ecrite"),
            ("oralClaim", "Orale"),
        )
        return DisplayList(vocab)

    def isOralComplaint(self):
        return self.claimType == "oralClaim"

    def isWrittenComplaint(self):
        return self.claimType == "writedClaim"

    def isPetition(self):
        return self.claimType == "writedClaim" and self.hasPetition

    def hasSignatureComplaint(self):
        return (
            self.claimType == "writedClaim"
            and self.hasPetition
            and self.signatureNumber
        )


registerType(Claimant, PROJECTNAME)
# end of class Claimant

##code-section module-footer #fill in your manual code here
##/code-section module-footer
