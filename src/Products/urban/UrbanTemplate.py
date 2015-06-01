# -*- coding: utf-8 -*-

from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.content.pod_template import PODTemplate

from zope.interface import implements

import logging
logger = logging.getLogger('Products.urban: UrbanTemplate')


class IUrbanTemplate(IPODTemplate):
    """
    UrbanTemplate dexterity schema.
    """


class UrbanTemplate(PODTemplate):
    """
    UrbanTemplate dexterity class.
    """

    implements(IUrbanTemplate)
