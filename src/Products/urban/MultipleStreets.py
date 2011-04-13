# -*- coding: utf-8 -*-
#
# File: Contact.py
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

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

class MultipleStreets:
    """
      This class manage multiple streets behaviour
    """
    security = ClassSecurityInfo()

    security.declarePublic('updateWorkLocation')
    def updateWorkLocation(self):
        """
           Update the primary workLocation informations
           We are working with UID of object here
        """
        #take extra values from the edit form passed in the REQUEST and manage them
        if not self.REQUEST.has_key('workLocationStreet', '') or \
           not self.REQUEST.has_key('workLocationNumber', ''):
               #in case we are just calling this method from at_post_edit_script for example
               #without necessary values in the request, we do nothing...
               return
        #we received the workLocationStreet and the workLocationNumber
        workLocationStreetUID = self.REQUEST.get('workLocationStreet', '')
        workLocationNumber = self.REQUEST.get('workLocationNumber', '')
        #we get the existing primary street if exists...
        primaryWorkLocation = self.getPrimaryWorkLocation(theuid=False)
        primaryWorkLocationStreetUID = primaryWorkLocationNumber = ''
        if primaryWorkLocation:
            primaryWorkLocationStreetUID = primaryWorkLocation.UID()
            primaryWorkLocationNumber = primaryWorkLocation.getNumber()
        #update if :
        #we removed an existing primary street
        #we modified an existing primary street
        #we added an existing primary street
        if (not workLocationStreetUID and primaryWorkLocationStreetUID) or \
            not workLocationStreetUID == primaryWorkLocationStreetUID or \
            not workLocationNumber == primaryWorkLocationNumber:
            #remove the primary workLocation in self if necessary
            #get the existing primary workLocation for removal...
            if primaryWorkLocationStreetUID:
                primaryWorkLocationStreetObj = self.uid_catalog(UID=primaryWorkLocationStreetUID)[0].getObject()
                self.manage_delObjects(primaryWorkLocationStreetObj.getId())
                #check if we need to add another one
                if not workLocationStreetUID:
                    return

            #then add the primary
            workLocationStreetObj = self.uid_catalog(UID=workLocationStreetUID)[0].getObject()
            normalizedNumber = self.plone_utils.normalizeString(workLocationNumber)
            id = "%s-%s" % (workLocationStreetObj.getId(), normalizedNumber)
            i = 1
            while id in self.objectIds():
                id = "%s-%d" % (id, i)
                i = i + 1
            data = {
                    'street': workLocationStreetObj,
                    'number': workLocationNumber,
                    'isSupplementary': False,
                    }
            newId = self.invokeFactory("WorkLocation", id=id, **data)
            obj = getattr(self, newId)
            obj.at_post_create_script()

    security.declarePublic('getWorkLocations')
    def getWorkLocations(self, theuid=False):
        """
           Return existing WorkLocation for self
        """
        res = []
        for workLocation in self.objectValues('WorkLocation'):
            if theuid:
                res.append(workLocation.UID())
            else:
                res.append(workLocation)
        return res

    security.declarePublic('getPrimaryWorkLocation')
    def getPrimaryWorkLocation(self, theuid=False):
        """
           Return the primary workLocation if exists
        """
        for workLocation in self.objectValues('WorkLocation'):
            if not workLocation.getIsSupplementary():
                if theuid:
                    return workLocation.UID()
                else:
                    return workLocation
        return ''

    security.declarePublic('getSupplementaryWorkLocations')
    def getSupplementaryWorkLocations(self, theuid=False):
        """
           Return the supplementary workLocations if exist
        """
        res = []
        for workLocation in self.objectValues('WorkLocation'):
            if workLocation.getIsSupplementary():
                if theuid:
                    res.append(workLocation.UID())
                else:
                    res.append(workLocation)
        return res

    security.declarePublic('getWorkLocationStreet')
    def getWorkLocationStreet(self):
        """
          Return the street name
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().getStreetName()
        return ''

    security.declarePublic('getWorkLocationStreetCode')
    def getWorkLocationStreetCode(self):
        """
          Return the street name
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().getStreetCode()
        return ''

    security.declarePublic('getWorkLocationHouseNumber')
    def getWorkLocationHouseNumber(self):
        """
          Return the street name
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getNumber()
        return ''

    security.declarePublic('getWorkLocationZipCode')
    def getWorkLocationZipCode(self):
        """
          Return the zip code
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().aq_inner.aq_parent.getZipCode()
        return ''

    security.declarePublic('getWorkLocationCity')
    def getWorkLocationCity(self):
        """
          Return the city of the primary WorkLocation
          We take the Street defined in the WorkLocation and the
          parent of this street is the City
        """
        primary = self.getPrimaryWorkLocation()
        if primary:
            return primary.getStreet().aq_inner.aq_parent.Title()
        return ''

    security.declarePublic('getWorkLocationInfos')
    def getWorkLocationInfos(self, only_primary=False):
        """
          Return informations about the address
        """
        if only_primary:
            #we only want the primary work location details
            return "%s, %s %s %s" % (self.getWorkLocationHouseNumber(), self.getWorkLocationStreet(), self.getWorkLocationZipCode(), self.getWorkLocationCity())
        else:
            #we want a string representing every selected work locations
            infos = ''
            for wl in getWorkLocations():
                if infos:
                    infos = infos + ' ' + _("urban", 'and') + ' '
                infos = infos + "%s, %s %s %s" % (self.getWorkLocationHouseNumber(), self.getWorkLocationStreet(), self.getWorkLocationZipCode(), self.getWorkLocationCity())
