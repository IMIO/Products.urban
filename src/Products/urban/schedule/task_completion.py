# encoding: utf-8

from imio.schedule.browser.task_completion import TaskEndSimpleStatusView
from imio.schedule.browser.task_completion import TaskEndStatusView

from plone import api

from Products.urban.UrbanVocabularyTerm import UrbanVocabulary


class MockTask(object):
    """
    Use this to mock subtasks in a custom status display.
    """

    def __init__(self, title, due_date, end_date, state):
        self.title = title
        self.due_date = due_date
        self.end_date = end_date
        self.state = state
        self.assigned_user = ""

    def Title(self):
        return self.title


class OpinionRequestSentStatus(TaskEndSimpleStatusView):
    """
    View of the popup showing the end completion details of a started task.
    Display the status of each end condition of the task.
    Display if the ending state is matched or not.
    """

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        licence = self.task.get_container()

        inquiry_objs = licence.getAllInquiriesAndAnnouncements()
        inquiry_obj = inquiry_objs[-1]
        opinion_events = inquiry_obj.getAllLinkedOpinionRequests()
        if not opinion_events:
            not_matched.append("Créer les événements de demande d'avis")

        for ask_opinion_event in opinion_events:
            if api.content.get_state(ask_opinion_event) == "creation":
                msg = 'Passer l\'événement <strong>"{}"</strong> dans l\'état <strong>"{}"</strong>'.format(
                    ask_opinion_event.Title(), "en attente d'avis"
                )
                not_matched.append(msg)
            elif api.content.get_state(ask_opinion_event) in [
                "waiting_opinion",
                "opinion_validation",
            ]:
                msg = 'En attente d\'avis <strong>"{}"</strong>. Date limite: <strong>{}</strong>'.format(
                    ask_opinion_event.Title(), self.task.due_date.strftime("%d/%m/%Y")
                )
                not_matched.append(msg)
            else:
                matched.append(ask_opinion_event.Title())

        return matched, not_matched


class OpinionRequestReceivedStatus(TaskEndStatusView):
    """
    View of the popup showing the end completion details of a started task.
    Display the status of each end condition of the task.
    Display if the ending state is matched or not.
    """

    subtask_title_label = "Avis reçus"
    subtask_todo_title_label = "Avis en attente de réponse"
    end_date_label = "Reçu le"

    def get_state(self, context):
        """
        Return the context workflow state.
        """
        if isinstance(context, MockTask):
            return context.state
        else:
            return api.content.get_state(context)

    def get_subtasks_status(self):
        """
        List all the opinion request status.
        """
        created, started, done = [], [], []
        licence = self.task.get_container()

        for ask_opinion_event in licence.getOpinionRequests():
            event_state = api.content.get_state(ask_opinion_event)
            title = ask_opinion_event.Title()
            due_date = ask_opinion_event.getTransmitDate()
            due_date = due_date and due_date + 15 or None
            end_date = ask_opinion_event.getReceiptDate()
            if event_state == "opinion_given":
                opinion_task = MockTask(title, due_date, end_date, "closed")
                done.append(opinion_task)
            elif event_state == "creation":
                opinion_task = MockTask(title, due_date, end_date, "creation")
                created.append(opinion_task)
            else:
                opinion_task = MockTask(title, due_date, end_date, "to_do")
                started.append(opinion_task)

        return created, started, done

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        return matched, not_matched


class FollowupEventsRedactedStatus(TaskEndSimpleStatusView):
    """ """

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        licence = self.task.get_container()

        report_event = licence.getCurrentReportEvent()
        if not report_event:
            return matched, not_matched

        selected_followups = report_event.get_regular_followup_propositions()
        followup_events = licence.getCurrentFollowUpEvents()
        followup_events_by_id = dict(
            [(event.getUrbaneventtypes().id, event) for event in followup_events]
        )
        voc = UrbanVocabulary(
            "urbaneventtypes", vocType="FollowUpEventConfig", value_to_use="title"
        )
        all_followups_voc = voc.getDisplayList(self)
        to_create = []
        to_propose = []
        for selected_followup in selected_followups:
            if selected_followup in followup_events_by_id:
                follow_up_event = followup_events_by_id[selected_followup]
                if api.content.get_state(follow_up_event) == "draft":
                    to_propose.append(
                        u'Proposer l\'événement <strong>"{}"</strong>'.format(
                            follow_up_event.Title().decode("utf-8")
                        )
                    )
                else:
                    matched.append(
                        u'Evénement <strong>"{}"</strong> proposé'.format(
                            follow_up_event.Title().decode("utf-8")
                        )
                    )
            else:
                to_create.append(
                    u'Créer et proposer l\'événement de réponse administrative <strong>"{}"</strong>'.format(
                        all_followups_voc.getValue(selected_followup)
                    )
                )
        not_matched.extend(to_create)
        not_matched.extend(to_propose)

        return matched, not_matched


class FollowupEventsValidatedStatus(TaskEndSimpleStatusView):
    """ """

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        licence = self.task.get_container()

        followup_events = licence.getCurrentFollowUpEvents()
        for followup_event in followup_events:
            if api.content.get_state(followup_event) == "to_validate":
                not_matched.append(
                    u'Valider l\'événement <strong>"{}"</strong>'.format(
                        followup_event.Title().decode("utf-8")
                    )
                )
            elif api.content.get_state(followup_event) == "to_send":
                matched.append(
                    u'Evénement <strong>"{}"</strong> validé'.format(
                        followup_event.Title().decode("utf-8")
                    )
                )

        return matched, not_matched


class FollowupEventsSentStatus(TaskEndSimpleStatusView):
    """ """

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        licence = self.task.get_container()

        followup_events = licence.getCurrentFollowUpEvents()
        for followup_event in followup_events:
            if api.content.get_state(followup_event) == "to_send":
                not_matched.append(
                    u'Clôturer l\'événement <strong>"{}"</strong>'.format(
                        followup_event.Title().decode("utf-8")
                    )
                )
            elif api.content.get_state(followup_event) == "closed":
                matched.append(
                    u'Evénement <strong>"{}"</strong> clôturé'.format(
                        followup_event.Title().decode("utf-8")
                    )
                )

        return matched, not_matched
