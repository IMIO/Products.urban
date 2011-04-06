# -*- coding: utf-8 -*-
#
# File: taskable.py
#
# Copyright (c) 2010 by CommunesPlone
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'
from zope.interface import implements
import interfaces

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Products.urban.config import *

interfacesToImplement = []

if HAS_PLONETASK:
    from Products.PloneTask.interfaces import ITask
    from Products.PloneTask.utils import getCustomAdapter
    interfacesToImplement = [ITask,]

class Taskable:
    """
      This class manage PloneTask integration
    """
    implements(interfacesToImplement)
    security = ClassSecurityInfo()

    security.declarePublic('getBeginDate')
    def getBeginDate(self):
        """
          Return the beginDate of the Licence
        """
        #try to get the beginDate of the UrbanEvent that start the Licence
        try:
            urbanevent = getattr(self, "depot-de-la-demande")
            return urbanevent.getBeginDate()
        except AttributeError:
            #if we can not get it, we return the CreationDate
            return DateTime(self.CreationDate())

    security.declarePublic('getEndDate')
    def getEndDate(self):
        """
          Return the endDate of the Licence
        """
        try:
            delay = self.getAnnoncedDelay()
        except:
            delay = 15
        if delay and str(delay).isdigit():
            return self.getBeginDate() + delay
        else:
            return self.getBeginDate()

    security.declarePublic('getDatesString')
    def getDatesString(self):
        """
          Produces a string representation of begin and end date for sorting purposes
        """
        return str(self.getBeginDate()) + '-' + str(self.getEndDate())

    security.declarePublic('adapted')
    def adapted(self):
        """
          Gets the "adapted" version of myself. If no custom adapter is found, this methods returns me
        """
        return getCustomAdapter(self, isTask=True)

    security.declarePublic('getPerformer')
    def getPerformer(self):
        """
          Return the performer of the task
        """
        return self.getFoldermanagers().getName1()

    security.declarePublic('isClosedAt')
    def isClosedAt(self, date):
        '''Check if a task is closed at the exact given date...
           p_date is DateTime or a list of 2 dates (interval)'''
        #check if the current state is "closed" for "UrbanEvent" or "accepted" for other portal_types
        portal_type = self.portal_type
        if (self.portal_type == 'UrbanEvent' and self.portal_workflow.getInfoFor(self, 'review_state') == "closed") or self.portal_workflow.getInfoFor(self, 'review_state') == "accepted":
            #get the date in the wf history the task was done
            wfHistory = self.getWorkflowHistory()
            if wfHistory:
                closeDate = wfHistory[0]['time']
                #either we received a date...
                if isinstance(date, DateTime):
                    if closeDate.strftime('%Y/%m/%d') == date.strftime('%Y/%m/%d'):
                        return closeDate, 'accept.png'
                else:
                    #or we receive a date interval in a list of 2 dates
                    fromDate = date[0]
                    toDate = date[1]
                    if (closeDate > fromDate and closeDate < toDate):
                        return closeDate, 'accept.png'
        return False, False
