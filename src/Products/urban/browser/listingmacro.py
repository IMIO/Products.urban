## -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.CMFPlone.PloneBatch import Batch


class ListingMacro(BrowserView):
    """
      This manage the urban listing macro
    """
