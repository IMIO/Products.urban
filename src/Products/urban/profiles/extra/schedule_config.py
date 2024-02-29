# -*- coding: utf-8 -*-

from imio.schedule.content.object_factories import EndConditionObject
from imio.schedule.content.object_factories import StartConditionObject
from imio.schedule.content.object_factories import CreationConditionObject
from imio.schedule.content.object_factories import MacroCreationConditionObject
from imio.schedule.content.object_factories import MacroEndConditionObject


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
                            "urban.schedule.condition.deposit_past_20days", "OR"
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
                            "urban.schedule.condition.deposit_past_20days"
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
                            "urban.schedule.condition.deposit_past_20days", "AND"
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
                EndConditionObject("urban.schedule.condition.announcement_done", "AND"),
            ),
            "calculation_delay": ("schedule.calculation_default_delay",),
            "additional_delay": 20,
        },
        {
            "type_name": "TaskConfig",
            "id": "announcement",
            "title": "Annonce de projet",
            "default_assigned_group": "urban_editors",
            "default_assigned_user": "urban.assign_folder_manager",
            "creation_state": ("complete",),
            "starting_states": ("complete",),
            "creation_conditions": (
                CreationConditionObject(
                    "urban.schedule.condition.announcement_done", "AND"
                ),
            ),
            "end_conditions": (
                EndConditionObject("schedule.end_when_due_date_reached", "AND"),
            ),
            "start_date": "urban.schedule.start_date.announcement_end_date",
            "calculation_delay": ("schedule.calculation_default_delay",),
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
                            "urban.schedule.condition.deposit_past_20days", "OR"
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
                            "urban.schedule.condition.deposit_past_20days"
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
                            "urban.schedule.condition.deposit_past_20days", "AND"
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
                            "urban.schedule.condition.deposit_past_20days", "OR"
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
                            "urban.schedule.condition.deposit_past_20days"
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
                            "urban.schedule.condition.deposit_past_20days", "AND"
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
                            "urban.schedule.condition.deposit_past_20days", "OR"
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
                            "urban.schedule.condition.deposit_past_20days"
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
                            "urban.schedule.condition.deposit_past_20days", "AND"
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
                            "urban.schedule.condition.deposit_past_20days", "OR"
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
                            "urban.schedule.condition.deposit_past_20days"
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
                            "urban.schedule.condition.deposit_past_20days", "AND"
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
}
