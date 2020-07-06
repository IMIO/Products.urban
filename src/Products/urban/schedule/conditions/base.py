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

    def get_last_followup_ticket(self):
        licence = self.task_container
        tickets = licence.getBoundTickets()
        if not tickets:
            return None

        report_events = licence.getAllReportEvents()[::-1]
        # check the most recent report with 'ticket' in the followup
        # proposition
        for report in report_events:
            if "ticket" in report.getFollowup_proposition():
                report_workflow_history = report.workflow_history.values()[0]
                report_creation_date = report_workflow_history[0]["time"]
                # if a referring ticket has been created after this report
                # return True
                for ticket in tickets:
                    ticket_workflow_history = ticket.workflow_history.values()[0]
                    ticket_creation_date = ticket_workflow_history[0]["time"]
                    if ticket_creation_date > report_creation_date:
                        return ticket
                    return None
