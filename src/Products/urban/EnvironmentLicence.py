# -*- coding: utf-8 -*-
#
# File: EnvironmentLicence.py
#
# Copyright (c) 2013 by CommunesPlone
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
from Products.urban.EnvironmentBase import EnvironmentBase
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.utils import setOptionalAttributes

optional_fields =['areaDescriptionText', 'hasConfidentialData', 'isTemporaryProject']
##/code-section module-header

schema = Schema((

    TextField(
        name='areaDescriptionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Areadescriptiontext',
            label_msgid='urban_label_areaDescriptionText',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    BooleanField(
        name='hasConfidentialData',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Hasconfidentialdata',
            label_msgid='urban_label_hasConfidentialData',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isTemporaryProject',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Istemporaryproject',
            label_msgid='urban_label_isTemporaryProject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentLicence_schema = BaseSchema.copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvironmentLicence(BaseContent, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentLicence)

    meta_type = 'EnvironmentLicence'
    _at_rename_after_creation = True

    schema = EnvironmentLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods


registerType(EnvironmentLicence, PROJECTNAME)
# end of class EnvironmentLicence

##code-section module-footer #fill in your manual code here
##/code-section module-footer

