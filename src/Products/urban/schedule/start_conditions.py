# -*- coding: utf-8 -*-

from urban.schedule.content.condition import StartCondition


class LicenceStartCondition(StartCondition):
    """
    Test start condition.
    """

    def evaluate(self, **kwargs):
        return True
