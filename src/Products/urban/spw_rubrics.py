# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from Products.urban.scripts.parse_spw_rubrics import parse_rubrics
from plone import api

import cgi
import json
import logging
import os


logger = logging.getLogger("urban: SPW rubrics")


# The SPW codeType values (I, S, SE, I_S) map to the existing legacy
# conditions folders, any other codeType (e.g. CMTD) gets its own folder.
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


# Titles of the rubric category folders,
# categories absent from this mapping keep their current title.
RUBRIC_CATEGORY_TITLES = {
    "94": u"94 Espèces exotiques",
    "COV-01": u"COV-01 Impression sur rotative offset à sécheur thermique",
    "COV-02": u"COV-02 Héliogravure d’édition",
    "COV-03": u"COV-03 Autres activités d’impression",
    "COV-04": u"COV-04 Nettoyage de surface",
    "COV-05": u"COV-05 Autres nettoyages de surface",
    "COV-06": u"COV-06 Revêtement et retouche des véhicules",
    "COV-07": u"COV-07 Laquage en continu",
    "COV-08": u"COV-08 Autres revêtements, y compris le revêtement de métaux, "
    u"de plastiques, de textiles, de feuilles de papier : "
    u"consommation de solvant > 5 t/an",
    "COV-09": u"COV-09 Revêtement de fils de bobinage",
    "COV-10": u"COV-10 Revêtement de surface en bois",
    "COV-11": u"COV-11 Nettoyage à sec",
    "COV-12": u"COV-12 Imprégnation du bois",
    "COV-13": u"COV-13 Revêtement du cuir",
    "COV-14": u"COV-14 Fabrication de chaussures",
    "COV-15": u"COV-15 Stratification de bois et de plastique",
    "COV-16": u"COV-16 Revêtement adhésif",
    "COV-17": u"COV-17 Fabrication de préparations, revêtements, vernis, "
    u"encres et colles",
    "COV-18": u"COV-18 Conversion de caoutchouc",
    "COV-19": u"COV-19 Extraction d’huiles végétales et de graisses animales "
    u"et activités de raffinage d’huile végétale",
    "COV-20": u"COV-20 Fabrication de produits pharmaceutiques",
    "COV-21": u"COV-21 Revêtement de véhicules (automobiles, cabines de "
    u"camion, camionnettes, camions et autobus) neufs",
}


def _folder_ids_for_code_type(code_type):
    return CODE_TYPE_TO_FOLDER_IDS.get(code_type, [code_type])


def _get_or_create_folder(container, folder_id, title, allowed_type):
    if folder_id in container:
        return container[folder_id]
    folder = api.content.create(
        container=container, type="Folder", id=folder_id, title=title
    )
    folder.setConstrainTypesMode(1)
    folder.setLocallyAllowedTypes([allowed_type])
    folder.setImmediatelyAddableTypes([allowed_type])
    return folder


def _update_rubric_category_title(category_folder):
    title = RUBRIC_CATEGORY_TITLES.get(category_folder.getId())
    if title and safe_unicode(category_folder.Title()) != title:
        category_folder.setTitle(title)
        category_folder.reindexObject(
            idxs=["Title", "SearchableText", "sortable_title"]
        )


def _sort_folder(folder):
    if folder.objectIds() == sorted(folder.objectIds()):
        return
    folder.orderObjects("getId")
    # orderObjects does not reindex the position used to sort the vocabularies
    for obj in folder.objectValues():
        obj.reindexObject(idxs=["getObjPositionInParent"])


def _get_or_create_condition(
    conditions_folder, condition_id, condition_data, code_type
):
    """Create the condition, or update it if its SPW values changed.

    Return a (condition, status) tuple, status being "created", "updated"
    or "unchanged".
    """
    if condition_id in conditions_folder:
        condition = conditions_folder[condition_id]
        if not _condition_has_changed(condition, condition_data, code_type):
            return condition, "unchanged"
        condition.setTitle(condition_data["title"])
        condition.setExtraValue(code_type)
        _set_condition_description(condition, condition_data)
        condition.reindexObject()
        return condition, "updated"

    condition = api.content.create(
        container=conditions_folder,
        type="UrbanVocabularyTerm",
        id=condition_id,
        title=condition_data["title"],
        extraValue=code_type,
    )
    _set_condition_description(condition, condition_data)
    return condition, "created"


def _set_condition_description(condition, condition_data):
    field = condition.getField("description")
    field.setContentType(condition, "text/html")
    condition.setDescription(
        _condition_link(condition_data["url"], condition_data["title"])
    )


def _condition_has_changed(condition, condition_data, code_type):
    """Return True if the SPW values differ from the ones stored on the condition."""
    description = condition.getField("description").getRaw(condition)
    expected_description = _condition_link(
        condition_data["url"], condition_data["title"]
    )
    return (
        safe_unicode(condition.Title()) != safe_unicode(condition_data["title"])
        or condition.getExtraValue() != code_type
        or safe_unicode(description) != expected_description
    )


def _condition_link(url, title):
    """Return an HTML link to the condition legal text, with escaped values."""
    return u'<a href="{0}">{1}</a>'.format(
        cgi.escape(url, quote=True), cgi.escape(title)
    )


def _rubric_has_changed(term, rubric):
    """Return True if the SPW values differ from the ones stored on the term."""
    description = term.getField("description").getRaw(term)
    return (
        term.getNumber() != rubric["number"]
        or str(term.getExtraValue()) != str(rubric["extraValue"])
        or safe_unicode(description) != safe_unicode(rubric["description"])
    )


def _compute_rubric_condition_uids(
    existing_uids, bound_conditions, condition_uids_by_key, spw_condition_uids
):
    """
    Return the exploitation condition UIDs a rubric should be linked to.

    SPW conditions are replaced by the ones currently bound in the mapping,
    so a condition removed from the SPW mapping is unlinked from the rubric.
    Conditions that are not part of the SPW list (added manually) are kept.
    """
    condition_uids = set(existing_uids) - spw_condition_uids
    for bound_condition in bound_conditions:
        key = (bound_condition["type"], bound_condition["id"])
        condition_uids.update(condition_uids_by_key.get(key, []))
    return condition_uids


def import_spw_rubrics():
    """
    Replace/complete the EnvironmentRubricTerm vocabulary with the
    reference rubric list provided by the SPW, so
    iA.Urban and NOTICe/Twice share a consistent list from the start, and
    link each rubric to its sectoral/integral exploitation conditions.

    Rubrics are parsed directly from the committed SPW XML export
    (`data/Rubriques_PE.xml`, see Products.urban.scripts.parse_spw_rubrics).
    The conditions mapping is read from a static JSON file
    (`data/spw_conditions.json`, `{"mapping": ..., "conditions": ...}`)
    generated ahead of time by `Products.urban.scripts.fetch_spw_conditions`.
    """
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    rubrics = parse_rubrics(os.path.join(data_dir, "Rubriques_PE.xml"))
    with open(os.path.join(data_dir, "spw_conditions.json")) as json_file:
        conditions_data = json.load(json_file)
    mapping = conditions_data["mapping"]
    all_conditions = conditions_data["conditions"]
    logger.info(
        "Loaded %s SPW rubrics and %s condition types (%s mapped rubrics)",
        len(rubrics),
        len(all_conditions),
        len(mapping),
    )

    portal_urban = api.portal.get_tool("portal_urban")
    rubrics_folder = portal_urban.rubrics
    conditions_root = portal_urban.exploitationconditions

    condition_uids_by_key = {}

    for code_type, conditions_by_id in all_conditions.iteritems():
        for conditions_folder_id in _folder_ids_for_code_type(code_type):
            logger.info(
                "Importing %s SPW conditions of type %s in folder %s",
                len(conditions_by_id),
                code_type,
                conditions_folder_id,
            )
            try:
                conditions_folder = _get_or_create_folder(
                    conditions_root,
                    conditions_folder_id,
                    FOLDER_TITLES.get(conditions_folder_id, conditions_folder_id),
                    "UrbanVocabularyTerm",
                )
            except Exception:
                logger.exception(
                    "Error while creating SPW conditions folder %s (type %s)",
                    conditions_folder_id,
                    code_type,
                )
                raise

            counts = {"created": 0, "updated": 0, "unchanged": 0}
            for condition_id, condition_data in conditions_by_id.iteritems():
                try:
                    condition, status = _get_or_create_condition(
                        conditions_folder, condition_id, condition_data, code_type
                    )
                except Exception:
                    logger.exception(
                        "Error while importing SPW condition %s (type %s) in %s",
                        condition_id,
                        code_type,
                        conditions_folder_id,
                    )
                    raise
                counts[status] += 1
                if status != "unchanged":
                    logger.debug("SPW condition %s %s", condition_id, status)
                condition_uids_by_key.setdefault((code_type, condition_id), [])
                condition_uids_by_key[(code_type, condition_id)].append(condition.UID())
            logger.info(
                "SPW conditions of type %s: %s created, %s updated, %s unchanged",
                code_type,
                counts["created"],
                counts["updated"],
                counts["unchanged"],
            )

    spw_condition_uids = set(
        uid for uids in condition_uids_by_key.values() for uid in uids
    )

    logger.info("%s SPW conditions imported", len(spw_condition_uids))

    created = 0
    updated = 0
    relinked = 0

    for index, rubric in enumerate(rubrics, 1):
        try:
            result = _import_rubric(
                rubric,
                rubrics_folder,
                mapping,
                condition_uids_by_key,
                spw_condition_uids,
            )
        except Exception:
            logger.exception(
                "Error while importing SPW rubric %s (id %s, identifier %s)",
                rubric["number"],
                rubric["id"],
                rubric["identifier"],
            )
            raise
        created += result["created"]
        updated += result["updated"]
        relinked += result["relinked"]
        if index % 100 == 0 or index == len(rubrics):
            logger.info("%s/%s SPW rubrics processed", index, len(rubrics))

    _sort_folder(rubrics_folder)
    for category_folder in rubrics_folder.objectValues("ATFolder"):
        _update_rubric_category_title(category_folder)
        _sort_folder(category_folder)

    logger.info(
        "SPW rubrics import done: %s created, %s updated, %s unchanged, "
        "%s with updated conditions",
        created,
        updated,
        len(rubrics) - created - updated,
        relinked,
    )


def _import_rubric(
    rubric, rubrics_folder, mapping, condition_uids_by_key, spw_condition_uids
):
    """Create or update one SPW rubric and link its exploitation conditions."""
    result = {"created": 0, "updated": 0, "relinked": 0}
    category_id = rubric["category_id"]
    category_folder = _get_or_create_folder(
        rubrics_folder,
        category_id,
        RUBRIC_CATEGORY_TITLES.get(category_id, category_id),
        "EnvironmentRubricTerm",
    )

    rubric_id = rubric["id"]
    if rubric_id in category_folder:
        term = category_folder[rubric_id]
        if _rubric_has_changed(term, rubric):
            term.setNumber(rubric["number"])
            term.setExtraValue(rubric["extraValue"])
            term.setDescription(rubric["description"])
            term.processForm()
            term.updateTitle()
            logger.debug("Updated SPW rubric %s", rubric["number"])
            result["updated"] = 1
    else:
        # Set `number` here: create() renames the object to its number right away,
        # and crashes if the number is still empty.

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
        logger.debug("Created SPW rubric %s", rubric["number"])
        result["created"] = 1

    bound_conditions = mapping.get(rubric["number"]) or []
    for bound_condition in bound_conditions:
        key = (bound_condition["type"], bound_condition["id"])
        if key not in condition_uids_by_key:
            logger.warning(
                "SPW rubric %s is bound to unknown condition %s (type %s)",
                rubric["number"],
                bound_condition["id"],
                bound_condition["type"],
            )

    existing_uids = set(term.getRawExploitationCondition() or [])
    condition_uids = _compute_rubric_condition_uids(
        existing_uids, bound_conditions, condition_uids_by_key, spw_condition_uids
    )
    if condition_uids != existing_uids:
        term.setExploitationCondition(list(condition_uids))
        logger.debug(
            "Updated conditions of SPW rubric %s: %s added, %s removed",
            rubric["number"],
            len(condition_uids - existing_uids),
            len(existing_uids - condition_uids),
        )
        result["relinked"] = 1
    return result
