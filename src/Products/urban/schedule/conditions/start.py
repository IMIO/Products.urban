# -*- coding: utf-8 -*-

from imio.schedule.content.condition import StartCondition


class LicenceStartCondition(StartCondition):
    """
    Test start condition.
    """

    def evaluate(self):
        return True
