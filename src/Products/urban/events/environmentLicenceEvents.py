# -*- coding: utf-8 -*-


def setExploitationConditions(licence, event):
    """
    A minimal set of integral/sectorial exploitation conditions are determined by the rubrics
    selected on an environment licence.
    """
    rubrics = licence.getRubrics()
    if not rubrics:
        licence.setMinimumLegalConditions([])
    else:
        condition_field = rubrics[0].getField("exploitationCondition")
        all_conditions = set()
        for rubric in rubrics:
            conditions = condition_field.getRaw(rubric)
            if conditions:
                all_conditions.update(set(conditions))
        conditions_uid = list(all_conditions)
        licence.setMinimumLegalConditions(conditions_uid)
