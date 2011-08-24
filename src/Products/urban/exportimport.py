# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger('urban: setuphandlers')
import hashlib

def addUrbanEventTypes(context):
    """
      Helper method for easily adding urbanEventTypes
    """
    #add some UrbanEventTypes...
    #get the urbanEventTypes dict from the profile
    #get the name of the profile by taking the last part of the _profile_path
    profile_name = context._profile_path.split('/')[-1]
    from_string = "from Products.urban.profiles.%s.data import urbanEventTypes" % profile_name
    try:
        exec(from_string)
    except ImportError:
        return
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
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
                loginfo = 'unknown'
                id = uet['id']
                loginfo = id
                #we pass every informations including the 'id' in the 'uet' dict
                folderEvent=getattr(uetFolder,id,None)
                if folderEvent:
                    newUet=folderEvent
                else:
                    newUetId = uetFolder.invokeFactory("UrbanEventType", **uet)
                    newUet = getattr(uetFolder, newUetId)
                #add the Files in the UrbanEventType
                for template in uet['podTemplates']:
                    id = "%s.odt" % template['id']
                    loginfo = id
                    title = template['title']
                    #read odt template
                    filePath = '%s/templates/%s' % (context._profile_path, id)
                    fileDescr = file(filePath, 'rb')
                    fileContent = fileDescr.read()
                    #calculate the md5 for new template
                    md5 = hashlib.md5(fileContent)
                    md5SignatureFS=md5.digest()
                    fileTemplate=getattr(newUet,id,None)
                    #if file exist, we must verify some conditions before update template
                    if fileTemplate:
                        profileNamePlone=fileTemplate.getProperty("profileName")
                        #don't modify ANY templates if
                        #   1. executing profile is tests and profile in use isn't tests
                        #   2. executing profile is 'xxx' and profile in use is 'yyy'
                        if profileNamePlone!="tests" and (profile_name != profileNamePlone or profile_name == "tests"):
                            break
                        #get the md5 in property of current template
                        md5SignatureProperty=fileTemplate.getProperty("md5Signature")
                        #calculate the md5 for current template
                        md5 = hashlib.md5(fileTemplate.data)
                        md5SignaturePlone=md5.digest()
                        #don't modify THIS template if
                        #   1. current template was manually modified by user
                        #   2. the new template is the same that the current
                        if md5SignaturePlone!=md5SignatureProperty or md5SignatureFS == md5SignaturePlone:
                            continue
                        newUetFile=fileTemplate
                        newUetFile.setFile(fileContent)
                    #if file not exist, we can create template
                    else:
                        newUetFileId = newUet.invokeFactory("File", id=id, title=title, file=fileContent)
                        newUetFile = getattr(newUet, newUetFileId)
                    #modify template's content
                    newUetFile.setContentType("application/vnd.oasis.opendocument.text")
                    newUetFile.setFilename(id)
                    #modify properties
                    dictProperties=dict(newUetFile.propertyItems())
                    if dictProperties.has_key("md5Signature"):
                        newUetFile.manage_changeProperties({"md5Signature":md5SignatureFS})
                    else:
                        newUetFile.manage_addProperty("md5Signature",md5SignatureFS,"string")
                    if dictProperties.has_key("profileName"):
                        newUetFile.manage_changeProperties({"profileName":profile_name})
                    else:
                        newUetFile.manage_addProperty("profileName",profile_name,"string")
                    newUetFile.reindexObject()
            except Exception, msg:
                #there was an error, reinstalling?  reapplying?  we pass...
                logger.warn("An error occured while processing the '%s' UrbanEvent: '%s'" % (loginfo, msg))
                pass
