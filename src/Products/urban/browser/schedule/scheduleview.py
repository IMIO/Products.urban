# -*- coding: utf-8 -*-
from Products.Five import BrowserView

from Products.urban.browser.schedule.form import ScheduleForm
from Products.urban.browser.schedule.table import ScheduleListingTable


class ScheduleView(BrowserView):
    """
      This manages urban schedule view
    """
    def __init__(self, context, request):
        super(ScheduleView, self).__init__(context, request)
        self.context = context
        self.request = request

        self.form = ScheduleForm(self.context, self.request)
        self.form.update()

        self.schedulelisting = ScheduleListingTable(self, self.request)
        self.schedulelisting.update()

    def renderScheduleListing(self):
        self.schedulelisting.update()

        return u'{listing}{batch}'.format(
            listing=self.schedulelisting.render(),
            batch=self.schedulelisting.renderBatch(),
        )
