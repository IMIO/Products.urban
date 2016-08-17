# -*- coding: utf-8 -*-

from Products.Archetypes.browser.edit import Edit

from zope.component import getMultiAdapter


class UrbanEventEdit(Edit):
    """
      This manage the edit view of UrbanEvent
    """

    def get_editable_fields(self, schemata):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        ws4pmSettings = getMultiAdapter(
            (portal_state.portal(), self.request),
            name='ws4pmclient-settings'
        )

        fields = schemata.editableFields(self.context, visible_only=True)

        if ws4pmSettings.checkAlreadySentToPloneMeeting(self.context):
            return [f for f in fields if not getattr(f, 'pm_text_field', False)]
        else:
            return fields
