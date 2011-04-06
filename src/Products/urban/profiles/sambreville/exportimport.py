# -*- coding: utf-8 -*-
#
# File: setuphandlers.py
#
# Copyright (c) 2009 by CommunesPlone
# Generator: ArchGenXML Version 2.4.1
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>"""
__docformat__ = 'plaintext'

import logging
logger = logging.getLogger('urban: sambreville profile')
from DateTime import DateTime

def isNoturbanSambrevilleProfile(context):
    return context.readDataFile("urban_sambreville_marker.txt") is None

def addDefaultObjects(context):
    """
       Add some users and objects for the profile...
    """
    if isNoturbanSambrevilleProfile(context): return

    #add some users, some architects and some foldermanagers...
    #add 2 users, one as reader and one as editor...
    site = context.getSite()
    try:
        site.portal_registration.addMember(id="urbanreader", password="urbanreader")
        site.portal_registration.addMember(id="urbaneditor", password="urbaneditor")
        #put users in the correct group
        site.acl_users.source_groups.addPrincipalToGroup("urbanreader", "urban_readers")
        site.acl_users.source_groups.addPrincipalToGroup("urbaneditor", "urban_editors")
    except:
        #if something wrong happens (one object already exists), we pass...
        pass

    #add some folder managers...
    try:
        tool = site.portal_urban
        fmFolder = getattr(tool.getUrbanConfig(None, urbanConfigId="buildlicence"), "foldermanagers")
        fmFolder.invokeFactory("FolderManager",id="brunowouters",name1="Wouters", name2="Bruno")
        fmFolder.invokeFactory("FolderManager",id="bothychristophe",name1="Bothy", name2="Christophe")
        fmFolder.invokeFactory("FolderManager",id="lienbenedicte",name1="Lien", name2="Bénédicte")
        fmFolder.invokeFactory("FolderManager",id="paquaydeborah",name1="Paquay", name2="Déborah")
    except:
        #if something wrong happens (one object already exists), we pass...
        pass

    #add some UrbanEventTypes...
    tool = site.portal_urban
    #get the uebanEventTypes dict from the profile
    #get the name of the profile by taking the last part of the _profile_path
    profile_name = context._profile_path.split('/')[-1]
    from_string = "from Products.urban.profiles.%s import urbanEventTypes" % profile_name
    try:
        exec(from_string)
    except ImportError:
        logger.warning("Could not exec '%s'" % from_string)
        return
    #add the UrbanEventType
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "urbaneventtypes")
        except AttributeError:
            #if we can not get the urbanConfig, we pass this one...
            logger.warn("An error occured while trying to get the '%s' urbanConfig" % urbanConfigId)
            continue
        for uet in urbanEventTypes[urbanConfigId]:
            try:
                id = uet.pop('id')
                newUetId = uetFolder.invokeFactory("UrbanEventType", id=id, **uet)
                newUet = getattr(uetFolder, newUetId)
                #add the Files in the UrbanEventType
                for template in uet['podTemplates']:
                    id = "%s.odt" % template['id']
                    title = template['title']
                    filePath = '%s/templates/%s' % (context._profile_path, id)
                    fileDescr = file(filePath, 'rb')
                    fileContent = fileDescr.read()
                    newUetFileId = newUet.invokeFactory("File", id=id, title=title, file=fileContent)
                    newUetFile = getattr(newUet, newUetFileId)
                    newUetFile.setContentType("application/vnd.oasis.opendocument.text")
                    newUetFile.reindexObject()
            except:
                #there was an error, reinstalling?  reapplying?  we pass...
                pass

def importNotaries(context):
    """
      Import notaries from the Informix application file export
    """
    importNewType(context, destination='notaries', newType='Notary', default_personTitle='master')

def importArchitects(context):
    """
      Import notaries from the Informix application file export
    """
    importNewType(context, destination='architects', newType='Architect', default_personTitle='')

def importGeometricians(context):
    """
      Import geometricians from the Informix application file export
    """
    importNewType(context, destination='geometricians', newType='Geometrician', default_personTitle='')

def importNewType(context, destination='notaries', newType='Notary', default_personTitle='master'):
    """
      Reimport existing elements from the Informix application file export
    """
    if isNoturbanSambrevilleProfile(context): return
 
    site = context.getSite()
    separator=';'
    destinationFolder = getattr(site.urban, destination)
    #open the destination'.txt' file in the current profile
    file = open(context._profile_path + '/%s.txt' % destination, 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    #get the folder where we are going the create the notaries in
    for line in file.readlines():
        print "Importing %s %d of %d" % (newType, i, numberOfRecords)
        elements = line.strip().split(separator)
        elementslen = len(elements)
        if elementslen == 5:
            oldserial, label, newTypeStreetCode, addresshousenumber, box = elements
        elif elementslen == 4:
            oldserial, label, newTypeStreetCode, addresshousenumber, box = elements + ['', ]
        elif elementslen == 3:
            oldserial, label, newTypeStreetCode, addresshousenumber, box = elements + ['', '', ]
        label = unicode(label, 'latin1')

        newTypeId = site.plone_utils.normalizeString(label)
        if not hasattr(destinationFolder, newTypeId):
            if box:
                addresshousenumber = "%s (%s)" % (addresshousenumber, box)
            dict = {
                    'personTitle': default_personTitle,
                    'name1': label,
                    'name2': '',
                    'society': '',
                    'number': addresshousenumber,
                    'email': '',
                    'phone': '',
                    'fax': '',
                    'nationalRegister': '',
                   }
            #if the newType still does not exist, we create it
            #get informations about the street
            if newTypeStreetCode > 999 and newTypeStreetCode < 7181:
                #this is a street on Sambreville
                streetFileName = "/sambreville_streets.txt"
            else:
                streetFileName = "/outside_streets.txt"
            #look for the street informations in the file
            streetFile = open(context._profile_path + streetFileName, 'r')
            for line in streetFile.readlines():
                streetCode, streetName, city, zipCode, country = line.strip().split(separator)
                if newTypeStreetCode == streetCode:
                    #we found the right street
                    streetName = unicode(streetName, 'latin1')
                    city = unicode(city, 'latin1')
                    country = unicode(country, 'latin1')
                    #add the country name id necessary
                    if not country in ['Belgique', 'belgique',]:
                        city = "%s (%s)" % (city, country)
                    dict['street'] = streetName
                    dict['zipcode'] = zipCode
                    dict['city'] = city
            newTypeObjId = destinationFolder.invokeFactory(newType, id=newTypeId, **dict)
            newTypeObj = getattr(destinationFolder, newTypeObjId)
            #keep the Informix serial so we can link elements to this newType
            newTypeObj.manage_addProperty('old_informix_serial', oldserial, 'string')
            newTypeObj.reindexObject()
        i = i+1
    file.close()

def importSambrevilleStreets(context):
    """
      Import Sambreville streets from the Informix application
    """
    if isNoturbanSambrevilleProfile(context): return

    site = context.getSite()
    separator=';'
    streetsFolder = getattr(site.portal_urban, 'streets')
    #open the 'sambreville_streets.txt' file in the current profile
    file = open(context._profile_path + '/sambreville_streets.txt', 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    #get the folder where we are going the create the streets in
    streetsFolder = getattr(site.portal_urban, 'streets')
    for line in file.readlines():
        print "Importing street %d of %d" % (i, numberOfRecords)
        streetCode, streetName, city, zipCode, country = line.strip().split(separator)
        streetName = unicode(streetName, 'latin1')
        city = unicode(city, 'latin1')
        country = unicode(country, 'latin1')
        streetId = site.plone_utils.normalizeString("%s-%s" % (streetCode, streetName))
        #check if we need to create the City
        cityId = site.plone_utils.normalizeString(city)
        if not hasattr(streetsFolder, cityId):
            #create the city
            cityFolderId = streetsFolder.invokeFactory('City', id=cityId, title=city, zipCode=zipCode)
            cityFolder = getattr(streetsFolder, cityId)
            cityFolder.reindexObject()
        else:
            cityFolder = getattr(streetsFolder, cityId)

        if not hasattr(cityFolder, streetId):
            #if the street still does not exist, we create it
            streetObjId = cityFolder.invokeFactory('Street', id=streetId, streetName=streetName, streetCode=streetCode)
            streetObj = getattr(cityFolder, streetObjId)
            streetObj.reindexObject()
        i = i+1
    file.close()

def importPcas(context):
    """
      Import existing Pcas
    """
    if isNoturbanSambrevilleProfile(context): return

    site = context.getSite()
    separator=';'
    streetsFolder = getattr(site.portal_urban, 'pcas')
    #open the 'parcellings.txt' file in the current profile
    file = open(context._profile_path + '/pcas.txt', 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    #get the folder where we are going the create the streets in
    pcasFolder = getattr(site.portal_urban, 'pcas')
    for line in file.readlines():
        print "Importing PCA %d of %d" % (i, numberOfRecords)
        oldserial, number, label, decreeDate, decreeType = line.strip().split(separator)
        label = unicode(label, 'latin1')
        number = unicode(number, 'latin1')
        pcaId = site.plone_utils.normalizeString(label)
        j = 1
        tmpPcaId = pcaId
        while hasattr(pcasFolder, tmpPcaId):
            tmpPcaId = ("%s-%d" % (pcaId, j))
            j = j + 1
        pcaId = tmpPcaId
        #create the PCA
        if decreeType.lower() == 'r':
            decreeType = 'royal'
        else:
            decreeType = 'departmental'
        decreeDate = DateTime(decreeDate.replace('-', '/'), datefmt='international')
        pcaObjId = pcasFolder.invokeFactory('PcaTerm', id=pcaId, label=label, number=number, decreeDate=decreeDate, decreeType=decreeType)
        pcaObj = getattr(pcasFolder, pcaObjId)
        #keep the Informix serial so we can link elements to this newType
        pcaObj.manage_addProperty('old_informix_serial', oldserial, 'string')
        pcaObj.at_post_create_script()
        i = i+1
    file.close()
