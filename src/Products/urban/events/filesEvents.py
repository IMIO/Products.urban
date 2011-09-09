# -*- coding: utf-8 -*-
import appy.pod
from appy.shared.utils import FolderDeleter, executeCommand
import os,time
from StringIO import StringIO
from Products.urban.utils import getOsTempFolder
from Products.CMFCore.utils import getToolByName

CONVSCRIPT = '%s/converter.py' %os.path.dirname(appy.pod.__file__)

def updateAllTemplatesStylesEvent(object, event):
    """
        Event activated by the modification of the configuration of urban
    """    
    if object.REQUEST.form.has_key('templateStyles_file'):
        #template style is modify, update all template with style.
        templateStylesFileName = createTemporayTemplateStyle(object)
        if templateStylesFileName:
            eventTypes = object.buildlicence.urbaneventtypes
            for uet in eventTypes.objectValues():
                for fileTemplate in uet.objectValues():
                    updateTemplateStyle(object,fileTemplate,templateStylesFileName)
            #delete temporary styles files
            os.remove(templateStylesFileName)
    return

def updateTemplateStylesEvent(object, event):
    """
        Event activated by adding an ATFile
    """
    if object.REQUEST.form.has_key('file_file') and object.aq_inner.aq_parent.Type() == 'UrbanEventType':
        tool = getToolByName(object, 'portal_urban')
        #template style is modify, update all template with style.
        templateStylesFileName = createTemporayTemplateStyle(tool)
        if templateStylesFileName:
            updateTemplateStyle(tool,object,templateStylesFileName)
            #delete temporary styles files
            os.remove(templateStylesFileName)
    return

def createTemporayTemplateStyle(object):
    """
        create Temporary file from template style
    """
    templateStyles = object.getTemplateStyles()
    if templateStyles and templateStyles.size:
        #save in temporary file, the templateStyles
        templateStylesFileName = '%s/%s_%f.%s' % (getOsTempFolder(), 'templateStyles', time.time(),'odt')
        newTemplateStyles = file(templateStylesFileName,"w" )
        newTemplateStyles.write(StringIO(templateStyles).read())
        newTemplateStyles.close()
        return templateStylesFileName
    return ''

def updateTemplateStyle(tool,fileTemplate,templateStylesFileName):
    """
        update template fileTemplate by templateStyle
    """    
    #save in temporary file, the template
    tempFileName = '%s/%s_%f.%s' % (getOsTempFolder(), fileTemplate._at_uid, time.time(),'odt')
    newTemplate = file(tempFileName,"w" )
    newTemplate.write(StringIO(fileTemplate).read())
    newTemplate.close()
    #merge style from templateStyle in template    
    cmd = '%s %s %s %s -p%d -t%s' % \
        (tool.getUnoEnabledPython(), CONVSCRIPT, tempFileName, 'odt',
            2002, templateStylesFileName)
    ooOutput = executeCommand(cmd)
    #read the merged file
    resTempFileName = tempFileName[:-3]+'res.odt'
    if os.path.isfile(resTempFileName):
        resTemplate = open(resTempFileName,'rb')
        #update template
        fileName = fileTemplate.id
        fileTemplate.setFile(resTemplate)
        fileTemplate.setContentType("application/vnd.oasis.opendocument.text")
        fileTemplate.setFilename(fileName)
        #delete temporary result files
        os.remove(resTempFileName)
    #delete temporary files
    os.remove(tempFileName)
