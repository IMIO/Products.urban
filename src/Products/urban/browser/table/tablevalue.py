# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.urban.config import URBAN_TYPES
from Products.urban.browser.table.interfaces import IItemForUrbanTable
from Products.urban.browser.table.interfaces import IBrainForUrbanTable
from Products.urban.browser.table.interfaces import IObjectForUrbanTable

from Products.ZCatalog.Lazy import LazyMap

from plone.memoize import instance

from z3c.table.value import ValuesMixin

from zope.interface import implements
from zope.component import queryAdapter

from plone import api


class ItemForUrbanTable():
    """
    """
    implements(IItemForUrbanTable)

    def __init__(self, value):
        self.value = value

    def __getattr__(self, attr_name):
        return getattr(self.value, attr_name)

    @instance.memoize
    def getTool(self, toolname=''):
        tool = api.portal.get_tool(toolname)
        return tool

    def getRawValue(self):
        return self.value

    def getObject(self):
        """ to implement """

    def getPortalType(self):
        return self.value.portal_type

    def getURL(self):
        """ to implement """

    def getState(self):
        """ to implement """

    def getWorkflowTransitions(self):
        portal_workflow = self.getTool('portal_workflow')
        transitions = portal_workflow.getTransitionsFor(self.getObject())
        return transitions

    @instance.memoize
    def canBeEdited(self):
        obj = self.getObject()
        portal_membership = self.getTool('portal_membership')
        member = portal_membership.getAuthenticatedMember()
        can_edit = member.has_permission('Modify portal content', obj)
        return can_edit

    @instance.memoize
    def canBeDeleted(self):
        obj = self.getObject()
        portal_membership = self.getTool('portal_membership')
        member = portal_membership.getAuthenticatedMember()
        can_delete = member.has_permission('Delete objects', obj)
        return can_delete

    def getPath(self):
        """ to implements."""


class BrainForUrbanTable(ItemForUrbanTable):
    """
    """
    implements(IBrainForUrbanTable)

    @instance.memoize
    def getObject(self):
        obj = self.value.getObject()
        return obj

    def Title(self):
        return self.value.Title

    @instance.memoize
    def getURL(self):
        url = self.value.getURL()
        return url

    def getState(self):
        state = self.value.review_state
        return state

    def getPath(self):
        return self.value.getPath()


class ObjectForUrbanTable(ItemForUrbanTable):
    """
    """
    implements(IObjectForUrbanTable)

    def getObject(self):
        return self.value

    def Title(self):
        return self.value.Title()

    @instance.memoize
    def getURL(self):
        url = self.value.absolute_url()
        return url

    def getState(self):
        portal_workflow = self.getTool('portal_workflow')
        state = portal_workflow.getInfoFor(self.value, 'review_state', '')
        return state

    def getPath(self):
        path = '/'.join(self.value.getPhysicalPath())
        return path


class ValuesForUrbanListing(ValuesMixin):
    """ """

    @property
    def values(self):
        def wrap(item):
            return queryAdapter(item, IItemForUrbanTable)

        items = self.getItems()
        wrapped_items = LazyMap(wrap, items)
        return wrapped_items

    def getItems(self):
        return self.table.raw_values


class ValuesForApplicantListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        return self.context.getApplicants()


class ValuesForApplicantHistoryListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        return self.context.get_applicants_history()


class ValuesForProprietariesListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        proprietaries = self.context.getProprietaries()
        return proprietaries


class ValuesForProprietariesHistoryListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        return self.context.get_proprietaries_history()


class ValuesForTenantsListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        tenants = self.context.getTenants()
        return tenants


class ValuesForPlaintiffListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        return self.context.getPlaintiffs()


class ValuesForClaimantsListing(ValuesForUrbanListing):
    """  return contact values from the context """

    def getItems(self):
        claimants = self.context.getClaimants()
        return claimants


class ValuesForLicenceListing(ValuesForUrbanListing):
    """ return licence values from the context  """

    def getItems(self):
        licence_brains = self.queryLicences()
        return licence_brains

    def queryLicences(self, **kwargs):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        catalog = api.portal.get_tool('portal_catalog')

        query_string = {
            'portal_type': URBAN_TYPES,
            'path': '/'.join(context.getPhysicalPath()),
            'sort_on': 'sortable_title',
            'sort_order': 'descending',
        }

        foldermanager = request.get('foldermanager', '')
        if foldermanager:
            query_string['folder_manager'] = foldermanager

        state = request.get('review_state', '')
        if state:
            query_string['review_state'] = state

        query_string.update(kwargs)

        # update catalog query with criterias found in the request
        for key in request.keys():
            value = request.get(key)
            if key in query_string and value:
                query_string[key] = value

        licence_brains = catalog(query_string)
        return licence_brains


class ValuesForAllLicencesListing(ValuesForLicenceListing):

    def queryLicences(self):
        query_string = {'sort_on': 'created'}
        return super(ValuesForAllLicencesListing, self).queryLicences(**query_string)


class ValuesForInspectionReportsListing(ValuesForUrbanListing):
    """  return inspection reports from the context """

    def getItems(self):
        reports = self.context.objectValues('UrbanEventInspectionReport')
        return reports
