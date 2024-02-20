# -*- coding: utf-8 -*-
#
# File: wfsubscribers.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"


##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from datetime import datetime

##/code-section module-header


def afterAccept(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if (
        not event.transition
        or event.transition.id not in ["accept"]
        or obj != event.object
    ):
        return
    ##code-section afterAccept #fill in your manual code here
    closeEveryUrbanEvents(obj)
    ##/code-section afterAccept


def afterRetire(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if (
        not event.transition
        or event.transition.id not in ["retire"]
        or obj != event.object
    ):
        return
    ##code-section afterRetire #fill in your manual code here
    closeEveryUrbanEvents(obj)
    ##/code-section afterRetire


def afterIncomplete(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if (
        not event.transition
        or event.transition.id not in ["isincomplete"]
        or obj != event.object
    ):
        return
    ##code-section afterIncomplete #fill in your manual code here
    closeEveryUrbanEvents(obj)
    ##/code-section afterIncomplete


def afterRefuse(obj, event):
    """generated workflow subscriber."""
    # do only change the code section inside this function.
    if (
        not event.transition
        or event.transition.id not in ["refuse"]
        or obj != event.object
    ):
        return
    ##code-section afterRefuse #fill in your manual code here
    closeEveryUrbanEvents(obj)
    ##/code-section afterRefuse


def closeEveryUrbanEvents(obj):
    """
    This look for every UrbanEvents and close them if they are not
    """
    wft = getToolByName(obj, "portal_workflow")
    urbanEvents = obj.getUrbanEvents()
    for urbanEvent in urbanEvents:
        if wft.getInfoFor(urbanEvent, "review_state") == "in_progress":
            wft.doActionFor(urbanEvent, "close")
