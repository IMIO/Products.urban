# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import moveElementAfter
from Products.urban.utils import getMd5Signature
from Products.urban.events.filesEvents import updateTemplateStylesEvent
import logging
logger = logging.getLogger('urban: setuphandlers')

def loga(msg, type="info", gslog=None):
    if not gslog:
        gslog = logging.getLogger('urban: setuphandlers')
    if type=="info":
        gslog.info(msg)
    elif type=="warn":
        gslog.warn(msg)
    return msg

def updateTemplates(context, container, templates, starting_position='', replace=False):
    log = []
    position_after = starting_position
    for template in templates:
        template_id = template['id']
        #in the case of GLOBAL_TEMPLATES, the id already ends with '.odt'
        if not template_id.endswith('.odt'):
            template_id = "%s.odt" % template_id
        filePath = '%s/templates/%s' % (context._profile_path, template_id)
        new_content = file(filePath, 'rb').read()
        log.append(updateTemplate(context, container, template, new_content, position_after, replace=replace))
        #log[-1][0] is the id of the last template added
        position_after = log[-1][0] 
    return log

def updateTemplate(context, container, template, new_content, position_after='', replace=False):
    def setProperty(file, property_name, property_value):
        if property_name in file.propertyIds():
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
        #if not in the correct profile -> no changes
        if profile_name != old_template.getProperty("profileName") != 'tests':
            status.append('no changes')
        #if in the correct profile but old template has been customised or has the same content than the new one -> no changes
        elif profile_name == old_template.getProperty("profileName"):
            # has the template in the product evolved ?
            if new_md5_signature == old_template.getProperty("md5Loaded"):
                status.append('no changes')
            # the template must be updated. Has the template manually evolved in the tool ?
            elif not replace and getMd5Signature(old_template.data) != old_template.getProperty("md5Modified"):
                status.append('no update: the template has been modified')
        if len(status) == 2:
            return status
        # we can update the template
        old_template.setFile(new_content)
        new_template = old_template
        status.append('updated')
    #else create a new template
    else:
        new_template_id = container.invokeFactory("File", id=new_template_id, title=template['title'], file=new_content) 
        new_template = getattr(container, new_template_id)
        new_template.setFormat("application/vnd.oasis.opendocument.text")
        status.append('created')

    #to do to if we added/updated a new template: the position in the folder and set some properties
    if position_after:
        moveElementAfter(new_template, container, 'id', position_after)
    else:
        container.moveObjectToPosition(new_template.getId(), 0)
    for property, value in {'profileName':profile_name, 'md5Loaded':new_md5_signature, 'md5Modified':new_md5_signature}.items():
        setProperty(new_template, property, value)
    updateTemplateStylesEvent(new_template, None)
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

    replace_globals = False
    site = context.getSite()
    # we check if the step is called by the external method urban_replace_templates, with the param replace_globals
    if site.REQUEST.form.has_key('replace_globals'):
        replace_globals = True

    log = []
    gslogger = context.getLogger('addGlobalTemplates')
    tool = getToolByName(site, 'portal_urban')
    templates_folder = getattr(tool, 'globaltemplates')
    template_log = updateTemplates(context, templates_folder, globalTemplates, replace=replace_globals)
    for status in template_log:
        if status[1] != 'no changes':
            log.append(loga("'global templates', template='%s' => %s"%(status[0], status[1]), gslog=gslogger))
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

    replace_events = False
    site = context.getSite()
    # we check if the step is called by the external method urban_replace_templates, with the param replace_events
    if site.REQUEST.form.has_key('replace_events'):
        replace_events = True

    log = []
    gslogger = context.getLogger('addUrbanEventTypes')
    tool = getToolByName(site, 'portal_urban')
    #add the UrbanEventType
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "urbaneventtypes")
        except AttributeError:
            #if we can not get the urbanConfig, we pass this one...
            log.append(loga("AttributeError while trying to get the '%s' urbanConfig" % urbanConfigId, type="warn", gslog=gslogger))
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
                log.append(loga("%s: event='%s' => %s"%(urbanConfigId, id, 'created'), gslog=gslogger))
            last_urbaneventype_id = id
            #add the Files in the UrbanEventType
            template_log = updateTemplates(context, newUet, uet['podTemplates'], replace=replace_events)
            for status in template_log:
                if status[1] != 'no changes':
                    log.append(loga("%s: evt='%s', template='%s' => %s"%(urbanConfigId, last_urbaneventype_id, status[0], status[1]), gslog=gslogger))
    return '\n'.join(log)
