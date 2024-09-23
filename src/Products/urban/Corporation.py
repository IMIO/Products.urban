# -*- coding: utf-8 -*-
#
# File: Corporation.py
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
from Products.urban.Applicant import Applicant
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

import cgi

##code-section module-header #fill in your manual code here
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

##/code-section module-header

schema = Schema(
    (
        StringField(
            name="denomination",
            widget=StringField._properties["widget"](
                label="Denomination",
                label_msgid="urban_label_denomination",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="legalForm",
            widget=StringField._properties["widget"](
                label="Legalform",
                label_msgid="urban_label_legalForm",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="tvaNumber",
            widget=StringField._properties["widget"](
                label="Tvanumber",
                label_msgid="urban_label_tvaNumber",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="bceNumber",
            widget=StringField._properties["widget"](
                label="Bcenumber",
                label_msgid="urban_label_bceNumber",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="personRole",
            widget=StringField._properties["widget"](
                label="Personrole",
                label_msgid="urban_label_personRole",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonTitle",
            widget=SelectionWidget(
                label="Persontitle",
                label_msgid="urban_label_personTitle",
                i18n_domain="urban",
            ),
            vocabulary=UrbanVocabulary(
                "persons_titles", vocType="PersonTitleTerm", inUrbanConfig=False
            ),
        ),
        StringField(
            name="contactPersonName",
            widget=StringField._properties["widget"](
                label="Name1",
                label_msgid="urban_label_name1",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonFirstname",
            widget=StringField._properties["widget"](
                label="Name2",
                label_msgid="urban_label_name2",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="personNationalRegister",
            widget=StringField._properties["widget"](
                size=30,
                label="Nationalregister",
                label_msgid="urban_label_nationalRegister",
                i18n_domain="urban",
            ),
            validators=("isBelgianNR",),
        ),
        StringField(
            name="contactNationalRegister",
            widget=StringField._properties["widget"](
                size=30,
                label="Nationalregister",
                label_msgid="urban_label_nationalRegister",
                i18n_domain="urban",
            ),
            validators=("isBelgianNR",),
        ),
        StringField(
            name="contactPersonEmail",
            widget=StringField._properties["widget"](
                label="Email",
                label_msgid="urban_label_email",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonPhone",
            widget=StringField._properties["widget"](
                label="Phone",
                label_msgid="urban_label_phone",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonStreet",
            widget=StringField._properties["widget"](
                label="ContactPersonStreet",
                label_msgid="urban_label_contactpersonstreet",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonNumber",
            widget=StringField._properties["widget"](
                label="ContactPersonNumber",
                label_msgid="urban_label_contactpersonnumber",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonZipcode",
            widget=StringField._properties["widget"](
                label="ContactPersonZipcode",
                label_msgid="urban_label_contactpersonzipcode",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="contactPersonCity",
            widget=StringField._properties["widget"](
                label="ContactPersonCity",
                label_msgid="urban_label_contactpersoncity",
                i18n_domain="urban",
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Corporation_schema = (
    BaseSchema.copy() + getattr(Applicant, "schema", Schema(())).copy() + schema.copy()
)

##code-section after-schema #fill in your manual code here
Corporation_schema["society"].widget.visible = False
Corporation_schema["representedBySociety"].widget.visible = False
Corporation_schema["representedBy"].widget.visible = False
Corporation_schema["nationalRegister"].widget.visible = False
# Corporation_schema['personTitle'].widget.visible = False
##/code-section after-schema


class Corporation(BaseContent, Applicant, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICorporation)

    meta_type = "Corporation"
    _at_rename_after_creation = True

    schema = Corporation_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("Title")

    def Title(self):
        """
        Generate the title...
        """
        title = "{}{}{}".format(
            self.getLegalForm(),
            self.getLegalForm() and " " or "",
            self.getDenomination(),
        )
        return title

    def _getNameSignaletic(
        self, short, linebyline, reverse=False, invertnames=False, withtitle=True
    ):
        title = self.getPersonTitleValue(short, False, reverse).decode("utf8")
        legalForm = self.getLegalForm().decode("utf8")
        denomination = self.getDenomination().decode("utf8")
        lastName = self.getName1().decode("utf-8")
        firstName = self.getName2().decode("utf-8")
        personRole = self.getPersonRole().decode("utf8")
        nameSignaletic = u"{} {}".format(legalForm, denomination)
        if linebyline:
            # escape HTML special characters like HTML entities
            legalForm = cgi.escape(legalForm)
            denomination = cgi.escape(denomination)
            firstName = cgi.escape(firstName)
            lastName = cgi.escape(lastName)
            personRole = cgi.escape(personRole)
            if withtitle:
                title = cgi.escape(title)
                nameSignaletic = u"%s %s<br />%s %s %s" % (
                    legalForm,
                    denomination,
                    title,
                    firstName,
                    lastName,
                )
            else:
                nameSignaletic = u"%s %s<br />%s %s %s" % (
                    legalForm,
                    denomination,
                    firstName,
                    lastName,
                )
        return nameSignaletic


registerType(Corporation, PROJECTNAME)
# end of class Corporation

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField("denomination", before="personTitle")
    schema.moveField("legalForm", after="denomination")
    schema.moveField("tvaNumber", after="fax")
    schema.moveField("bceNumber", after="tvaNumber")
    schema.moveField("personTitle", after="bceNumber")
    schema.moveField("personRole", after="personTitle")
    schema.moveField("name1", after="personRole")
    schema.moveField("name2", after="name1")
    schema.moveField("personNationalRegister", after="name2")
    schema.moveField("contactPersonStreet", after="contactPersonPhone")
    schema.moveField("contactPersonNumber", after="contactPersonStreet")
    schema.moveField("contactPersonZipcode", after="contactPersonNumber")
    schema.moveField("contactNationalRegister", after="contactPersonEmail")
    schema.moveField("contactPersonCity", after="contactPersonZipcode")


finalizeSchema(Corporation_schema)
##/code-section module-footer
