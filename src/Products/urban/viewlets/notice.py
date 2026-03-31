# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate


class NoticeTransmitState(ViewletBase):
    """This viewlet displays the state of information coming from / going to NOTICe."""

    def _get_notifications(self, key, default):
        annotations = IAnnotations(self.context)
        annotation_key = "notice_notification"
        return annotations.get(annotation_key, {}).get(key, default)

    @property
    def incoming(self):
        result = {}
        incoming_params = self._get_notifications("incoming", {})
        if incoming_params:
            result["id"] = incoming_params["notice_id"]
            result["date"] = incoming_params["reception_date"].strftime(
                "%d/%m/%Y, %H:%M:%S"
            )
            result["type_label"] = translate(
                incoming_params["notice_type"], "urban", context=self.request
            )
        return result

    @property
    def outgoings(self):
        results = []
        outgoing_params = self._get_notifications("outgoing", [])
        if outgoing_params:
            for outgoing in outgoing_params:
                results.append(
                    {
                        "incoming_notice_id": outgoing["incoming_notice_id"],
                        "timestamp": outgoing["timestamp"],
                        "date": outgoing["send_date"].strftime("%d/%m/%Y, %H:%M:%S"),
                        "type_label": translate(
                            outgoing["outgoing_notice_type"],
                            "urban",
                            context=self.request,
                        ),
                        "user": outgoing["user"],
                    }
                )
        return results

    index = ViewPageTemplateFile("templates/notice_transmit_state.pt")
