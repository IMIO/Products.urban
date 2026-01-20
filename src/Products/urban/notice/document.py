# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from base64 import b64decode
from plone.namedfile.file import NamedBlobFile


class NoticeDocument(NoticeElement):
    """Class that represent a document from Notice Webservice"""

    _notice_keys = (
        "notice_id",
        "document_id",
        "document_type_code",
        "document_mimetype",
        "filename",
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
    def id(self):
        return self.filename.encode("ascii", errors="ignore")

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
    def filename(self):
        known_extensions = {
            "application/xml": u".xml",
            "application/pdf": u".pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": u".docx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": u".xlsx",
        }
        extension = known_extensions.get(self.document_mimetype)
        return (
            self.title + extension
            if extension
            else self.title
        )

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
                filename=self.filename,
                contentType=self.document_mimetype,
            )
            return _file.open()

    @property
    def document_type_code(self):
        return self.json["documentData"]["type"]["code"]

    @property
    def document_mimetype(self):
        return self.json["documentData"]["mimeType"]
