# -*- coding: utf-8 -*-

from .interface import ISendMailAction
from Products.urban.contentrules import mail_with_attachment
from Products.urban.contentrules.interface import IGetDocumentToAttach
from plone import api
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IGetDocumentToAttach)
@adapter(Interface, Interface, ISendMailAction)
class GetDocumentToAttach(mail_with_attachment.GetDocumentToAttach):
    def __call__(self):
        return [
            api.content.get(path=file.encode("utf-8"))
            for file in getattr(self.event, "files", [])
        ]
