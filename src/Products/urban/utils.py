# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from imio.schedule.utils import tuple_to_interface

from HTMLParser import HTMLParser

from Products.ATContentTypes.interfaces.file import IATFile
from Products.urban.config import URBAN_TYPES
from Products.urban.config import URBAN_ENVIRONMENT_TYPES
from Products.urban.interfaces import IUrbanDoc

from plone import api

from zope.annotation import IAnnotations
from zope.component import getMultiAdapter

import random
import string
import hashlib
import pkg_resources


def getCurrentFolderManager():
    """
     Returns the current FolderManager initials or object
    """
    portal_urban = api.portal.get_tool('portal_urban')
    foldermanagers = portal_urban.foldermanagers
    current_user_id = api.user.get_current().getId()
    for foldermanager in foldermanagers.objectValues('FolderManager'):
        if foldermanager.getPloneUserId() == current_user_id:
            return foldermanager
    return None


def getLicenceSchema(licencetype):
    if licencetype not in URBAN_TYPES:
        return None
    types_tool = api.portal.get_tool('portal_types')
    type_info = types_tool.getTypeInfo(licencetype)
    metatype = type_info.getProperty('content_meta_type')
    module_name = 'Products.urban.content.licence.%s' % metatype
    attribute = "%s_schema" % metatype
    module = __import__(module_name, fromlist=[attribute])
    return getattr(module, attribute)


def moveElementAfter(object_to_move, container, attr_name, attr_value_to_match):
    new_position = container.getObjectPosition(object_to_move.getId())
    contents = container.objectValues()
    indexes = range(len(contents))
    indexes.reverse()
    for i in indexes:
        if getattr(contents[i], attr_name) == attr_value_to_match and object_to_move != contents[i]:
            new_position = 1 + container.getObjectPosition(contents[i].getId())
            container.moveObjectToPosition(object_to_move.getId(), new_position)
            return


def generatePassword(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))


def getMd5Signature(data):
    md5 = hashlib.md5(data)
    return md5.hexdigest()


def setOptionalAttributes(schema, optional_fields):
    """
      This method set the optional attribute and widget condition on schema fields listed in optional_fields
    """
    for fieldname in optional_fields:
        field = schema.get(fieldname)
        if field is not None:
            setattr(field, 'optional', True)
            field.widget.setCondition("python: here.attributeIsUsed('%s')" % fieldname)


def setSchemataForInquiry(schema):
    """
      Put the the fields coming from Inquiry in a specific schemata
    """
    from Products.urban.content.Inquiry import Inquiry
    _setSchemataForInquiry(schema, Inquiry)


def setSchemataForCODT_Inquiry(schema):
    """
      Put the the fields coming from Inquiry in a specific schemata
    """
    from Products.urban.content.CODT_Inquiry import CODT_Inquiry
    _setSchemataForInquiry(schema, CODT_Inquiry)


def setSchemataForCODT_UniqueLicenceInquiry(schema):
    """
      Put the the fields coming from Inquiry in a specific schemata
    """
    from Products.urban.content.CODT_UniqueLicenceInquiry import CODT_UniqueLicenceInquiry
    _setSchemataForInquiry(schema, CODT_UniqueLicenceInquiry)


def _setSchemataForInquiry(schema, inquiry_class):
    """
      Put the the fields coming from Inquiry in a specific schemata
    """
    inquiryFields = inquiry_class.schema.filterFields(isMetadata=False)
    #do not take the 2 first fields into account, this is 'id' and 'title'
    inquiryFields = inquiryFields[2:]
    for inquiryField in inquiryFields:
        if schema[inquiryField.getName()].schemata == 'default':
            schema[inquiryField.getName()].schemata = 'urban_inquiry'


#class and function to strip a text from all its HTML tags
class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def getLicenceFolderId(licencetype):
    return '{}s'.format(licencetype.lower())


def getAllLicenceFolderIds():
    return [getLicenceFolderId(licencetype) for licencetype in URBAN_TYPES]


def getUrbanOnlyLicenceFolderIds():
    return [getLicenceFolderId(licencetype) for licencetype in URBAN_TYPES if licencetype not in URBAN_ENVIRONMENT_TYPES]


def getEnvironmentLicenceFolderIds():
    return [getLicenceFolderId(licencetype) for licencetype in URBAN_ENVIRONMENT_TYPES]


def getLicenceFolder(licencetype):
    portal = api.portal.getSite()
    urban = portal.urban
    folder_id = getLicenceFolderId(licencetype)
    licence_folder = getattr(urban, folder_id)
    return licence_folder


def removeItems(liste, items):
    [liste.remove(i) for i in items if liste.count(i)]
    return liste


def getSchemataFields(context, displayed_fields, schemata='', exclude=[]):
    def isDisplayable(field):
        if hasattr(field, 'optional') and field.optional and field.getName() not in displayed_fields:
            return False
        if field.getName() in exclude:
            return False
        if not field.widget.visible:
            return False
        if field.widget.visible.get('view', None) not in [True, 'visible']:
            return False
        if not field.checkPermission('r', context):
            return False
        return True

    context = aq_inner(context)
    schema = context.__class__.schema
    fields = [field for field in schema.getSchemataFields(schemata) if isDisplayable(field)]

    return fields


def get_interface_by_path(interface_path):
    """
    """
    splitted_path = interface_path.split('.')
    interface_tuple = ('.'.join(splitted_path[0:-1]), splitted_path[-1])
    return tuple_to_interface(interface_tuple)


def is_attachment(obj):
    """
    """
    is_file = IATFile.providedBy(obj)
    is_doc = IUrbanDoc.providedBy(obj)
    is_attachment = is_file and not is_doc
    return is_attachment


def get_ws_meetingitem_infos(urban_event, extra_attributes=False):
    """
    """
    annotations = IAnnotations(urban_event)
    if 'imio.pm.wsclient-sent_to' in annotations:
        request = api.portal.getRequest()
        portal_state = getMultiAdapter(
            (urban_event, request),
            name=u'plone_portal_state'
        )
        ws4pmSettings = getMultiAdapter(
            (portal_state.portal(), request),
            name='ws4pmclient-settings'
        )
        items = ws4pmSettings._soap_searchItems({'externalIdentifier': urban_event.UID()})
        if extra_attributes and items:
            items = ws4pmSettings._soap_getItemInfos({'UID': items[0].UID, 'showExtraInfos': True})
        return items


def run_entry_points(group, name, *args, **kwargs):
    for entrypoint in pkg_resources.iter_entry_points(group=group, name=name):
        plugin = entrypoint.load()
        return plugin(*args, **kwargs)
