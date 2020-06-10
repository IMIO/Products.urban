# -*- coding: utf-8 -*-

from Products.urban import _
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.browser.select import SelectWidget
from z3c.form.browser.text import TextWidget
from zope import schema
from zope.interface import implementer

import logging


logger = logging.getLogger('collective.documentgenerator: PODTemplate')


class IPODTemplate(model.Schema):
    """
    PODTemplate dexterity schema.
    """

    form.widget('divisionCode', TextWidget)
    divisionCode = schema.TextLine(
        title=_(u'Divisioncode'),
        description=u'urban_label_divisionCode',
        required=False,
    )

    form.widget('partie', RadioFieldWidget)
    partie = schema.Bool(
        title=_(u'Partie'),
        default=False,
        required=False,
    )

#    form.widget('style_template', SelectWidget)
#    style_template = schema.List(
#        title=_(u'Style template'),
#        description=_(u'Choose the style template to apply for this template.'),
#        value_type=schema.Choice(source='collective.documentgenerator.StyleTemplates'),
#        required=False,
#    )


@implementer(IPODTemplate)
class PODTemplate(Item):
    """
    PODTemplate dexterity class.
    """
