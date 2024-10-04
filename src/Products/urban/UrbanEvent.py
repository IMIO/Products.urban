# -*- coding: utf-8 -*-
#
# File: UrbanEvent.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.utils import WIDGET_DATE_END_YEAR
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from DateTime import DateTime

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.ATContentTypes.interfaces.file import IATFile
from Products.CMFCore.utils import getToolByName

from collective.plonefinder.browser.interfaces import IFinderUploadCapable
from collective.quickupload.interfaces import IQuickUploadCapable
from Products.urban.interfaces import IUrbanDoc
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import is_attachment
from Products.urban.utils import setOptionalAttributes
from Products.urban import UrbanMessage as _
from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from zope.component import getUtility, getMultiAdapter
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.engine.interfaces import IRuleStorage

from plone import api

from zope.i18n import translate


slave_fields_transfertype = (
    {
        "name": "transferDescription",
        "action": "hide",
        "hide_values": ("full",),
    },
)
##/code-section module-header

schema = Schema(
    (
        DateTimeField(
            name="eventDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                label_method="eventDateLabel",
                starting_year=1930,
                ending_year=2100,
                label=_("urban_label_eventDate", default="Eventdate"),
            ),
            default_method="getDefaultTime",
        ),
        StringField(
            name="depositType",
            widget=SelectionWidget(
                label=_("urban_label_depositType", default="Deposittype"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("deposittype", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        DateTimeField(
            name="transmitDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_transmitDate", default="Transmitdate"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="transmitToClaimantsDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_(
                    "urban_label_transmitToClaimantsDate",
                    default="Transmittoclaimantsdate",
                ),
            ),
            optional=True,
        ),
        DateTimeField(
            name="receiptDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_receiptDate", default="Receipt date"),
            ),
            optional=True,
        ),
        StringField(
            name="receivedDocumentReference",
            widget=StringField._properties["widget"](
                label=_(
                    "urban_label_receivedDocumentReference",
                    default="Receiveddocumentreference",
                ),
            ),
            optional=True,
        ),
        DateTimeField(
            name="auditionDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_auditionDate", default="Auditiondate"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="decisionDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_decisionDate", default="Decisiondate"),
            ),
            optional=True,
        ),
        StringField(
            name="decision",
            widget=SelectionWidget(
                label=_("urban_label_decision", default="Decision"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("decisions", inUrbanConfig=True),
            default_method="getDefaultValue",
        ),
        StringField(
            name="collegeOpinion",
            widget=SelectionWidget(
                label=_("urban_label_collegeOpinion", default="Collegeopinion"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("collegeopinions", inUrbanConfig=True),
            default_method="getDefaultValue",
        ),
        TextField(
            name="decisionText",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_decisionText", default="Decisiontext"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        DateTimeField(
            name="recourseDecisionDisplayDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_(
                    "urban_label_recourseDecisionDisplayDate",
                    default="Recoursedecisiondisplaydate",
                ),
            ),
            optional=True,
        ),
        StringField(
            name="recourseDecision",
            widget=SelectionWidget(
                label=_("urban_label_recourseDecision", default="Recoursedecision"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("recoursedecisions", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        StringField(
            name="adviceAgreementLevel",
            widget=SelectionWidget(
                format="select",
                label=_(
                    "urban_label_adviceAgreementLevel", default="Adviceagreementlevel"
                ),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary="listAdviceAgreementLevels",
        ),
        BooleanField(
            name="isOptional",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_("urban_label_isOptional", default="Isoptional"),
            ),
        ),
        StringField(
            name="externalDecision",
            widget=SelectionWidget(
                label=_("urban_label_externalDecision", default="Advice"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("externaldecisions", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        TextField(
            name="opinionText",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_opinionText", default="Opiniontext"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        TextField(
            name="analysis",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_analysis", default="Analysis"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        ReferenceField(
            name="eventRecipient",
            widget=ReferenceBrowserWidget(
                label=_("urban_label_eventRecipient", default="Destinataire"),
                allow_search=1,
                allow_browse=0,
                show_indexes=1,
                show_index_selector=1,
                available_indexes={
                    "getFirstname": "First name",
                    "getSurname": "Surname",
                },
                wild_card_search=True,
            ),
            allowed_types=("Recipient", "Applicant", "Architect"),
            optional=True,
            relationship="recipients",
        ),
        ReferenceField(
            name="urbaneventtypes",
            widget=ReferenceBrowserWidget(
                visible=False,
                label=_("urban_label_urbaneventtypes", default="Urbaneventtypes"),
            ),
            allowed_types=("EventConfig", "OpinionEventConfig", "FollowUpEventConfig"),
            multiValued=0,
            relationship="UrbanEventType",
        ),
        TextField(
            name="pmTitle",
            allowable_content_types=("text/plain",),
            widget=TextAreaWidget(
                label=_("urban_label_pmTitle", default="Pmtitle"),
            ),
            default_method="getDefaultText",
            default_content_type="text/plain",
            default_output_type="text/plain",
            optional=True,
            pm_text_field=True,
        ),
        TextField(
            name="pmDescription",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pmDescription", default="Pmdescription"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
            pm_text_field=True,
        ),
        TextField(
            name="pmMotivation",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pmMotivation", default="Pmmotivation"),
                i18n_domain="urban",
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
            pm_text_field=True,
        ),
        TextField(
            name="pmDecision",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_pmDecision", default="Pmdecision"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
            pm_text_field=True,
        ),
        TextField(
            name="officeCoordinate",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_officeCoordinate", default="Officecoordinate"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        TextField(
            name="suspensionReason",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_suspensionReason", default="Suspensionreason"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        DateTimeField(
            name="suspensionEndDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_suspensionEndDate", default="suspensionEndDate"),
            ),
            optional=True,
        ),
        StringField(
            name="delegateSignatures",
            widget=SelectionWidget(
                format="radio",
                label=_("urban_label_delegateSignatures", default="Delegatesignatures"),
            ),
            enforceVocabulary=True,
            optional=True,
            vocabulary=UrbanVocabulary("delegatesignatures", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="mainSignatures",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_mainSignatures", default="Mainsignatures"),
            ),
            multiValued=True,
            vocabulary=UrbanVocabulary("mainsignatures", inUrbanConfig=False),
            default_method="getDefaultValue",
        ),
        StringField(
            name="bank_account",
            widget=StringField._properties["widget"](
                label=_("urban_label_bank_account", default="Bank_account"),
            ),
            optional=True,
        ),
        StringField(
            name="bank_account_owner",
            widget=StringField._properties["widget"](
                label=_("urban_label_bank_account_owner", default="Bank_account_owner"),
            ),
            optional=True,
        ),
        StringField(
            name="amount_collected",
            widget=StringField._properties["widget"](
                label=_("urban_label_amount_collected", default="Amount_collected"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="displayDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_displayDate", default="Displaydate"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="displayDateEnd",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_displayDateEnd", default="Displaydateiend"),
            ),
            optional=True,
        ),
        TextField(
            name="decisionProject",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_decisionProject", default="Decisionproject"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        TextField(
            name="misc_description",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_("urban_label_description", default="Description"),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/x-html-safe",
            optional=True,
        ),
        DateTimeField(
            name="reportCreationDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_reportCreationDate", default="ReportCreationDate"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="reportReceptionDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_(
                    "urban_label_reportReceptionDate", default="ReportReceptionDate"
                ),
            ),
            optional=True,
        ),
        DateTimeField(
            name="paymentDeadline",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_paymentDeadline", default="PaymentDeadline"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="ultimeDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_ultimeDate", default="UltimeDate"),
            ),
            optional=True,
        ),
        LinesField(
            name="transferType",
            widget=SelectionWidget(
                format="select",
                label=_("urban_label_transfertype", default="TransferType"),
            ),
            vocabulary="listTransferType",
            optional=True,
        ),
        TextField(
            name="transferDescription",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_transferdescription", default="TransferDescription"
                ),
            ),
            default_method="getDefaultText",
            default_content_type="text/html",
            default_output_type="text/html",
            optional=True,
        ),
        DateTimeField(
            name="videoConferenceDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1960,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_videoConferenceDate", default="videoConferencedate"),
            ),
            optional=True,
        ),
        DateTimeField(
            name="validityEndDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1960,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_validityEndDate", default="validityEndDate"),
            ),
            optional=True,
        ),

    ),
)

##code-section after-local-schema #fill in your manual code here
optional_fields = [
    field.getName()
    for field in schema.filterFields(isMetadata=False)
    if field.getName() not in ["eventDate", "urbaneventtypes"]
]
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanEvent_schema = BaseFolderSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
UrbanEvent_schema["title"].widget.condition = "python:here.showTitle()"
UrbanEvent_schema["title"].default_method = "defaultTitle"
UrbanEvent_schema["title"].required = False
##/code-section after-schema


class UrbanEvent(BaseFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEvent, IFinderUploadCapable, IQuickUploadCapable)

    meta_type = "UrbanEvent"
    _at_rename_after_creation = False
    __ac_local_roles_block__ = True

    schema = UrbanEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("getDefaultValue")

    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return [""]

        empty_value = getattr(field, "multivalued", "") and [] or ""
        if hasattr(field, "vocabulary") and isinstance(
            field.vocabulary, UrbanVocabulary
        ):
            licence = context.aq_parent
            return field.vocabulary.get_default_values(licence)
        return empty_value

    security.declarePublic("getDefaultText")

    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = getToolByName(self, "portal_urban")
        return urban_tool.getTextDefaultValue(
            field.getName(), context, html=html, config=self.getUrbaneventtypes()
        )

    def getKeyDate(self):
        event_type = self.getUrbaneventtypes()
        keydate_field = "eventDate"
        if event_type:
            keydate_fields = [date for date in event_type.getKeyDates()]
            keydate_field = keydate_fields and keydate_fields[0] or "eventDate"
        keydate = self.getField(keydate_field).get(self)

        return keydate

    def getDefaultTime(self):
        return DateTime()

    security.declarePublic("getTemplates")

    def getTemplates(self):
        """
        Returns contained templates (File)
        """
        if not self.getUrbaneventtypes():
            return []
        return self.getUrbaneventtypes().getTemplates()

    security.declarePublic("eventDateLabel")

    def eventDateLabel(self):
        """
        Returns the variable label
        """
        return self.getUrbaneventtypes().getEventDateLabel()

    security.declarePublic("listAdviceAgreementLevels")

    def listAdviceAgreementLevels(self):
        """
        Vocabulary for field 'adviceAgreementLevels'
        """
        lst = [
            [
                "agreementlevel_read_advice",
                translate(
                    "agreementlevel_read_advice",
                    "urban",
                    context=self.REQUEST,
                    default="Read advice",
                ),
            ],
            [
                "agreementlevel_respect_charges",
                translate(
                    "agreementlevel_respect_charges",
                    "urban",
                    context=self.REQUEST,
                    default="Respect charges",
                ),
            ],
        ]

        vocab = []
        # we add an empty vocab value of type "choose a value"
        val = translate(
            "urban", EMPTY_VOCAB_VALUE, context=self, default=EMPTY_VOCAB_VALUE
        )
        vocab.append(("", val))
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic("isInt")

    def isInt(self, s):
        """
        Check if 's' is an integer, return True or False...
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    security.declarePublic("parseCadastreStreet")

    def parseCadastreStreet(self, street):
        """
        Return a parsed version of data from Cadastre so we obtain something
        more beautiful to display
        """
        if street is None:
            return "NO ADDRESS FOUND"
        print "\n\n Street: " + street
        i = 0
        toreturn = ""
        while (i < len(street)) and (street[i] != ","):
            toreturn = toreturn + street[i]
            i = i + 1
        if i < len(street):
            while (i < len(street)) and (not self.isInt(street[i])):
                i = i + 1
            toreturn = toreturn + " "
        while i < len(street):
            toreturn = toreturn + street[i]
            i = i + 1
        return toreturn

    security.declarePublic("parseCadastreName")

    def parseCadastreName(self, name):
        """ """
        print "\n\nName: " + name
        i = 0
        nom1 = ""
        prenom1 = ""
        nom2 = ""
        prenom2 = ""
        toreturn = ""
        if name.rfind(",") > 0:
            while (i < len(name)) and (name[i] != ","):
                nom1 = nom1 + name[i]
                i = i + 1
            if i < len(name):
                i = i + 1
            while (i < len(name)) and (name[i] != " "):
                i = i + 1
            if i < len(name):
                i = i + 1
            while (i < len(name)) and (name[i] not in ["&", " "]):
                prenom1 = prenom1 + name[i]
                i = i + 1
            if i < len(name) and name[i] != "&":
                i = i + 1
            toreturn = prenom1
            if prenom1 != "":
                toreturn = toreturn + " "
            toreturn = toreturn + nom1
            if name.rfind("&") > 0 and i < name.rfind("&"):
                while (i < len(name)) and (name[i] != "&"):
                    i = i + 1
                if name[i] == "&":
                    toreturn = toreturn + " - M. "
                    i = i + 1
                while (i < len(name)) and (name[i] != ","):
                    nom2 = nom2 + name[i]
                    i = i + 1
                if i < len(name):
                    i = i + 1
                while (i < len(name)) and (name[i] != " "):
                    i = i + 1
                if i < len(name):
                    i = i + 1
                while (i < len(name)) and (name[i] != " "):
                    prenom2 = prenom2 + name[i]
                    i = i + 1
                toreturn = toreturn + prenom2
                if prenom2 != "":
                    toreturn = toreturn + " "
                toreturn = toreturn + nom2
        else:
            toreturn = name
        return "M. %s" % toreturn

    security.declarePublic("getDocuments")

    def getDocuments(self):
        """
        Return the documents (File) of the UrbanEvent
        """
        documents = [obj for obj in self.objectValues() if IUrbanDoc.providedBy(obj)]
        return documents

    security.declarePublic("getAttachments")

    def getAttachments(self):
        """
        Return the attachments (File) of the UrbanEvent
        """
        attachments = [obj for obj in self.objectValues() if is_attachment(obj)]
        return attachments

    def getRecipients(self):
        """
        Returns a list of recipients
        """
        return self.objectValues("RecipientCadastre")

    security.declarePublic("RecipientsCadastreCSV")

    def RecipientsCadastreCSV(self):
        """
        Generates a fake CSV file used in POD templates
        """
        recipients = self.objectValues("RecipientCadastre")
        toreturn = "[CSV]TitreNomPrenom|AdresseLigne1|AdresseLigne2"
        wft = getToolByName(self, "portal_workflow")
        for recipient in recipients:
            # do not take "disabled" recipients into account
            if wft.getInfoFor(recipient, "review_state") == "disabled":
                continue
            street = recipient.getStreet() and recipient.getStreet() or ""
            number = recipient.getNumber() and recipient.getNumber() or ""
            address = recipient.getAdr1() and recipient.getAdr1() or ""
            toreturn = (
                toreturn
                + "%"
                + recipient.getName()
                + "|"
                + street
                + ", "
                + number
                + "|"
                + address
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getFormattedDate")

    def getFormattedDate(
        self,
        date=None,
        withCityNamePrefix=False,
        forDelivery=False,
        translatemonth=True,
    ):
        """
        Return the date
        withCityNamePrefix and forDelivery are exclusive in the logic here above
        """
        if not date:
            date = self.getEventDate()
        elif type(date) == str:
            date = self.getField(date).getAccessor(self)()
        tool = getToolByName(self, "portal_urban")
        formattedDate = tool.formatDate(date, translatemonth=translatemonth)
        cityName = unicode(tool.getCityName(), "utf-8")
        if withCityNamePrefix:
            return translate(
                "formatted_date_with_cityname",
                "urban",
                context=self.REQUEST,
                mapping={
                    "cityName": cityName,
                    "formattedDate": formattedDate.decode("utf8"),
                },
            ).encode("utf8")
        if forDelivery:
            return translate(
                "formatted_date_for_delivery",
                "urban",
                context=self.REQUEST,
                mapping={
                    "cityName": cityName,
                    "formattedDate": formattedDate.decode("utf8"),
                },
            ).encode("utf8")
        return formattedDate

    def attributeIsUsed(self, attrName):
        """ """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return attrName in self.getUrbaneventtypes().getActivatedFields()
        else:
            return False

    def showTitle(self):
        """ """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return urbanEventType.getShowTitle()
        else:
            return False

    def defaultTitle(self):
        """ """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return urbanEventType.Title()
        else:
            return ""

    security.declarePublic("getUrbaneventtypes")

    def getUrbaneventtypes(self):
        """ """
        event_config = self.getField("urbaneventtypes").get(self)
        if not event_config and self.REQUEST.form.get("urbaneventtypes"):
            uid_catalog = api.portal.get_tool("uid_catalog")
            event_config = uid_catalog(UID=self.REQUEST.form["urbaneventtypes"])[
                0
            ].getObject()
        return event_config

    security.declarePublic("getDecision")

    def getDecision(self, theObject=False):
        """
        Returns the decision value or the UrbanVocabularyTerm if theObject=True
        """
        res = self.getField("decision").get(self)
        if res and theObject:
            tool = getToolByName(self, "portal_urban")
            res = getattr(tool.decisions, res)
        return res

    security.declarePublic("getDecision")

    def getExternalDecision(self, theObject=False):
        """
        Returns the external decision value or the UrbanVocabularyTerm if theObject=True
        """
        res = self.getField("externalDecision").get(self)
        if res == [""]:
            res = ""
        if res and theObject:
            tool = getToolByName(self, "portal_urban")
            res = getattr(tool.externaldecisions, res)
        return res

    def get_state(self):
        state = api.content.get_state(self)
        return state

    security.declarePublic("listTransferType")

    def listTransferType(self):
        """
        This vocabulary for field transferType returns the types of transfer (full, partial)
        """
        vocab = (
            ("full", translate(_("full_transfer"), context=self.REQUEST)),
            ("partial", translate(_("partial_transfer"), context=self.REQUEST)),
        )
        return DisplayList(vocab)

    def getObjectPosition(self, id):
        # !!! Fix to handle file exporting on Event with c.exportimport
        return 0

    def get_all_rules_for_this_event(self):
        portal = api.portal.get()
        assignable = IRuleAssignmentManager(portal)
        storage = getUtility(IRuleStorage)

        rules = []
        for key in [key for key in assignable]:
            conditions = []
            rule = storage.get(key, None)
            if rule is None:
                continue
            if not rule.enabled:
                continue
            for condition in rule.conditions:
                class EventTemp():
                    object = self
                executable = getMultiAdapter((self, condition, EventTemp), IExecutable)
                conditions.append(executable())
            if all(conditions):
                rules.append(rule)
        return rules


registerType(UrbanEvent, PROJECTNAME)
# end of class UrbanEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer
