# -*- coding: utf-8 -*-
#
# File: City.py
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
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="zipCode",
            widget=StringField._properties["widget"](
                size=20,
                label="Zipcode",
                label_msgid="urban_label_zipCode",
                i18n_domain="urban",
            ),
            validators=("isInt",),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

City_schema = BaseFolderSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class City(BaseFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ICity)

    meta_type = "City"
    _at_rename_after_creation = True

    schema = City_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(City, PROJECTNAME)
# end of class City

##code-section module-footer #fill in your manual code here
##/code-section module-footer
