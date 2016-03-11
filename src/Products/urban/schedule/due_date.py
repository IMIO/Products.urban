# -*- coding: utf-8 -*-

from urban.schedule.content.logic import StartDate


class DepositDate(StartDate):
    """
    Returns the deposit date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        deposit = licence.getLastDeposit()
        deposit_date = deposit and deposit.getEventDate() or licence.creation_date
        return deposit_date


class AcknowledgementDate(StartDate):
    """
    Returns the deposit date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        ack = licence.getLastAcknowledgment()
        ack_date = ack and ack.getEventDate() or None
        return ack_date


class InquriryEndDate(StartDate):
    """
    Returns the inquiry end date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        end_date = licence.getInvestigationEnd()
        return end_date
