# ------------------------------------------------------------------------------
from plone.app.layout.viewlets import ViewletBase
# ------------------------------------------------------------------------------
class FirefoxViewlet(ViewletBase):
    '''This viewlet displays the firefox-text if browser isn't firefox.'''    

    def show(self):
        """
          Check if we need to show the viewlet content or not
        """
        #show the viewlet if we are not using Firefox
        return 'Firefox' not in self.request.get('HTTP_USER_AGENT', '')
