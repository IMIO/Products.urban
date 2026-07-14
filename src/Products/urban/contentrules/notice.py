# -*- coding: utf-8 -*-

from Products.CMFCore.interfaces import IContentish
from Products.urban import UrbanMessage as _
from plone.app.contentrules.handlers import execute_rules
from plone.stringinterp.adapters import BaseSubstitution
from zope.component import adapter
from zope.component.interfaces import IObjectEvent
from zope.component.interfaces import ObjectEvent
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implements


class INoticeImportEvent(IObjectEvent):
    """Interface for NOTICe notification event"""


class INoticeImportSucceededEvent(INoticeImportEvent):
    """Interface for event when a NOTICe notification was successfully imported"""


class INoticeImportFailedEvent(INoticeImportEvent):
    """Interface for event when a NOTICe notification has failed to import"""


class INoticeResponseFailedEvent(INoticeImportEvent):
    """Interface for event when a response to a NOTICe notification has failed"""


class NoticeImportSucceededEvent(ObjectEvent):
    implements(INoticeImportSucceededEvent)


class NoticeImportFailedEvent(ObjectEvent):
    implements(INoticeImportFailedEvent)


class NoticeResponseFailedEvent(ObjectEvent):
    implements(INoticeResponseFailedEvent)


def notice_import(event):
    execute_rules(event)


@adapter(IContentish)
class NoticeIdSubstitution(BaseSubstitution):

    category = _(u"NOTICe")
    description = _(u"NOTICe ID")

    def safe_call(self):
        return getattr(self.wrapper, "notice_id", "")


@adapter(IContentish)
class NoticeTypeSubstitution(BaseSubstitution):

    category = _(u"NOTICe")
    description = _(u"NOTICe Type")

    def safe_call(self):
        return getattr(self.wrapper, "notice_type", "")


@adapter(IContentish)
class NoticeErrorSubstitution(BaseSubstitution):

    category = _(u"NOTICe")
    description = _(u"NOTICe Error")

    def safe_call(self):
        return getattr(self.wrapper, "notice_error", "")
