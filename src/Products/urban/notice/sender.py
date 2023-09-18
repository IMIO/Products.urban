# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement


class NoticeSender(NoticeElement):
    def __init__(self, service, json):
        self.service = service
        self.json = json

    @property
    def name1(self):
        return self._get_data("contactName")

    @property
    def email(self):
        return self._get_data("contactMail", "email", "_value_1")

    @property
    def phone(self):
        return self._get_data("contactPhone", "phoneNumber", "_valuel_1")
