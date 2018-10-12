# -*- coding: utf-8 -*-

from imio.schedule.content.delay import BaseCalculationDelay


class AnnoncedDelay(BaseCalculationDelay):
    """
    Return the selected annonced delay of the procedure.
    """

    def calculate_delay(self):
        licence = self.task_container
        delay = licence.getAnnoncedDelay()
        if licence.getHasModifiedBlueprints():
            delay = licence.getDelayAfterModifiedBlueprints()
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
        if licence.getHasModifiedBlueprints():
            raw_delay = licence.getDelayAfterModifiedBlueprints()
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
    Return 20 if class 2 or 30 if class 1.
    """

    def calculate_delay(self):
        licence = self.task_container
        delay = 0
        if 'class_1' in licence.getProcedureChoice():
            delay = 30
        if 'class_2' in licence.getProcedureChoice():
            delay = 20

        return delay
