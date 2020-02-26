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
        ignore = ['ticket', 'close']
        follow_ups = [fw_up for fw_up in report.getFollowup_proposition() if fw_up not in ignore]
        return follow_ups

    def get_followup_events(self):
        licence = self.task_container

        last_answer_date = None
        for action in licence.workflow_history.values()[0][::-1]:
            if action['review_state'] == 'administrative_answer':
                last_answer_date = action['time']
                break
        if not last_answer_date:
            return

        selected_follow_ups = self.get_followups()
        if not selected_follow_ups:
            return

        followup_events = licence.getAllFollowUpEvents()
        to_return = []
        for followup in followup_events:
            workflow_history = followup.workflow_history.values()[0]
            creation_date = workflow_history[0]['time']
            if creation_date > last_answer_date:
                uet = followup.getUrbaneventtypes()
                if uet and uet.id in selected_follow_ups:
                    to_return.append(followup)
        return to_return
