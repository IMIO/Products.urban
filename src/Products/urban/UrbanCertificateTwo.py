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
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.indexes import UrbanIndexes
from Products.urban.base import UrbanBase
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry

optional_fields = []
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

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanCertificateTwo_schema = BaseFolderSchema.copy() + \
    getattr(UrbanCertificateBase, 'schema', Schema(())).copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
#put the the fields coming from Inquiry in a specific schemata
setSchemataForInquiry(UrbanCertificateTwo_schema)
##/code-section after-schema

class UrbanCertificateTwo(BaseFolder, UrbanIndexes,  UrbanBase, UrbanCertificateBase, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanCertificateTwo)

    meta_type = 'UrbanCertificateTwo'
    _at_rename_after_creation = True

    schema = UrbanCertificateTwo_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location', \
                      'urban_investigation_and_advices']
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

