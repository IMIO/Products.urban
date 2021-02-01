# -*- coding: utf-8 -*-
#
# File: UrbanEventOpinionRequest.py
#
# Copyright (c) 2015 by CommunesPlone
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
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from plone import api
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='linkedInquiry',
        widget=ReferenceBrowserWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
            label='Linkedinquiry',
            label_msgid='urban_label_linkedInquiry',
            i18n_domain='urban',
        ),
        multiValued=0,
        relationship='linkedInquiry',
        allowed_types=('Inquiry', 'BuildLicence'),
        write_permission="Manage portal",
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

class UrbanEventOpinionRequest(UrbanEvent, BrowserDefaultMixin):
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

    # Manually created methods

    security.declarePublic('getTemplates')

    def getTemplates(self):
        """
          Returns contained templates (File)
        """
        if not self.getUrbaneventtypes():
            return []
        custom_templates = self.getUrbaneventtypes().getTemplates()
        if custom_templates:
            return custom_templates

        licence_config = self.aq_parent.getLicenceConfig()
        opinionrequest_config = getattr(licence_config.eventconfigs, "config-opinion-request")
        return opinionrequest_config.getTemplates()

    security.declarePublic('getLinkedOrganisationTerm')
    def getLinkedOrganisationTerm(self):
        """
          Returns of the term that is linked to the linked UrbanEventType
        """
        return self.getUrbaneventtypes()

    security.declarePublic('getLinkedOrganisationTermId')
    def getLinkedOrganisationTermId(self):
        """
          Returns the id of the term that is linked to the linked UrbanEventType
        """
        event_type = self.getUrbaneventtypes()
        if event_type:
            return event_type.getId()



registerType(UrbanEventOpinionRequest, PROJECTNAME)
# end of class UrbanEventOpinionRequest

##code-section module-footer #fill in your manual code here
##/code-section module-footer

