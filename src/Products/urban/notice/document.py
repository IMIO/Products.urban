# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from plone.namedfile.file import NamedBlobFile
from base64 import b64decode


class NoticeDocument(NoticeElement):
    """Class that represent a document from Notice Webservice"""

    _notice_keys = (
        "notice_id",
        "document_id",
    )
    _excluded_keys = ("document",)

    def __init__(self, service, json, notice_id):
        self.service = service
        self.json = json
        self.notice_id = notice_id

    @property
    def type(self):
        """Return the portal type"""
        return "File"

    @property
    def title(self):
        return self.json["documentData"]["filename"]

    @property
    def description(self):
        return self.json["documentData"]["description"]

    @property
    def document_id(self):
        return self.json["documentData"]["documentId"]

    @property
    def document(self):
        """Get document data from WS"""
        if not hasattr(self, "_document"):
            self._document = self.service.get_notification_document(
                self.notice_id, self.document_id
            )
        return self._document

    @property
    def file(self):
        if self.document:
            _file = NamedBlobFile(
                data=self.document,
                filename=self.title.decode("utf8"),
                contentType=self.json["documentData"]["mimeType"],
            )
            return _file.open()

    @property
    def document_type_code(self):
        return self.json["documentData"]["type"]["code"]

    @property
    def document_mimetype(self):
        return self.json["documentData"]["mimeType"]
