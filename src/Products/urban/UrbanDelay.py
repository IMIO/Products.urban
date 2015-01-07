# -*- coding: utf-8 -*-
#
# File: UrbanDelay.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.UrbanConfigurationValue import UrbanConfigurationValue
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    IntegerField(
        name='deadLineDelay',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Deadlinedelay',
            label_msgid='urban_label_deadLineDelay',
            i18n_domain='urban',
        ),
        required=True,
        validators=('isInt',),
    ),
    IntegerField(
        name='alertDelay',
        default=0,
        widget=IntegerField._properties['widget'](
            description='Set the number of days the alert will be shown before the deadline delay',
            description_msgid="urban_alertdelay_descr",
            label='Alertdelay',
            label_msgid='urban_label_alertDelay',
            i18n_domain='urban',
        ),
        required=True,
        validators=('isInt',),
    ),
    StringField(
        name='delayComputation',
        widget=StringField._properties['widget'](
            size=100,
            description="Enter a TAL condition that defines the delay calculation. The parameters event and licence are available.",
            description_msgid="delay_computation_descr",
            label='Delaycomputation',
            label_msgid='urban_label_delayComputation',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanDelay_schema = BaseSchema.copy() + \
    getattr(UrbanConfigurationValue, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanDelay(BaseContent, UrbanConfigurationValue, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanDelay)

    meta_type = 'UrbanDelay'
    _at_rename_after_creation = True

    schema = UrbanDelay_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(UrbanDelay, PROJECTNAME)
# end of class UrbanDelay

##code-section module-footer #fill in your manual code here
##/code-section module-footer

