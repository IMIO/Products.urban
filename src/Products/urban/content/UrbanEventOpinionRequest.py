# -*- coding: utf-8 -*-
#
# File: UrbanEventOpinionRequest.py
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
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='linkedInquiry',
        widget=ReferenceBrowserWidget(
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
        wf_tool = getToolByName(self, 'portal_workflow')
        if len(self.getUrbaneventtypes().listFolderContents({'portal_type': 'UrbanDoc'})):
            return [template for template in self.getUrbaneventtypes().listFolderContents({'portal_type': 'UrbanDoc'})
                    if wf_tool.getInfoFor(template, 'review_state') == 'enabled']
        urbantool = getToolByName(self,'portal_urban')
        opinionrequest_config = getattr(getattr(urbantool, self.aq_parent.portal_type.lower()).urbaneventtypes, "config-opinion-request")
        return opinionrequest_config.listFolderContents({'portal_type': 'UrbanDoc'})

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
        return self.getUrbaneventtypes().getId()



registerType(UrbanEventOpinionRequest, PROJECTNAME)
# end of class UrbanEventOpinionRequest

##code-section module-footer #fill in your manual code here
##/code-section module-footer

