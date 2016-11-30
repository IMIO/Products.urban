# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from imio.schedule.utils import tuple_to_interface

from HTMLParser import HTMLParser

from Products.urban.config import URBAN_TYPES

from plone import api

import random
import string
import hashlib


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
    module_name = 'Products.urban.%s' % metatype
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
    from Products.urban.Inquiry import Inquiry
    inquiryFields = Inquiry.schema.filterFields(isMetadata=False)
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
        if hasattr(field, 'edit_only') and field.edit_only:
            return False
        if field.getName() in exclude:
            return False
        if not field.widget.visible:
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
