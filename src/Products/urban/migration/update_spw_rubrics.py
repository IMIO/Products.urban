# encoding: utf-8

"""
Isolated from update_290.py (which was getting large): import of the SPW
reference rubrics (EnvironmentRubricTerm vocabulary) and their linked
sectoral/integral exploitation conditions.
#voir avec martin
"""

import json
import logging
import os

from plone import api

from Products.urban.scripts.parse_spw_rubrics import parse_rubrics


logger = logging.getLogger("urban: Import SPW reference rubrics")


# The SPW codeType values (I, S, SE, I_S) map to the existing legacy
CODE_TYPE_TO_FOLDER_IDS = {
    "I": ["CI"],
    "S": ["CS"],
    "SE": ["CS_Eau"],
    "I_S": ["CI_CS"],
}


FOLDER_TITLES = {
    "CI": u"Conditions intégrales",
    "CS": u"Conditions sectorielles",
    "CS_Eau": u"Conditions sectorielles Eau",
    "CI_CS": u"Conditions intégrales et sectorielles",
}


def _folder_ids_for_code_type(code_type):
    return CODE_TYPE_TO_FOLDER_IDS.get(
        code_type, [code_type.replace("/", "_").replace("-", "_")]
    )


def _get_or_create_folder(container, folder_id, title, allowed_type):
    if folder_id in container:
        return getattr(container, folder_id)
    folder = api.content.create(
        container=container, type="Folder", id=folder_id, title=title
    )
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes([allowed_type])
    folder.setImmediatelyAddableTypes([allowed_type])
    return folder


def _get_or_create_condition(conditions_folder, condition_id, condition_data, code_type):
    if condition_id in conditions_folder:
        return getattr(conditions_folder, condition_id)

    condition = api.content.create(
        container=conditions_folder,
        type="UrbanVocabularyTerm",
        id=condition_id,
        title=condition_data["title"],
        extraValue=code_type,
    )
    field = condition.getField("description")
    field.setContentType(condition, "text/html")
    condition.setDescription(
        u'<a href="{0}">{1}</a>'.format(condition_data["url"], condition_data["title"])
    )
    return condition


def import_spw_rubrics(context):
    """
    Update the EnvironmentRubricTerm vocabulary with the
    reference rubric list provided by the SPW .


    The conditions mapping is read from a static JSON file
    (`data/spw_conditions.json`, `{"mapping": ..., "conditions": ...}`)
    generated ahead of time by `Products.urban.scripts.fetch_spw_conditions`
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    rubrics = parse_rubrics(os.path.join(data_dir, "Rubriques_PE.xml"))
    with open(os.path.join(data_dir, "spw_conditions.json")) as json_file:
        conditions_data = json.load(json_file)
    mapping = conditions_data["mapping"]
    all_conditions = conditions_data["conditions"]

    portal_urban = api.portal.get_tool("portal_urban")
    rubrics_folder = portal_urban.rubrics
    conditions_root = portal_urban.exploitationconditions

    condition_uids_by_key = {}

    for code_type, conditions_by_id in all_conditions.iteritems():
        for conditions_folder_id in _folder_ids_for_code_type(code_type):
            conditions_folder = _get_or_create_folder(
                conditions_root,
                conditions_folder_id,
                FOLDER_TITLES.get(conditions_folder_id, conditions_folder_id),
                "UrbanVocabularyTerm",
            )

            for condition_id, condition_data in conditions_by_id.iteritems():
                condition = _get_or_create_condition(
                    conditions_folder, condition_id, condition_data, code_type
                )
                condition_uids_by_key.setdefault((code_type, condition_id), [])
                condition_uids_by_key[(code_type, condition_id)].append(
                    condition.UID()
                )

    for rubric in rubrics:
        category_id = rubric["category_id"]
        category_folder = _get_or_create_folder(
            rubrics_folder, category_id, category_id, "EnvironmentRubricTerm"
        )

        rubric_id = rubric["id"]
        if rubric_id in category_folder:
            term = getattr(category_folder, rubric_id)
            term.setNumber(rubric["number"])
            term.setExtraValue(rubric["extraValue"])
            term.setDescription(rubric["description"])
            term.processForm()
        else:
            term = api.content.create(
                container=category_folder,
                type="EnvironmentRubricTerm",
                id=rubric_id,
                title=rubric_id,
                number=rubric["number"],
                extraValue=rubric["extraValue"],
                description=rubric["description"],
            )
        term.updateTitle()

        bound_conditions = mapping.get(rubric["number"])
        if not bound_conditions:
            continue

        existing_uids = set(term.getRawExploitationCondition() or [])
        condition_uids = set(existing_uids)
        for bound_condition in bound_conditions:
            key = (bound_condition["type"], bound_condition["id"])
            condition_uids.update(condition_uids_by_key.get(key, []))

        if condition_uids != existing_uids:
            term.setExploitationCondition(list(condition_uids))

    logger.info("SPW rubrics import done")
