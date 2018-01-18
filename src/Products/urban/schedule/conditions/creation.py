# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api

from imio.schedule.content.condition import CreationCondition


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
        return len(brains) > 0
