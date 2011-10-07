# -*- coding: utf-8 -*-

import os
import random
import string
from Products.Archetypes.interfaces import IStringField

def moveElementAfter(object_to_move, container, attr_name, attr_value_to_match):
    new_position = object_to_move.getObjectPosition(object_to_move.id)
    for content in container.objectValues():
        attr = getattr(content, attr_name)
        if isinstance(attr, unicode):
            attr = attr.encode()
        if getattr(content, attr_name) == attr_value_to_match and object_to_move != content:
            new_position = 1 + content.getObjectPosition(content.id)
    object_to_move.moveObjectToPosition(object_to_move.id, new_position)

def generatePassword(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))

def getOsTempFolder():
    tmp = '/tmp'
    if os.path.exists(tmp) and os.path.isdir(tmp):
        res = tmp
    elif os.environ.has_key('TMP'):
        res = os.environ['TMP']
    elif os.environ.has_key('TEMP'):
        res = os.environ['TEMP']
    else:
        raise "Sorry, I can't find a temp folder on your machine."
    return res

def setOptionalAttributes(schema, optional_fields):
    """
      This method set the optional attribute and widget condition on schema fields listed in optional_fields
    """
    for fieldname in optional_fields:
        field = schema.get(fieldname)
        if field is not None:
            setattr(field, 'optional', True)
            field.widget.setCondition("python: here.attributeIsUsed('%s')"%fieldname)
