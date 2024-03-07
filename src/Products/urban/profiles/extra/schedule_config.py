# -*- coding: utf-8 -*-

from imio.schedule.content.object_factories import EndConditionObject
from imio.schedule.content.object_factories import StartConditionObject
from imio.schedule.content.object_factories import CreationConditionObject
from imio.schedule.content.object_factories import MacroCreationConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject
from imio.schedule.content.object_factories import MacroStartConditionObject
from imio.schedule.content.object_factories import RecurrenceConditionObject


schedule_config = {
    "codt_buildlicence": [
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("deposit",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_first_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "ending_states": ("deposit",),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",  # infinite deadline
                    "additional_delay": 180,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet2",
            "title": "Incomplet pour la seconde fois",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("inacceptable",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_second_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "notify_refused",
                    "title": "Notifier le refus",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("inacceptable",),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.refused"),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 15,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "reception",
            "title": "Réception du dossier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "starting_states": ("deposit",),
            "ending_states": ("complete", "incomplete"),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "activate_recurrency": True,
            "recurrence_states": ("deposit",),
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "deposit",
                    "title": "Renseigner la date de dépôt",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 5,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "check_completion",
                    "title": "Vérifier la complétude",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "ending_states": ("complete", "incomplete"),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "OR",
                            display_status=False,
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "send_acknoledgment",
                    "title": "Envoyer l'accusé de réception",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.acknowledgment_done", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            display_status=False,
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_past_20days",
                    "title": "Choix de la procédure après 20 jours",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "AND",
                            display_status=False,
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 30,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_fd",
                    "title": "Choix de la procédure par le FD",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "AND"
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_received_from_FD",
                            "AND",
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": None,
                },
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "announcement-preparation",
            "title": "Préparer l'annonce de projet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.will_have_announcement", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.announcement_dates_defined", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.will_have_announcement", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 20,
        },
        {
            "type_name": "TaskConfig",
            "id": "announcement",
            "title": "Annonce de projet en cours",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.announcement_dates_defined", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.announcement_done", "AND"),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.announcement_dates_defined", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.announcement_end_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry-preparation",
            "title": "Préparer l'enquête publique",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.will_have_inquiry", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.will_have_inquiry", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 20,
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry",
            "title": "Enquête publique en cours",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.inquiry_done", "AND"),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "creer-demande-avis",
            "title": "Préparer demandes d'avis",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.has_opinion_requests", "AND"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_created", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.has_opinion_requests", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "demande-avis-en-cours",
            "title": "Avis en cours",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_done", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 30,
            "activate_recurrency": True,
            "marker_interfaces": [
                u"Products.urban.schedule.interfaces.ISendOpinionRequestsTask"
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "ask_FD_opinion",
            "title": "Demander l'avis du FD",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.need_FD_opinion", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.FD_opinion_asked", "AND"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": -55,
        },
        {
            "type_name": "TaskConfig",
            "id": "FD_opinion_overdue",
            "title": "Avis du FD hors délai",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.FD_opinion_overdue", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.FD_opinion_received", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.task_starting_date",
            "additional_delay": 0,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "ending_states": ("accepted", "refused"),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.acknowledgment_done"
                ),
            ),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_notified"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.decision_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.acknowledgment_date",
                    "calculation_delay": ("urban.schedule.delay.annonced_delay",),
                    "additional_delay": -1,
                },
            ],
        },
    ],
    "codt_article127": [
        {
            "type_name": "TaskConfig",
            "id": "fin-de-delai",
            "title": "Fin de délai",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "creation_conditions": (
                CreationConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.licence_decision_college_event_created"
                ),
            ),
            "start_date": "urban.schedule.start_date.deposit_date",
            "additional_delay": 60,
        },
        {
            "type_name": "TaskConfig",
            "id": "passage-college-pour-envoi-fd",
            "title": "Passage collège pour envoi FD",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "creation_conditions": (
                CreationConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.college_opinion_transmit_done"
                ),
            ),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": -60,
        },
        {
            "type_name": "TaskConfig",
            "id": "octroi-du-permis-par-le-fd",
            "title": "Octroi du permis par le FD",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "ending_states": ("inacceptable", "accepted", "retired", "refused"),
            "creation_conditions": (
                CreationConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "start_date": "urban.schedule.start_date.deposit_date",
            "additional_delay": 130,
        },
    ],
    "codt_parceloutlicence": [
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("deposit",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_first_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",  # infinite deadline
                    "additional_delay": 180,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet2",
            "title": "Incomplet pour la seconde fois",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("inacceptable",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_second_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "notify_refused",
                    "title": "Notifier le refus",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("inacceptable",),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.refused"),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 15,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "reception",
            "title": "Réception du dossier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "starting_states": ("deposit",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "activate_recurrency": True,
            "recurrence_states": ("deposit",),
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "deposit",
                    "title": "Renseigner la date de dépôt",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 5,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "check_completion",
                    "title": "Vérifier la complétude",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "ending_states": ("complete", "incomplete"),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "OR",
                            display_status=False,
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "send_acknoledgment",
                    "title": "Envoyer l'accusé de réception",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.acknowledgment_done", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            display_status=False,
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_past_20days",
                    "title": "Choix de la procédure après 20 jours",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "AND",
                            display_status=False,
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 30,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_fd",
                    "title": "Choix de la procédure par le FD",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "AND"
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_received_from_FD",
                            "AND",
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": None,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "ending_states": ("accepted", "refused"),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.acknowledgment_done"
                ),
            ),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_notified"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.decision_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.acknowledgment_date",
                    "calculation_delay": ("urban.schedule.delay.annonced_delay",),
                    "additional_delay": -7,
                },
            ],
        },
    ],
    "codt_commerciallicence": [
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("deposit",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_first_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",  # infinite deadline
                    "additional_delay": 180,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet2",
            "title": "Incomplet pour la seconde fois",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("inacceptable",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_second_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "notify_refused",
                    "title": "Notifier le refus",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("inacceptable",),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.refused"),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 15,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "reception",
            "title": "Réception du dossier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "starting_states": ("deposit",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "activate_recurrency": True,
            "recurrence_states": ("deposit",),
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "deposit",
                    "title": "Renseigner la date de dépôt",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 5,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "check_completion",
                    "title": "Vérifier la complétude",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "ending_states": ("complete", "incomplete"),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "OR",
                            display_status=False,
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "send_acknoledgment",
                    "title": "Envoyer l'accusé de réception",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.acknowledgment_done", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            display_status=False,
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_past_20days",
                    "title": "Choix de la procédure après 20 jours",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "AND",
                            display_status=False,
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 30,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_fd",
                    "title": "Choix de la procédure par le FD",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "AND"
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_received_from_FD",
                            "AND",
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": None,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "ending_states": ("accepted", "refused"),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.acknowledgment_done"
                ),
            ),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_notified"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.decision_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.acknowledgment_date",
                    "calculation_delay": ("urban.schedule.delay.annonced_delay",),
                    "additional_delay": -7,
                },
            ],
        },
    ],
    "codt_integratedlicence": [
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("deposit",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_first_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",  # infinite deadline
                    "additional_delay": 180,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet2",
            "title": "Incomplet pour la seconde fois",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("inacceptable",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_second_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "notify_refused",
                    "title": "Notifier le refus",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("inacceptable",),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.refused"),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 15,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "reception",
            "title": "Réception du dossier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "starting_states": ("deposit",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "activate_recurrency": True,
            "recurrence_states": ("deposit",),
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "deposit",
                    "title": "Renseigner la date de dépôt",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 5,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "check_completion",
                    "title": "Vérifier la complétude",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "ending_states": ("complete", "incomplete"),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "OR",
                            display_status=False,
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "send_acknoledgment",
                    "title": "Envoyer l'accusé de réception",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.acknowledgment_done", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            display_status=False,
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_past_20days",
                    "title": "Choix de la procédure après 20 jours",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "AND",
                            display_status=False,
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 30,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_fd",
                    "title": "Choix de la procédure par le FD",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "AND"
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_received_from_FD",
                            "AND",
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": None,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "ending_states": ("accepted", "refused"),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.acknowledgment_done"
                ),
            ),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_notified"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.decision_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.acknowledgment_date",
                    "calculation_delay": ("urban.schedule.delay.annonced_delay",),
                    "additional_delay": -7,
                },
            ],
        },
    ],
    "codt_urbancertificatetwo": [
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("deposit",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_first_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",  # infinite deadline
                    "additional_delay": 180,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet2",
            "title": "Incomplet pour la seconde fois",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("inacceptable",),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.incomplete_second_time"
                ),
            ),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "notify_refused",
                    "title": "Notifier le refus",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("inacceptable",),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.refused"),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "additional_delay": 15,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "reception",
            "title": "Réception du dossier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "starting_states": ("deposit",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "activate_recurrency": True,
            "recurrence_states": ("deposit",),
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "deposit",
                    "title": "Renseigner la date de dépôt",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 5,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "check_completion",
                    "title": "Vérifier la complétude",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("deposit",),
                    "starting_states": ("deposit",),
                    "ending_states": ("complete", "incomplete"),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "OR",
                            display_status=False,
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "recurrence_states": ("deposit",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "send_acknoledgment",
                    "title": "Envoyer l'accusé de réception",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.acknowledgment_done", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            display_status=False,
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_past_20days",
                    "title": "Choix de la procédure après 20 jours",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_20days",
                            "AND",
                            display_status=False,
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done", "AND"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": 30,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "procedure_choice_fd",
                    "title": "Choix de la procédure par le FD",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.deposit_past_30days", "AND"
                        ),
                        CreationConditionObject(
                            "urban.schedule.condition.default_acknowledgement"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject("urban.schedule.condition.deposit_done"),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_received_from_FD",
                            "AND",
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.procedure_choice_done"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.deposit_date",
                    "calculation_delay": ("schedule.calculation_default_delay",),
                    "additional_delay": None,
                },
            ],
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "ending_states": ("accepted", "refused"),
            "creation_conditions": (
                MacroCreationConditionObject(
                    "urban.schedule.condition.acknowledgment_done"
                ),
            ),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_notified"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "calculation_delay": ("urban.schedule.delay.annonced_delay",),
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("complete",),
                    "starting_states": ("complete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.decision_notified"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.acknowledgment_date",
                    "calculation_delay": ("urban.schedule.delay.annonced_delay",),
                    "additional_delay": -7,
                },
            ],
        },
    ],
    "division": [
        {
            "type_name": "TaskConfig",
            "id": "deposit",
            "title": "Réception",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("in_progress",),
            "starting_states": ("in_progress",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.deposit_event_created", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "deliverance",
            "title": "Octroi",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("in_progress",),
            "starting_states": ("in_progress",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.deposit_event_created", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.decision_event_closed", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 30,
        },
    ],
    "codt_notaryletter": [
        {
            "type_name": "TaskConfig",
            "id": "deposit",
            "title": "Réception",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("in_progress",),
            "starting_states": ("in_progress",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.deposit_event_created", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "notary-request",
            "title": "Requête notariale",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("in_progress",),
            "starting_states": ("in_progress",),
            "start_date": "urban.schedule.start_date.deposit_date",
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.deposit_event_created", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.decision_event_closed", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 30,
        },
    ],
    "envclasstwo": [
        {
            "type_name": "TaskConfig",
            "id": "deposit",
            "title": "Dépot du dossier",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "transmit_to_spw",
            "title": "Transmis au SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "schedule.start_date.task_starting_date",
            "creation_conditions": (
                CreationConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.transmit_to_spw_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "spw_check_completion",
            "title": "Vérification complétude par le SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "urban.schedule.start_date.spw_receipt_date",
            "start_conditions": (
                StartConditionObject("urban.schedule.condition.transmit_to_spw_done"),
            ),
            "ending_states": ("complete", "incomplete", "inacceptable"),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 20,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("complete", "inacceptable", "abandoned"),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",
                    "additional_delay": 1,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.incomplete_for_6_months", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",
                    "additional_delay": 183,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "transmis_complements_au_spw",
                    "title": "Transmis des compléments au SPW",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_transmit_to_spw"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.complements_deposit_date",
                    "additional_delay": 3,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "verif_complements",
                    "title": "Vérification compléments par le SPW",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "ending_states": ("complete", "inacceptable", "abandoned"),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_transmit_to_spw"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.complements_deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "irrecevable-apres-6-mois",
                    "title": "Irrecevable après 6 mois",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "ending_states": ("complete", "inacceptable", "abandoned"),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.incomplete_for_6_months"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "additional_delay": 0,
                },
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "transmit_complete",
            "title": "Transmis complet",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.acknowledgment_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "identification-rubriques",
            "title": "Identification des rubriques",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.rubrics_choice_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 1,
        },
        {
            "type_name": "TaskConfig",
            "id": "creer-demande-avis",
            "title": "Préparer demandes d'avis",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.has_opinion_requests", "AND"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_created", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "demande-avis-en-cours",
            "title": "Avis en cours",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_done", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 30,
            "activate_recurrency": True,
            "marker_interfaces": [
                u"Products.urban.schedule.interfaces.ISendOpinionRequestsTask"
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry-preparation",
            "title": "Préparer l'enquête publique",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.is_not_temporary_licence", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 1,
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry",
            "title": "Enquête publique en cours",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.inquiry_done", "AND"),
            ),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "rapport-analyse",
            "title": "Rapport d'analyse",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.is_not_temporary_licence", "AND"
                ),
            ),
            "start_conditions": (
                StartConditionObject("urban.schedule.condition.inquiry_done"),
            ),
            "ending_states": ("college_opinion",),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "additional_delay": 2,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "envoi-avis-college-au-spw",
            "title": "Envoi de l'avis collège au SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("college_opinion",),
            "starting_states": ("college_opinion",),
            "start_conditions": (
                MacroStartConditionObject("urban.schedule.condition.inquiry_done"),
            ),
            "ending_states": ("FT_opinion",),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "additional_delay": 10,
            "subtasks": [
                {
                    "type_name": "MacroTaskConfig",
                    "id": "premier-passage",
                    "title": "Premier passage collège",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("college_opinion",),
                    "starting_states": ("college_opinion",),
                    "start_date": "urban.schedule.start_date.inquiry_end_date",
                    "end_conditions": (
                        MacroEndConditionObject(
                            "urban.schedule.condition.college_opinion_done"
                        ),
                    ),
                    "additional_delay": 2,
                    "subtasks": [
                        {
                            "type_name": "TaskConfig",
                            "id": "rediger-projet-avis",
                            "title": "Rédiger le projet d'avis",
                            "default_assigned_group": "environment_editors",
                            "default_assigned_user": "urban.assign_folder_manager",
                            "creation_state": ("college_opinion",),
                            "starting_states": ("college_opinion",),
                            "end_conditions": (
                                EndConditionObject(
                                    "urban.schedule.condition.college_opinion_in_progress"
                                ),
                            ),
                            "start_date": "urban.schedule.start_date.inquiry_end_date",
                            "additional_delay": 1,
                        },
                    ],
                },
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "rapport-synthese",
            "title": "Rapport de synthèse",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("FT_opinion",),
            "ending_states": ("final_decision_in_progress",),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.spw_project_receipt_done"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date.",
            "additional_delay": 70,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("final_decision_in_progress",),
            "ending_states": ("accepted", "refused", "inacceptable"),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_delivered"),
            ),
            "start_date": "urban.schedule.start_date.spw_decision_project_receipt_date",
            "additional_delay": 20,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "urban_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("final_decision_in_progress",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.college_authority"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.decision_written"),
                    ),
                    "start_date": "urban.schedule.start_date.spw_decision_project_receipt_date",
                    "additional_delay": 2,
                },
            ],
        },
    ],
    "envclassone": [
        {
            "type_name": "TaskConfig",
            "id": "deposit",
            "title": "Dépot du dossier",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "transmit_to_spw",
            "title": "Transmis au SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "schedule.start_date.task_starting_date",
            "creation_conditions": (
                CreationConditionObject("urban.schedule.condition.deposit_done"),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.transmit_to_spw_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "spw_check_completion",
            "title": "Vérification complétude par le SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("deposit",),
            "start_date": "urban.schedule.start_date.spw_receipt_date",
            "start_conditions": (
                StartConditionObject("urban.schedule.condition.transmit_to_spw_done"),
            ),
            "ending_states": ("complete", "incomplete", "inacceptable"),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 20,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "incomplet",
            "title": "Incomplet",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("incomplete",),
            "starting_states": ("incomplete",),
            "ending_states": ("complete", "inacceptable", "abandoned"),
            "start_date": "schedule.start_date.subtask_highest_due_date",
            "additional_delay": 0,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "demande_complements",
                    "title": "Demander des compléments",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "starting_states": ("incomplete",),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",
                    "additional_delay": 1,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "attente_complements",
                    "title": "En attente de compléments",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.incomplete_for_6_months", "OR"
                        ),
                        EndConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.ask_complements_date",
                    "additional_delay": 183,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "transmis_complements_au_spw",
                    "title": "Transmis des compléments au SPW",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_received"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject(
                            "urban.schedule.condition.complements_transmit_to_spw"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.complements_deposit_date",
                    "additional_delay": 3,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "verif_complements",
                    "title": "Vérification compléments par le SPW",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "ending_states": ("complete", "inacceptable", "abandoned"),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.complements_transmit_to_spw"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.complements_deposit_date",
                    "additional_delay": 20,
                },
                {
                    "type_name": "TaskConfig",
                    "id": "irrecevable-apres-6-mois",
                    "title": "Irrecevable après 6 mois",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("incomplete",),
                    "ending_states": ("complete", "inacceptable", "abandoned"),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.incomplete_for_6_months"
                        ),
                    ),
                    "start_conditions": (
                        StartConditionObject(
                            "urban.schedule.condition.complements_asked"
                        ),
                    ),
                    "start_date": "urban.schedule.start_date.creation_date",
                    "additional_delay": 0,
                },
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "transmit_complete",
            "title": "Transmis complet",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.acknowledgment_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "identification-rubriques",
            "title": "Identification des rubriques",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "start_date": "schedule.start_date.task_starting_date",
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.rubrics_choice_done"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 1,
        },
        {
            "type_name": "TaskConfig",
            "id": "creer-demande-avis",
            "title": "Préparer demandes d'avis",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.has_opinion_requests", "AND"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_created", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "demande-avis-en-cours",
            "title": "Avis en cours",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress"
                ),
            ),
            "starting_states": ("complete",),
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.opinion_requests_done", "AND"
                ),
            ),
            "activate_recurrency": True,
            "recurrence_states": ("complete",),
            "recurrence_conditions": (
                RecurrenceConditionObject(
                    "urban.schedule.condition.opinion_requests_in_progress", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "additional_delay": 60,
            "activate_recurrency": True,
            "marker_interfaces": [
                u"Products.urban.schedule.interfaces.ISendOpinionRequestsTask"
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry-preparation",
            "title": "Préparer l'enquête publique",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.is_not_temporary_licence", "AND"
                ),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date",
            "end_conditions": (
                EndConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 1,
        },
        {
            "type_name": "TaskConfig",
            "id": "inquiry",
            "title": "Enquête publique en cours",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.inquiry_dates_defined", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.inquiry_done", "AND"),
            ),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 0,
        },
        {
            "type_name": "TaskConfig",
            "id": "rapport-analyse",
            "title": "Rapport d'analyse",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.is_not_temporary_licence", "AND"
                ),
            ),
            "start_conditions": (
                StartConditionObject("urban.schedule.condition.inquiry_done"),
            ),
            "ending_states": ("college_opinion",),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "additional_delay": 2,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "envoi-avis-college-au-spw",
            "title": "Envoi de l'avis collège au SPW",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("college_opinion",),
            "starting_states": ("college_opinion",),
            "start_conditions": (
                MacroStartConditionObject("urban.schedule.condition.inquiry_done"),
            ),
            "ending_states": ("FT_opinion",),
            "start_date": "urban.schedule.start_date.inquiry_end_date",
            "additional_delay": 10,
            "subtasks": [
                {
                    "type_name": "MacroTaskConfig",
                    "id": "premier-passage",
                    "title": "Premier passage collège",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("college_opinion",),
                    "starting_states": ("college_opinion",),
                    "start_date": "urban.schedule.start_date.inquiry_end_date",
                    "end_conditions": (
                        MacroEndConditionObject(
                            "urban.schedule.condition.college_opinion_done"
                        ),
                    ),
                    "additional_delay": 2,
                    "subtasks": [
                        {
                            "type_name": "TaskConfig",
                            "id": "rediger-projet-avis",
                            "title": "Rédiger le projet d'avis",
                            "default_assigned_group": "environment_editors",
                            "default_assigned_user": "urban.assign_folder_manager",
                            "creation_state": ("college_opinion",),
                            "starting_states": ("college_opinion",),
                            "end_conditions": (
                                EndConditionObject(
                                    "urban.schedule.condition.college_opinion_in_progress"
                                ),
                            ),
                            "start_date": "urban.schedule.start_date.inquiry_end_date",
                            "additional_delay": 1,
                        },
                    ],
                },
            ],
        },
        {
            "type_name": "TaskConfig",
            "id": "rapport-synthese",
            "title": "Rapport de synthèse",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("FT_opinion",),
            "ending_states": ("final_decision_in_progress",),
            "end_conditions": (
                EndConditionObject("urban.schedule.condition.spw_project_receipt_done"),
            ),
            "start_date": "urban.schedule.start_date.acknowledgment_date.",
            "additional_delay": 110,
        },
        {
            "type_name": "MacroTaskConfig",
            "id": "decision-finale",
            "title": "Décision finale à notifier",
            "default_assigned_group": "environment_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("final_decision_in_progress",),
            "ending_states": ("accepted", "refused", "inacceptable"),
            "end_conditions": (
                MacroEndConditionObject("urban.schedule.condition.decision_delivered"),
            ),
            "start_date": "urban.schedule.start_date.spw_decision_project_receipt_date",
            "additional_delay": 30,
            "subtasks": [
                {
                    "type_name": "TaskConfig",
                    "id": "rediger-proposition-decision",
                    "title": "Rédiger la décision",
                    "default_assigned_group": "environment_editors",
                    "default_assigned_user": "urban.assign_folder_manager",
                    "creation_state": ("final_decision_in_progress",),
                    "creation_conditions": (
                        CreationConditionObject(
                            "urban.schedule.condition.college_authority"
                        ),
                    ),
                    "end_conditions": (
                        EndConditionObject("urban.schedule.condition.decision_written"),
                    ),
                    "start_date": "urban.schedule.start_date.spw_decision_project_receipt_date",
                    "additional_delay": 2,
                },
            ],
        },
    ],
}
