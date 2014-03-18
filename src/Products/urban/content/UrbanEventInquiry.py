# -*- coding: utf-8 -*-
#
# File: UrbanEventInquiry.py
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
from Products.urban.content.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='explanationsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            condition="python:here.attributeIsUsed('explanationsDate')",
            format="%d/%m/%Y%H",
            label='Explanationsdate',
            label_msgid='urban_label_explanationsDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='claimsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            condition="python:here.attributeIsUsed('claimsDate')",
            format="%d/%m/%Y%H",
            label='Claimsdate',
            label_msgid='urban_label_claimsDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    TextField(
        name='claimsText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            condition="python:here.attributeIsUsed('claimsText')",
            label='Claimstext',
            label_msgid='urban_label_claimsText',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_output_type='text/html',
        optional= True,
    ),
    ReferenceField(
        name='linkedInquiry',
        widget=ReferenceBrowserWidget(
            visible=False,
            label='Linkedinquiry',
            label_msgid='urban_label_linkedInquiry',
            i18n_domain='urban',
        ),
        allowed_types=('Inquiry', 'UrbanCertificateTwo', 'BuildLicence', 'EnvironmentBase', 'MiscDemand'),
        multiValued=0,
        relationship='linkedInquiry',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventInquiry_schema = BaseFolderSchema.copy() + \
    getattr(UrbanEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventInquiry(BaseFolder, UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventInquiry)

    meta_type = 'UrbanEventInquiry'
    _at_rename_after_creation = True

    schema = UrbanEventInquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(UrbanEventInquiry, PROJECTNAME)
# end of class UrbanEventInquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

