# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class FirefoxViewlet(ViewletBase):
    """This viewlet displays the firefox-text if browser isn't firefox."""

    def show(self):
        """
        Check if we need to show the viewlet content or not
        """
        # show the viewlet if we are not using Firefox
        user_agent = self.request.get("HTTP_USER_AGENT", "")
        display = not ("Firefox" in user_agent or "Chrome" in user_agent)
        return display
