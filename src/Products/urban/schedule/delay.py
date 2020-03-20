# -*- coding: utf-8 -*-

from imio.schedule.content.delay import BaseCalculationDelay

from Products.urban.interfaces import ICODT_Inquiry
from Products.urban.interfaces import IInquiry

COVID_DELAY = 30


class AnnoncedDelay(BaseCalculationDelay):
    """
    Return the selected annonced delay of the procedure.
    """

    def calculate_delay(self):
        delay = self.task_container.getAnnoncedDelay() or 0
        if delay.endswith('j'):
            delay = int(delay[:-1])
            delay += self.inquiry_suspension_delay()
        if self.task_container.getCovid():
            delay += COVID_DELAY
        return delay

    def inquiry_suspension_delay(self):
        licence = self.task_container
        delay = 0

        if IInquiry.providedBy(licence):
            for inquiry in licence.getAllInquiries():
                inquiry_event = inquiry.getLinkedUrbanEventInquiry()
                ack_event = licence.getLastAcknowledgment()
                if inquiry_event and ack_event and inquiry_event.getInvestigationStart() > ack_event.getEventDate():
                    delay += inquiry.get_suspension_delay()

        if ICODT_Inquiry.providedBy(licence):
            for announcement in licence.getAllAnnouncements():
                announcement_event = announcement.getLinkedUrbanEventInquiry()
                ack_event = licence.getLastAcknowledgment()
                if announcement_event and ack_event and announcement_event.getInvestigationStart() > ack_event.getEventDate():
                    delay += announcement.get_suspension_delay()

        return delay


class UniqueLicenceAnnoncedDelay(AnnoncedDelay):
    """
    Return the selected annonced delay of the procedure -20 if class 2
    or -30 if class 1.
    """

    def calculate_delay(self):
        licence = self.task_container
        raw_delay = licence.getAnnoncedDelay()
        delay = 0
        if raw_delay.endswith('j'):
            delay = int(raw_delay[:-1])
            if 'class_1' in licence.getProcedureChoice():
                delay = delay - 30
            if 'class_2' in licence.getProcedureChoice():
                delay = delay - 20

        delay += self.inquiry_suspension_delay()
        if self.task_container.getCovid():
            delay += COVID_DELAY
        return delay


class UniqueLicenceNotificationDelay(AnnoncedDelay):
    """
    Return 20 if class 2 or 30 if class 1 only if spw licence project
    has been received, else return licence annonced delay.
    """

    def calculate_delay(self):
        licence = self.task_container
        delay = 0
        if licence.getLastDecisionProjectFromSPW():
            if 'class_1' in licence.getProcedureChoice():
                delay = 30
            if 'class_2' in licence.getProcedureChoice():
                delay = 20
        else:
            delay = self.task_container.getAnnoncedDelay()
            if delay.endswith('j'):
                delay = int(delay[:-1])
            else:
                delay = 0
        delay += self.inquiry_suspension_delay()
        if self.task_container.getCovid():
            delay += COVID_DELAY
        return delay
