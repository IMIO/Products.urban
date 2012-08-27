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

    def getLicencesBatch(self, context, sort='sortable_title', batchlen=20, **kwargs):
        catalog = getToolByName(context, 'portal_catalog')
        queryString = {
                'portal_type':URBAN_TYPES,
                'path':'/'.join(context.getPhysicalPath()),
                'sort_on':sort,
                'sort_order':'reverse',
                }
        queryString.update(kwargs)
        brains = catalog(queryString)
        b_start = int(context.REQUEST.get('b_start', 0))
        batch = Batch(brains, batchlen, b_start, orphan=0)
        return batch
