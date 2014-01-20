# -*- coding: utf-8 -*-
from Products.urban.browser.table.interfaces import IUrbanTable

from zope.interface import Interface


class IScheduleListingTable(IUrbanTable):
    """
    Marker interface for schedule display table
    """


class ITimeDelayColumn(Interface):
    """
    Marker interface for a schedule delay Column
    """
