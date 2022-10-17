# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class Unlock(BrowserView):
    """
    Unlock contents.
    """

    def __call__(self):
        for obj in self.context.objectValues():
            if obj.wl_isLocked():
                obj.wl_clearLocks()
