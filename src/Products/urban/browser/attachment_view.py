# -*- coding: utf-8 -*-

from Products.Five import BrowserView


class AttachmentView(BrowserView):
    """
    File attachment custom View.
    """

    def __call__(self):
        return self.request.response.redirect(
            self.context.aq_parent.absolute_url() + "#fieldsetlegend-attachments"
        )
