# -*- coding: utf-8 -*-

from DateTime import DateTime

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
            if field.schemata == 'default' and not hasattr(field, 'optional') \
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
        start_date = DateTime(self.request.start)
        end_date = start_date + 20
        return end_date.strftime('%Y-%m-%d')
