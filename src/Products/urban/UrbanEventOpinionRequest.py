# -*- coding: utf-8 -*-
#
# File: UrbanEventOpinionRequest.py
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
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    StringField(
        name='requestedOrganisation',
        widget=StringField._properties['widget'](
            label='Requestedorganisation',
            label_msgid='urban_label_requestedOrganisation',
            i18n_domain='urban',
        ),
        optional= False,
        write_permission="Manage portal",
        default_method="getDefaultRequestedOrganisation",
    ),
    StringField(
        name='linkedInquiryUID',
        widget=StringField._properties['widget'](
            label='Linkedinquiryuid',
            label_msgid='urban_label_linkedInquiryUID',
            i18n_domain='urban',
        ),
        optional= False,
        write_permission="Manage portal",
        default_method="getDefaultLinkedInquiry",
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEventOpinionRequest_schema = BaseSchema.copy() + \
    getattr(UrbanEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventOpinionRequest(BaseContent, UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanEventOpinionRequest)

    meta_type = 'UrbanEventOpinionRequest'
    _at_rename_after_creation = True

    schema = UrbanEventOpinionRequest_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(UrbanEventOpinionRequest, PROJECTNAME)
# end of class UrbanEventOpinionRequest

##code-section module-footer #fill in your manual code here
##/code-section module-footer

