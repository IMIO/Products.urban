# -*- coding: utf-8 -*-
#
# File: UrbanConfigurationValue.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from plone import api
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (
        BooleanField(
            name="isDefaultValue",
            default=False,
            widget=BooleanField._properties["widget"](
                label="Isdefaultvalue",
                label_msgid="urban_label_isDefaultValue",
                i18n_domain="urban",
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanConfigurationValue_schema = BaseSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class UrbanConfigurationValue(BaseContent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IUrbanConfigurationValue)

    meta_type = "UrbanConfigurationValue"
    _at_rename_after_creation = True

    schema = UrbanConfigurationValue_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def to_dict(self):
        dict_ = {
            "UID": self.UID(),
            "enabled": api.content.get_state(self) == "enabled",
            "portal_type": self.portal_type,
        }
        for f in self.schema.fields():
            if f.schemata != "metadata":
                val = f.getAccessor(self)()
                if type(val) is str:
                    val = val.decode("utf8")
                dict_[f.__name__] = val
        return dict_


registerType(UrbanConfigurationValue, PROJECTNAME)
# end of class UrbanConfigurationValue

##code-section module-footer #fill in your manual code here
##/code-section module-footer
