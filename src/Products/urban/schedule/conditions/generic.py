# -*- coding: utf-8 -*-

from datetime import date
from datetime import datetime

from imio.schedule.content.condition import Condition

from Products.urban.config import LICENCE_FINAL_STATES
from imio.schedule.config import states_by_status
from imio.schedule.config import STARTED

from Products.urban.schedule.conditions.base import BaseInspection
from Products.urban.schedule.interfaces import IFollowupDeadLineTask

from plone import api

from DateTime import DateTime


class DepositDoneCondition(Condition):
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


class SingleComplementAsked(Condition):
    """
    Licence MissingPart event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_asked = False
        missing_part_event = licence.getLastMissingPart()
        if missing_part_event:
            recent = self.task.creation_date < missing_part_event.creation_date
            complements_asked = api.content.get_state(missing_part_event) == "closed"
            complements_asked = complements_asked and recent

        return complements_asked


class SingleComplementReceived(Condition):
    """
    Licence MissingPartDeposit event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_received = False
        deposit_part_event = licence.getLastMissingPartDeposit()
        if deposit_part_event:
            complements_received = api.content.get_state(deposit_part_event) == "closed"
        else:
            return False

        if self.task.created() > deposit_part_event.created():
            return False

        return complements_received


class ComplementsAsked(Condition):
    """
    Licence MissingPart event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_asked = False
        missing_part_event = licence.getLastMissingPart()
        if missing_part_event:
            complements_asked = api.content.get_state(missing_part_event) == "closed"
            recent = self.task.creation_date < missing_part_event.creation_date
            complements_asked = complements_asked and recent

        return complements_asked


class AcknowledgmentDoneOrComplementsAskedCondition(Condition):
    """
    Licence acknowlegdment event is closed or we have asked recent complements.
    """

    def evaluate(self):
        licence = self.task_container

        acknowledgment_done = False
        acknowledgment_event = licence.getLastAcknowledgment()
        if acknowledgment_event:
            acknowledgment_done = (
                api.content.get_state(acknowledgment_event) == "closed"
            )
            recent = self.task.creation_date < acknowledgment_event.creation_date
            acknowledgment_done = acknowledgment_done and recent

        complements_asked = False
        missing_part_event = licence.getLastMissingPart()
        if missing_part_event:
            complements_asked = api.content.get_state(missing_part_event) == "closed"
            recent = self.task.creation_date < missing_part_event.creation_date
            complements_asked = complements_asked and recent

        return acknowledgment_done or complements_asked


class ComplementsReceived(Condition):
    """
    Licence MissingPartDeposit event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_received = False
        deposit_part_event = licence.getLastMissingPartDeposit()
        if deposit_part_event:
            complements_received = api.content.get_state(deposit_part_event) == "closed"
            recent = self.task.creation_date < deposit_part_event.creation_date
            complements_received = complements_received and recent

        return complements_received


class ComplementsTransmitToSPW(Condition):
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


class IncompleteForSixMonths(Condition):
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


class ProcedureChoiceDone(Condition):
    """
    Licence has some value selected in the field 'folderCategory'.
    """

    def evaluate(self):
        licence = self.task_container
        if (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
        ):
            ukn = "ukn" not in licence.getProcedureChoiceModifiedBlueprints()
        else:
            ukn = "ukn" not in licence.getProcedureChoice()
        return ukn


class UrbanAnalysisDone(Condition):
    """
    Licence 'fiche technique urbanisme' event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        catalog = api.portal.get_tool("portal_catalog")

        analysis_done = False
        analysis_event = catalog(
            Title="Fiche technique urbanisme",
            path={"query": "/".join(licence.getPhysicalPath())},
        )
        if analysis_event:
            analysis_event = analysis_event[0].getObject()
            analysis_done = api.content.get_state(analysis_event) == "closed"

        return analysis_done


class TransmitSPWDoneCondition(Condition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container

        transmit_done = False
        transmit_event = licence.getLastTransmitToSPW()
        if transmit_event:
            transmit_done = api.content.get_state(transmit_event) == "closed"

        return transmit_done


class AcknowledgmentCreatedCondition(Condition):
    """
    Licence acknowlegdment event is created but not closed.
    """

    def evaluate(self):
        licence = self.task_container

        acknowledgment_created = False
        acknowledgment_event = licence.getLastAcknowledgment()
        if acknowledgment_event:
            acknowledgment_created = (
                api.content.get_state(acknowledgment_event) != "closed"
            )

        return acknowledgment_created


class AcknowledgmentDoneCondition(Condition):
    """
    Licence acknowlegdment event is closed.
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


class NoInquiryCondition(Condition):
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


class InquiryDatesDefinedCondition(Condition):
    """
    Licence inquiry start and end dates are defined.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry = licence.getLastInquiry()
        if not inquiry:
            return False

        start_date = inquiry.getInvestigationStart()
        end_date = inquiry.getInvestigationEnd()
        dates_defined = start_date and end_date
        return dates_defined


class InquiryEventCreatedCondition(Condition):
    """
    Licence inquiry event is created.
    """

    def evaluate(self):
        licence = self.task_container

        created = False
        inquiry_event = licence.getLastInquiry()
        if inquiry_event:
            created = api.content.get_state(inquiry_event) != "closed"

        return created


class InquiryDoneCondition(Condition):
    """
    Licence inquiry event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        inquiry_done = False
        inquiry_event = licence.getLastInquiry()
        if inquiry_event:
            inquiry_done = api.content.get_state(inquiry_event) == "closed"

        return inquiry_done


class AnnouncementDatesDefinedCondition(Condition):
    """
    Licence announcement start and end dates are defined.
    """

    def evaluate(self):
        licence = self.task_container
        announcement = licence.getLastAnnouncement()
        if not announcement:
            return False

        start_date = announcement.getInvestigationStart()
        end_date = announcement.getInvestigationEnd()
        dates_defined = start_date and end_date
        return dates_defined


class AnnouncementEventCreatedCondition(Condition):
    """
    Licence announcement event is created.
    """

    def evaluate(self):
        licence = self.task_container

        created = False
        announcement_event = licence.getLastAnnouncement()
        if announcement_event:
            created = api.content.get_state(announcement_event) != "closed"

        return created


class AnnouncementDoneCondition(Condition):
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


class HasOpinionRequests(Condition):
    """
    There are some values selected in the field sollicitOpinionsTo.
    """

    def evaluate(self):
        licence = self.task_container
        return licence.getSolicitOpinionsTo()


class OpinionRequestsEventsCreated(Condition):
    """
    Each opinion request event is created.
    """

    def evaluate(self):
        licence = self.task_container
        for opinion in licence.getSolicitOpinionsTo():
            if not licence.getOpinionRequests(organisation=opinion):
                return False
        return True


class OpinionRequestsDone(Condition):
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


class RubricsChoiceDone(Condition):
    """
    Rubrics field has values selected.
    """

    def evaluate(self):
        licence = self.task_container
        return bool(licence.getRubrics())


class CollegeOpinionTransmitToSPWDoneCondition(Condition):
    """
    Licence 'college opinion transmit to SPW' event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        college_opinion_transmit_done = False
        college_opinion_transmit_event = licence.getLastCollegeOpinionTransmitToSPW()
        if college_opinion_transmit_event:
            college_opinion_transmit_done = (
                api.content.get_state(college_opinion_transmit_event) == "closed"
            )

        return college_opinion_transmit_done


class SPWProjectReceivedCondition(Condition):
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


class LicenceSuspension(Condition):
    """
    Licence is suspended.
    """

    def evaluate(self):
        is_suspended = api.content.get_state(self.task_container) == "suspension"
        return is_suspended


class LicenceInCompletionState(Condition):
    """
    Licence is in a state showing that completion check has been done
    """

    def evaluate(self):
        checked_completion = api.content.get_state(self.task_container) in [
            "complete",
            "incomplete",
        ]
        return checked_completion


class FDDecisionEventCreatedCondition(Condition):
    """
    Licence fd decision event is created but not closed.
    """

    def evaluate(self):
        licence = self.task_container

        fd_decision_created = False
        fd_decision_event = licence.getLastWalloonRegionDecisionEvent()
        if fd_decision_event:
            fd_decision_created = api.content.get_state(fd_decision_event) != "closed"

        return fd_decision_created


class FDDecisionEventDoneCondition(Condition):
    """
    Licence fd decision event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        fd_decision_done = False
        fd_decision_event = licence.getLastWalloonRegionDecisionEvent()
        if fd_decision_event:
            fd_decision_done = api.content.get_state(fd_decision_event) == "closed"

        return fd_decision_done


class WalloonRegionPrimoEventDone(Condition):
    """
    Primo event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        primo_done = False
        primo_event = licence.getLastWalloonRegionPrimo()
        if primo_event:
            primo_done = api.content.get_state(primo_event) == "closed"

        return primo_done


class LicenceDecisionCollegeEventCreated(Condition):
    """
    TheLicence event is created.
    """

    def evaluate(self):
        licence = self.task_container
        event_created = licence.getLastTheLicence()

        return event_created


class DepositDateIsPast20Days(Condition):
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


class ProcedureChoiceNotified(Condition):
    """
    The procedure choice has been notified to the applicant (or received from FD)
    """

    def evaluate(self):
        licence = self.task_container
        notification = licence.getLastProcedureChoiceNotification()
        return notification


class DepositDateIsPast30Days(Condition):
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


class LicenceRefused(Condition):
    """
    Licence is refused.
    """

    def evaluate(self):
        licence = self.task_container

        refused_event = licence.getLastRefusedNotification()
        if refused_event:
            return api.content.get_state(refused_event) == "closed"
        return False


class DecisionNotified(Condition):
    """
    Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastLicenceNotification()
        if decision_event:
            return api.content.get_state(decision_event) == "closed"
        return False


class DecisionDelivered(Condition):
    """
    Environment Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastLicenceDelivery()
        if decision_event:
            return api.content.get_state(decision_event) == "closed"
        return False


class LicenceEndedCondition(Condition):
    """
    Licence is in a final state
    """

    def evaluate(self):
        licence = self.task_container
        is_ended = api.content.get_state(licence) in LICENCE_FINAL_STATES
        return is_ended


class LicenceThawedCondition(Condition):
    """
    Licence is not in frozen state
    """

    def evaluate(self):
        licence = self.task_container
        thawed = api.content.get_state(licence) != "frozen_suspension"
        return thawed


class AlwaysFalseCondition(Condition):
    """
    always return False
    """

    def evaluate(self):
        return False


class InspectionCondition(Condition, BaseInspection):
    """
    Base class for inspection condition checking values on the last report event
    Provides a method returning the last relevant inspection report event.
    """


class AllInspectionFollowupsAreDone(InspectionCondition):
    """
    All followup events are in the state 'closed'.
    """

    def evaluate(self):
        follow_ups = self.get_followups()
        follow_up_events = self.get_followup_events()
        if len(follow_up_events) < len(follow_ups):
            return False

        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) != "closed":
                return False
        return True


class AllInspectionFollowupsAreWritten(InspectionCondition):
    """
    All followup events are at least in the state 'to_validate'.
    """

    def evaluate(self):
        follow_ups = self.get_followups()
        follow_up_events = self.get_followup_events()
        if len(follow_up_events) < len(follow_ups):
            return False

        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "draft":
                return False
        return True


class SomeInspectionFollowupsAreWritten(InspectionCondition):
    """
    At least one followup event is in the state 'to_validate'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "to_validate":
                return True
        return False


class NoInspectionFollowupsToValidate(InspectionCondition):
    """
    No followup event is in the state 'to_validate'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "to_validate":
                return False
        return True


class NoInspectionFollowupsToSend(InspectionCondition):
    """
    No followup event is in the state 'to_send'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == "to_send":
                return False
        return True


class FollowUpTicketCreated(InspectionCondition):
    """
    A ticket has been created as an inspection followup result.
    """

    def evaluate(self):
        followup_ticket = self.get_last_followup_ticket()
        if not followup_ticket:
            return False
        created = api.content.get_state(followup_ticket) != "ended"
        return created


class FollowUpTicketClosed(InspectionCondition):
    """
    The ticket created as a followup action has been closed.
    """

    def evaluate(self):
        followup_ticket = self.get_last_followup_ticket()
        if not followup_ticket:
            return False
        ended = api.content.get_state(followup_ticket) == "ended"
        return ended


class FollowUpWithDelayOverdue(Condition):
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


class TicketEventClosed(Condition):
    """
    The ticket event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        ticket_event = licence.getLastTheTicket()
        if not ticket_event:
            return False
        closed = api.content.get_state(ticket_event) == "closed"
        return closed
