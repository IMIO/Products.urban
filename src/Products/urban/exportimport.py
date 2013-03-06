# -*- coding: utf-8 -*-
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.GenericSetup.utils import XMLAdapterBase

from Products.urban.interfaces import IUrbanTool

from Products.CMFCore.utils import getToolByName
from Products.urban.utils import moveElementAfter
from Products.urban.utils import getMd5Signature
from Products.urban.events.filesEvents import updateTemplateStylesEvent
import logging
logger = logging.getLogger('urban: setuphandlers')


class UrbanToolXMLAdapter(XMLAdapterBase):

    __used_for__ = IUrbanTool

    _LOGGER_ID = 'portal_urban'

    name = 'portal_urban'

    boolean_fields = ['isDecentralized', 'generateSingletonDocuments']
    integer_fields = ['openOfficePort']
    string_fields = [
        'NISNum',
        'cityName',
        'sqlHost',
        'sqlName',
        'sqlUser',
        'sqlPassword',
        'webServerHost',
        'pylonsHost',
        'mapExtent',
        'unoEnabledPython',
        'editionOutputFormat',
    ]

    def _exportNode(self):
        """Export the object as a DOM node"""

        node = self._extractProperties()
        self._logger.info('Urban tool exported.')

        return node

    def _importNode(self, node):
        """Import the object from the DOM node"""

        if self.environ.shouldPurge():
            self._purgeProperties()

        self._initProperties(node)

        self._logger.info('Urban tool imported.')

    def _purgeProperties(self):
        self.context.supported_langs = ['en']

    def _initProperties(self, node):
        for child in node.childNodes:
            if child.nodeName in self.boolean_fields:
                value = self._convertToBoolean(child.getAttribute('value'))
                setattr(self.context, child.nodeName, value)
            elif child.nodeName in self.integer_fields:
                value = int(child.getAttribute('value'))
                setattr(self.context, child.nodeName, value)
            elif child.nodeName in self.string_fields:
                value = child.getAttribute('value')
                setattr(self.context, child.nodeName, value)

    def _extractProperties(self):
        node = self._doc.createElement('object')

        for field in self.boolean_fields:
            child = self._doc.createElement(field)
            child.setAttribute('value', str(bool(getattr(self.context, field))))
            node.appendChild(child)

        for field in self.integer_fields:
            child = self._doc.createElement(field)
            child.setAttribute('value', str(getattr(self.context, field)))
            node.appendChild(child)

        for field in self.string_fields:
            child = self._doc.createElement(field)
            child.setAttribute('value', getattr(self.context, field))
            node.appendChild(child)

        return node


def importUrbanTool(context):
    """Import Urban tool settings from an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban')

    importObjects(tool, '', context)


def exportUrbanTool(context):
    """Export Urban tool settings as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_urban', None)
    if tool is None:
        logger = context.getLogger('portal_urban')
        logger.info('Nothing to export.')
        return

    exportObjects(tool, '', context)


def loga(msg, type="info", gslog=None):
    if not gslog:
        gslog = logging.getLogger('urban: setuphandlers')
    if type == "info":
        gslog.info(msg)
    elif type == "warning":
        gslog.warning(msg)
    elif type == "warn":
        gslog.warn(msg)
    return msg


def updateTemplates(context, container, templates, starting_position='', reload=False, replace_mod=False):
    log = []
    position_after = starting_position
    for template in templates:
        template_id = template['id']
        #in the case of GLOBAL_TEMPLATES, the id already ends with '.odt'
        if not template_id.endswith('.odt'):
            template_id = "%s.odt" % template_id
        filePath = '%s/templates/%s' % (context._profile_path, template_id)
        new_content = file(filePath, 'rb').read()
        log.append(updateTemplate(context, container, template, new_content, position_after, reload=reload, replace_mod=replace_mod))
        #log[-1][0] is the id of the last template added
        position_after = log[-1][0]
    return log


def updateTemplate(context, container, template, new_content, position_after='', reload=False, replace_mod=False):
    def setProperty(file, property_name, property_value):
        if property_name in file.propertyIds():
            file.manage_changeProperties({property_name: property_value})
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
            # Is the template different on the file system
            if new_md5_signature != old_template.getProperty("md5Loaded"):
                # We will replace unless the template has been manually modified and we don't force replace
                if not replace_mod and getMd5Signature(old_template.data) != old_template.getProperty("md5Modified"):
                    status.append('no update: the template has been modified')
            # No change on the file system. Forcing ?
            elif reload:
                # We will replace unless the template has been manually modified and we don't force replace
                if not replace_mod and getMd5Signature(old_template.data) != old_template.getProperty("md5Modified"):
                    status.append('no update: the template has been modified')
            else:
                status.append('no changes')
        if len(status) == 2:
            return status
        # we can update the template
        old_template.setFile(new_content)
        new_template = old_template
        status.append('updated')
    #else create a new template
    else:
        new_template_id = container.invokeFactory("UrbanDoc", id=new_template_id, title=template['title'], file=new_content,
                                                  TALCondition=('TALCondition' in template) and template['TALCondition'] or '')
        new_template = getattr(container, new_template_id)
        status.append('created')

    new_template.setFilename(new_template_id)
    new_template.setFormat("application/vnd.oasis.opendocument.text")

    #to do to if we added/updated a new template: the position in the folder and set some properties
    if position_after:
        moveElementAfter(new_template, container, 'id', position_after)
    else:
        container.moveObjectToPosition(new_template.getId(), 0)
    for property, value in {'profileName': profile_name, 'md5Loaded': new_md5_signature, 'md5Modified': new_md5_signature}.items():
        setProperty(new_template, property, value)
    updateTemplateStylesEvent(new_template, None)
    new_template.reindexObject()
    return status


def updateAllUrbanTemplates(context):
    if context.readDataFile('urban_extra_marker.txt') is None:
        return
    addGlobalTemplates(context)
    addUrbanEventTypes(context)


def addGlobalTemplates(context):
    """
    Helper method to add/update the templates at the root of urban config
    """
    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.data' % profile_name
    attribute = 'globalTemplates'
    module = __import__(module_name, fromlist=[attribute])
    globalTemplates = getattr(module, attribute)

    reload_globals = False
    replace_mod_globals = False
    site = context.getSite()
    # we check if the step is called by the external method urban_replace_templates, with the param replace_globals
    if 'reload_globals' in site.REQUEST.form:
        reload_globals = True
    if 'replace_mod_globals' in site.REQUEST.form:
        replace_mod_globals = True

    log = []
    gslogger = context.getLogger('addGlobalTemplates')
    tool = getToolByName(site, 'portal_urban')
    templates_folder = getattr(tool, 'globaltemplates')
    template_log = updateTemplates(context, templates_folder, globalTemplates, replace_mod=replace_mod_globals, reload=reload_globals)
    for status in template_log:
        if status[1] != 'no changes':
            log.append(loga("'global templates', template='%s' => %s" % (status[0], status[1]), gslog=gslogger))
    return '\n'.join(log)


def addUrbanEventTypes(context):
    """
      Helper method for easily adding urbanEventTypes
    """
    #add some UrbanEventTypes...
    #get the urbanEventTypes dict from the profile
    #get the name of the profile by taking the last part of the _profile_path
    profile_name = context._profile_path.split('/')[-1]
    module_name = 'Products.urban.profiles.%s.data' % profile_name
    attribute = 'urbanEventTypes'
    module = __import__(module_name, fromlist=[attribute])
    urbanEventTypes = getattr(module, attribute)

    reload_events = False
    replace_mod_events = False
    site = context.getSite()
    # we check if the step is called by the external method urban_replace_templates, with the param replace_events
    if 'reload_events' in site.REQUEST.form:
        reload_events = True
    if 'replace_mod_events' in site.REQUEST.form:
        replace_mod_events = True

    log = []
    gslogger = context.getLogger('addUrbanEventTypes')
    tool = getToolByName(site, 'portal_urban')
    #add the UrbanEventType
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(tool.getUrbanConfig(None, urbanConfigId=urbanConfigId), "urbaneventtypes")
        except AttributeError:
            #if we can not get the urbanConfig, we pass this one...
            log.append(loga("AttributeError while trying to get the '%s' urbanConfig" % urbanConfigId, type="warning", gslog=gslogger))
            continue
        last_urbaneventype_id = None
        for uet in urbanEventTypes[urbanConfigId]:
            id = uet['id']
            #we pass every informations including the 'id' in the 'uet' dict
            folderEvent = getattr(uetFolder, id, None)
            if folderEvent:
                newUet = folderEvent
            else:
                newUetId = uetFolder.invokeFactory("UrbanEventType", **uet)
                newUet = getattr(uetFolder, newUetId)
                if last_urbaneventype_id:
                    moveElementAfter(newUet, uetFolder, 'id', last_urbaneventype_id)
                else:
                    uetFolder.moveObjectToPosition(newUet.getId(), 0)
                log.append(loga("%s: event='%s' => %s" % (urbanConfigId, id, 'created'), gslog=gslogger))
            last_urbaneventype_id = id
            #add the Files in the UrbanEventType
            template_log = updateTemplates(context, newUet, uet['podTemplates'], replace_mod=replace_mod_events, reload=reload_events)
            for status in template_log:
                if status[1] != 'no changes':
                    log.append(loga("%s: evt='%s', template='%s' => %s" % (urbanConfigId, last_urbaneventype_id, status[0], status[1]), gslog=gslogger))
    return '\n'.join(log)
