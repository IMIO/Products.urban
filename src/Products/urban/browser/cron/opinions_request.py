# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class CheckOpinionsRequest(BrowserView):
    """
    Browser view to call with cron to automatically
    close all the outdated opinions request.
    """

    def __call__(self):
        """ """
