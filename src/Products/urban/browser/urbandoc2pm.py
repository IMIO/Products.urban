# -*- coding: utf-8 -*-

from Products.Five import BrowserView

import base64


class UrbanDoc2PloneMeeting(BrowserView):
    """
    """
    def getAnnexes(self):
        documents = self.context.getAttachments()
        documents.extend(self.context.getDocuments())
        annexes = []
        for doc in documents:
            annexes.append(
                {
                    'title': doc.title.encode('utf-8'),
                    'filename': doc.getFilename().encode('utf-8'),
                    'file': base64.b64encode(doc.getFile().data),
                }
            )
        return annexes
