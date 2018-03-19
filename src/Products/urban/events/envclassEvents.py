# encoding: utf-8
from imio.history.utils import add_event_to_history


def updateHistory(obj, envent):
    updateRubricHistory(obj)
    updateAdditionalLegalConditionsHistory(obj)
    pass


def updateRubricHistory(obj):
    rubrics = obj.getRubrics()
    if rubrics:
        extra_rubrics = dict()
        extra_rubrics['rubrics_history'] = [rubric.id for rubric in rubrics]
        extra_rubrics['rubrics_history'] = [addi.id for addi in addi]

        [rubric, addi]
        add_event_to_history(obj, 'rubrics_history', 'update_rubrics', extra_infos=extra_rubrics, verify=True)


def updateAdditionalLegalConditionsHistory(obj):
    additionalLegalConditions = obj.getAdditionalLegalConditions()[1].id
    if additionalLegalConditions:
        extra_rubrics = dict()
        extra_rubrics['additionalLegalConditions_history'] = [additionalLegalCondition.id for additionalLegalCondition in additionalLegalConditions]
        add_event_to_history(obj, 'additionalLegalConditions_history', 'update_additionalLegalConditions', extra_infos=extra_rubrics, verify=True)

