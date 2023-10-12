# -*- coding: utf-8 -*-

from plone import api

from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import getCurrentFolderManager
from Products.urban.schedule.vocabulary import URBAN_TYPES_INTERFACES

from collective.faceted.task.events.task_events import activate_faceted_tasks_listing

from imio.schedule.utils import end_all_open_tasks
from imio.schedule.utils import get_task_configs

from zope.annotation import IAnnotations
from zope.interface import alsoProvides


def setDefaultValuesEvent(licence, event):
    """
    set default values on licence fields
    """
    request = event.object.REQUEST
    if licence.checkCreationFlag():
        if request and request.getURL().endswith("@@masterselect-jsonvalue-toggle"):
            # This is a major performance improvment and default values are not
            # necessary for this view
            return
        else:
            _setDefaultFolderManagers(licence)
            _setDefaultSelectValues(licence)
            _setDefaultTextValues(licence)
            _setDefaultReference(licence)


def _setDefaultSelectValues(licence):
    select_fields = [
        field
        for field in licence.schema.fields()
        if field.default_method == "getDefaultValue"
    ]
    for field in select_fields:
        default_value = licence.getDefaultValue(licence, field)
        if not default_value:
            continue
        field_mutator = getattr(licence, field.mutator)
        field_mutator(default_value)


def _setDefaultTextValues(licence):
    select_fields = [
        field
        for field in licence.schema.fields()
        if field.default_method == "getDefaultText"
    ]
    for field in select_fields:
        is_html = "html" in field.default_content_type
        default_value = licence.getDefaultText(licence, field, is_html)
        if not default_value:
            continue
        field_mutator = getattr(licence, field.mutator)
        field_mutator(default_value)


def _setDefaultFolderManagers(licence):
    default_folder_manager = licence.getLicenceConfig().getDefault_foldermanager()
    if default_folder_manager:
        licence.setFoldermanagers(default_folder_manager)
    else:
        licence.setFoldermanagers(getCurrentFolderManager())


def _setDefaultReference(licence):
    licence.setReference(licence.getDefaultReference())


def postCreationActions(licence, event):
    # set permissions on licence
    # check the numerotation need to be incremented
    _checkNumerotation(licence)
    # update the licence title
    updateLicenceTitle(licence, event)


def updateLicenceTitle(licence, event):
    licence.updateTitle()
    licence.reindexObject(idxs=["Title", "sortable_title"])


def updateTaskIndexes(task_container, event):
    task_configs = get_task_configs(task_container)

    if not task_configs:
        return

    with api.env.adopt_roles(["Manager"]):
        for config in task_configs:
            tasks = config.get_task_instances(task_container)
            for task in tasks:
                task.reindexObject(idxs=["commentators"])


def updateBoundLicences(licence, events):
    """
    If ticket or inspection refers to this licence, update their title and indexes
    as the refered address and aplicants may have changed.
    """
    annotations = IAnnotations(licence)
    ticket_uids = annotations.get("urban.bound_tickets") or set([])
    inspection_uids = annotations.get("urban.bound_inspections") or set([])
    roaddecree_uids = annotations.get("urban.bound_roaddecrees") or set([])
    uids = inspection_uids.union(ticket_uids).union(roaddecree_uids)
    catalog = api.portal.get_tool("portal_catalog")
    bound_licences_brains = catalog(UID=uids)
    for bound_licences_brain in bound_licences_brains:
        bound_licence = bound_licences_brain.getObject()
        bound_licence.updateTitle()
        bound_licence.reindexObject(
            idxs=[
                "Title",
                "sortable_title",
                "applicantInfosIndex",
                "address",
                "StreetNumber",
                "StreetsUID",
                "parcelInfosIndex",
            ]
        )
        # make sure to update  the whole reference chain licence <- inspection <- ticket
        updateBoundLicences(bound_licence, events)


def updateEventsFoldermanager(licence, event):
    events = licence.objectValues("UrbanEvent")
    events += licence.objectValues("UrbanEventOpinionRequest")
    for urban_event in events:
        urban_event.reindexObject(idxs=["folder_manager"])


def _setManagerPermissionOnLicence(licence):
    # there is no need for other users than Managers to List folder contents
    # set this permission here if we use the simple_publication_workflow...
    licence.manage_permission(
        "List folder contents",
        [
            "Manager",
        ],
        acquire=0,
    )


def _checkNumerotation(licence):
    config = licence.getUrbanConfig()
    portal_urban = config.aq_parent
    source_config = getattr(portal_urban, config.getNumerotationSource())
    # increment the numerotation in the tool only if its the one that has been generated
    if config.generateReference(licence) in licence.getReference():
        value = source_config.getNumerotation()
        if not str(value).isdigit():
            value = "0"
        else:
            value = int(value)
            value = value + 1
        # set the new value
        source_config.setNumerotation(value)
        source_config.reindexObject()


def setMarkerInterface(licence, event):
    """ """
    portal_type = licence.portal_type
    marker_interface = URBAN_TYPES_INTERFACES.get(portal_type, None)
    if marker_interface and not marker_interface.providedBy(licence):
        alsoProvides(licence, marker_interface)


def reindex_attachments_permissions(container, event):
    """ """
    if "portal_factory" in container.REQUEST.getURL():
        return
    query = {
        "portal_type": "File",
        "path": {
            "query": "/".join(container.getPhysicalPath()),
            "depth": 1,
        },
    }
    catalog = api.portal.get_tool("portal_catalog")
    attachments = catalog(query)
    with api.env.adopt_roles(["Manager"]):
        for attachment_brain in attachments:
            attachment = attachment_brain.getObject()
            attachment.reindexObject(idxs=["allowedRolesAndUsers"])

    if IUrbanEvent.providedBy(container):
        licence = container.aq_parent
        reindex_attachments_permissions(licence, event)


def reindex_licence_permissions(container, event):
    """
    Reindex licence permissions when triggering internal opinion request events
    """
    if IUrbanEvent.providedBy(container):
        licence = container.aq_parent
        licence.reindexObject(idxs=["allowedRolesAndUsers"])


def set_faceted_navigation(licence, event):
    """
    Activate faceted navigation licences.
    """
    activate_faceted_tasks_listing(licence, event)


def close_all_tasks(licence, event):
    config = licence.getLicenceConfig()
    licence_state = api.content.get_state(licence)
    if licence_state in config.getStates_to_end_all_tasks() or []:
        end_all_open_tasks(licence)
