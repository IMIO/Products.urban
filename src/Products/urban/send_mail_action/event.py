# -*- coding: utf-8 -*-

from zope.component.interfaces import ObjectEvent
from .interface import ISendMailAction
from zope.interface import implements

class SendMailAction(ObjectEvent):

    implements(ISendMailAction)

    def __init__(self, object, files):
        self.files = files
        ObjectEvent.__init__(self, object)
