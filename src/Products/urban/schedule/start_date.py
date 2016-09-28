# -*- coding: utf-8 -*-

from imio.schedule.content.logic import StartDate


class CreationDate(StartDate):
    """
    Returns the deposit date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        return licence.creation_date


class DepositDate(StartDate):
    """
    Returns the deposit date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        deposit = licence.getLastDeposit()
        deposit_date = deposit and deposit.getEventDate() or None
        return deposit_date


class AskComplementsDate(StartDate):
    """
    Returns the missing part event date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        missing_part = licence.getLastMissingPart()
        ask_complements_date = missing_part and missing_part.getEventDate() or None
        return ask_complements_date


class AcknowledgmentDate(StartDate):
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
        inquiry = licence.getLastInquiry()
        end_date = inquiry.getInvestigationEnd()
        return end_date
