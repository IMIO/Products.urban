# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations


class NoticeTransmitState(ViewletBase):
    """This viewlet displays the state of information sent to NOTICe."""

    def get_transmits(self):
        annotations = IAnnotations(self.context)
        dates = annotations.get("notice_transmit_dates", {})
        return [{"label": label, "date": date.strftime("%d/%m/%Y")} for (label, date) in dates.items()]

    index = ViewPageTemplateFile("templates/notice_transmit_state.pt")
