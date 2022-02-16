# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope import schema

from Products.urban import UrbanMessage as _


class IAllOpenNotifications(Interface):
    """ """
    notifications = schema.Dict(
        title=_(u"All Open NOTICe notifications"),
        description=_(u"key is noticeid, value is a dict with 3 values [notification label, urban reference, licence UID]"),
        key_type=schema.ASCIILine(),
        value_type=schema.Dict(
            key_type=schema.ASCIILine(),
            value_type=schema.ASCIILine()
        )
    )
