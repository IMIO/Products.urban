# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement


class NoticeParty(NoticeElement):
    def __init__(self, service, json):
        self.service = service
        self.json = json

    @property
    def type(self):
        if self.legalForm:
            return "Corporation"
        return "Applicant"

    @property
    def title(self):
        if self.legalForm:
            return self.denomination
        return u" ".join(filter(None, [self.personTitle, self.name1, self.name2]))

    @property
    def bceNumber(self):
        return self._get_data("enterpriseNumber")

    @property
    def enterprise_type(self):
        return self._get_data("enterpriseType")

    @property
    def legalForm(self):
        return self._get_data("legalForm")

    @property
    def denomination(self):
        return self._get_data("denomination")

    @property
    def personTitle(self):
        return self._get_data("title")

    @property
    def name1(self):
        return self._get_data("lastname")

    @property
    def name2(self):
        return self._get_data("firstname")

    @property
    def nationalRegister(self):
        return self._get_data("personNumber")

    @property
    def _mailing_address(self):
        return self._get_data("mailingAddresses", "mailingAddress")

    @property
    def street(self):
        mailing_address = self._mailing_address
        if mailing_address:
            return mailing_address[0]["street"]

    @property
    def number(self):
        mailing_address = self._mailing_address
        if mailing_address:
            return mailing_address[0]["houseNumber"]

    @property
    def city(self):
        mailing_address = self._mailing_address
        if mailing_address:
            return mailing_address[0]["municipality"]

    @property
    def zipcode(self):
        mailing_address = self._mailing_address
        if mailing_address:
            return mailing_address[0]["postCode"]

    @property
    def country(self):
        mapping = {
            "BE": "belgium",
            "FR": "france",
            "LU": "luxembourg",
            "DE": "germany",
            "NL": "netherlands",
        }
        mailing_address = self._mailing_address
        if mailing_address:
            return mapping.get(mailing_address[0]["country"])

    @property
    def phone(self):
        return self._get_data("phoneNumber", "phoneNumber", "_value_1")

    @property
    def email(self):
        return self._get_data("email", "email", "_value_1")