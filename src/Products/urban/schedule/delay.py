# -*- coding: utf-8 -*-

from imio.schedule.content.delay import BaseCalculationDelay


class AnnoncedDelay(BaseCalculationDelay):
    """
    Return the slected annonced delay of the procedure.
    """

    def calculate_delay(self):
        delay = self.task_container.getAnnoncedDelay()
        if delay.endswith('j'):
            return int(delay[:-1])
        return 0


class UniqueLicenceAnnoncedDelay(BaseCalculationDelay):
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

        return delay


class UniqueLicenceNotificationDelay(BaseCalculationDelay):
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
        return delay
