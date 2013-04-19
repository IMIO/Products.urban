## -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.memoize import instance

from z3c.table.value import ValuesMixin

from zope.interface import implements

from Products.urban.config import URBAN_TYPES
from Products.urban.browser.interfaces import IItemForUrbanTable, IBrainForUrbanTable


class ItemForUrbanTable():
    """
    """
    implements(IItemForUrbanTable)

    def __init__(self, value):
        self.value = value

    @instance.memoize
    def getTool(self, toolname=''):
        context = self.getObject()
        tool = getToolByName(context, toolname)
        return tool

    def getRawValue(self):
        return self.value

    def getObject(self):
        """ to override """

    def getPortalType(self):
        return self.value.portal_type

    def getURL(self):
        """ to override """

    def getState(self):
        """ to override """

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

    def getActions(self):
        portal_properties = self.getTool('portal_properties')

        obj = self.getObject()
        actions = {}

        if self.canBeEdited():
            external_edition = obj.portal_type in ['File', 'UrbanDoc'] and portal_properties.site_properties.ext_editor
            edit_action = external_edition and 'external_edit' or 'edit'
            actions['edit'] = edit_action

        if self.canBeDeleted():
            actions['delete'] = 'delete_confirmation'

        return actions


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


class ObjectForUrbanTable(ItemForUrbanTable):
    """
    """

    @instance.memoize
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


class ValuesForContactListing(ValuesMixin):
    """  return contact values from the context """

    @property
    def values(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        query_string = {
            'meta_type': 'Contact',
            'path': {
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1,
            },
        }
        contact_brains = catalog(query_string)
        return contact_brains


class ValuesForParcellingListing(ValuesMixin):
    """  return parcelling values from the context """

    @property
    def values(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        query_string = {
            'portal_type': 'ParcellingTerm',
            'path': {
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1,
            },
        }
        contact_brains = catalog(query_string)
        return contact_brains


class ValuesForLicenceListing(ValuesMixin):
    """ return licence values from the context  """

    @property
    def values(self):
        licence_brains = self.queryLicences()
        return licence_brains

    def queryLicences(self, **kwargs):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        catalog = getToolByName(context, 'portal_catalog')

        queryString = {
            'portal_type': URBAN_TYPES,
            'path': '/'.join(context.getPhysicalPath()),
        }

        foldermanager = request.get('foldermanager', '')
        if foldermanager:
            queryString['folder_manager'] = foldermanager

        state = request.get('review_state', '')
        if state:
            queryString['review_state'] = state

        queryString.update(kwargs)
        licence_brains = catalog(queryString)
        return licence_brains
