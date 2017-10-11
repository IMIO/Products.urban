# -*- coding: utf-8 -*-

from collective.documentgenerator.AT_renderer import DefaultATFieldRenderer


class DateATFieldRenderer(DefaultATFieldRenderer):
    """
    """

    def render_value(self):
        date = self.field.get(self.context)
        display = date.strftime('%d/%m/%Y')

        return display
