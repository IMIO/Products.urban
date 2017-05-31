# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api

from imio.schedule.content.condition import Condition


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
            created = api.content.get_state(inquiry_event) != 'closed'

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
            inquiry_done = api.content.get_state(inquiry_event) == 'closed'

        return inquiry_done


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
            if api.content.get_state(opinion) != 'opinion_given':
                return False

        return True


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
            return api.content.get_state(refused_event) == 'closed'
        return False


class DecisionNotified(Condition):
    """
    Licence decision was notified
    """

    def evaluate(self):
        licence = self.task_container

        decision_event = licence.getLastTheLicence()
        if decision_event:
            return api.content.get_state(decision_event) == 'closed'
        return False
