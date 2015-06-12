from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class LongTextView(BrowserView):
    """
      This manage the view of long text
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.field = self.request.get('field', None)
        if not self.field:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('Nothing to show !!!'), type="error")

    def getFieldText(self):
        """
          Returns the entire text
        """
        context = aq_inner(self.context)
        if hasattr(context, self.field):
            return getattr(context, 'get' + self.field[0].capitalize() + self.field[1:])()
        else:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('The field does not exist !!!'), mapping={"field": self.field}, type="error")
