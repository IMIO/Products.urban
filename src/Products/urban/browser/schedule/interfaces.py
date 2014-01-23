# -*- coding: utf-8 -*-
from zope.interface import Interface


class IScheduleListingTable(Interface):
    """
    Marker interface for schedule display table
    """


class ITimeDelayColumn(Interface):
    """
    Marker interface for a schedule delay Column
    """


class IDelayTerm(Interface):
    """
    Marker interface for a maximum deadline Column
    """
