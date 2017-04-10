# -*- coding: utf-8 -*-

from Products.Archetypes.browser.edit import Edit

from zope.component import queryMultiAdapter


class UrbanEventEdit(Edit):
    """
      This manage the edit view of UrbanEvent
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

        fields = [i for i in self.context.schema.fields() if i.schemata == 'default' and not hasattr(i, 'optional') and i.widget.visible and i.widget.visible['view'] == 'visible']
        linkedUrbanEventType = self.context.getUrbaneventtypes()

        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            field = self.context.getField(activatedField)
            fields.append(field)

        if ws4pmSettings and ws4pmSettings.checkAlreadySentToPloneMeeting(self.context):
            return [f for f in fields if not getattr(f, 'pm_text_field', False)]
        else:
            return fields
