# -*- coding: utf-8 -*-
#
# File: ParcelOutLicence.py
#
# Copyright (c) 2012 by CommunesPlone
# Generator: ArchGenXML Version 2.6
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
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from GenericLicence import GenericLicence
from GenericLicence import GenericLicence_schema
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
import appy.pod.renderer
import os
import psycopg2
from Products.urban.utils import setOptionalAttributes

optional_fields = []
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='geometricians',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title':'Nom'},
            base_query="geometriciansBaseQuery",
            wild_card_search=True,
            label='Geometricians',
            label_msgid='urban_label_geometricians',
            i18n_domain='urban',
        ),
        allowed_types=('Geometrician',),
        multiValued=1,
        relationship='parcelOutGeometricians',
        required=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

ParcelOutLicence_schema = GenericLicence_schema.copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
ParcelOutLicence_schema['title'].required = False
##/code-section after-schema

class ParcelOutLicence(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IParcelOutLicence)

    meta_type = 'ParcelOutLicence'
    _at_rename_after_creation = True

    schema = ParcelOutLicence_schema

    ##code-section class-header #fill in your manual code here
    archetype_name = 'ParcelOutLicence'
    ##/code-section class-header

    # Methods

    security.declarePublic('generateReference')
    def generateReference(self):
        """
        """
        pass

    # Manually created methods

    security.declarePublic('geometriciansBaseQuery')
    def geometriciansBaseQuery(self):
        """
          Do add some details for the base query
          Here, we want to be sure that geometricians are alphabetically sorted
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        dict = {}
        dict['path'] = {'query':'%s/urban/geometricians' % (rootPath)}
        dict['sort_on'] = 'sortable_title'
        return dict

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_create_script(self)

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_edit_script(self)



registerType(ParcelOutLicence, PROJECTNAME)
# end of class ParcelOutLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

