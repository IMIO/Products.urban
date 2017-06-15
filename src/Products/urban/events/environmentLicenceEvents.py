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
        condition_field = rubrics[0].getField('exploitationCondition')
        conditions_uid = list(set([condition_field.getRaw(rubric) for rubric in rubrics]))
        licence.setMinimumLegalConditions(conditions_uid)
