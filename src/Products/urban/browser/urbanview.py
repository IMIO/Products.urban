from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES

class UrbanView(BrowserView):
    """
      This manage the view of urban
    """
    def isUrbanManager(self):
        from Products.CMFCore.utils import getToolByName
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        return member.has_role('Manager') or member.has_role('Editor', getToolByName(context, 'portal_urban'))

    def getLicencesBatch(self, context, sort='sortable_title', **kwargs):
        catalog = getToolByName(context, 'portal_catalog')
        request = aq_inner(self.request)
        foldermanager = request.get('foldermanager', '')
        state = request.get('review_state', '')
        batchlen = int(request.get('batch_len', '') and request.get('batch_len') or self.listBatchSizes()[0])
        sort = request.get('sort_by', sort) and request.get('sort_by') or sort
        sort_order = request.get('reverse_order', 'descending')

        queryString = {
                'portal_type':URBAN_TYPES,
                'path':'/'.join(context.getPhysicalPath()),
                'sort_on':sort,
                'sort_order':sort_order,
                }
        if foldermanager:
            queryString['folder_manager'] = foldermanager
        if state:
            queryString['review_state'] = state
        queryString.update(kwargs)
        brains = catalog(queryString)
        b_start = int(context.REQUEST.get('b_start', 0))
        batch = Batch(brains, batchlen, b_start, orphan=0)
        return batch

    def getArgument(self, key_to_match):
        request = aq_inner(self.request)
        if type(key_to_match) == list:
            return dict([(key, request.get(key, '')) for key in key_to_match])
        request = aq_inner(self.request)
        return request.get(key_to_match, '')

    def listFolderManagers(self):
        """
          Returns the available folder managers
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        urban_tool = getToolByName(context, 'portal_urban')
        current_foldermanager = urban_tool.getCurrentFolderManager(initials=False)
        return [(brain.UID, brain.Title.split('(')[0]) for brain in catalog(portal_type='FolderManager') if brain.UID != current_foldermanager.UID()]

    def amIFolderManager(self):
        """
         return the folder manager bound to the current plone id user if it exists
        """
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban')
        return urban_tool.getCurrentFolderManager(initials=False)

    def listAvailableStates(self):
        """
         return available licence states
        """
        return ['in_progress', 'accepted', 'refused', 'incomplete']

    def listBatchSizes(self):
        """
        """
        return ['20', '30', '50', '100']

class UrbanViewMacros(BrowserView):
    """
      This manage the macros of urban view
    """
