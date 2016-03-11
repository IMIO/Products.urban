# -*- coding: utf-8 -*-

from plone import api

from urban.schedule.content.condition import Condition


class FolderCompleteCondition(Condition):
    """
    Licence folderComplete event is created.
    """

    def evaluate(self):
        licence = self.task_container

        is_complete = False
        folder_complete_event = licence.getLastAcknowledgment()
        if folder_complete_event:
            is_complete = api.content.get_state(folder_complete_event) == 'closed'

        return is_complete


class InquiryCondition(Condition):
    """
    Licence has an inquiry start date and end date defined.
    """

    def evaluate(self):
        licence = self.task_container

        start_date = licence.getInvestigationStart()
        end_date = licence.getInvestigationEnd()
        has_inquiry = start_date and end_date

        return has_inquiry


class InquiryIsDone(Condition):
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
