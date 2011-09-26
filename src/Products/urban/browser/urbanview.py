from Acquisition import aq_inner
from Products.Five import BrowserView

class UrbanView(BrowserView):
    """
      This manage the view of urban
    """
    def isScheduleAvailable(self):
        context = aq_inner(self.context)
        try:
            scheduleview = context.restrictedTraverse('@@schedule')
            return True
        except AttributeError:
            return False

    def isUrbanManager(self):
        from Products.CMFCore.utils import getToolByName
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        return member.has_role('Manager') or member.has_role('Editor', getToolByName(context, 'portal_urban'))
