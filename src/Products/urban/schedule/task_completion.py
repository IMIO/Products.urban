# encoding: utf-8

from imio.schedule.browser.task_completion import TaskEndSimpleStatusView
from imio.schedule.browser.task_completion import TaskEndStatusView

from plone import api


class MockTask(object):
    """
    Use this to mock subtasks in a custom status display.
    """

    def __init__(self, title, due_date, end_date, state):
        self.title = title
        self.due_date = due_date
        self.end_date = end_date
        self.state = state
        self.assigned_user = ''

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

        opinion_events = licence.getOpinionRequests()
        if not opinion_events:
            not_matched.append('Créer les événements de demande d\'avis')

        for ask_opinion_event in opinion_events:
            if api.content.get_state(ask_opinion_event) == 'creation':
                msg = 'Passer l\'événement <strong>"{}"</strong> dans l\'état <strong>"{}"</strong>'.format(
                    ask_opinion_event.Title(),
                    'en attente d\'avis'
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

    subtask_title_label = 'Avis reçus'
    subtask_todo_title_label = 'Avis en attente de réponse'
    end_date_label = 'Reçu le'

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
            end_date = ask_opinion_event.getReceiptDate()
            if event_state == 'opinion_given':
                opinion_task = MockTask(title, due_date, end_date, 'closed')
                done.append(opinion_task)
            elif event_state == 'creation':
                opinion_task = MockTask(title, due_date, end_date, 'creation')
                created.append(opinion_task)
            else:
                opinion_task = MockTask(title, due_date, end_date, 'to_do')
                started.append(opinion_task)

        return created, started, done

    def get_conditions_status(self):
        """
        List all the opinion request status.
        """
        matched, not_matched = [], []
        return matched, not_matched
