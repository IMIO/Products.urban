# -*- coding: utf-8 -*-

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

        return complements_received


class ProcedureChoiceDone(Condition):
    """
    Licence has some value selected in the field 'folderCategory'.
    """

    def evaluate(self):
        licence = self.task_container
        return licence.getFolderCategory()


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


class AcknowledgmentDoneCondition(Condition):
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


class NoInquiryCondition(Condition):
    """
    Licence  has no inquiry selected on procedureChoice field.
    """

    def evaluate(self):
        licence = self.task_container
        no_inquiry = 'inquiry' not in licence.getProcedureChoice()
        return no_inquiry


class InquiryEventCreatedCondition(Condition):
    """
    Licence inquiry event is created.
    """

    def evaluate(self):
        licence = self.task_container
        created = licence.getLastInquiry() and True or False
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
