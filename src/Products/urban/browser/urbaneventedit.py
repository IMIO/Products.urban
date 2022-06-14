# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

from numpy import busdaycalendar
from numpy import busday_offset

from plone import api

from Products.Archetypes.browser.edit import Edit

from zope.component import queryMultiAdapter


class UrbanEventEdit(Edit):
    """
    This manage the edit view of UrbanEvent.
    """

    def get_editable_fields(self, schemata):
        portal_state = queryMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        ws4pmSettings = queryMultiAdapter(
            (portal_state.portal(), self.request),
            name='ws4pmclient-settings'
        )

        fields = []
        for field in self.context.schema.fields():
            if field.schemata == 'default' and not hasattr(field, 'optional')\
               and field.widget.visible and field.widget.visible['view']:
                fields.append(field)

        linkedUrbanEventType = self.context.getUrbaneventtypes()

        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            field = self.context.getField(activatedField)
            if field not in fields:
                fields.append(field)

        if ws4pmSettings and ws4pmSettings.checkAlreadySentToPloneMeeting(self.context):
            return [f for f in fields if not getattr(f, 'pm_text_field', False)]
        else:
            return fields

    def get_event_config_uid(self):
        return self.context.getUrbaneventtypes().UID()

class UrbanEventInquiryEdit(UrbanEventEdit):
    """
    This manage the edit view of UrbanEventInquri.
    """

    def get_editable_fields(self, schemata):
        fields = super(UrbanEventInquiryEdit, self).get_editable_fields(schemata)
        inquiry_dates = ['investigationStart', 'investigationEnd']
        fields = [f for f in fields if f.getName() not in inquiry_dates]
        return fields


class ComputeInquiryDelay(object):
    """
    """

    def __call__(self):
        """
        """
        urban_tool = api.portal.get_tool('portal_urban')
        try:
            start_date = datetime.strptime(self.request.start, '%Y-%m-%d 00:00').date()
        except ValueError:
            start_date = datetime.strptime(self.request.start, '%Y/%m/%d').date()

        inquiry_delay = 14
        licence = self.context.aq_parent
        if hasattr(licence, 'getRoadAdaptation'):
            if licence.getRoadAdaptation() and licence.getRoadAdaptation() != ['']:
                inquiry_delay = 29

        if licence.portal_type in ['EnvClassOne']:
            inquiry_delay = 29
        if licence.portal_type == 'CODT_UniqueLicence':
            if licence.getInquiry_category() == 'B':
                inquiry_delay = 29
            if licence.getInquiry_category() == 'C':
                inquiry_delay = 14
        if self.context.getLinkedInquiry().getInquiry_type() == 'announcement':
            inquiry_delay = 14
        weekmask = urban_tool.get_week_offdays(as_mask=True)
        offday_periods = urban_tool.get_offday_periods(types='inquiry_suspension')
        holidays = urban_tool.get_offdays(types='holydays')

        for period in offday_periods:
            start = period['start_date']
            end = period['end_date']
            date_range = [start + timedelta(days=d) for d in range((end - start).days + 1)]
            holidays.extend(date_range)

        # first calculate end date without weekends
        calendar = busdaycalendar(weekmask='1111111', holidays=holidays)
        end_date = busday_offset(start_date, inquiry_delay, roll='forward', busdaycal=calendar)
        # then round the end date to not fall during a weekend
        calendar = busdaycalendar(weekmask=weekmask, holidays=holidays)
        rounded_end_date = busday_offset(end_date, 0, roll='forward', busdaycal=calendar)
        return str(rounded_end_date)
