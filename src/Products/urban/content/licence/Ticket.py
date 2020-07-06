# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.config import PROJECTNAME
from Products.urban.config import URBAN_TYPES
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import (
    ReferenceBrowserWidget,
)
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from plone import api

from zope.i18n import translate

slave_fields_bound_inspection = (
    {
        "name": "workLocations",
        "action": "hide",
        "hide_values": (True,),
    },
)

optional_fields = ["managed_by_prosecutor"]

schema = Schema(
    (
        StringField(
            name="referenceProsecution",
            widget=StringField._properties["widget"](
                size=60,
                label=_(
                    "urban_label_referenceProsecution", default="Referenceprosecution"
                ),
            ),
            schemata="urban_description",
        ),
        StringField(
            name="policeTicketReference",
            widget=StringField._properties["widget"](
                size=60,
                label=_(
                    "urban_label_policeTicketReference", default="Policeticketreference"
                ),
            ),
            schemata="urban_description",
        ),
        ReferenceField(
            name="bound_inspection",
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=False,
                force_close_on_insert=True,
                startup_directory="urban",
                show_indexes=False,
                wild_card_search=True,
                restrict_browsing_to_startup_directory=True,
                label=_("urban_label_bound_inspection", default="Bound inspection"),
            ),
            allowed_types=["Inspection"],
            schemata="urban_description",
            multiValued=False,
            relationship="bound_inspection",
        ),
        BooleanField(
            name="use_bound_inspection_infos",
            default=False,
            widget=MasterBooleanWidget(
                slave_fields=slave_fields_bound_inspection,
                label=_(
                    "urban_label_use_bound_inspection_infos",
                    default="Use_bound_inspection_infos",
                ),
            ),
            schemata="urban_description",
        ),
        ReferenceField(
            name="bound_licences",
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=False,
                force_close_on_insert=True,
                startup_directory="urban",
                show_indexes=False,
                wild_card_search=True,
                restrict_browsing_to_startup_directory=True,
                label=_("urban_label_bound_licences", default="Bound licences"),
            ),
            allowed_types=[
                t
                for t in URBAN_TYPES
                if t
                not in [
                    "Ticket",
                    "Inspection",
                    "ProjectMeeting",
                    "PatrimonyCertificate",
                    "CODT_NotaryLetter",
                    "CODT_UrbanCertificateOne" "NotaryLetter",
                    "UrbanCertificateOne",
                ]
            ],
            schemata="urban_description",
            multiValued=True,
            relationship="bound_licences",
        ),
        BooleanField(
            name="managed_by_prosecutor",
            default=False,
            widget=BooleanField._properties["widget"](
                label=_(
                    "urban_label_managed_by_prosecutor", default="Managed_by_prosecutor"
                ),
            ),
            schemata="urban_description",
        ),
    ),
)

setOptionalAttributes(schema, optional_fields)

Ticket_schema = (
    BaseFolderSchema.copy()
    + getattr(GenericLicence, "schema", Schema(())).copy()
    + schema.copy()
)


class Ticket(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ITicket)

    meta_type = "Ticket"
    _at_rename_after_creation = True
    schema = Ticket_schema

    security.declarePublic("getApplicants")

    def getWorkLocations(self):
        if self.getUse_bound_inspection_infos():
            bound_licence = self.getBound_inspection()
            if bound_licence:
                return bound_licence.getWorkLocations()

        field = self.getField("workLocations")
        worklocations = field.get(self)
        return worklocations

    def getParcels(self):
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                return bound_inspection.getParcels()

        return super(Ticket, self).getParcels()

    security.declarePublic("getOfficialParcels")

    def getOfficialParcels(self):
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                return bound_inspection.getOfficialParcels()

        return super(Ticket, self).getOfficialParcels()

    security.declarePublic("updateTitle")

    def updateTitle(self):
        """
        Update the title to clearly identify the licence
        """
        if self.getWorkLocations():
            worklocations = self.getWorkLocationSignaletic().split("  et ")[0]
        else:
            worklocations = translate(
                "no_address_defined", "urban", context=self.REQUEST
            ).encode("utf8")
        title = "{}{} - {} - {}".format(
            self.getReference(),
            self.getPoliceTicketReference()
            and " - " + self.getPoliceTicketReference()
            or "",
            self.getLicenceSubject(),
            worklocations,
        )
        self.setTitle(title)
        self.reindexObject(
            idxs=(
                "Title",
                "sortable_title",
            )
        )

    security.declarePublic("getApplicants")

    def getApplicants(self):
        """ """
        applicants = super(Ticket, self).getApplicants()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                applicants.extend(bound_inspection.getApplicants())

        return list(set(applicants))

    security.declarePublic("get_applicants_history")

    def get_applicants_history(self):
        applicants = super(Ticket, self).get_applicants_history()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                applicants.extend(bound_inspection.get_applicants_history())

        return list(set(applicants))

    security.declarePublic("getProprietaries")

    def getProprietaries(self):
        """ """
        proprietaries = super(Ticket, self).getProprietaries()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                proprietaries.extend(bound_inspection.getProprietaries())

        return proprietaries

    security.declarePublic("getCorporations")

    def getCorporations(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "Corporation"
            and api.content.get_state(corp) == "enabled"
        ]
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                corporations.extend(bound_inspection.getCorporations())
        return list(set(corporations))

    security.declarePublic("get_corporations_history")

    def get_corporations_history(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "Corporation"
            and api.content.get_state(corp) == "disabled"
        ]
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                corporations.extend(bound_inspection.get_corporations_history())
        return list(set(corporations))

    security.declarePublic("getTenants")

    def getTenants(self):
        """
        Return the list of plaintiffs for the Licence
        """
        tenants = [
            app for app in self.objectValues("Applicant") if app.portal_type == "Tenant"
        ]
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                tenants.extend(bound_inspection.getTenants())
        return list(set(tenants))

    security.declarePublic("getPlaintiffs")

    def getPlaintiffs(self):
        """
        Return the list of plaintiffs for the Licence
        """
        plaintiffs = [
            app
            for app in self.objectValues("Applicant")
            if app.portal_type == "Plaintiff"
        ]
        corporations = self.getCorporationPlaintiffs()
        plaintiffs.extend(corporations)
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                plaintiffs.extend(bound_inspection.getPlaintiffs())
        return plaintiffs

    security.declarePublic("getCorporationPlaintiffs")

    def getCorporationPlaintiffs(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "CorporationPlaintiff"
        ]
        return corporations

    def getLastDeposit(self):
        return self.getLastEvent(interfaces.IDepositEvent)

    def getLastMissingPart(self):
        return self.getLastEvent(interfaces.IMissingPartEvent)

    def getLastMissingPartDeposit(self):
        return self.getLastEvent(interfaces.IMissingPartDepositEvent)

    def getLastTheTicket(self):
        return self.getLastEvent(interfaces.ITheTicketEvent)

    def getLastAcknowledgment(self):
        return self.getLastEvent(interfaces.IAcknowledgmentEvent)

    def getLastTechnicalAnalysis(self):
        return self.getLastEvent(interfaces.ITechnicalAnalysis)

    security.declarePublic("mayAddFollowUpEvent")

    def mayAddFollowUpEvent(self, followup_id):
        """
        This is used as TALExpression for the UrbanEventFollowUp
        We may add an UrbanEventFollowUp only if the previous one is closed
        """
        report_events = self.getAllReportEvents()
        if not report_events:
            return False

        limit = 0
        for report_event in report_events:
            if followup_id in report_event.getFollowup_proposition():
                limit += 1
        limit = limit - len(self.getFollowUpEventsById(followup_id))
        return limit > 0

    security.declarePublic("getLastReportEvent")

    def getLastReportEvent(self):
        return self.getLastEvent(interfaces.IInspectionReportEvent)

    security.declarePublic("getAllReportEvents")

    def getAllReportEvents(self):
        return self.getAllEvents(interfaces.IInspectionReportEvent)

    security.declarePublic("getCurrentReportEvent")

    def getCurrentReportEvent(self):
        last_analysis_date = None
        for action in self.workflow_history.values()[0][::-1]:
            if action["review_state"] == "technical_analysis":
                last_analysis_date = action["time"]
                break

        if not last_analysis_date:
            return

        report_events = self.getAllReportEvents()
        for report in report_events:
            workflow_history = report.workflow_history.values()[0]
            creation_date = workflow_history[0]["time"]
            if creation_date > last_analysis_date:
                return report

    security.declarePublic("getFollowUpEventsById")

    def getFollowUpEventsById(self, followup_id):
        followup_events = self.objectValues("UrbanEventFollowUp")
        if followup_id == "":
            return followup_events
        res = []
        for followup_event in followup_events:
            if followup_event.getFollowUpId() == followup_id:
                res.append(followup_event)
        return res

    security.declarePublic("getLastFollowUpEvent")

    def getLastFollowUpEvent(self):
        return self.getLastEvent(interfaces.IUrbanEventFollowUp)

    security.declarePublic("getAllFollowUpEvents")

    def getAllFollowUpEvents(self):
        return self.getAllEvents(interfaces.IUrbanEventFollowUp)

    security.declarePublic("getCurrentFollowUpEvents")

    def getCurrentFollowUpEvents(self):
        last_answer_date = None
        for action in self.workflow_history.values()[0][::-1]:
            if action["review_state"] == "waiting_for_agreement":
                last_answer_date = action["time"]
                break
        if not last_answer_date:
            return []

        report = self.getCurrentReportEvent()
        if not report:
            return []
        selected_follow_ups = [fw_up for fw_up in report.getFollowup_proposition()]
        if not selected_follow_ups:
            return []

        followup_events = self.getAllFollowUpEvents()
        to_return = []
        for followup in followup_events:
            workflow_history = followup.workflow_history.values()[0]
            creation_date = workflow_history[0]["time"]
            if creation_date > last_answer_date:
                uet = followup.getUrbaneventtypes()
                if uet and uet.id in selected_follow_ups:
                    to_return.append(followup)
        return to_return

    security.declarePublic("getLastFollowUpEventWithDelay")

    def getLastFollowUpEventWithDelay(self):
        return self.getLastEvent(interfaces.IUrbanEventFollowUpWithDelay)


registerType(Ticket, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema["folderCategory"].widget.visible = {"edit": "invisible", "view": "invisible"}
    schema.moveField("referenceProsecution", after="reference")
    schema.moveField("policeTicketReference", after="referenceProsecution")
    schema.moveField("bound_inspection", before="workLocations")
    schema.moveField("use_bound_inspection_infos", after="bound_inspection")
    schema.moveField("bound_licences", after="use_bound_inspection_infos")
    schema.moveField("managed_by_prosecutor", after="foldermanagers")
    schema.moveField("description", after="managed_by_prosecutor")
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


finalize_schema(Ticket_schema)
