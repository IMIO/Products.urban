# -*- coding: utf-8 -*-


class BaseInspection:
    """
    Base class for inspection condition checking values on the last report event
    Provides a method returning the last relevant inspection report event.
    """

    def get_current_inspection_report(self):
        licence = self.task_container
        report = licence.getCurrentReportEvent()
        return report

    def get_followups(self):
        report = self.get_current_inspection_report()
        if not report:
            return []
        follow_ups = report.get_regular_followup_propositions()
        return follow_ups

    def get_followup_events(self):
        licence = self.task_container
        followup_events = licence.getCurrentFollowUpEvents()
        return followup_events
