# -*- coding: utf-8 -*-

from .interface import ISendMailAction
from zope.component.interfaces import ObjectEvent
from zope.interface import implements


class SendMailAction(ObjectEvent):

    implements(ISendMailAction)

    def __init__(self, object, files):
        self.files = files
        ObjectEvent.__init__(self, object)
