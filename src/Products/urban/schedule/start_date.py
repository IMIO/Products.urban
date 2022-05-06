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
        deposit_date = None
        if deposit:
            deposit_date = deposit.getEventDate() or deposit.getReceiptDate()
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


class ComplementsDepositDate(StartDate):
    """
    Returns the missing part event date of the licence.
    """

    def start_date(self):
        licence = self.task_container
        missing_part_deposit = licence.getLastMissingPartDeposit()
        deposit_date = missing_part_deposit and missing_part_deposit.getEventDate() or None
        return deposit_date


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
        receipt_date = None
        if transmit:
            receipt_date = transmit.getReceiptDate() or transmit.getEventDate()
        return receipt_date


class DecisionProjectFromSPWReceiptDate(StartDate):
    """
    Returns the receipt date of the licence project sent by the SPW.
    """

    def start_date(self):
        licence = self.task_container
        receipt = licence.getLastDecisionProjectFromSPW()
        receipt_date = receipt and receipt.getEventDate() or None
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


class AskOpinionDate(StartDate):
    """
    Returns ask date of the opinion request.
    """

    def start_date(self):
        opinion_request = self.task_container
        ask_date = opinion_request.getTransmitDate()

        # case where we just pushed the 'ask_opinion' button but the date has
        # no been set yet.
        if not ask_date:
            for wf_action in opinion_request.workflow_history['opinion_request_workflow']:
                if wf_action['action'] == 'ask_opinion':
                    ask_date = wf_action['time']

        return ask_date


class DecisionProjectFromSPWReceiptDateOrAcknowledgmentDate(StartDate):
    """
    Returns the receipt date of the licence project sent by the SPW
    or the last acknowledgement date if no licence project yet.
    """

    def start_date(self):
        licence = self.task_container
        ack = licence.getLastAcknowledgment()
        ack_date = ack and ack.getEventDate() or None
        receipt = licence.getLastDecisionProjectFromSPW()
        receipt_date = receipt and receipt.getEventDate() or None
        ack = licence.getLastAcknowledgment()
        ack_date = ack and ack.getEventDate() or None
        return receipt_date or ack_date


class TicketSentToProsecutionDate(StartDate):
    """
    Returns the date of the TheTicket event.
    """

    def start_date(self):
        licence = self.task_container
        deposit = licence.getLastTheTicket()
        deposit_date = deposit and deposit.getEventDate() or None
        return deposit_date


class FollowupEventDate(StartDate):
    """
    Returns the date of the TheTicket event.
    """

    def start_date(self):
        licence = self.task_container
        followup = licence.getLastFollowUpEventWithDelay()
        followup_date = followup and followup.getEventDate() or None
        return followup_date
