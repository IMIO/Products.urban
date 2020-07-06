# -*- coding: utf-8 -*-

from Products.Five import BrowserView

from plone import api

import base64


class UrbanDoc2PloneMeeting(BrowserView):
    """ """

    def getAnnexes(self):
        plone_utils = api.portal.get_tool("plone_utils")
        documents = self.context.getAttachments()
        documents.extend(self.context.getDocuments())
        annexes = []
        for doc in documents:
            filename = (
                type(doc.getFilename()) is str
                and doc.getFilename().decode("utf-8")
                or doc.getFilename().encode("utf-8")
            )
            annexes.append(
                {
                    "title": plone_utils.normalizeString(doc.title),
                    "filename": plone_utils.normalizeString(filename),
                    "file": base64.b64encode(doc.getFile().data),
                }
            )
        return annexes
