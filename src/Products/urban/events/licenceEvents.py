# -*- coding: utf-8 -*-

from Products.urban.utils import getCurrentFolderManager
from Products.urban.schedule.vocabulary import URBAN_TYPES_INTERFACES

from zope.interface import alsoProvides


def setDefaultValuesEvent(licence, event):
    """
     set default values on licence fields
    """
    if licence.checkCreationFlag():
        _setDefaultFolderManagers(licence)
        _setDefaultSelectValues(licence)
        _setDefaultTextValues(licence)


def _setDefaultSelectValues(licence):
    select_fields = [field for field in licence.schema.fields() if field.default_method == 'getDefaultValue']
    for field in select_fields:
        default_value = licence.getDefaultValue(licence, field)
        field_mutator = getattr(licence, field.mutator)
        field_mutator(default_value)


def _setDefaultTextValues(licence):
    select_fields = [field for field in licence.schema.fields() if field.default_method == 'getDefaultText']
    for field in select_fields:
        is_html = 'html' in field.default_content_type
        default_value = licence.getDefaultText(licence, field, is_html)
        field_mutator = getattr(licence, field.mutator)
        field_mutator(default_value)


def _setDefaultFolderManagers(licence):
    licence.setFoldermanagers(getCurrentFolderManager())


def postCreationActions(licence, event):
    # set permissions on licence
    _setManagerPermissionOnLicence(licence)
    # check the numerotation need to be incremented
    _checkNumerotation(licence)
    # update the licence title
    updateLicenceTitle(licence, event)


def updateLicenceTitle(licence, event):
    licence.updateTitle()
    licence.reindexObject()


def updateEventsFoldermanager(licence, event):
    events = licence.objectValues('UrbanEvent')
    events += licence.objectValues('UrbanEventOpinionRequest')
    for urban_event in events:
        urban_event.reindexObject(idxs=['folder_manager'])


def _setManagerPermissionOnLicence(licence):
    #there is no need for other users than Managers to List folder contents
    #set this permission here if we use the simple_publication_workflow...
    licence.manage_permission('List folder contents', ['Manager', ], acquire=0)


def _checkNumerotation(licence):
    config = licence.getUrbanConfig()
    portal_urban = config.aq_parent
    source_config = getattr(portal_urban, config.getNumerotationSource())
    #increment the numerotation in the tool only if its the one that has been generated
    if config.generateReference(licence) == licence.getReference():
        value = source_config.getNumerotation()
        if not str(value).isdigit():
            value = '0'
        else:
            value = int(value)
            value = value + 1
        #set the new value
        source_config.setNumerotation(value)
        source_config.reindexObject()


def setMarkerInterface(licence, event):
    """
    """
    portal_type = licence.portal_type
    marker_interface = URBAN_TYPES_INTERFACES.get(portal_type, None)
    if marker_interface and not marker_interface.providedBy(licence):
        alsoProvides(licence, marker_interface)
