# -*- coding: utf-8 -*-

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
        schema[inquiryField.getName()].schemata = 'urban_investigation_and_advices'


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
