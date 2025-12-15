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
        return [
            {
                "label": translate(label, "urban", context=self.REQUEST),
                "date": date.strftime("%d/%m/%Y"),
            }
            for (label, date) in dates.items()
        ]

    index = ViewPageTemplateFile("templates/notice_transmit_state.pt")
