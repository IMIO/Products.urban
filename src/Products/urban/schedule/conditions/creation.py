# -*- coding: utf-8 -*-

from imio.schedule.content.condition import CreationCondition


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
