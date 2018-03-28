# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from plone import api

import base64


class UrbanDoc2PloneMeeting(BrowserView):
    """
    """
    def getAnnexes(self):
        plone_utils = api.portal.get_tool('plone_utils')
        documents = self.context.getAttachments()
        documents.extend(self.context.getDocuments())
        annexes = []
        for doc in documents:
            annexes.append(
                {
                    'title': plone_utils.normalizeString(doc.title),
                    'filename': plone_utils.normalizeString(doc.getFilename().decode('utf-8')),
                    'file': base64.b64encode(doc.getFile().data),
                }
            )
        return annexes
