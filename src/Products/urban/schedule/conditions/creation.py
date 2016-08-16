# -*- coding: utf-8 -*-

from imio.schedule.content.condition import CreationCondition

from plone import api


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


class WillHaveInquiry(CreationCondition):
    """
    'inquiry' is selected on the field 'procedureChoice'.
    """

    def evaluate(self):
        licence = self.task_container
        return 'inquiry' in licence.getProcedureChoice()


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
    Licence has an inquiry start date and end date defined.
    """

    def evaluate(self):
        licence = self.task_container

        start_date = licence.getInvestigationStart()
        end_date = licence.getInvestigationEnd()
        has_inquiry = start_date and end_date

        return has_inquiry


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
