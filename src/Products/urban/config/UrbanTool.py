# -*- coding: utf-8 -*-
#
# File: UrbanTool.py
#
# Copyright (c) 2014 by CommunesPlone
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible=False,
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='NISNum',
        widget=StringField._properties['widget'](
            label='Nisnum',
            label_msgid='urban_label_NISNum',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='cityName',
        default='MaCommune',
        widget=StringField._properties['widget'](
            label='Cityname',
            label_msgid='urban_label_cityName',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    DataGridField(
        name='divisionsRenaming',
        widget=DataGridWidget(
            columns={'division': FixedColumn('Division', visible=False), 'name': FixedColumn('Name'), 'alternative_name': Column('Alternative Name')},
            label='Divisionsrenaming',
            label_msgid='urban_label_divisionsRenaming',
            i18n_domain='urban',
        ),
        fixed_rows='getDivisionsConfigRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=True,
        schemata='public_settings',
        columns=('division', 'name', 'alternative_name',),
    ),
    BooleanField(
        name='isDecentralized',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isdecentralized',
            label_msgid='urban_label_isDecentralized',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    StringField(
        name='sqlHost',
        widget=StringField._properties['widget'](
            label='Sqlhost',
            label_msgid='urban_label_sqlHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlName',
        widget=StringField._properties['widget'](
            label='Sqlname',
            label_msgid='urban_label_sqlName',
            i18n_domain='urban',
        ),
        required=True,
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlUser',
        widget=StringField._properties['widget'](
            label='Sqluser',
            label_msgid='urban_label_sqlUser',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlPassword',
        widget=PasswordWidget(
            label='Sqlpassword',
            label_msgid='urban_label_sqlPassword',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='webServerHost',
        widget=StringField._properties['widget'](
            label='Webserverhost',
            label_msgid='urban_label_webServerHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='pylonsHost',
        widget=StringField._properties['widget'](
            label='Pylonshost',
            label_msgid='urban_label_pylonsHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='mapExtent',
        widget=StringField._properties['widget'](
            description="Enter the 4 coordinates of the map, each coordinate separated by a comma.",
            description_msgid="urban_descr_mapExtent",
            label='Mapextent',
            label_msgid='urban_label_mapExtent',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='unoEnabledPython',
        default="/usr/bin/python",
        widget=StringField._properties['widget'](
            label="Path of a UNO-enabled Python interpreter (ie /usr/bin/python)",
            description="UnoEnabledPython",
            description_msgid="uno_enabled_python",
            label_msgid='urban_label_unoEnabledPython',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    IntegerField(
        name='openOfficePort',
        default=2002,
        widget=IntegerField._properties['widget'](
            description="OpenOfficePort",
            description_msgid="open_office_port",
            label='Openofficeport',
            label_msgid='urban_label_openOfficePort',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='editionOutputFormat',
        default='odt',
        widget=SelectionWidget(
            label='Editionoutputformat',
            label_msgid='urban_label_editionOutputFormat',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='public_settings',
        vocabulary=GENERATED_DOCUMENT_FORMATS.keys(),
    ),
    BooleanField(
        name='generateSingletonDocuments',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Generatesingletondocuments',
            label_msgid='urban_label_generateSingletonDocuments',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    BooleanField(
        name='invertAddressNames',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Invertaddressnames',
            label_msgid='urban_label_invertAddressNames',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    BooleanField(
        name='usePloneMeetingWSClient',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Useplonemeetingwsclient',
            label_msgid='urban_label_usePloneMeetingWSClient',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanTool_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanTool(UniqueObject, OrderedBaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanTool)

    meta_type = 'UrbanTool'
    _at_rename_after_creation = True

    schema = UrbanTool_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        OrderedBaseFolder.__init__(self,'portal_urban')
        self.setTitle('Urban configuration')

        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()

        ##code-section post-edit-method-footer #fill in your manual code here
        ##/code-section post-edit-method-footer


    # Methods

registerType(UrbanTool, PROJECTNAME)
# end of class UrbanTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer

