# -*- coding: utf-8 -*-
#
# File: Street.py
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

from Products.urban.utils import WIDGET_DATE_END_YEAR
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Acquisition import aq_inner, aq_parent
from Products.CMFCore import permissions

##/code-section module-header

schema = Schema(
    (
        IntegerField(
            name="bestAddressKey",
            default=0,
            widget=IntegerField._properties["widget"](
                description="When adding manually a new street, please let the default value",
                description_msgid="street_best_address_key_descr",
                label="Bestaddresskey",
                label_msgid="urban_label_bestAddressKey",
                i18n_domain="urban",
            ),
            required=True,
            validators=("isInt",),
        ),
        IntegerField(
            name="streetCode",
            widget=IntegerField._properties["widget"](
                size=20,
                label="Streetcode",
                label_msgid="urban_label_streetCode",
                i18n_domain="urban",
            ),
            required=True,
            validators=("isInt",),
        ),
        StringField(
            name="streetName",
            widget=StringField._properties["widget"](
                label="Streetname",
                label_msgid="urban_label_streetName",
                i18n_domain="urban",
            ),
            required=True,
        ),
        DateTimeField(
            name="startDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                description="Encoding date by default",
                description_msgid="street_start_date_descr",
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label="Startdate",
                label_msgid="urban_label_startDate",
                i18n_domain="urban",
            ),
            required=True,
        ),
        DateTimeField(
            name="endDate",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                description="Expiration date. Keep empty for valid streets. Fill in for history.",
                description_msgid="street_end_date_descr",
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label="Enddate",
                label_msgid="urban_label_endDate",
                i18n_domain="urban",
            ),
        ),
        StringField(
            name="regionalRoad",
            widget=StringField._properties["widget"](
                label="Regionalroad",
                label_msgid="urban_label_regionalRoad",
                i18n_domain="urban",
            ),
        ),
    ),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Street_schema = BaseSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
del Street_schema["title"]
##/code-section after-schema


class Street(BaseContent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IStreet)

    meta_type = "Street"
    _at_rename_after_creation = True

    schema = Street_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic("Title")

    def Title(self):
        """
        Update the title to clearly identify the street in the city
        """
        # format is "streetName (cityZipeCode - cityTitle)"
        city = self.getParentNode()
        title = "%s (%s - %s)" % (self.getStreetName(), city.getZipCode(), city.Title())
        return str(title)

    security.declareProtected(permissions.View, "SearchableText")

    def SearchableText(self):
        """
        Override to take Title into account
        """
        return self.Title()

    def getCity(self):
        """
        Returns the city
        """
        return aq_parent(aq_inner(self))


registerType(Street, PROJECTNAME)
# end of class Street

##code-section module-footer #fill in your manual code here
##/code-section module-footer
