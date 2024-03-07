# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.vocabulary import CachedCollectionVocabulary

from plone import api

from Products.urban import UrbanMessage as _
from Products.urban.config import URBAN_TYPES
from Products.urban.config import URBAN_CWATUPE_TYPES
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.config import URBAN_ENVIRONMENT_TYPES
from Products.urban.dashboard import utils
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class WorkflowStatesVocabulary(object):
    """
    List all states of a given workflow 'workflow_name'.
    """

    workflow_name = ""

    def __call__(self, context):
        wf_tool = api.portal.get_tool("portal_workflow")
        licence_wf = wf_tool.get(self.workflow_name)

        vocabulary_terms = []
        for state in licence_wf.states.objectValues():
            vocabulary_terms.append(
                SimpleTerm(
                    state.id,
                    state.id,
                    translate(state.id, "plone", context=context.REQUEST),
                )
            )

        vocabulary = SimpleVocabulary(
            sorted(vocabulary_terms, key=lambda term: term.title)
        )
        return vocabulary


class LicencesWorkflowStates(WorkflowStatesVocabulary):
    """
    List all states of urban licence workflow.
    """

    workflow_name = "urban_licence_workflow"


class InspectionFollowupVocabulary(object):
    """
    Return all possible inspection report followup propositions
    """

    def __call__(self, context):
        voc = UrbanVocabulary(
            "urbaneventtypes", vocType="FollowUpEventConfig", value_to_use="title"
        )
        config_voc = voc.getDisplayList(licence_type="Inspection")
        portal = api.portal.get()
        full_voc = [
            ("close", translate(_("close_inspection"), context=portal.REQUEST)),
            ("ticket", translate(_("ticket"), context=portal.REQUEST)),
        ]
        for key in config_voc.keys():
            full_voc.append((key, config_voc.getValue(key)))

        vocabulary_terms = [SimpleTerm(k, k, v) for k, v in full_voc]
        vocabulary = SimpleVocabulary(
            sorted(vocabulary_terms, key=lambda term: term.title)
        )
        return vocabulary


class CovidVocabulary(object):
    """ """

    def __call__(self, context):
        portal = api.portal.get()
        vocabulary = [
            SimpleTerm("COVID", "COVID", translate(_("covid"), context=portal.REQUEST))
        ]
        return vocabulary


class DashboardCollections(CachedCollectionVocabulary):
    def _brains(self, context):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        ids = ["collection_all_licences"] + [
            "collection_{}".format(l_type.lower()) for l_type in URBAN_TYPES
        ]
        brains = catalog(id=ids)
        brains = list(brains)
        brains.sort(key=lambda x: ids.index(x.id))
        return brains

    def _cache_invalidation_key(self, context, real_context):
        """cachekey method for self.__call__."""
        return super(DashboardCollections, self)._cache_invalidation_key(
            context, real_context
        ) + (self.category,)

    def __call__(self, context, real_context):
        self.category = utils.get_procedure_category(
            context,
            self.get_request(context),
        )
        terms = super(DashboardCollections, self).__call__(
            context,
            real_context,
        )
        filtered_terms = [
            t
            for t in terms
            if t.value.split("/")[-1] in self.get_collection_ids(context)
        ]
        return SimpleVocabulary(filtered_terms)

    def _compute_redirect_to(self, collection, criterion):
        """ """
        redirect_to = super(DashboardCollections, self)._compute_redirect_to(
            collection,
            criterion,
        )
        return redirect_to.replace(
            "no_redirect=1",
            "no_redirect=1&category={0}".format(self.category),
        )

    def get_request(self, context):
        return getattr(context, "REQUEST", getRequest())

    def _format_id(self, type):
        """Format a UrbanType to the collection id"""
        return "collection_{0}".format(type.lower())

    def get_collection_ids(self, context):
        ids = ["collection_all_licences"]
        ids.extend(map(self._format_id, URBAN_ENVIRONMENT_TYPES))
        if self.category == "CODT" or self.category == "ALL":
            ids.extend(map(self._format_id, URBAN_CODT_TYPES))
        if self.category == "CWATUPE" or self.category == "ALL":
            ids.extend(map(self._format_id, URBAN_CWATUPE_TYPES))
        return ids


class CollectionCategory(object):
    def __call__(self, context, query=None):
        # do not display any category
        return SimpleVocabulary([])
