# -*- coding: utf-8 -*-
#
# File: UrbanCertificateTwo.py
#
# Copyright (c) 2011 by CommunesPlone
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
from Products.urban.UrbanCertificateBase import UrbanCertificateBase
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.indexes import UrbanIndexes
from collective.referencedatagridfield import ReferenceDataGridField
from collective.referencedatagridfield import ReferenceDataGridWidget
from Products.urban.taskable import Taskable
from Products.urban.base import UrbanBase
from Products.urban.utils import setRawSchema
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='investigationStart',
        widget=DateTimeField._properties['widget'](
            show_hm=0,
            label='Investigationstart',
            label_msgid='urban_label_investigationStart',
            i18n_domain='urban',
        ),
    ),
    DateTimeField(
        name='investigationEnd',
        widget=DateTimeField._properties['widget'](
            show_hm=0,
            label='Investigationend',
            label_msgid='urban_label_investigationEnd',
            i18n_domain='urban',
        ),
    ),
    IntegerField(
        name='investigationOralReclamationNumber',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Investigationoralreclamationnumber',
            label_msgid='urban_label_investigationOralReclamationNumber',
            i18n_domain='urban',
        ),
    ),
    IntegerField(
        name='investigationWriteReclamationNumber',
        default=0,
        widget=IntegerField._properties['widget'](
            label='Investigationwritereclamationnumber',
            label_msgid='urban_label_investigationWriteReclamationNumber',
            i18n_domain='urban',
        ),
    ),
    ReferenceDataGridField(
        name='workLocations',
        widget=ReferenceDataGridWidget(
            startup_directory='/portal_urban/streets',
            macro="street_referencedatagridwidget",
            visible={'edit' : 'visible', 'view' : 'visible'},
            label='street',
            label_msgid='urban_label_workLocations',
            i18n_domain='urban',
        ),
        allowed_types=('Street', 'Locality'),
        schemata='default',
        columns=('numero','title' ,'link' ,'uid'),
        relationship='Street',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setRawSchema(schema)
##/code-section after-local-schema

UrbanCertificateTwo_schema = BaseFolderSchema.copy() + \
    getattr(UrbanCertificateBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanCertificateTwo(BaseFolder, UrbanIndexes,  UrbanBase, UrbanCertificateBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanCertificateTwo)

    meta_type = 'UrbanCertificateTwo'
    _at_rename_after_creation = True

    schema = UrbanCertificateTwo_schema

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
        super(UrbanCertificateBase).__thisclass__.at_post_create_script(self)

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        super(UrbanCertificateBase).__thisclass__.at_post_edit_script(self)



registerType(UrbanCertificateTwo, PROJECTNAME)
# end of class UrbanCertificateTwo

##code-section module-footer #fill in your manual code here
##/code-section module-footer

