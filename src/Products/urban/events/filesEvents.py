# -*- coding: utf-8 -*-
import appy.pod
from appy.shared.utils import executeCommand
import os, time
from StringIO import StringIO
from Products.urban.utils import getOsTempFolder
from Products.urban.utils import getMd5Signature
from Products.urban.config import URBAN_TYPES
from Products.CMFCore.utils import getToolByName
import logging

logger = logging.getLogger('urban: filesEvents')

CONVSCRIPT = '%s/converter.py' % os.path.dirname(appy.pod.__file__)

def updateAllTemplatesStylesEvent(object, event):
    """
        Event activated by the modification of the configuration of urban
    """
    if object.absolute_url_path().endswith('/portal_urban/globaltemplates/styles.odt'):
        tool = getToolByName(object, 'portal_urban')
        #template style is modify, update all template with style.
        templateStylesFileName = _createTemporayTemplateStyle(tool, object)
        if templateStylesFileName:
            for licence_type in URBAN_TYPES:
                urbanEventTypesFolder = getattr(tool, licence_type.lower()).urbaneventtypes
                numberOfUrbanEventTypes = len(urbanEventTypesFolder.objectValues('UrbanEventType'))
                logger.info("%d event types to update." % numberOfUrbanEventTypes)
                #we want a list to be able to call .index here above
                urbanEventTypes = list(urbanEventTypesFolder.objectValues('UrbanEventType'))
                for uet in urbanEventTypes:
                    logger.info("Updating UrbanEventType %d/%d : %s" % (urbanEventTypes.index(uet) + 1, numberOfUrbanEventTypes, uet.Title()))
                    for fileTemplate in uet.objectValues('ATBlob'):
                        _updateTemplateStyle(tool, fileTemplate, templateStylesFileName)
                        logger.info(" %s => updated" % fileTemplate.Title())
            #delete temporary styles files
            os.remove(templateStylesFileName)
    return

def updateTemplateStylesEvent(object, event):
    """
        Event activated by adding an ATFile
    """
    #we update the File if it is a template contained in an UrbanEventType actually
    #and we check if there is something to update
    if object.aq_inner.aq_parent.Type() == 'UrbanEventType':
        tool = getToolByName(object, 'portal_urban')
        #template style is modify, update all template with style.
        styles = getattr(getattr(tool, 'globaltemplates'), 'styles.odt')
        templateStylesFileName = _createTemporayTemplateStyle(tool, styles)
        if templateStylesFileName:
            _updateTemplateStyle(tool, object, templateStylesFileName)
            #delete temporary styles files
            os.remove(templateStylesFileName)
    return

def _createTemporayTemplateStyle(tool, templateStyles):
    """
        create Temporary file from template style
    """
    if templateStyles and templateStyles.size:
        #save in temporary file, the templateStyles
        templateStylesFileName = '%s/%s_%f.%s' % (getOsTempFolder(), 'templateStyles', time.time(),'odt')
        newTemplateStyles = file(templateStylesFileName,"w" )
        newTemplateStyles.write(StringIO(templateStyles).read())
        newTemplateStyles.close()
        return templateStylesFileName
    return ''

def _updateTemplateStyle(tool, fileTemplate, templateStylesFileName):
    """
        update template fileTemplate by templateStyle
    """
    style_changes_only = 'md5Modified' in fileTemplate.propertyIds() and \
                         getMd5Signature(fileTemplate.data) == fileTemplate.getProperty('md5Modified')
    #save in temporary file, the template
    tempFileName = '%s/%s_%f.%s' % (getOsTempFolder(), fileTemplate._at_uid, time.time(),'odt')
    newTemplate = file(tempFileName,"w" )
    newTemplate.write(StringIO(fileTemplate).read())
    newTemplate.close()
    #merge style from templateStyle in template
    cmd = '%s %s %s %s -p%d -t%s' % \
        (tool.getUnoEnabledPython(), CONVSCRIPT, tempFileName, 'odt',
            tool.getOpenOfficePort(), templateStylesFileName)
    executeCommand(cmd)
    #read the merged file
    resTempFileName = tempFileName[:-3]+'res.odt'
    if os.path.isfile(resTempFileName):
        resTemplate = open(resTempFileName,'rb')
        #update template
        fileName = fileTemplate.id
        fileTemplate.setFile(resTemplate)
        fileTemplate.setContentType("application/vnd.oasis.opendocument.text")
        fileTemplate.setFilename(fileName)
        #if it was a template model and that only styles were modified: update the md5styles property
        if style_changes_only:
            fileTemplate.manage_changeProperties({'md5Modified':getMd5Signature(fileTemplate.data)})
        #delete temporary result files
        os.remove(resTempFileName)
    #delete temporary files
    os.remove(tempFileName)
