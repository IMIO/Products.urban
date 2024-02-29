# -*- coding: utf-8 -*-
#
# File: ProjectMeeting.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.MiscDemand import finalizeSchema
from Products.urban.content.licence.MiscDemand import MiscDemand
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema(
    (),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

ProjectMeeting_schema = (
    BaseFolderSchema.copy()
    + getattr(MiscDemand, "schema", Schema(())).copy()
    + schema.copy()
)

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class ProjectMeeting(BaseFolder, MiscDemand, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IProjectMeeting)

    meta_type = "ProjectMeeting"
    _at_rename_after_creation = True

    schema = ProjectMeeting_schema

    # Methods


registerType(ProjectMeeting, PROJECTNAME)
# end of class ProjectMeeting


##code-section module-footer #fill in your manual code here
# finalizeSchema come from MiscDemand as its the same changes
finalizeSchema(ProjectMeeting_schema)
##/code-section module-footer
