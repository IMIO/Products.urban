# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.urban.utils import get_licence_context
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

    @property
    def outgoing_documents(self):
        results = []

        event_path = "/".join(self.context.getPhysicalPath())
        matching_documents = []
        contexts = get_licence_context(self.context, get_all_object=True)
        if not contexts:
            return results

        for context in contexts:
            for doc in context.listFolderContents(
                contentFilter={"portal_type": ["ATFile", "ATImage", "File", "Image"]}
            ):
                annotations = IAnnotations(doc)
                key = "notice_notification"
                notice = annotations.get(key, {})
                outgoings = notice.get("outgoing", [])
                for outgoing in outgoings:
                    if outgoing.get("event_path") == event_path:
                        matching_documents.append((doc, outgoing))

        for doc, outgoing in matching_documents:
            results.append(
                {
                    "date": outgoing["date"].strftime("%d/%m/%Y, %H:%M:%S"),
                    "user": outgoing["user"],
                    "document_title": doc.Title(),
                    "document_url": doc.absolute_url(),
                }
            )
        return results

    index = ViewPageTemplateFile("templates/notice_transmit_state.pt")
