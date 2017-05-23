# -*- coding: utf-8 -*-

from imio.dashboard.vocabulary import ConditionAwareCollectionVocabulary

from plone import api

from Products.urban.config import URBAN_TYPES
from Products.urban.config import URBAN_CWATUPE_TYPES
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.config import URBAN_ENVIRONMENT_TYPES

from zope.i18n import translate as _
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class WorkflowStatesVocabulary(object):
    """
    List all states of a given workflow 'workflow_name'.
    """

    workflow_name = ''

    def __call__(self, context):
        wf_tool = api.portal.get_tool('portal_workflow')
        licence_wf = wf_tool.get(self.workflow_name)

        vocabulary_terms = []
        for state in licence_wf.states.objectValues():
            vocabulary_terms.append(
                SimpleTerm(
                    state.id,
                    state.id,
                    _(state.id, 'plone', context=context.REQUEST)
                )
            )

        vocabulary = SimpleVocabulary(sorted(vocabulary_terms, key=lambda term: term.title))
        return vocabulary


class LicencesWorkflowStates(WorkflowStatesVocabulary):
    """
    List all states of urban licence workflow.
    """

    workflow_name = 'urban_licence_workflow'


class DashboardCollections(ConditionAwareCollectionVocabulary):

    def _brains(self, context):
        """ """
        portal = api.portal.get()
        urban_folder = portal.urban
        brains = self.get_collection_brains(urban_folder)

        for licence_type in URBAN_TYPES:
            licence_folder = getattr(urban_folder, licence_type.lower() + 's')
            brains.extend(self.get_collection_brains(licence_folder))

        return brains

    def get_collection_brains(self, folder):
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(
            path={
                'query': '/'.join(folder.getPhysicalPath()),
                'depth': 1
            },
            object_provides='imio.dashboard.interfaces.IDashboardCollection',
            sort_on='getObjPositionInParent'
        )
        return list(brains)

    def __call__(self, context, query=None):
        terms = super(DashboardCollections, self).__call__(
            context,
            query=query,
        )
        filtered_terms = [t for t in terms
                          if t.value.id in self.get_collection_ids(context)]
        return SimpleVocabulary(filtered_terms)

    def get_procedure_category(self, context):
        """Get the procedure category (CODT or CWATUPE) from context"""
        if context.id == 'urban':
            return 'ALL'
        if context.id.startswith('codt'):
            return 'CODT'
        return 'CWATUPE'

    def _format_id(self, type):
        """Format a UrbanType to the collection id"""
        return 'collection_{0}'.format(type.lower())

    def get_collection_ids(self, context):
        ids = ['collection_all_licences']
        ids.extend(map(self._format_id, URBAN_ENVIRONMENT_TYPES))
        category = self.get_procedure_category(context)
        if category == 'CODT' or category == 'ALL':
            ids.extend(map(self._format_id, URBAN_CODT_TYPES))
        if category == 'CWATUPE' or category == 'ALL':
            ids.extend(map(self._format_id, URBAN_CWATUPE_TYPES))
        return ids


class CollectionCategory(object):

    def __call__(self, context, query=None):
        # do not display any category
        return SimpleVocabulary([])
