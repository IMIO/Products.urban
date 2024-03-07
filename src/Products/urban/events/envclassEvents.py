# encoding: utf-8
from imio.history.utils import add_event_to_history


def update_history(obj, event):
    if hasattr(obj, "getRubrics") and obj.getRubrics():
        update_history_for_vocabulary_field(obj, "rubrics")
    if (
        hasattr(obj, "getAdditionalLegalConditions")
        and obj.getAdditionalLegalConditions()
    ):
        update_history_for_vocabulary_field(obj, "additionalLegalConditions")


def update_history_for_vocabulary_field(obj, fieldname):
    getter = "get{0}{1}".format(
        fieldname[0].upper(),
        fieldname[1:],
    )
    getter_function = getattr(obj, getter)
    value = getter_function()
    if value is not None:
        key = "{0}_history".format(fieldname)
        action = "update_{0}".format(fieldname)
        history_values = {key: [e.id for e in value]}
        last_values = get_value_history_by_index(obj, key, -1, action=action)
        if has_changes(history_values[key], last_values[key]):
            add_event_to_history(obj, key, action, extra_infos=history_values)


def get_value_history_by_index(obj, history_attr, index, action=None):
    """
    Return given history record by index -1 is the latest, -2 the previous, ...
    """
    default = {history_attr: []}
    if not hasattr(obj, history_attr):
        return default
    history = getattr(obj, history_attr)
    if action is not None:
        history = [e for e in history if e["action"] == action]
    if index > len(history) or index * -1 > len(history):
        return default
    return history[index]


def has_changes(current_values, last_history_values):
    return str(current_values) != str(last_history_values)
