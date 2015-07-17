# -*- coding: utf-8 -*-

from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate
from collective.documentgenerator.content.pod_template import ConfigurablePODTemplate

from zope.interface import implements

import logging
logger = logging.getLogger('Products.urban: UrbanTemplate')


class IUrbanTemplate(IConfigurablePODTemplate):
    """
    UrbanTemplate dexterity schema.
    """


class UrbanTemplate(ConfigurablePODTemplate):
    """
    UrbanTemplate dexterity class.
    """

    implements(IUrbanTemplate)
