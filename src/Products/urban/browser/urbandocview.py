from Products.Five import BrowserView


class UrbanDocView(BrowserView):
    """
      This manage the view of an UrbanDoc
    """

    def showTALCondition(self, field):
        context = self.context
        return field.getName() != 'TALCondition' or 'portal_urban' in context.absolute_url_path().split('/')
