# -*- coding: utf-8 -*-

import os
from Products.Archetypes.interfaces import IStringField

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
