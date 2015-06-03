# -*- coding: utf-8 -*-

from Products.urban import UrbanMessage as _

from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.formwidget.namedfile import NamedFileWidget
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model

from zope.interface import implements

import logging
logger = logging.getLogger('Products.urban: UrbanDoc')


class IUrbanDoc(model.Schema):
    """
    UrbanDoc dexterity schema.
    """

    model.primary('file')
    form.widget('file', NamedFileWidget)
    file = NamedBlobFile(
        title=_(u'File'),
    )


class UrbanDoc(Item):
    """
    UrbanDoc dexterity class.
    """

    implements(IUrbanDoc)
