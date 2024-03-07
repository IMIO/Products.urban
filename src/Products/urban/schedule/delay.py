# -*- coding: utf-8 -*-

from imio.schedule.content.delay import BaseCalculationDelay
from imio.schedule.content.delay import DefaultFreezeDuration

from plone import api

from Products.urban.interfaces import ICODT_Inquiry
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IInquiry
from Products.urban.schedule.interfaces import ITaskWithSuspensionDelay
from Products.urban.schedule.interfaces import ITaskWithWholeSuspensionDelay


class UrbanBaseDelay(BaseCalculationDelay):
    """ """

    def calculate_delay(self):
        task = self.task
        is_licence = IGenericLicence.providedBy(self.task_container)
        if not is_licence:
            return 0

        licence = self.task_container
        marked_suspension_1 = ITaskWithSuspensionDelay.providedBy(task)
        marked_suspension_2 = ITaskWithWholeSuspensionDelay.providedBy(task)
        if not licence.getCovid() or (
            not marked_suspension_1 and not marked_suspension_2
        ):
            return 0

        suspension_start = api.portal.get_registry_record(
            "Products.urban.interfaces.IGlobalSuspensionPeriod.start_date"
        )
        suspension_end = api.portal.get_registry_record(
            "Products.urban.interfaces.IGlobalSuspensionPeriod.end_date"
        )
        suspension_period = suspension_end - suspension_start

        start_date = self.start_date
        if start_date < suspension_start:
            return suspension_period.days

        elif start_date < suspension_end:
            if ITaskWithWholeSuspensionDelay.providedBy(task):
                return suspension_period.days
            else:
                suspension_prorata = suspension_end - start_date
                return suspension_prorata.days
        return 0


class AnnoncedDelay(UrbanBaseDelay):
    """
    Return the selected annonced delay of the procedure.
    """

    def calculate_delay(self, with_modified_blueprints=True):
        base_delay = super(AnnoncedDelay, self).calculate_delay()
        licence = self.task_container
        delay = licence.getAnnoncedDelay() or 0
        if hasattr(licence, "decisional_delay"):
            delay = licence.getDecisional_delay()
        if with_modified_blueprints and licence.getHasModifiedBlueprints():
            delay = licence.getDelayAfterModifiedBlueprints() or 0
        if delay and delay.endswith("j"):
            delay = int(delay[:-1])
            delay += self.inquiry_suspension_delay()
        return delay + base_delay

    def inquiry_suspension_delay(self):
        licence = self.task_container
        delay = 0

        if IInquiry.providedBy(licence):
            for inquiry in licence.getAllInquiries():
                inquiry_event = inquiry.getLinkedUrbanEventInquiry()
                ack_event = licence.getLastAcknowledgment()
                if (
                    inquiry_event
                    and ack_event
                    and inquiry_event.getInvestigationStart() > ack_event.getEventDate()
                ):
                    delay += inquiry.get_suspension_delay()

        if ICODT_Inquiry.providedBy(licence):
            for announcement in licence.getAllAnnouncements():
                announcement_event = announcement.getLinkedUrbanEventInquiry()
                ack_event = licence.getLastAcknowledgment()
                if (
                    announcement_event
                    and ack_event
                    and announcement_event.getInvestigationStart()
                    > ack_event.getEventDate()
                ):
                    delay += announcement.get_suspension_delay()

        return delay


class UniqueLicenceAnnoncedDelay(AnnoncedDelay):
    """
    Return the selected annonced delay of the procedure -20 if class 2
    or -30 if class 1.
    """

    def calculate_delay(self, with_modified_blueprints=True):
        licence = self.task_container
        delay = super(UniqueLicenceAnnoncedDelay, self).calculate_delay(
            with_modified_blueprints
        )
        if type(delay) in [str, unicode] and delay.endswith("j"):
            delay = int(delay[:-1])
        if "class_1" in licence.getProcedureChoice():
            delay = delay - 30
        if "class_2" in licence.getProcedureChoice():
            delay = delay - 20

        delay += self.inquiry_suspension_delay()
        return delay


class UniqueLicenceNotificationDelay(AnnoncedDelay):
    """
    Return 20 if class 2 or 30 if class 1 only if spw licence project
    has been received, else return licence annonced delay.
    """

    def calculate_delay(self, with_modified_blueprints=True):
        licence = self.task_container
        delay = super(UniqueLicenceNotificationDelay, self).calculate_delay(
            with_modified_blueprints
        )
        if licence.getLastDecisionProjectFromSPW():
            if "class_1" in licence.getProcedureChoice():
                delay = 30
            if "class_2" in licence.getProcedureChoice():
                delay = 20
        else:
            delay = self.task_container.getAnnoncedDelay()
            if type(delay) in [str, unicode] and delay.endswith("j"):
                delay = int(delay[:-1])
            elif not delay:
                delay = 0
        delay += self.inquiry_suspension_delay()
        return delay


class InspectionFollowUpDelay(AnnoncedDelay):
    """
    Return the delay on the linked report of the followup with delay
    """

    def calculate_delay(self):
        licence = self.task_container
        followup = licence.getLastFollowUpEventWithDelay()
        report = followup.getLinkedReport()
        delay = report.getDelay() and int(report.getDelay()) or 0
        return delay


class CouncildecisionDelay(UrbanBaseDelay):
    """
    Return the selected council decision delay of the RoadDecree.
    """

    def calculate_delay(self, with_modified_blueprints=True):
        base_delay = super(AnnoncedDelay, self).calculate_delay()
        licence = self.task_container
        delay = licence.getDecisional_delay() or 0
        if delay and delay.endswith("j"):
            delay = int(delay[:-1])
        return delay + base_delay


class UrbanFreezeDuration(DefaultFreezeDuration):
    """ """

    def __init__(self, task_container, task):
        self.container = task_container
        self.task = task

    @property
    def freeze_duration(self):
        licence = self.container
        new_freeze_duration = 0
        for suspension_event in licence.getAllSuspensionEvents():
            start = suspension_event.getEventDate()
            end = suspension_event.getSuspensionEndDate()
            if start and end:
                new_freeze_duration += int(end - start)

        if new_freeze_duration:
            return new_freeze_duration
        return super(UrbanFreezeDuration, self).freeze_duration
