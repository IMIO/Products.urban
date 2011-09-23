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