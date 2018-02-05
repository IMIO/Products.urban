# -*- coding: utf-8 -*-

from imio.schedule.content.logic import StartDate


class InfiniteDate(StartDate):
    """
    Returns inifinite start date.
    """

    def start_date(self):
        return None


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


class AcknowledgmentTransmitDate(StartDate):
    """
    Returns the deposit date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        ack = licence.getLastAcknowledgment()
        ack_transmit_date = ack and ack.getTransmitDate() or None
        return ack_transmit_date


class InquriryEndDate(StartDate):
    """
    Returns the inquiry end date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        inquiry = licence.getLastInquiry(use_catalog=False)
        end_date = inquiry and inquiry.getInvestigationEnd() or None
        return end_date


class AnnouncementEndDate(StartDate):
    """
    Returns the announcement  end date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        announcement = licence.getLastAnnouncement()
        end_date = announcement and announcement.getInvestigationEnd() or None
        return end_date


class SPWReceiptDate(StartDate):
    """
    Returns the date of the licence receipt to the SPW.
    """

    def start_date(self):
        licence = self.task_container
        transmit = licence.getLastTransmitToSPW()
        receipt_date = transmit and transmit.getReceiptDate() or None
        return receipt_date


class WalloonRegionDecisionDate(StartDate):
    """
    Returns the receipt date of the licence project sent by the SPW.
    """

    def start_date(self):
        licence = self.task_container
        receipt = licence.getLastWalloonRegionDecisionEvent()
        receipt_date = receipt and receipt.getEventDate() or None
        return receipt_date
