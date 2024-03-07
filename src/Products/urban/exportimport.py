# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from Products.urban.scripts.odtsearch import SearchPODTemplates
from Products.urban.utils import moveElementAfter
from Products.urban.utils import getMd5Signature

from plone.app.textfield import RichTextValue
from plone.namedfile.file import NamedBlobFile
from plone import api


import StringIO
import csv
import logging

logger = logging.getLogger("urban: setuphandlers")


AVAILABLE_SUBTEMPLATES = {}


def loga(msg, type="info", gslog=None):
    if not gslog:
        gslog = logging.getLogger("urban: setuphandlers")
    if type == "info":
        gslog.info(msg)
    elif type == "warning":
        gslog.warning(msg)
    elif type == "warn":
        gslog.warn(msg)
    return msg


def updateTemplates(
    context, container, templates, starting_position="", new_install=True
):
    log = []
    position_after = starting_position
    for template in templates:
        template_id = template["id"]
        filePath = "%s/templates/%s" % (context._profile_path, template_id)
        new_content = file(filePath, "rb").read()
        log.append(
            updateTemplate(
                context, container, template, new_content, position_after, new_install
            )
        )
        # log[-1][0] is the id of the last template added
        position_after = log[-1][0]
    return log


def updateTemplate(
    context, container, template, new_content, position_after="", new_install=True
):
    def setProperty(file, property_name, property_value):
        if property_name in file.propertyIds():
            file.manage_changeProperties({property_name: property_value})
        else:
            file.manage_addProperty(property_name, property_value, "string")

    template_id = template["id"]
    if type(template_id) is str:
        template_id = template_id.decode("utf-8")
    profile_name = context._profile_path.split("/")[-1]
    status = [template_id]
    new_md5_signature = getMd5Signature(new_content)
    old_template = getattr(container, template_id, None)
    # if theres an existing template with the same id
    if old_template:
        # if not in the correct profile -> no changes
        if profile_name != old_template.getProperty("profileName") != "extra":
            status.append("no changes")
        # if in the correct profile but old template has been customised or has the same content than the new one -> no changes
        elif profile_name == old_template.getProperty("profileName"):
            # Is the template different on the file system
            data = (
                type(old_template.odt_file) in [list, tuple]
                and old_template.odt_file[0].data
                or old_template.odt_file.data
            )
            if getMd5Signature(data) != old_template.getProperty("md5Modified"):
                # We will replace unless the template has been manually modified and we don't force replace
                if getMd5Signature(
                    old_template.odt_file.data
                ) != old_template.getProperty("md5Modified"):
                    status.append("no update: the template has been modified")
            else:
                status.append("no changes")
        if len(status) == 2:
            return status
        # we can update the template
        old_template.odt_file = (
            NamedBlobFile(
                data=new_content,
                filename=template_id,
                contentType="application/vnd.oasis.opendocument.text",
            ),
        )
        new_template = old_template
        status.append("updated")
    # else create a new template
    else:
        portal_type = template.pop("portal_type", "UrbanTemplate")
        if portal_type == "UrbanTemplate":
            template["merge_templates"] = getDefaultSubTemplates(context, template_id)
            template["mailing_loop_template"] = getDefaultMailingLoopTemplate(
                context, template_id
            )

        template_id = container.invokeFactory(
            portal_type,
            odt_file=NamedBlobFile(
                data=new_content,
                filename=template_id,
                contentType="application/vnd.oasis.opendocument.text",
            ),
            **template
        )
        new_template = getattr(container, template_id)
        if not new_install:
            api.content.transition(new_template, "disable")
        status.append("created")

    new_template.setFilename(template_id)
    new_template.setFormat("application/vnd.oasis.opendocument.text")

    # to do to if we added/updated a new template: the position in the folder and set some properties
    if position_after:
        moveElementAfter(new_template, container, "id", position_after)
    else:
        container.moveObjectToPosition(new_template.getId(), 0)
    for property, value in {
        "profileName": profile_name,
        "md5Loaded": new_md5_signature,
        "md5Modified": new_md5_signature,
    }.items():
        setProperty(new_template, property, value)
    # to adapt !!!
    # updateTemplateStylesEvent(new_template, None)
    new_template.reindexObject()
    return status


def getDefaultMailingLoopTemplate(context, template_id):
    globaltemplates = context.getSite().portal_urban.globaltemplates
    folder_name = (
        template_id.startswith("env") and "environmenttemplates" or "urbantemplates"
    )
    mailing_loop_template = getattr(
        getattr(globaltemplates, folder_name), "publipostage.odt"
    )
    return mailing_loop_template.UID()


def getDefaultSubTemplates(context, template_id):
    file_path = "%s/templates/%s" % (context._profile_path, template_id)
    search = SearchPODTemplates("from document\(at=(.*),", [file_path], silent=True)
    search_results = search.run()
    category = template_id.startswith("env") and "env" or "urb"
    available_subtemplates = availableSubTemplates(context)

    footer_template = available_subtemplates[category].get("footer", None)
    subtemplates = (
        footer_template
        and [
            {
                "pod_context_name": "footer",
                "template": footer_template,
                "do_rendering": True,
            }
        ]
        or []
    )
    if search_results:
        search_result = search_results.values()[0]
        for match in search_result[1][0]["matches"]:
            subtemplate_name = match.groups()[0]
            subtemplate = available_subtemplates[category].get(subtemplate_name, None)
            if subtemplate:
                line = {
                    "pod_context_name": subtemplate_name,
                    "template": subtemplate,
                    "do_rendering": True,
                }
                subtemplates.append(line)

    return subtemplates


def availableSubTemplates(context):
    globaltemplates = context.getSite().portal_urban.globaltemplates
    env_subtemplates = globaltemplates.environmenttemplates
    urb_subtemplates = globaltemplates.urbantemplates
    subtemplates = {
        "urb": dict(
            [
                (sub.id.split(".")[0], sub.UID())
                for sub in urb_subtemplates.objectValues()
            ]
        ),
        "env": dict(
            [
                (sub.id.split(".")[0], sub.UID())
                for sub in env_subtemplates.objectValues()
            ]
        ),
    }
    return subtemplates


def updateAllUrbanTemplates(context):
    if context.readDataFile("urban_extra_marker.txt") is None:
        return
    addGlobalTemplates(context)
    addDashboardTemplates(context)
    addEventConfigs(context)


def addGlobalTemplates(context):
    """
    Helper method to add/update the templates at the root of urban config
    """
    profile_name = context._profile_path.split("/")[-1]
    module_name = "Products.urban.profiles.%s.data" % profile_name
    attribute = "globalTemplates"
    module = __import__(module_name, fromlist=[attribute])
    global_templates = getattr(module, attribute)

    site = context.getSite()

    log = []
    gslogger = context.getLogger("addGlobalTemplates")
    tool = getToolByName(site, "portal_urban")
    templates_folder = getattr(tool, "globaltemplates")

    for subfolder_id in ["urbantemplates", "environmenttemplates"]:
        templates_subfolder = getattr(templates_folder, subfolder_id)
        template_log = updateTemplates(
            context, templates_subfolder, global_templates[subfolder_id]
        )
        for status in template_log:
            if status[1] != "no changes":
                log.append(
                    loga(
                        "'%s global templates', template='%s' => %s"
                        % (subfolder_id, status[0], status[1]),
                        gslog=gslogger,
                    )
                )

    template_log = updateTemplates(context, templates_folder, global_templates["."])
    for status in template_log:
        if status[1] != "no changes":
            log.append(
                loga(
                    "'global templates', template='%s' => %s" % (status[0], status[1]),
                    gslog=gslogger,
                )
            )

    return "\n".join(log)


def addDashboardTemplates(context):
    """
    Helper method to add/update dashboard templates at the root of urban config
    """
    profile_name = context._profile_path.split("/")[-1]
    module_name = "Products.urban.profiles.%s.data" % profile_name
    attribute = "dashboardTemplates"
    module = __import__(module_name, fromlist=[attribute])
    dashboard_templates = getattr(module, attribute).copy()

    site = context.getSite()

    log = []
    gslogger = context.getLogger("addDashboardTemplates")
    tool = getToolByName(site, "portal_urban")
    templates_folder = getattr(tool, "dashboardtemplates")

    template_log = updateTemplates(context, templates_folder, dashboard_templates["."])
    for status in template_log:
        if status[1] != "no changes":
            log.append(
                loga(
                    "'dashboard templates', template='%s' => %s"
                    % (status[0], status[1]),
                    gslog=gslogger,
                )
            )

    return "\n".join(log)


def addEventConfigs(context):
    """
    Helper method for easily adding urbanEventTypes
    """
    # do the import on call to be able to monkey patch it in tests
    from Products.urban.config import NIS

    if context.readDataFile("urban_extra_marker.txt") is None:
        return

    site = context.getSite()
    # add some EventConfigs...
    # get the urbanEventTypes dict from the profile
    # get the name of the profile by taking the last part of the _profile_path
    profile_name = context._profile_path.split("/")[-1]
    module_name = "Products.urban.profiles.%s.data" % profile_name
    attribute = "EventConfigs"
    module = __import__(module_name, fromlist=[attribute])
    urbanEventTypes = getattr(module, attribute)
    module_name = "Products.urban.profiles.%s.refnis" % profile_name
    attribute = "REFNIS_2019"
    module = __import__(module_name, fromlist=[attribute])
    refNIS_2019 = getattr(module, attribute)

    log = []
    gslogger = context.getLogger("addEventConfigs")
    tool = getToolByName(site, "portal_urban")
    matched_externalDirection = None
    for refNIS in refNIS_2019:
        if str(refNIS["Code INS"]) == NIS:
            matched_externalDirection = refNIS["Directions extérieures"]
            break
    # add the EventConfig
    for urbanConfigId in urbanEventTypes:
        try:
            uetFolder = getattr(
                tool.getLicenceConfig(None, urbanConfigId=urbanConfigId), "eventconfigs"
            )
        except AttributeError:
            # if we can not get the urbanConfig, we pass this one...
            log.append(
                loga(
                    "AttributeError while trying to get the '%s' urbanConfig"
                    % urbanConfigId,
                    type="warning",
                    gslog=gslogger,
                )
            )
            continue
        last_urbaneventype_id = None
        new_install = len(uetFolder.objectIds()) == 0
        for uet in urbanEventTypes[urbanConfigId]:
            id = uet["id"]
            # we pass every informations including the 'id' in the 'uet' dict
            folderEvent = getattr(uetFolder, id, None)
            if folderEvent:
                newUet = folderEvent
            else:
                portal_type = uet.get("portal_type", "EventConfig")
                if portal_type == "OpinionEventConfig":
                    if not matched_externalDirection:
                        continue
                    else:
                        externalDirections = uet.get("externalDirections", None)
                        if externalDirections:
                            if matched_externalDirection not in externalDirections:
                                continue
                newUetId = uetFolder.invokeFactory(portal_type, **uet)
                newUet = getattr(uetFolder, newUetId)
                if newUet.description == "":
                    newUet.description = RichTextValue("")
                if last_urbaneventype_id:
                    moveElementAfter(newUet, uetFolder, "id", last_urbaneventype_id)
                else:
                    uetFolder.moveObjectToPosition(newUet.getId(), 0)
                if not new_install:
                    api.content.transition(newUet, "disable")
                log.append(
                    loga(
                        "%s: event='%s' => %s" % (urbanConfigId, id, "created"),
                        gslog=gslogger,
                    )
                )
            last_urbaneventype_id = id
            # add the Files in the EventConfig
            template_log = updateTemplates(
                context, newUet, uet["podTemplates"], new_install=new_install
            )
            for status in template_log:
                if status[1] != "no changes":
                    log.append(
                        loga(
                            "%s: evt='%s', template='%s' => %s"
                            % (
                                urbanConfigId,
                                last_urbaneventype_id,
                                status[0],
                                status[1],
                            ),
                            gslog=gslogger,
                        )
                    )
    return "\n".join(log)


def addCustomOpinionEventConfigs(context):
    """
    Helper method for easily adding urbanEventTypes
    """
    if context.readDataFile("urban_extra_marker.txt") is None:
        return
    # add some EventConfigs...
    site = context.getSite()
    opinions_cfg = getattr(site, "opinions_config", None)
    if not opinions_cfg:
        return

    log = []
    gslogger = context.getLogger("addEventConfigs")
    portal_urban = getToolByName(site, "portal_urban")
    header = ["id", "title", "abbreviation", "description"]

    # add the EventConfig
    for licence_cfg in portal_urban.objectValues("LicenceConfig"):
        events_cfg = licence_cfg.eventconfigs
        last_eventcfg_id = "config-opinion-request"
        if not hasattr(events_cfg, last_eventcfg_id):
            continue
        for line in csv.DictReader(
            StringIO.StringIO(opinions_cfg()), fieldnames=header, delimiter=";"
        ):
            opinion_cfg_id = line["id"]
            line["description"] = RichTextValue(line["description"])
            line["title"] = "Demande d'avis {}".format(line["title"])
            line["eventPortalType"] = "UrbanEventOpinionRequest"
            line["eventType"] = ("Products.urban.interfaces.IOpinionRequestEvent",)
            line["activatedFields"] = (
                "transmitDate",
                "receiptDate",
                "receivedDocumentReference",
                "externalDecision",
            )
            line["TALCondition"] = "python: event.mayAddOpinionRequestEvent(here)"
            line["eventDateLabel"] = "Date"

            opinion_cfg = getattr(events_cfg, opinion_cfg_id, None)
            if not opinion_cfg:
                opinion_cfg_id = events_cfg.invokeFactory("OpinionEventConfig", **line)
                opinion_cfg = getattr(events_cfg, opinion_cfg_id)
                if last_eventcfg_id:
                    moveElementAfter(opinion_cfg, events_cfg, "id", last_eventcfg_id)
                else:
                    events_cfg.moveObjectToPosition(opinion_cfg.getId(), 0)
                opinion_cfg.reindexObject()
                log.append(
                    loga(
                        "%s: event='%s' => %s" % (opinion_cfg_id, id, "created"),
                        gslog=gslogger,
                    )
                )
            last_eventcfg_id = opinion_cfg_id
            # add the Files in the EventConfig
    return "\n".join(log)
