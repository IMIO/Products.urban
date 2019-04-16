# -*- coding: utf-8 -*-

from DateTime import DateTime
from datetime import datetime
from plone import api

from imio.schedule.content.condition import CreationCondition


class DepositDoneCondition(CreationCondition):
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


class AcknowledgmentDoneCondition(CreationCondition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container

        acknowledgment_done = False
        acknowledgment_event = licence.getLastAcknowledgment()
        if acknowledgment_event:
            acknowledgment_done = api.content.get_state(acknowledgment_event) == 'closed'

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
            complements_asked = api.content.get_state(missing_part_event) == 'closed'

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
            complements_received = api.content.get_state(deposit_part_event) == 'closed'

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
            complements_transmit = api.content.get_state(deposit_part_event) == 'closed'

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
        return 'inquiry' in licence.getProcedureChoice()


class WillHaveAnnouncement(CreationCondition):
    """
    'light_inquiry' or 'initative_light_inquiry' is selected
    on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        light_inquiry = 'light_inquiry' in licence.getProcedureChoice()
        initiative_light_inquiry = 'initiative_light_inquiry' in licence.getProcedureChoice()
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
        no_inquiry = 'inquiry' not in licence.getProcedureChoice()
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
            announcement_done = api.content.get_state(announcement_event) == 'closed'

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
            if api.content.get_state(opinion) != 'opinion_given':
                return False

        return True


class IsInternalOpinionRequest(CreationCondition):
    """
    Urban event is an internal opinion request
    """

    def evaluate(self):
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services']
        opinion_request = self.task_container
        opinion_config = opinion_request.getUrbaneventtypes()

        if not opinion_config.getIs_internal_service():
            return False

        record = registry_field.get(opinion_config.getInternal_service(), None)
        if record and self.task_config.id in [record['task_answer_id'], record['task_validate_id']]:
            return True

        return False


class HasFDOpinionRequest(CreationCondition):
    """
    'FD' is selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        return 'FD' in licence.getProcedureChoice()


class HasNoFDOpinionRequest(CreationCondition):
    """
    'FD' is not selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        return 'FD' not in licence.getProcedureChoice()


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
        incomplete_UID = self.task_config.aq_parent['incomplet'].UID()
        brains = api.content.find(
            context=licence,
            task_config_UID=incomplete_UID,
            review_state='closed',
        )
        first_incomplete_done = len(brains) > 0
        if not first_incomplete_done:
            return False
        wf_history = licence.workflow_history
        two_incomplete_transitions = 2 <= len([tr for tr in wf_history[wf_history.keys()[0]] if tr['action'] == 'isincomplete'])
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
            receipt_done = api.content.get_state(receipt_event) == 'closed'

        return receipt_done


class LicenceAuthorityIsCollege(CreationCondition):
    """
    Environment licence authority is college
    """

    def evaluate(self):
        licence = self.task_container
        authority_is_college = licence.getAuthority() == 'college'
        return authority_is_college


class IsNotTemporaryLicence(CreationCondition):
    """
    Environment licence procedure type is not temporary.
    """

    def evaluate(self):
        licence = self.task_container
        not_temporary = licence.getProcedureChoice() != 'temporary'
        return not_temporary
