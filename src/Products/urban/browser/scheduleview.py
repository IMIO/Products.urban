# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.urban.interfaces import IGenericLicence
#from Products.urban.browser.urbantable import ScheduleTable

from plone import api


class ScheduleView(BrowserView):
    """
      This manages urban schedule view
    """
    def __init__(self, context, request):
        super(ScheduleView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getLicencesInProgress(self):
        catalog = api.portal.get_tool('portal_catalog')
        licences_in_progress = catalog(
            object_provides=IGenericLicence.__identifier__,
            review_state='in_progress',
        )

        return licences_in_progress
