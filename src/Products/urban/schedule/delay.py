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
