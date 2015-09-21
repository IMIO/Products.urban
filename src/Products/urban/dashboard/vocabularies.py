# -*- coding: utf-8 -*-

from plone import api

from zope.i18n import translate as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class LicencesWorkflowStates(object):
    """
    List all states of urban licence workflow.
    """

    def __call__(self, context):
        wf_tool = api.portal.get_tool('portal_workflow')
        licence_wf = wf_tool.get('urban_licence_workflow')

        vocabulary_terms = []
        for state in licence_wf.states.objectValues():
            vocabulary_terms.append(
                SimpleTerm(
                    state.id,
                    state.id,
                    _(state.id, 'plone', context.REQUEST)
                )
            )

        vocabulary = SimpleVocabulary(vocabulary_terms)
        return vocabulary


class CollectionCategory(object):

    def __call__(self, context, query=None):
        # do not display any category
        return SimpleVocabulary([])
