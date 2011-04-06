# -*- coding: utf-8 -*-
#
# File: WorkLocation.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.5
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='street',
        widget=ReferenceBrowserWidget(
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title':'workLocationStreet',},
            force_close_on_insert=True,
            label='Street',
            label_msgid='urban_label_street',
            i18n_domain='urban',
        ),
        allowed_types= ('Street',),
        relationship="street",
        required=True,
    ),
    StringField(
        name='number',
        widget=StringField._properties['widget'](
            label='Number',
            label_msgid='urban_label_number',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='isSupplementary',
        default=True,
        widget=BooleanField._properties['widget'](
            visible=False,
            label='Issupplementary',
            label_msgid='urban_label_isSupplementary',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

WorkLocation_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
WorkLocation_schema['title'].required = False
WorkLocation_schema['title'].widget.visible = False
##/code-section after-schema

class WorkLocation(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IWorkLocation)

    meta_type = 'WorkLocation'
    _at_rename_after_creation = True

    schema = WorkLocation_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        self.updateTitle()

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title
        """
        street = self.getStreet()
        number = self.getNumber()
        streetTitle = ""
        if street:
            streetTitle = street.Title()
        if number:
            title = "%s, %s" % (streetTitle, number)
        else:
            title = "%s" % streetTitle
        self.setTitle(str(title))
        self.reindexObject()

    security.declarePublic('getSignaletic')
    def getSignaletic(self):
        """
           Return a string representing the worklocation
        """
        street = self.getStreet()
        if not street:
            return ''
        city = street.aq_inner.aq_parent
        number = self.getNumber()
        if number:
            return "%s, %s - %d %s" % (self.getNumber(), street.getStreetName(), city.getZipCode(), city.Title())
        else:
            return "%s - %d %s" % (street.getStreetName(), city.getZipCode(), city.Title())



registerType(WorkLocation, PROJECTNAME)
# end of class WorkLocation

##code-section module-footer #fill in your manual code here
##/code-section module-footer

