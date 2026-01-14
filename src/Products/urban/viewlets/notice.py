# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate


class NoticeTransmitState(ViewletBase):
    """This viewlet displays the state of information sent to NOTICe."""

    def get_transmits(self):
        annotations = IAnnotations(self.context)
        dates = annotations.get("notice_transmit_dates", {})

        results = []
        for (label, value) in dates.items():
            if type(value) is dict:
                results.append({
                    "label": translate(label, "urban", context=self.request),
                    "date": value.get("date").strftime("%d/%m/%Y"),
                    "user": value.get("user"),
                })
            else:  # old style; before we also stored the user, "value" was the date
                results.append({
                    "label": translate(label, "urban", context=self.request),
                    "date": value.strftime("%d/%m/%Y"),
                    "user": "",
                })
        return results

    index = ViewPageTemplateFile("templates/notice_transmit_state.pt")
