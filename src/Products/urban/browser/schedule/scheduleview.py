# -*- coding: utf-8 -*-
from Products.urban.browser.schedule.form import ScheduleForm
from Products.urban.browser.schedule.table import ScheduleListingTable

from five import grok

from plone.z3cform.z2 import switch_on

from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import Interface

grok.templatedir('templates')


class ScheduleView(grok.View):
    """
      This manages urban schedule view
    """
    grok.context(Interface)
    grok.name('schedule')
    grok.require('zope2.View')

    template = ViewPageTemplateFile('templates/scheduleview.pt')

    def update(self):
        switch_on(self)

        self.form = ScheduleForm(self.context, self.request)
        self.form.update()

        self.schedulelisting = ScheduleListingTable(self, self.request)
        self.schedulelisting.update()

        super(ScheduleView, self).update()
