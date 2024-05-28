# -*- coding: utf-8 -*-

from plone import api
from Products.urban.contentrules import mail_with_attachment
from Products.urban.contentrules.interface import IGetDocumentToAttach
from zope.component import adapter
from zope.interface import Interface, implementer

from .interface import ISendMailAction


@implementer(IGetDocumentToAttach)
@adapter(Interface, Interface, ISendMailAction)
class GetDocumentToAttach(mail_with_attachment.GetDocumentToAttach):
    def __call__(self):
        return [api.content.get(UID=file) for file in getattr(self.event, "files", [])]
