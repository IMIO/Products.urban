# -*- coding: utf-8 -*-
from Products.urban.browser.schedule.form import ScheduleForm
from Products.urban.browser.schedule.table import ScheduleListingTable

from Products.urban.utils import getCurrentFolderManager

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

    def refreshBatch(self, batch_start):
        # switch_on(self)
        self.schedulelisting.batchStart = batch_start
        self.schedulelisting.update()

        super(ScheduleView, self).update()

    def update(self):
        switch_on(self)

        self.form = ScheduleForm(self.context, self.request)
        # Restrict the form inputs to the licences managed by the current
        # forder manager
        self._restrictFormToAllowedLicences()
        self.form.update()

        self.schedulelisting = ScheduleListingTable(self, self.request)
        self.schedulelisting.update()

        super(ScheduleView, self).update()

    def _restrictFormToAllowedLicences(self):
        foldermanager = getCurrentFolderManager()

        if not foldermanager:
            return

        managed_licences = foldermanager.getManageableLicences()
        fields = self.form.fields
        fields_name_to_display = ['events_{}'.format(licencetype.lower()) for licencetype in managed_licences]
        fields_name_to_hide = [
            field_name for field_name in fields.keys() if
            field_name.startswith('events_') and field_name not in fields_name_to_display
        ]

        displayed_fields = fields.omit(*fields_name_to_hide)

        self.form.fields = displayed_fields
