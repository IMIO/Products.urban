# encoding: utf-8
from imio.history.utils import add_event_to_history


def updateHistory(obj, event):
    update_rubric_history(obj)
    update_alc_history(obj)


def update_rubric_history(obj):
    """
    update history of Rubric object
    """
    rubrics = obj.getRubrics()
    if rubrics is not None:
        extra_rubrics = dict()
        extra_rubrics['rubrics_history'] = [rubric.id for rubric in rubrics]
        if has_changes(extra_rubrics['rubrics_history'], get_value_history_by_index(obj, 'rubrics_history', -1)):
            add_event_to_history(obj, 'rubrics_history', 'update_rubrics', extra_infos=extra_rubrics)


def update_alc_history(obj):
    """
    update history of AdditionalLegalConditions object
    """
    additionalLegalConditions = obj.getAdditionalLegalConditions()
    if additionalLegalConditions is not None:
        extra_alc = dict()
        extra_alc['alc_history'] = [alc.id for alc in additionalLegalConditions]
        if has_changes(extra_alc['alc_history'], get_value_history_by_index(obj, 'alc_history', -1)):
            add_event_to_history(obj, 'alc_history', 'update_alc', extra_infos=extra_alc)


def get_value_history_by_index(obj, history_attr, index):
    """
    get history -2 value. the last position is the actual value
    :param obj:
    :param history_attr:
    :return:
    """
    if getattr(obj, history_attr, False):
        if len(getattr(obj, history_attr)) == 1:
            return getattr(obj, history_attr)[-1]
        if len(getattr(obj, history_attr)) > 1:
            return getattr(obj, history_attr)[index]
    return []


def has_changes(current_values, last_history_values):
    return set(current_values) != set(last_history_values)
