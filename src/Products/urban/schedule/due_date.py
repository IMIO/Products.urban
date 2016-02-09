# -*- coding: utf-8 -*-

from urban.schedule.content.due_date import DueDate


class DepositDate(DueDate):
    """
    DueDate returning the deposit date of the licence.
    """

    def due_date(self, **kwargs):
        licence = self.task_container
        deposit = licence.getLastDeposit()
        deposit_date = deposit and deposit.getEventDate() or licence.creation_date
        return deposit_date
