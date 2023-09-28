# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement


class NoticeRubric(NoticeElement):
    def __init__(self, service, json):
        self.service = service
        self.json = json

    @property
    def classe(self):
        """Rubric class"""
        return self._get_data("ns4:classe", "code")

    @property
    def code(self):
        """Rubric code"""
        return self._get_data("ns4:code")

    @property
    def title(self):
        """Rubric title"""
        return self._get_data("ns4:completeLabel")