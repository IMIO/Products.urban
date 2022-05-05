# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api

from imio.schedule.content.condition import Condition

from Products.urban.config import LICENCE_FINAL_STATES
from Products.urban.schedule.conditions.base import BaseInspection

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
            deposit_done = api.content.get_state(deposit_event) == 'closed'

        return deposit_done


class DepositEventCreated(Condition):
    """
    Licence deposit event is created.
    """

    def evaluate(self):
        licence = self.task_container
        deposit_event = licence.getLastDeposit()
        return deposit_event


class SingleComplementAsked(Condition):
    """
    Licence MissingPart event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_asked = False
        missing_part_event = licence.getLastMissingPart()
        if missing_part_event:
            complements_asked = api.content.get_state(missing_part_event) == 'closed'

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
            complements_received = api.content.get_state(deposit_part_event) == 'closed'
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
            complements_asked = api.content.get_state(missing_part_event) == 'closed'
            recent = self.task.creation_date < missing_part_event.creation_date
            complements_asked = complements_asked and recent

        return complements_asked


class ComplementsReceived(Condition):
    """
    Licence MissingPartDeposit event is created and closed.
    """

    def evaluate(self):
        licence = self.task_container

        complements_received = False
        deposit_part_event = licence.getLastMissingPartDeposit()
        if deposit_part_event:
            complements_received = api.content.get_state(deposit_part_event) == 'closed'
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
            complements_transmit = api.content.get_state(deposit_part_event) == 'closed'

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
        return 'ukn' not in licence.getProcedureChoice()


class UrbanAnalysisDone(Condition):
    """
    Licence 'fiche technique urbanisme' event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        catalog = api.portal.get_tool('portal_catalog')

        analysis_done = False
        analysis_event = catalog(
            Title='Fiche technique urbanisme',
            path={'query': '/'.join(licence.getPhysicalPath())}
        )
        if analysis_event:
            analysis_event = analysis_event[0].getObject()
            analysis_done = api.content.get_state(analysis_event) == 'closed'

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
            transmit_done = api.content.get_state(transmit_event) == 'closed'

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
            acknowledgment_created = api.content.get_state(acknowledgment_event) != 'closed'

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
            acknowledgment_done = api.content.get_state(acknowledgment_event) == 'closed'

        return acknowledgment_done


class NoInquiryCondition(Condition):
    """
    Licence has no inquiry selected on procedureChoice field.
    """

    def evaluate(self):
        licence = self.task_container
        no_inquiry = 'inquiry' not in licence.getProcedureChoice()
        return no_inquiry


class InquiryDatesDefinedCondition(Condition):
    """
    Licence inquiry start and end dates are defined.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_objs = licence.getAllInquiries()
        if inquiry_objs:
            inquiry_obj = inquiry_objs[-1]
            inquiry_event = inquiry_obj.getLinkedUrbanEventInquiry()
            if not inquiry_event or api.content.get_state(inquiry_event) == 'closed':
                return False

            start_date = inquiry_event.getInvestigationStart()
            end_date = inquiry_event.getInvestigationEnd()
            dates_defined = start_date and end_date
            return dates_defined
        return False


class InquiryEventCreatedCondition(Condition):
    """
    Licence inquiry event is created.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_objs = licence.getAllInquiries()
        if inquiry_objs:
            inquiry_obj = inquiry_objs[-1]
            inquiry_event = inquiry_obj.getLinkedUrbanEventInquiry()
            return bool(inquiry_event)
        return False


class InquiryDoneCondition(Condition):
    """
    Licence inquiry event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_objs = licence.getAllInquiries()
        if inquiry_objs:
            inquiry_obj = inquiry_objs[-1]
            inquiry_event = inquiry_obj.getLinkedUrbanEventInquiry()
            if inquiry_event and api.content.get_state(inquiry_event) == 'closed':
                return True
        return False


class AnnouncementDatesDefinedCondition(Condition):
    """
    Licence announcement start and end dates are defined.
    """

    def evaluate(self):
        licence = self.task_container
        announcement_objs = licence.getAllAnnouncements()
        if announcement_objs:
            announcement_obj = announcement_objs[-1]
            announcement_event = announcement_obj.getLinkedUrbanEventInquiry()
            if not announcement_event or api.content.get_state(announcement_event) == 'closed':
                return False

            start_date = announcement_event.getInvestigationStart()
            end_date = announcement_event.getInvestigationEnd()
            dates_defined = start_date and end_date
            return dates_defined
        return False


class AnnouncementEventCreatedCondition(Condition):
    """
    Licence announcement event is created.
    """

    def evaluate(self):
        licence = self.task_container
        announcement_objs = licence.getAllAnnouncements()
        if announcement_objs:
            announcement_obj = announcement_objs[-1]
            announcement_event = announcement_obj.getLinkedUrbanEventInquiry()
            return bool(announcement_event)
        return False


class AnnouncementDoneCondition(Condition):
    """
    Licence announcement event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        announcement_objs = licence.getAllAnnouncements()
        if announcement_objs:
            announcement_obj = announcement_objs[-1]
            announcement_event = announcement_obj.getLinkedUrbanEventInquiry()
            if announcement_event and api.content.get_state(announcement_event) == 'closed':
                return True
        return False


class HasOpinionRequests(Condition):
    """
    There are some values selected in the field sollicitOpinionsTo.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_obj = licence.getAllInquiriesAndAnnouncements()[-1]
        or_events = inquiry_obj.getAllLinkedOpinionRequests()

        asked_opinions = inquiry_obj.getSolicitOpinionsTo()
        asked_optional_opinions = inquiry_obj.getSolicitOpinionsToOptional()
        if len(or_events) != len(asked_opinions) + len(asked_optional_opinions):
            return True
        return False


class OpinionRequestsEventsCreated(Condition):
    """
    Each opinion request event is created.
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_obj = licence.getAllInquiriesAndAnnouncements()[-1]
        or_events = inquiry_obj.getAllLinkedOpinionRequests()

        asked_opinions = inquiry_obj.getSolicitOpinionsTo()
        asked_optional_opinions = inquiry_obj.getSolicitOpinionsToOptional()
        if len(or_events) == len(asked_opinions) + len(asked_optional_opinions):
            return True
        return False


class OpinionRequestsDone(Condition):
    """
    Each opinion request event has received an opinion.
    <=> is on the state 'opinion_given'
    """

    def evaluate(self):
        licence = self.task_container
        inquiry_obj = licence.getAllInquiriesAndAnnouncements()[-1]
        or_events = inquiry_obj.getAllLinkedOpinionRequests()

        for opinion in or_events:
            if api.content.get_state(opinion) != 'opinion_given':
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
            college_opinion_transmit_done = api.content.get_state(college_opinion_transmit_event) == 'closed'

        return college_opinion_transmit_done


class CollegeOpinionDoneCondition(Condition):
    """
    Licence 'college opinion (pre-decision)' event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        college_opinion_done = False
        college_opinion_event = licence.getLastCollegeOpinion()
        if college_opinion_event:
            college_opinion_done = api.content.get_state(college_opinion_event) == 'closed'

        return college_opinion_done


class CollegeOpinionInProgressCondition(Condition):
    """
    Licence 'college opinion (pre-decision)' event is in progress, the opinion is written.
    """

    def evaluate(self):
        licence = self.task_container

        college_opinion_done = False
        college_opinion_event = licence.getLastCollegeOpinion()
        if college_opinion_event:
            college_opinion_done = api.content.get_state(college_opinion_event) == 'decision_in_progress'

        return college_opinion_done


class SPWProjectReceivedCondition(Condition):
    """
    Licence SPW projetc receipt event is closed.
    """

    def evaluate(self):
        licence = self.task_container

        receipt_done = False
        receipt_event = licence.getLastDecisionProjectFromSPW()
        if receipt_event:
            receipt_done = api.content.get_state(receipt_event) == 'closed'

        return receipt_done


class LicenceSuspension(Condition):
    """
    Licence is suspended.
    """

    def evaluate(self):
        is_suspended = api.content.get_state(self.task_container) == 'suspension'
        return is_suspended


class LicenceInCompletionState(Condition):
    """
    Licence is in a state showing that completion check has been done
    """

    def evaluate(self):
        checked_completion = api.content.get_state(self.task_container) in ['complete', 'incomplete']
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
            fd_decision_created = api.content.get_state(fd_decision_event) != 'closed'

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
            fd_decision_done = api.content.get_state(fd_decision_event) == 'closed'

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
            primo_done = api.content.get_state(primo_event) == 'closed'

        return primo_done


class FDCondition(Condition):
    """
    Base class for FD opinion request condition
    """

    def __init__(self, licence, task):
        super(FDCondition, self).__init__(licence, task)
        self.FD_event = licence.getLastWalloonRegionOpinionRequest()


class FDOpinionAsked(FDCondition):
    """
    Opinion request is sent to FD
    """

    def evaluate(self):
        if not self.FD_event:
            return False
        # 'closed' => case where the FD event is a college event
        return api.content.get_state(self.FD_event) in ['waiting_opinion', 'closed']


class FDOpinionReceived(FDCondition):
    """
    """

    def evaluate(self):
        if not self.FD_event:
            return False
        # 'closed' => case where the FD event is a college event
        return api.content.get_state(self.FD_event) in ['opinion_given', 'closed']


class LicenceDecisionCollegeEventCreated(Condition):
    """
    TheLicence event is created.
    """

    def evaluate(self):
        licence = self.task_container
        event_created = licence.getLastTheLicence()

        return event_created


class DecisionEventClosed(Condition):
    """
    TheLicence event is closed.
    """

    def evaluate(self):
        licence = self.task_container
        decision_event = licence.getLastTheLicence()
        if decision_event:
            return api.content.get_state(decision_event) == 'closed'
        return False


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
            return api.content.get_state(refused_event) == 'closed'
        return False


class DecisionNotified(Condition):
    """
    Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastLicenceNotification()
        if decision_event:
            return api.content.get_state(decision_event) == 'closed'
        return False


class DecisionWritten(Condition):
    """
    Environment Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastLicenceDelivery()
        if decision_event:
            return api.content.get_state(decision_event) == 'decision_in_progress'
        return False


class DecisionDelivered(Condition):
    """
    Environment Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastLicenceDelivery()
        if decision_event:
            return api.content.get_state(decision_event) == 'closed'
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
        thawed = api.content.get_state(licence) != 'frozen_suspension'
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
            if api.content.get_state(follow_up_event) != 'closed':
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
            if api.content.get_state(follow_up_event) == 'draft':
                return False
        return True


class SomeInspectionFollowupsAreWritten(InspectionCondition):
    """
    At least one followup event is in the state 'to_validate'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == 'to_validate':
                return True
        return False


class NoInspectionFollowupsToValidate(InspectionCondition):
    """
    No followup event is in the state 'to_validate'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == 'to_validate':
                return False
        return True


class NoInspectionFollowupsToSend(InspectionCondition):
    """
    No followup event is in the state 'to_send'.
    """

    def evaluate(self):
        follow_up_events = self.get_followup_events()
        for follow_up_event in follow_up_events:
            if api.content.get_state(follow_up_event) == 'to_send':
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
        created = api.content.get_state(followup_ticket) != 'ended'
        return created


class FollowUpTicketClosed(InspectionCondition):
    """
    The ticket created as a followup action has been closed.
    """
    def evaluate(self):
        followup_ticket = self.get_last_followup_ticket()
        if not followup_ticket:
            return False
        ended = api.content.get_state(followup_ticket) == 'ended'
        return ended


class TicketEventClosed(Condition):
    """
    The ticket event is closed.
    """
    def evaluate(self):
        licence = self.task_container
        ticket_event = licence.getLastTheTicket()
        if not ticket_event:
            return False
        closed = api.content.get_state(ticket_event) == 'closed'
        return closed
