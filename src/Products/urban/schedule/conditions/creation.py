# -*- coding: utf-8 -*-

from DateTime import DateTime
from datetime import date
from datetime import datetime

from imio.schedule.config import states_by_status
from imio.schedule.config import STARTED
from imio.schedule.content.condition import CreationCondition

from Products.urban.schedule.conditions.base import BaseInspection
from Products.urban.schedule.interfaces import IFollowupDeadLineTask

from plone import api


class DepositDoneCondition(CreationCondition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container

        deposit_done = False
        deposit_event = licence.getLastDeposit()
        if deposit_event:
            deposit_done = api.content.get_state(deposit_event) == "closed"

        return deposit_done


class AcknowledgmentDoneCondition(CreationCondition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container

        acknowledgment_done = False
        acknowledgment_event = licence.getLastAcknowledgment()
        if acknowledgment_event:
            acknowledgment_done = (
                api.content.get_state(acknowledgment_event) == "closed"
            )

        return acknowledgment_done


class DefaultAcknowledgmentCondition(CreationCondition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container
        acknowledgment_event = licence.getLastAcknowledgment()
        return not acknowledgment_event


class DefaultCODTAcknowledgmentCondition(CreationCondition):
    """
    There's no default acknowlegdment created.
    """

    def evaluate(self):
        licence = self.task_container
        acknowledgment_event = licence.getLastDefaultAcknowledgment()
        return acknowledgment_event


class SingleComplementAsked(CreationCondition):
    """
    Licence MissingPart event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_asked = False
        missing_part_event = licence.getLastMissingPart()
        if missing_part_event:
            complements_asked = api.content.get_state(missing_part_event) == "closed"
        else:
            return False

        previous_tasks = self.task_config.get_closed_tasks(self.task_container)
        last_task = previous_tasks and previous_tasks[-1] or None
        if last_task and last_task.created() > missing_part_event.created():
            return False

        return complements_asked


class SingleComplementReceived(CreationCondition):
    """
    Licence MissingPartDeposit event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_received = False
        deposit_part_event = licence.getLastMissingPartDeposit()
        if deposit_part_event:
            complements_received = api.content.get_state(deposit_part_event) == "closed"

        return complements_received


class ComplementsTransmitToSPW(CreationCondition):
    """
    Licence MissingPartTransmitToSPW event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_transmit = False
        deposit_part_event = licence.getLastMissingPartTransmitToSPW()
        if deposit_part_event:
            complements_transmit = api.content.get_state(deposit_part_event) == "closed"

        return complements_transmit


class IncompleteForSixMonths(CreationCondition):
    """
    Unique licence have been incomplete for 6 months
    """

    def evaluate(self):
        licence = self.task_container
        missing_part_event = licence.getLastMissingPart()
        days_delta = 0
        if missing_part_event:
            days_delta = DateTime() - missing_part_event.getEventDate()

        return days_delta >= 183


class WillHaveInquiry(CreationCondition):
    """
    'inquiry' is selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            initiative_inquiry = (
                "initiative_inquiry" in licence.getProcedureChoiceModifiedBlueprints()
            )
            inquiry = "inquiry" in licence.getProcedureChoiceModifiedBlueprints()
        else:
            initiative_inquiry = "initiative_inquiry" in licence.getProcedureChoice()
            inquiry = "inquiry" in licence.getProcedureChoice()
        have_inquiry = initiative_inquiry or inquiry
        return have_inquiry


class WillHaveAnnouncement(CreationCondition):
    """
    'light_inquiry' or 'initative_light_inquiry' is selected
    on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            light_inquiry = (
                "light_inquiry" in licence.getProcedureChoiceModifiedBlueprints()
            )
            initiative_light_inquiry = (
                "initiative_light_inquiry"
                in licence.getProcedureChoiceModifiedBlueprints()
            )
        else:
            light_inquiry = "light_inquiry" in licence.getProcedureChoice()
            initiative_light_inquiry = (
                "initiative_light_inquiry" in licence.getProcedureChoice()
            )
        announcement = light_inquiry or initiative_light_inquiry
        return announcement


class HasNewInquiryCondition(CreationCondition):
    """
    Licence has a new inquiry defined.
    """

    def evaluate(self):
        licence = self.task_container

        inquiry_event = licence.getLastInquiry()  # Inquiry event
        if inquiry_event:
            inquiries = licence.getAllInquiries()  # Inquiries objects

            # if the linked inquiry of the last inquiry event is not the last
            # inquiry object means we have a new inquiry (but its event has not
            # been created yet)
            missing_inquiry_event = inquiry_event.getLinkedInquiry() != inquiries[-1]

            return missing_inquiry_event

        return False


class NoInquiryCondition(CreationCondition):
    """
    Licence has no inquiry selected on procedureChoice field.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            no_inquiry = "inquiry" not in licence.getProcedureChoiceModifiedBlueprints()
        else:
            no_inquiry = "inquiry" not in licence.getProcedureChoice()
        return no_inquiry


class InquiryCondition(CreationCondition):
    """
    Licence has an inquiry defined.
    """

    def evaluate(self):
        licence = self.task_container

        inquiry = licence.getLastInquiry()
        has_inquiry = bool(inquiry)

        return has_inquiry


class AnnouncementCondition(CreationCondition):
    """
    Licence has an announcement defined.
    """

    def evaluate(self):
        licence = self.task_container

        announcement = licence.getLastAnnouncement()
        has_announcement = bool(announcement)

        return has_announcement


class AnnouncementDoneCondition(CreationCondition):
    """
    Licence announcement event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        announcement_done = False
        announcement_event = licence.getLastAnnouncement()
        if announcement_event:
            announcement_done = api.content.get_state(announcement_event) == "closed"

        return announcement_done


class HasOpinionRequests(CreationCondition):
    """
    There are some values selected in the field sollicitOpinionsTo.
    """

    def evaluate(self):
        licence = self.task_container
        return licence.getSolicitOpinionsTo()


class OpinionRequestsDone(CreationCondition):
    """
    Each opinion request event has received an opinion.
    <=> is on the state 'opinion_given'
    """

    def evaluate(self):
        licence = self.task_container
        or_events = licence.getOpinionRequests()

        if len(or_events) != len(licence.getSolicitOpinionsTo()):
            return False

        for opinion in or_events:
            if api.content.get_state(opinion) != "opinion_given":
                return False

        return True


class IsInternalOpinionRequest(CreationCondition):
    """
    Urban event is an internal opinion request
    """

    def evaluate(self):
        registry = api.portal.get_tool("portal_registry")
        registry_field = registry[
            "Products.urban.interfaces.IInternalOpinionServices.services"
        ]
        opinion_request = self.task_container
        opinion_config = opinion_request.getUrbaneventtypes()

        if not opinion_config.getIs_internal_service():
            return False

        record = registry_field.get(opinion_config.getInternal_service(), None)
        if record and self.task_config.id in [
            record["task_answer_id"],
            record["task_validate_id"],
        ]:
            return True

        return False


class HasFDOpinionRequest(CreationCondition):
    """
    'FD' is selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            FD = "FD" in licence.getProcedureChoiceModifiedBlueprints()
        else:
            FD = "FD" in licence.getProcedureChoice()
        return FD


class HasNoFDOpinionRequest(CreationCondition):
    """
    'FD' is not selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            no_FD = "FD" not in licence.getProcedureChoice()
        else:
            no_FD = "FD" not in licence.getProcedureChoiceModifiedBlueprints()
        return no_FD


class DepositDateIsPast20Days(CreationCondition):
    """
    The deposit date is past by 20 days
    """

    def evaluate(self):
        licence = self.task_container

        deposit_event = licence.getLastDeposit()
        if deposit_event:
            date1 = deposit_event.eventDate.asdatetime()
            date2 = datetime.now(date1.tzinfo)
            return (date2.date() - date1.date()).days > 20
        return False


class DepositDateIsPast30Days(CreationCondition):
    """
    The deposit date is past by 30 days
    """

    def evaluate(self):
        licence = self.task_container

        deposit_event = licence.getLastDeposit()
        if deposit_event:
            date1 = deposit_event.eventDate.asdatetime()
            date2 = datetime.now(date1.tzinfo)
            return (date2.date() - date1.date()).days > 30
        return False


class DepositDateIsUnder30Days(DepositDateIsPast30Days):
    """
    The deposit date is past by 30 days
    """

    def evaluate(self):
        return not super(DepositDateIsUnder30Days, self).evaluate()


class IncompleteForTheFirstTime(CreationCondition):
    """
    This is the first time that the folder is incomplete
    """

    def evaluate(self):
        licence = self.task_container
        missing_part_deposit = licence.getLastMissingPartDeposit()
        return missing_part_deposit is None


class IncompleteForTheSecondTime(CreationCondition):
    """
    This is the second time that the folder is incomplete
    """

    def evaluate(self):
        licence = self.task_container
        missing_part_deposit = licence.getLastMissingPartDeposit()
        if missing_part_deposit is None:
            return False
        incomplete_UID = self.task_config.aq_parent["incomplet"].UID()
        brains = api.content.find(
            context=licence,
            task_config_UID=incomplete_UID,
            review_state="closed",
        )
        first_incomplete_done = len(brains) > 0
        if not first_incomplete_done:
            return False
        wf_history = licence.workflow_history
        incomplete_history = [
            tr
            for tr in wf_history[wf_history.keys()[0]]
            if tr["action"] == "isincomplete"
        ]
        two_incomplete_transitions = 2 <= len(incomplete_history)

        if not two_incomplete_transitions:
            return False
        return True


class SPWProjectReceivedCondition(CreationCondition):
    """
    Licence SPW projetc receipt event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        receipt_done = False
        receipt_event = licence.getLastDecisionProjectFromSPW()
        if receipt_event:
            receipt_done = api.content.get_state(receipt_event) == "closed"

        return receipt_done


class LicenceAuthorityIsCollege(CreationCondition):
    """
    Environment licence authority is college
    """

    def evaluate(self):
        licence = self.task_container
        authority_is_college = licence.getAuthority() == "college"
        return authority_is_college


class IsNotTemporaryLicence(CreationCondition):
    """
    Environment licence procedure type is not temporary.
    """

    def evaluate(self):
        licence = self.task_container
        not_temporary = licence.getProcedureChoice() != "temporary"
        return not_temporary


class InspectionCreationCondition(CreationCondition, BaseInspection):
    """
    Base class for inspection condition checking values on the last report event
    Provides a method returning the last relevant inspection report event.
    """


class ShouldDoInspectionFollowups(InspectionCreationCondition):
    """
    Return true if follow_ups differents of 'ticket' and 'close' are selected in
    the current inspection report.
    """

    def evaluate(self):
        follow_ups = self.get_followups()
        return bool(follow_ups)


class ShouldWriteOneInspectionFollowUp(InspectionCreationCondition):
    """
    Return True if:
        - a followup proposition has no corresponding event created
        - a followup proposition event is not at least in the state to_validate
    """

    def evaluate(self):
        follow_ups = self.get_followups()
        follow_up_events = self.get_followup_events()
        if len(follow_up_events) < len(follow_ups):
            return True

        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "draft":
                return True
        return False


class SomeInspectionFollowupsAreWritten(InspectionCreationCondition):
    """
    At least one followup event is in the state 'to_validate'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "to_validate":
                return True
        return False


class SomeInspectionFollowupsToSend(InspectionCreationCondition):
    """
    At least one followup event is in the state 'to_send'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "to_send":
                return True
        return False


class ShouldEndInspection(InspectionCreationCondition):
    """
    Should end inspection when 'close' is selected in the followup proposition of the
    last inspection report event.
    """

    def evaluate(self):
        report = self.get_current_inspection_report()
        if report and "close" in report.getFollowup_proposition():
            return True
        return False


class ShouldCreateTicket(InspectionCreationCondition):
    """
    Should create Ticket when 'ticket' is selected in the followup proposition of the
    last inspection report event.
    """

    def evaluate(self):
        report = self.get_current_inspection_report()
        if (
            report
            and "ticket" in report.getFollowup_proposition()
            and not self.get_last_followup_ticket()
        ):
            return True
        return False


class FollowUpTicketCreated(InspectionCreationCondition):
    """
    A ticket has been created as an inspection followup result.
    """

    def evaluate(self):
        followup_ticket = self.get_last_followup_ticket()
        if not followup_ticket:
            return False
        created = api.content.get_state(followup_ticket) != "ended"
        return created


class FollowUpTicketClosed(InspectionCreationCondition):
    """
    The ticket created as a followup action has been closed.
    """

    def evaluate(self):
        followup_ticket = self.get_last_followup_ticket()
        if not followup_ticket:
            return False
        is_closed = api.content.get_state(followup_ticket) == "ended"
        # do this task only once per ticket
        if is_closed:
            same_closed_tasks = self.task_config.get_closed_tasks(self.task_container)
            ticket_workflow_history = followup_ticket.workflow_history.values()[0]
            ticket_creation_date = ticket_workflow_history[0]["time"]
            for task in same_closed_tasks:
                task_workflow_history = task.workflow_history.values()[0]
                task_creation_date = task_workflow_history[0]["time"]
                if task_creation_date > ticket_creation_date:
                    return False

        return is_closed


class FollowUpWithDelayClosed(InspectionCreationCondition):
    """
    The followup event created as a followup action has been closed.
    """

    def evaluate(self):
        followup_event = self.task_container.getLastFollowUpEventWithDelay()
        if not followup_event:
            return False
        is_closed = api.content.get_state(followup_event) == "closed"
        # do this task only once per followup event
        if is_closed:
            same_closed_tasks = self.task_config.get_closed_tasks(self.task_container)
            event_workflow_history = followup_event.workflow_history.values()[0]
            event_creation_date = event_workflow_history[0]["time"]
            for task in same_closed_tasks:
                task_workflow_history = task.workflow_history.values()[0]
                task_creation_date = task_workflow_history[0]["time"]
                if task_creation_date > event_creation_date:
                    return False

        return is_closed


class FollowUpWithDelayOverdue(CreationCondition):
    """
    The ticket created as a followup action has been closed.
    """

    def evaluate(self):
        inspection = self.task_container
        for obj in inspection.objectValues():
            if IFollowupDeadLineTask.providedBy(obj):
                task = obj
                if (
                    task.get_state() in states_by_status[STARTED]
                    and task.due_date < date.today()
                ):
                    return True
        return False


class ProsecutionAnswerOverDeadline(CreationCondition):
    """
    The ticket event has been closed under 90 days.
    """

    def evaluate(self):
        licence = self.task_container
        ticket_event = licence.getLastTheTicket()
        if ticket_event and ticket_event.getEventDate():
            over_delay = DateTime() - ticket_event.getEventDate() > 90
            return over_delay
        return False
