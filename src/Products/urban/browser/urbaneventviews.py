# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from Products.urban import services
from Products.urban import UrbanMessage as _
from Products.urban import utils
from Products.urban.browser.licence.licenceview import LicenceView
from Products.urban.browser.mapview import MapView
from Products.urban.browser.table.urbantable import ApplicantHistoryTable
from Products.urban.browser.table.urbantable import ApplicantTable
from Products.urban.browser.table.urbantable import ClaimantsTable
from Products.urban.browser.table.urbantable import DocumentsTable
from Products.urban.browser.table.urbantable import EventAttachmentsTable
from Products.urban.browser.table.urbantable import RecipientsCadastreTable
from Products.urban.interfaces import IGenericLicence
from Products.urban.send_mail_action.forms import MAIL_ACTION_KEY
from StringIO import StringIO
from eea.faceted.vocabularies.autocomplete import IAutocompleteSuggest
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.namedfile.field import NamedFile
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope.annotation import interfaces
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import Interface

import collections
import csv
import logging
import re
import json


logger = logging.getLogger("Urban Event")

claimants_csv_fieldnames = [
    "personTitle",
    "name1",
    "name2",
    "society",
    "street",
    "number",
    "zipcode",
    "city",
    "country",
    "email",
    "phone",
    "gsm",
    "nationalRegister",
    "claimType",
    "hasPetition",
    "outOfTime",
    "claimDate",
    "claimingText",
    "wantDecisionCopy",
]

EXCEL_HEADER_RECIPIENT = "Titre (sel.),Nom,Prénom,Rue,N° de police,Code postal (num.),Localité,Pays (sel.),N° registre national,CAPAKEY,Nature parcelle,Rue parcelle,N° de police parcelle"
CARTO_HEADER = '"CAPAKEY";"nature";"datesituation";"proprio"'
EXCEL_HEADER_CLAIMANT = '"Titre (sel.)","Nom","Prénom","Société","Rue","N° de police","Code postal (num.)","Localité","Pays (sel.)","E-mail","Téléphone","GSM","N° registre national","Type de réclamation","Pétition","Hors délai","Date de réception","Texte de la réclamation","Souhaite une copie de la décision"'


class UrbanEventView(BrowserView):
    """
    This manage the view of UrbanEvent
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        plone_utils = api.portal.get_tool("plone_utils")
        if self.is_planned_mailing:
            plone_utils.addPortalMessage(
                _("The mailings will be ready tomorrow!"), type="warning"
            )
        # disable portlets
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)

    def getActivatedFields(self):
        """
        Return all the activated fields of this UrbanEvent
        """
        context = aq_inner(self.context)
        linkedUrbanEventType = context.getUrbaneventtypes()
        fields = [
            i
            for i in context.schema.fields()
            if i.schemata == "default"
            and not hasattr(i, "optional")
            and i.widget.visible
            and i.widget.visible["view"] == "visible"
        ]
        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            field = context.getField(activatedField)
            if field not in fields:
                fields.append(field)
        return fields

    def getFieldsToShow(self):
        """
        Return fields to display about the UrbanEvent
        """
        fields = [
            f for f in self.getActivatedFields() if not hasattr(f, "pm_text_field")
        ]
        return fields

    def getDateCustomLabel(self):
        """ """
        return self.context.getUrbaneventtypes().getEventDateLabel()

    def getPmFields(self):
        """
        Return activated pm fields to build the pm summary
        """
        fields = [f for f in self.getActivatedFields() if hasattr(f, "pm_text_field")]
        return fields

    def show_pm_summary(self):
        """ """
        return bool(self.getPmFields())

    def empty_pm_summary(self):
        """ """
        fields = self.getPmFields()

        for field_ in fields:
            text = field_.get(self.context)
            if text:
                return False

        return True

    def isTextField(self, field):
        return field.type == "text"

    def mayAddUrbanEvent(self):
        """
        Return True if the current user may add an UrbanEvent
        """
        context = aq_inner(self.context)
        member = api.portal.get_tool("portal_membership").getAuthenticatedMember()
        if member.has_permission("ATContentTypes: Add File", context):
            return True
        return False

    def mayAddAttachment(self):
        """
        Return True if the current user may add an attachment (File)
        """
        context = aq_inner(self.context)
        member = api.portal.get_tool("portal_membership").getAuthenticatedMember()
        if member.has_permission("ATContentTypes: Add File", context):
            return True
        return False

    def renderGeneratedDocumentsListing(self):
        event = aq_inner(self.context)
        documents = event.getDocuments()
        if not documents:
            return ""

        documentlisting = DocumentsTable(self.context, self.request, values=documents)
        documentlisting.update()
        return documentlisting.render()

    def renderAttachmentsListing(self):
        event = aq_inner(self.context)
        attachments = event.getAttachments()
        if not attachments:
            return ""

        table = EventAttachmentsTable(self.context, self.request, values=attachments)
        table.update()
        return table.render()

    def getListOfTemplatesToGenerate(self):
        """
        Return a list of dicts. Each dict contains all the infos needed in the html <href> tag to create the
        corresponding link for document generation
        """
        context = aq_inner(self.context)
        template_list = []
        for template in context.getTemplates():
            if template.can_be_generated(context):
                template_list.append(
                    {
                        "name": template.id.split(".")[0],
                        "title": template.Title(),
                        "class": "",
                        "href": self._generateDocumentHref(context, template),
                    }
                )

        for generated_doc in context.objectValues():
            for template in template_list:
                if generated_doc.Title() == template["title"]:
                    template["class"] = "urban-document-already-created"
        return template_list

    def _generateDocumentHref(self, context, template):
        """ """
        link = "{base_url}/urban-document-generation?template_uid={uid}".format(
            base_url=context.absolute_url(), uid=template.UID()
        )
        return link

    def getUrbaneventtypes(self):
        """
        Return the accessor urbanEventTypes()
        """
        context = aq_inner(self.context)
        return context.getUrbaneventtypes()

    def get_state(self):
        return api.content.get_state(self.context)

    def getApplicants(self):
        """ """
        applicants = [
            appl
            for appl in self.context.ap_parent.objectValues("Applicant")
            if appl.portal_type == "Applicant"
            and api.content.get_state(appl) == "enabled"
        ]
        corporations = self.getCorporations()
        applicants.extend(corporations)
        return applicants

    def get_applicants_history(self):
        return [
            appl
            for appl in self.context.ap_parent.objectValues("Applicant")
            if api.content.get_state(appl) == "disabled"
        ]

    def renderApplicantListing(self):
        if not self.context.getApplicants():
            return ""
        contacttable = ApplicantTable(self.context, self.request)
        contacttable.update()
        return contacttable.render()

    def renderApplicantHistoryListing(self):
        if not self.context.getApplicants():
            return ""
        table = ApplicantHistoryTable(self.context, self.request)
        table.update()
        return table.render()

    @property
    def is_planned_mailing(self):
        planned_mailings = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncMailing.mailings_to_do"
            )
            or {}
        )
        is_planned = self.context.UID() in planned_mailings
        return is_planned

    def is_CODT2024(self):
        licence = self.context.aq_parent
        return licence.is_CODT2024()

    def is_not_CODT2024(self):
        licence = self.context.aq_parent
        return licence.is_not_CODT2024()

    def getProrogationDelay(self):
        licence = self.context.aq_parent
        return licence.getProrogationDelay()

    def getCompletenessDelay(self):
        licence = self.context.aq_parent
        return licence.getCompletenessDelay()

    def getReferFDDelay(self):
        licence = self.context.aq_parent
        return licence.getReferFDDelay()

    def getFDAdviceDelay(self):
        licence = self.context.aq_parent
        return licence.getFDAdviceDelay()

    def mail_send(self):
        annotations = interfaces.IAnnotations(self.context)
        notif = annotations.get(MAIL_ACTION_KEY, None)
        if notif is None or len(notif) == 0:
            return False

        notif.sort(key=lambda elem: elem["time"])
        user = notif[-1].get("user")
        username = notif[-1].get("username", None)
        if username is None or username == "":
            username = user

        return _(
            "Mail already send for ${title} by ${user}, ${date}",
            mapping={
                "title": safe_unicode(notif[-1]["title"].lower()),
                "user": safe_unicode(username),
                "date": notif[-1]["time"].strftime("%d/%m/%Y, %H:%M:%S"),
            },
        )


class IImportClaimantListingForm(Interface):

    listing_file_claimants = NamedFile(
        title=_(u"Listing file (claimants)"),
        description=_(
            u"A specially formatted CSV file must be used for import. "
            u"The CSV file can be created from the ODT template file "
            u"(can be downloaded <a href='/++resource++Products.urban/reclamant_reimport.ods'>here</a>) "
            u"by 'save as' in CSV format"
        ),
    )


class ImportClaimantListingForm(form.Form):

    method = "post"
    fields = field.Fields(IImportClaimantListingForm)
    ignoreContext = True

    @button.buttonAndHandler(_("Import"), name="import-claimants")
    def handleImport(self, action):
        inquiry_UID = self.context.UID()
        planned_claimants_import = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncClaimantsImports.claimants_to_import"
            )
            or []
        )
        data, errors = self.extractData()
        if errors:
            interfaces.IAnnotations(self.context)["urban.claimants_to_import"] = ""
            if inquiry_UID in planned_claimants_import:
                planned_claimants_import.remove(inquiry_UID)
        else:
            csv_file = data["listing_file_claimants"]
            csv_integrity_error = self.validate_csv_integrity(csv_file)
            if csv_integrity_error:
                api.portal.show_message(csv_integrity_error, self.request, "error")
            else:
                interfaces.IAnnotations(self.context)[
                    "urban.claimants_to_import"
                ] = csv_file.data
                if inquiry_UID not in planned_claimants_import:
                    planned_claimants_import.append(inquiry_UID)
        api.portal.set_registry_record(
            "Products.urban.interfaces.IAsyncClaimantsImports.claimants_to_import",
            planned_claimants_import,
        )
        return not bool(errors)

    def validate_csv_integrity(self, csv_file):
        if csv_file.contentType not in ("text/csv"):
            return _(
                u"The imported file (${name}) doesn't appear to be a CSV file.",
                mapping={u"name": csv_file.filename},
            )

        error = _(
            u"The imported file (${name}) couldn't be read properly. Please verify its structure and try again.",
            mapping={u"name": csv_file.filename},
        )

        if not csv_file.data.startswith(EXCEL_HEADER_CLAIMANT):
            return error

        try:
            reader = csv.DictReader(
                StringIO(csv_file.data),
                claimants_csv_fieldnames,
                delimiter=",",
                quotechar='"',
            )
            claimant_args = [
                row for row in reader if row["name1"] or row["name2"] or row["society"]
            ][1:]
        except csv.Error as error:
            return error

        try:
            claimant_args = [
                self.check_claimant_arg(row) for row in claimant_args
            ]
        except ValueError as err:
            return _(
                "Import cancel : error with claimant ${claimant} on value ${value}",
                mapping={
                    "claimant": err[0],
                    "value": err[1]
                }
            )

        return None

    def check_claimant_arg(self, row):
        hasPetition = row.get("hasPetition", False)
        outOfTime = row.get("outOfTime", False)
        wantDecisionCopy = row.get("wantDecisionCopy", False)

        try:
            handle_boolean_value(hasPetition)
        except ValueError as err:
            raise ValueError(row["name1"], "hasPetition")

        try:
            handle_boolean_value(outOfTime)
        except ValueError as err:
            raise ValueError(row["name1"], "outOfTime")

        try:
            handle_boolean_value(wantDecisionCopy)
        except ValueError as err:
            raise ValueError(row["name1"], "wantDecisionCopy")
        
        return row


class IImportRecipientListingForm(Interface):

    listing_file_recipients = NamedFile(
        title=_(u"Listing file (recipients)"),
        description=_(
            u"A specially formatted CSV file must be used for import. "
            u"The CSV file can be created from the ODT template file "
            u"(can be downloaded <a href='/++resource++Products.urban/destinaires_reimport.ods'>here</a>) "
            u"by 'save as' in CSV format"
        ),
    )


class ImportRecipientListingForm(form.Form):

    method = "post"
    fields = field.Fields(IImportRecipientListingForm)
    ignoreContext = True

    @button.buttonAndHandler(_("Import"), name="import-recipients")
    def handleImport(self, action):
        self.import_recipients_from_csv()
        self.request.response.redirect(
            self.context.absolute_url()
            + "/#fieldsetlegend-urbaneventinquiry_recipients"
        )

    def handle_data_to_add_recipients(self, recipient_args):

        portal_urban = api.portal.get_tool("portal_urban")
        plone_utils = api.portal.get_tool("plone_utils")

        new_national_reg_ids = [
            recipient_arg["id"]
            for recipient_arg in recipient_args
            if recipient_arg["id"]
        ]

        # look for national registry numbers present multiple times in CSV
        # fail import if duplicates are found
        counter = collections.Counter(new_national_reg_ids)
        duplicate_numbers = [
            number for (number, count) in counter.most_common() if count > 1
        ]
        if duplicate_numbers:
            msg = _(
                u"duplicate_numbers_found_msg",
                default=u"Some national registry numbers are used multiple times in the CSV; please remove them and try again.\n${numbers}",
                mapping={u"numbers": ", ".join(duplicate_numbers)},
            )
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return

        # look for national registry numbers already used as recipient object ids
        # fail import if duplicates are found
        existing_object_ids = list(self.context.objectIds())
        duplicate_ids = set(new_national_reg_ids).intersection(existing_object_ids)
        if duplicate_ids:
            msg = _(
                u"duplicate_ids_found_msg",
                default=u"Some national registry numbers already exist in this list; please remove them from the CSV and try again.\n${ids}",
                mapping={u"ids": ", ".join(duplicate_ids)},
            )
            IStatusMessage(self.request).addStatusMessage(msg, type="error")
            return

        country_mapping = {"": ""}
        country_folder = portal_urban.country
        for country_obj in country_folder.objectValues():
            country_mapping[country_obj.Title()] = country_obj.id

        for recipient_arg in recipient_args:
            if "personTitle" in recipient_arg:
                del recipient_arg["personTitle"]  # no use for it yet

            if not recipient_arg["id"]:
                recipient_arg["id"] = plone_utils.normalizeString(
                    " ".join([recipient_arg["name"], recipient_arg["firstname"]])
                )
                if recipient_arg["id"] in self.context.objectIds():
                    count = 1
                    new_id = "{0}-{1}".format(recipient_arg["id"], count)
                    while new_id in self.context.objectIds():
                        count += 1
                        new_id = "{0}-{1}".format(recipient_arg["id"], count)
                    recipient_arg["id"] = new_id

            recipient_arg["country"] = country_mapping[recipient_arg["country"]]
            recipient_arg["adr1"] = "{} {}".format(
                recipient_arg["zipcode"], recipient_arg["city"]
            )
            recipient_arg["adr2"] = "{} {}".format(
                recipient_arg["street"], recipient_arg["number"]
            )
            # create recipient
            with api.env.adopt_roles(["Manager"]):
                recipient_id = self.context.invokeFactory(
                    "RecipientCadastre", **recipient_arg
                )
                recipient_obj = getattr(self.context, recipient_id)

        plone_utils.addPortalMessage(_("urban_imported_recipients"), type="info")

    def handle_data_from_excel(self, data):
        fieldnames = [
            "personTitle",
            "name",
            "firstname",
            "street",
            "number",
            "zipcode",
            "city",
            "country",
            "id",
            "capakey",
            "parcel_nature",
            "parcel_street",
            "parcel_police_number",
        ]

        if data:
            reader = csv.DictReader(
                StringIO(data), fieldnames, delimiter=",", quotechar='"'
            )
        else:
            reader = []

        try:
            recipient_args = [row for row in reader if row["name"]][1:]
        except csv.Error as error:
            IStatusMessage(self.request).addStatusMessage(
                _(
                    u"The CSV file couldn't be read properly. Please verify its structure and try again."
                ),
                type="error",
            )
            return

        self.handle_data_to_add_recipients(recipient_args)

    def secondary_extract_proprio(self, proprio):
        country_pattern = (
            r"^\d{10,11}\s.*\s\((?:\d{4}-\d{2}-\d{2})?\)\sAdr:\s(?P<country>[A-Z]{2})"
        )
        match_country = re.match(country_pattern, proprio)
        if not match_country:
            return None
        pattern_mapping = {
            "FR": (
                r"^(?P<id>\d{10,11})\s(?P<name>.*)\s"
                r"\((?P<dob>(?:\d{4}-\d{2}-\d{2})?)\)\s"
                r"Adr:\s(?P<country>[A-Z]{2})\s+"
                r"(?P<number>\d+[\s\/-]?[a-zA-Z]?(?:Bis)?\s?\d*),?\s+"
                r"(?P<street>.+?)\s(?P<zipcode>\d{5})\s+(?P<city>.+)$"
            )
        }
        country_code = match_country.groupdict()["country"]
        if country_code not in pattern_mapping:
            return None
        match = re.match(pattern_mapping[country_code], proprio)
        return match

    def extract_proprio(self, proprios, capakey, parcel_nature):
        proprio_list = proprios.split(";")
        errors = []
        proprios = []
        for proprio in proprio_list:
            pattern_be = (
                r"^(?P<id>\d{10,11})\s(?P<name>.*)\s"
                r"\((?P<dob>(?:\d{4}-\d{2}-\d{2})?)\)\s"
                r"Adr:\s(?P<country>[A-Z]{2})\s(?P<zipcode>\d{4,5})\s+"
                r"(?P<city>[A-ZÈÉÊËÁÀÂÖÔÏÎÚÙÛÜŸÇ\s-]+)\s+"
                r"(?P<street>.+?)\s+(?P<number>\d+[\s\/-]?[a-zA-Z]?\s?\d*)$"
            )
            match = re.match(pattern_be, proprio.strip())
            if not match:
                second_match = self.secondary_extract_proprio(proprio.strip())
                if not second_match:
                    errors.append(proprio)
                    continue
                match = second_match
            match_dict = match.groupdict()
            match_dict["capakey"] = capakey
            match_dict["parcel_nature"] = parcel_nature
            match_dict["name"] = match_dict["name"].strip()
            country = match_dict.get("country", None)
            if country:
                country_mapping = {
                    "BE": "Belgique",
                    "FR": "France",
                    "NL": "Pays Bas",
                    "LU": "Luxembourg",
                    "DE": "Allemagne",
                }
                match_dict["country"] = country_mapping.get(country, "")
            if match_dict["dob"] != "":
                names = match_dict["name"].split(" ")
                match_dict["firstname"] = names.pop(0)
                match_dict["name"] = " ".join(names)
            del match_dict["dob"]
            proprios.append(match_dict)
        return proprios, errors

    def handle_data_from_carto(self, data):
        if data:
            reader = csv.DictReader(StringIO(data), delimiter=";", quotechar='"')
        else:
            reader = []
        recipient_args = []
        errors = []
        for parcel in reader:
            capakey = parcel.get("CAPAKEY", None)
            parcel_nature = parcel.get("nature", None)
            proprios = parcel.get("proprio", None)
            if not proprios:
                continue
            proprio_list, error = self.extract_proprio(proprios, capakey, parcel_nature)
            if error:
                errors += error
            recipient_args += proprio_list
        if errors:
            errors = [error.decode("utf-8") for error in errors]
            msg = _(
                u"Couldn't import this(these) owner(s): ${owners}",
                mapping={"owners": "; ".join(list(set(errors)))},
            )
            logger.warning(
                u"Couldn't import this(these) owner(s): \n\t{}".format(
                    "\n\t".join(list(set(errors)))
                )
            )
            IStatusMessage(self.request).addStatusMessage(msg, type="warning")
        id_numbers = []
        new_recipient_args = []
        for recipient in recipient_args:
            if recipient["id"] in id_numbers:
                continue
            id_numbers.append(recipient["id"])
            new_recipient_args.append(recipient)

        self.handle_data_to_add_recipients(new_recipient_args)

    def import_recipients_from_csv(self):
        data, errors = self.extractData()
        if errors:
            return False

        csv_file = data["listing_file_recipients"]
        data = csv_file.data
        if data.startswith(EXCEL_HEADER_RECIPIENT):
            self.handle_data_from_excel(data)
        elif data.startswith(CARTO_HEADER):
            self.handle_data_from_carto(data)
        else:
            msg = u"The CSV file couldn't be read properly. Please verify its structure and try again."
            IStatusMessage(self.request).addStatusMessage(
                _(msg),
                type="error",
            )

def handle_boolean_value(value):
    if value == "Vrai" or value is True:
        return True
    if value == "Faux" or value == "" or value is False:
        return False
    raise ValueError(value)

class UrbanEventInquiryBaseView(UrbanEventView, MapView, LicenceView):
    """
    This manage the base view of UrbanEventInquiry
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)
        self.import_claimants_listing_form = ImportClaimantListingForm(context, request)
        self.import_claimants_listing_form.update()
        self.import_recipients_listing_form = ImportRecipientListingForm(
            context, request
        )
        self.import_recipients_listing_form.update()

    @property
    def has_planned_claimant_import(self):
        planned_claimants_import = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncClaimantsImports.claimants_to_import"
            )
            or []
        )
        is_planned = self.context.UID() in planned_claimants_import
        return is_planned

    def import_claimants_from_csv(self):
        portal_urban = api.portal.get_tool("portal_urban")
        plone_utils = api.portal.get_tool("plone_utils")
        site = api.portal.get()

        titles_mapping = {"": ""}
        titles_folder = portal_urban.persons_titles
        for title_obj in titles_folder.objectValues():
            titles_mapping[title_obj.Title()] = title_obj.id

        country_mapping = {"": ""}
        country_folder = portal_urban.country
        for country_obj in country_folder.objectValues():
            country_mapping[country_obj.Title()] = country_obj.id

        claim_type_mapping = {
            "Écrite": "writedClaim",
            "Orale": "oralClaim",
        }

        claimants_file = interfaces.IAnnotations(self.context)[
            "urban.claimants_to_import"
        ]
        if claimants_file:
            reader = csv.DictReader(
                StringIO(claimants_file),
                claimants_csv_fieldnames,
                delimiter=",",
                quotechar='"',
            )
        else:
            reader = []
        try:
            claimant_args = [
                row
                for row in reader
                if row["name1"] or row["name2"] or row["society"]
            ][1:]
        except csv.Error as error:
            return
        
        try:
            claimant_args = [
                self.handle_claimant_arg(row, titles_mapping, country_mapping, site, claim_type_mapping)
                for row in claimant_args
            ]
        except ValueError as err:
            msg = _(
                "Import cancel : error with claimant ${claimant} on value ${value}",
                mapping={
                    "claimant": err[0],
                    "value": err[1]
                }
            )
            plone_utils.addPortalMessage(msg, type="error")
            return

        for claimant_arg in claimant_args:
            # create claimant
            with api.env.adopt_roles(["Manager"]):
                self.context.invokeFactory("Claimant", **claimant_arg)
            logger.info(
                "imported claimant {id}, {name} {surname}".format(
                    id=claimant_arg["id"],
                    name=claimant_arg["name1"],
                    surname=claimant_arg["name2"],
                )
            )

    def handle_claimant_arg(self, row, titles_mapping, country_mapping, site, claim_type_mapping):
        # default values
        if not row["claimType"]:
            row["claimType"] = "Écrite"

        try:
            row["hasPetition"] = handle_boolean_value(
                row.get("hasPetition", False)
            )
        except ValueError as err:
            raise ValueError(row["name1"], "hasPetition")

        try:
            row["outOfTime"] = handle_boolean_value(
                row.get("outOfTime", False)
            )
        except ValueError as err:
            raise ValueError(row["name1"], "outOfTime")

        try:
            row["wantDecisionCopy"] = handle_boolean_value(
                row.get("wantDecisionCopy", False)
            )
        except ValueError as err:
            raise ValueError(row["name1"], "wantDecisionCopy")

        # mappings
        row["personTitle"] = titles_mapping.get(
            row["personTitle"], "notitle"
        )
        row["country"] = country_mapping.get(
            row["country"], "belgium"
        )
        row["id"] = site.plone_utils.normalizeString(
            row["name1"] + row["name2"] + row["society"]
        )
        row["claimType"] = claim_type_mapping[row["claimType"]]
        count = 0
        if row["id"] in self.context.objectIds():
            count += 1
            new_id = row["id"] + "-" + str(count)
            while new_id in self.context.objectIds():
                count += 1
                new_id = row["id"] + "-" + str(count)
            row["id"] = new_id
        return row

    def getParcels(self):
        context = aq_inner(self.context)
        return context.getParcels()

    def renderClaimantsListing(self):
        if not self.context.getClaimants():
            return ""
        contactlisting = ClaimantsTable(self.context, self.request)
        contactlisting.update()
        return contactlisting.render()

    def getLinkedInquiry(self):
        context = aq_inner(self.context)
        return context.getLinkedInquiry()

    def getInquiryFields(self):
        """
        This will return fields to display about the Inquiry
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        fields = []
        if not linkedInquiry:
            # this should not happen...
            return None
        displayed_fields = self.getUsedAttributes()
        schemata = (
            IGenericLicence.providedBy(linkedInquiry) and "urban_inquiry" or "default"
        )
        inquiry_fields = utils.getSchemataFields(
            linkedInquiry, displayed_fields, schemata
        )
        for inquiry_field in inquiry_fields:
            if inquiry_field.__name__ == "claimsText":
                # as this text can be very long, we do not want to show it with the other
                # fields, we will display it in the "Claimants" part of the template
                continue
            fields.append(inquiry_field)

        return fields

    def getInquiryReclamationNumbers(self):

        inquiryReclamationNumbers = []
        context = aq_inner(self.context)
        totalOral = 0
        totalWrite = 0
        if context.getClaimants():
            for claimant in context.getClaimants():
                if claimant.getClaimType() == "oralClaim":
                    totalOral += 1
                elif claimant.getClaimType() == "writedClaim":
                    totalWrite += 1

        inquiryReclamationNumbers.append(totalOral)
        inquiryReclamationNumbers.append(totalWrite)
        return inquiryReclamationNumbers

    def getLinkToTheInquiries(self):
        """
        This will return a link to the inquiries on the linked licence
        """
        context = aq_inner(self.context)
        return (
            context.aq_inner.aq_parent.absolute_url() + "/#fieldsetlegend-urban_inquiry"
        )

    def getLinkedInquiryTitle(self):
        """
        This will return the title of the linked Inquiry
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        if linkedInquiry:
            if IGenericLicence.providedBy(linkedInquiry):
                # we do not use Title as this inquiry is the licence
                return linkedInquiry.generateInquiryTitle()
            else:
                return linkedInquiry.Title()

    def check_dates_for_suspension(self):
        inquiry_event = self.context
        start_date = inquiry_event.getInvestigationStart()
        end_date = inquiry_event.getInvestigationEnd()
        if not start_date or not end_date:
            return True, "", ""

        licence = inquiry_event.aq_parent
        portal_urban = api.portal.get_tool("portal_urban")
        suspension_periods = portal_urban.get_offday_periods("inquiry_suspension")

        for suspension_period in suspension_periods:
            suspension_start = DateTime(str(suspension_period["start_date"]))
            suspension_end = DateTime(str(suspension_period["end_date"]))
            if end_date >= suspension_start and end_date < suspension_end + 1:
                return (
                    False,
                    suspension_start.strftime("%d/%m/%Y"),
                    suspension_end.strftime("%d/%m/%Y"),
                )
        return True, "", ""


class UrbanEventAnnouncementView(UrbanEventInquiryBaseView):
    """
    This manage the view of UrbanEventAnnouncement
    """

    def __init__(self, context, request):
        super(UrbanEventAnnouncementView, self).__init__(context, request)
        plone_utils = api.portal.get_tool("plone_utils")
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils.addPortalMessage(
                _(
                    "This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !"
                ),
                type="error",
            )
        if self.has_planned_claimant_import:
            plone_utils.addPortalMessage(
                _("The claimants import will be ready tomorrow!"), type="warning"
            )
        if self.is_planned_mailing:
            plone_utils.addPortalMessage(
                _("The mailings will be ready tomorrow!"), type="warning"
            )
        (
            suspension_check,
            suspension_start,
            suspension_end,
        ) = self.check_dates_for_suspension()
        if not suspension_check:
            plone_utils.addPortalMessage(
                _(
                    "Suspension period from to: please check the end date",
                    mapping={"from": suspension_start, "to": suspension_end},
                ),
                type="warning",
            )
        # disable portlets
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)


class UrbanEventInquiryView(UrbanEventInquiryBaseView):
    """
    This manage the view of UrbanEventInquiry
    """

    def __init__(self, context, request):
        super(UrbanEventInquiryView, self).__init__(context, request)
        plone_utils = api.portal.get_tool("plone_utils")
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils.addPortalMessage(
                _(
                    "This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !"
                ),
                type="error",
            )
        if self.hasPOWithoutAddress():
            plone_utils.addPortalMessage(
                _(
                    "There are parcel owners without any address found! Desactivate them!"
                ),
                type="warning",
            )
        if self.is_planned_inquiry:
            plone_utils.addPortalMessage(
                _("The parcel radius search will be ready tomorrow!"), type="warning"
            )
        if self.is_planned_mailing:
            plone_utils.addPortalMessage(
                _("The mailings will be ready tomorrow!"), type="warning"
            )
        if self.has_planned_claimant_import:
            plone_utils.addPortalMessage(
                _("The claimants import will be ready tomorrow!"), type="warning"
            )
        (
            suspension_check,
            suspension_start,
            suspension_end,
        ) = self.check_dates_for_suspension()
        if not suspension_check:
            plone_utils.addPortalMessage(
                _(
                    "Suspension period from to: please check the end date",
                    mapping={"from": suspension_start, "to": suspension_end},
                ),
                type="warning",
            )
        # disable portlets
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)

    def __call__(self):
        if "find_recipients_cadastre" in self.request.form:
            radius = self.getInquiryRadius()
            return self.getInvestigationPOs(radius)
        if "find_address_cadastre" in self.request.form:
            radius = self.getInquiryRadius()
            return self.get_investigation_adress(radius)
        return self.index()

    def renderRecipientsCadastreListing(self):
        recipients = self.context.getRecipients()
        if not recipients:
            return ""
        contactlisting = RecipientsCadastreTable(
            self.context, self.request, values=recipients
        )
        contactlisting.update()
        return contactlisting.render()

    def getRecipients(self):
        context = aq_inner(self.context)
        return context.getRecipients()

    def hasPOWithoutAddress(self):
        context = aq_inner(self.context)
        for parcel_owner in context.getRecipients(onlyActive=True):
            if not parcel_owner.getStreet() or not parcel_owner.getAdr1():
                return True
        return False

    @property
    def is_planned_inquiry(self):
        planned_inquiries = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do"
            )
            or {}
        )
        is_planned = self.context.UID() in planned_inquiries
        return is_planned

    def create_recipient_cadastre(self, location, parcel, street_uid, zip_scope=None):
        context = aq_inner(self.context)
        number = location.get("number", "").encode("utf-8")
        street_obj = api.content.get(UID=street_uid)
        street = street_obj.streetName.encode("utf-8")
        city_obj = street_obj.getCity()
        city = city_obj.title.encode("utf-8")
        zipcode = city_obj.zipCode.encode("utf-8")
        if zip_scope is not None and zipcode not in zip_scope:
            zip_scope.append(zipcode)
        normalizer = getUtility(IIDNormalizer)
        id = normalizer.normalize("{}-{}".format(street, number))
        if id in context:
            return zip_scope
        new_owner_id = context.invokeFactory(
            "RecipientCadastre",
            id=id,
            # keep adr1 and adr2 fields for historical reasons.
            adr1="{} {}".format(zipcode, city),
            adr2="{} {}".format(street, number),
            number=number,
            street=street,
            zipcode=zipcode,
            city=city,
            capakey=parcel.capakey,
            parcel_street=parcel.locations
            and parcel.locations.values()[0]["street_name"]
            or "",
            parcel_police_number=parcel.locations
            and parcel.locations.values()[0]["number"]
            or "",
            parcel_nature=", ".join(parcel.natures),
        )
        owner_obj = getattr(context, new_owner_id)
        owner_obj.setTitle("{} {}".format(street, number))
        return zip_scope

    def get_investigation_adress(self, radius=0, force=False):
        context = aq_inner(self.context)
        urban_tool = api.portal.get_tool("portal_urban")

        licence = context.aq_inner.aq_parent
        cadastre = services.cadastre.new_session()
        neighbour_parcels = cadastre.query_parcels_in_radius(
            center_parcels=licence.getParcels(), radius=radius
        )

        if (
            not force
            and urban_tool.getAsyncInquiryRadius()
            and len(neighbour_parcels) > 40
        ):
            planned_inquiries = (
                api.portal.get_registry_record(
                    "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_address_to_do"
                )
                or {}
            )
            planned_inquiries[self.context.UID()] = radius
            api.portal.set_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_address_to_do",
                planned_inquiries,
            )
            return self.request.response.redirect(
                self.context.absolute_url()
                + "/#fieldsetlegend-urbaneventinquiry_recipients"
            )

        errors = []
        zip_scope = []
        too_many_result = []
        cache = {}
        for parcel in neighbour_parcels:
            locations = parcel.locations
            for location in locations.values():
                address = location.get("street_name", None)
                number = location.get("number", None)
                if address is None or address == "" or number is None or number == "":
                    continue
                if address in cache:
                    zip_scope = self.create_recipient_cadastre(
                        location, parcel, cache[address], zip_scope
                    )
                self.request.set("term", address)
                adapter = getMultiAdapter(
                    (self.context, self.request),
                    IAutocompleteSuggest,
                    name="sreets-autocomplete-suggest",
                )
                results = adapter.compute_suggestions()
                if len(results) == 0:
                    msg = _(
                        "Can't find the street : ${street}",
                        mapping={"street": address},
                    )
                    logger.error("Can't find the street : {}".format(address))
                    IStatusMessage(self.request).addStatusMessage(msg, type="error")
                    continue
                if len(results) > 1:
                    too_many_result.append(
                        {"results": results, "location": location, "parcel": parcel}
                    )
                    continue
                cache[address] = results[0]["id"]
                zip_scope = self.create_recipient_cadastre(
                    location, parcel, results[0]["id"], zip_scope
                )
        cadastre.close()
        self.check_too_many_result(too_many_result, zip_scope)
        return context.REQUEST.RESPONSE.redirect(
            context.absolute_url() + "/#fieldsetlegend-urbaneventinquiry_recipients"
        )

    def check_too_many_result(self, too_many_result, zip_scope):
        cache = {}
        for item in too_many_result:
            street_name = item["location"]["street_name"]
            if street_name in cache:
                self.create_recipient_cadastre(
                    item["location"], item["parcel"], cache[street_name]
                )
            for result in item["results"]:
                street = api.content.get(UID=result["id"])
                zip_code = street.getCity().zipCode
                if zip_code in zip_scope:
                    self.create_recipient_cadastre(
                        item["location"], item["parcel"], result["id"]
                    )
                    cache[street_name] = result["id"]
                    break

    def getInvestigationPOs(self, radius=0, force=False):
        """
        Search parcel owners in a radius of 50 meters...
        """
        # if we do the search again, we first delete old datas...
        # remove every RecipientCadastre
        context = aq_inner(self.context)
        urban_tool = api.portal.get_tool("portal_urban")
        if self.is_planned_inquiry and not force:
            return self.request.response.redirect(self.context.absolute_url())

        licence = context.aq_inner.aq_parent
        cadastre = services.cadastre.new_session()
        neighbour_parcels = cadastre.query_parcels_in_radius(
            center_parcels=licence.getParcels(), radius=radius
        )

        if (
            not force
            and urban_tool.getAsyncInquiryRadius()
            and len(neighbour_parcels) > 40
        ):
            planned_inquiries = (
                api.portal.get_registry_record(
                    "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do"
                )
                or {}
            )
            planned_inquiries[self.context.UID()] = radius
            api.portal.set_registry_record(
                "Products.urban.interfaces.IAsyncInquiryRadius.inquiries_to_do",
                planned_inquiries,
            )
            return self.request.response.redirect(
                self.context.absolute_url()
                + "/#fieldsetlegend-urbaneventinquiry_recipients"
            )

        for parcel in neighbour_parcels:
            for owner_id, owner in parcel.owners.iteritems():
                name = str(owner["name"].encode("utf-8"))
                firstname = str(owner["firstname"].encode("utf-8"))
                country = str(owner["country"].encode("utf-8"))
                zipcode = str(owner["zipcode"].encode("utf-8"))
                city = str(owner["city"].encode("utf-8"))
                street = str(owner["street"].encode("utf-8"))
                number = str(owner["number"].encode("utf-8"))

                # to avoid having several times the same Recipient (that could for example be on several parcels
                # we first look in portal_catalog where Recipients are catalogued
                owner_obj = owner_id and getattr(context, owner_id, None)
                if owner_id and not owner_obj:
                    logger.info("Import owner {}{}".format(name, firstname))
                    new_owner_id = context.invokeFactory(
                        "RecipientCadastre",
                        id=owner_id,
                        name=name,
                        firstname=firstname,
                        # keep adr1 and adr2 fields for historical reasons.
                        adr1="{} {}".format(zipcode, city),
                        adr2="{} {}".format(street, number),
                        number=number,
                        street=street,
                        zipcode=zipcode,
                        city=city,
                        country=country.lower(),
                        capakey=parcel.capakey,
                        parcel_street=parcel.locations
                        and parcel.locations.values()[0]["street_name"]
                        or "",
                        parcel_police_number=parcel.locations
                        and parcel.locations.values()[0]["number"]
                        or "",
                        parcel_nature=", ".join(parcel.natures),
                    )
                    owner_obj = getattr(context, new_owner_id)
                    owner_obj.setTitle("{} {}".format(name, firstname))
        cadastre.close()
        return context.REQUEST.RESPONSE.redirect(
            context.absolute_url() + "/#fieldsetlegend-urbaneventinquiry_recipients"
        )

    def getInquiryRadius(self):
        licence = self.context.aq_parent
        investigation_radius = getattr(licence, "investigation_radius", None)

        if investigation_radius is None:
            return 50
        if isinstance(investigation_radius, list):
            investigation_radius = investigation_radius[0]

        try:
            output = int(investigation_radius.split("m")[0])
        except Exception as e:
            output = 50

        return output
