# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import moveElementAfter
from Products.urban.utils import getMd5Signature
import logging
logger = logging.getLogger('urban: setuphandlers')

def loga(msg):
    logger.warn(msg)
    return msg

def updateTemplates(context, container, templates, starting_position=''):
    log = []
    position_after = starting_position
    for template in templates:
        template_id = template['id']
        #in the case of GLOBAL_TEMPLATES, the id already ends with '.odt'
        if not template_id.endswith('.odt'):
            template_id = "%s.odt" % template_id
        filePath = '%s/templates/%s' % (context._profile_path, template_id)
        new_content = file(filePath, 'rb').read()
        log.append(updateTemplate(context, container, template, new_content, position_after))
        #log[-1][0] is the id of the last template added
        position_after = log[-1][0] 
    return log

def updateTemplate(context, container, template, new_content, position_after=''):
    def setProperty(file, property_name, property_value):
        properties = dict(file.propertyItems())
        if property_name in properties.keys():
            file.manage_changeProperties({property_name:property_value})
        else:
            file.manage_addProperty(property_name, property_value, "string")

    new_template_id = template['id']
    #in the case of GLOBAL_TEMPLATES, the id already ends with '.odt'
    if not new_template_id.endswith('.odt'):
        new_template_id = "%s.odt" % new_template_id
    profile_name = context._profile_path.split('/')[-1]
    status = [new_template_id]
    new_md5_signature = getMd5Signature(new_content)
    old_template = getattr(container, new_template_id, None)
    #if theres an existing template with the same id 
    if old_template:
        #check the md5
        #if no difference in the content or not in the good profile, then do nothing
        if (new_md5_signature == old_template.getProperty("md5Signature")) \
        or (profile_name != old_template.getProperty("profileName") != 'tests'):
            status.append('no changes')
            return status
        #else update the template
        else:
            old_template.setFile(new_content)
            new_template = old_template
            status.append('updated')
    #else create a new template
    else:
        new_template_id = container.invokeFactory("File", id=new_template_id, title=template['title'], file=new_content) 
        new_template = getattr(container, new_template_id)
        status.append('created')

    #to do to if we added/updated a new template: the position in the folder and set some properties
    if position_after:
        moveElementAfter(new_template, container, 'id', position_after)
    else:
        container.moveObjectToPosition(new_template.getId(), 0)
    for property, value in {'profileName':profile_name, 'md5Signature':new_md5_signature}.items():
        setProperty(new_template, property, value)
    new_template.reindexObject()
    return status

def updateAllUrbanTemplates(context):
    if context.readDataFile('urban_tests_marker.txt') is None:
        return
    addGlobalTemplates(context)
    addUrbanEventTypes(context)

def addGlobalTemplates(context):
    """
    Helper method to add/update the templates at the root of urban config
    """
    profile_name = context._profile_path.split('/')[-1]
    from_string = "from Products.urban.profiles.%s.data import globalTemplates" % profile_name
    try:
        exec(from_string) in locals()
    except ImportError:
        return

    log = []
    tool = getToolByName(context.getSite(), 'portal_urban')
    templates_folder = getattr(tool, 'globaltemplates')
    template_log = updateTemplates(context, templates_folder, globalTemplates)
    for status in template_log:
        if status[1] != 'no changes':
            log.append(loga("'global templates', template='%s' => %s"%(status[0], status[1])))
    return '\n'.join(log)

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
        exec(from_string) in locals()
    except ImportError:
        return

    log = []
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')
    #add the UrbanEventType
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "urbaneventtypes")
        except AttributeError:
            #if we can not get the urbanConfig, we pass this one...
            log.append(loga("AttributeError while trying to get the '%s' urbanConfig" % urbanConfigId))
            continue
        last_urbaneventype_id = None
        for uet in urbanEventTypes[urbanConfigId]:
            id = uet['id']
            #we pass every informations including the 'id' in the 'uet' dict
            folderEvent=getattr(uetFolder,id,None)
            if folderEvent:
                newUet=folderEvent
            else:
                newUetId = uetFolder.invokeFactory("UrbanEventType", **uet)
                newUet = getattr(uetFolder, newUetId)
                if last_urbaneventype_id:
                    moveElementAfter(newUet, uetFolder, 'id', last_urbaneventype_id)
                else:
                    uetFolder.moveObjectToPosition(newUet.getId(), 0)
                log.append(loga("%s: event='%s' => %s"%(urbanConfigId, id, 'created')))
            last_urbaneventype_id = id
            #add the Files in the UrbanEventType
            template_log = updateTemplates(context, newUet, uet['podTemplates'])
            for status in template_log:
                if status[1] != 'no changes':
                    log.append(loga("%s: evt='%s', template='%s' => %s"%(urbanConfigId, last_urbaneventype_id, status[0], status[1])))
    return '\n'.join(log)
