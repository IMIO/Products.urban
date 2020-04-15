# -*- coding: utf-8 -*-

from collective.documentgenerator.AT_renderer import DefaultATFieldRenderer


class DateATFieldRenderer(DefaultATFieldRenderer):
    """
    """

    def render_value(self):
        date = self.field.get(self.context)
        display = date.strftime('%d/%m/%Y')

        return display


class ApplicantDefaultFieldRenderer(DefaultATFieldRenderer):
    """
    Return the accessor to be sure we go through the 'same address as works' hooks
    """

    def render(self, no_value=''):
        """
        Compute the rendering of the display value.
        To override for each different type of ATFieldRenderer.
        """
        return self.field.getAccessor(self.context)() or no_value
