# -*- coding: utf-8 -*-
#
# File: urban.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"


# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().

import logging

logger = logging.getLogger("urban")
logger.debug("Installing Product")

import os
import os.path
from App.Common import package_home
from plone.app.upgrade.utils import alias_module
from plone.app.blob.content import ATBlob
import Products.CMFPlone.interfaces
from Products.Archetypes import listTypes
from Products.Archetypes.atapi import *
from Products.Archetypes.utils import capitalize
from Products.CMFCore import DirectoryView
from Products.CMFCore import permissions as cmfpermissions
from Products.CMFCore import utils as cmfutils
from Products.CMFPlone.utils import ToolInit
from config import *

DirectoryView.registerDirectory("skins", product_globals)


##code-section custom-init-head #fill in your manual code here
from zope.i18nmessageid import MessageFactory

UrbanMessage = MessageFactory("urban")
from Products.validation import validation
from validators.validator import isTextFieldConfiguredValidator

validation.register(isTextFieldConfiguredValidator("isTextFieldConfigured"))
from validators.validator import isValidStreetNameValidator

validation.register(isValidStreetNameValidator("isValidStreetName"))
from validators.validator import procedureChoiceValidator

validation.register(procedureChoiceValidator("isValidProcedureChoice"))
from validators.validator import isValidSectionValidator

validation.register(isValidSectionValidator("isValidSection"))
from validators.validator import isValidRadicalValidator

validation.register(isValidRadicalValidator("isValidRadical"))
from validators.validator import isValidBisValidator

validation.register(isValidBisValidator("isValidBis"))
from validators.validator import isValidExposantValidator

validation.register(isValidExposantValidator("isValidExposant"))
from validators.validator import isValidPuissanceValidator

validation.register(isValidPuissanceValidator("isValidPuissance"))
from validators.validator import isNotDuplicatedReferenceValidator

validation.register(isNotDuplicatedReferenceValidator("isNotDuplicatedReference"))
from validators.validator import isReferenceValidator

validation.register(isReferenceValidator("isReference"))
from validators.validator import isInteger

validation.register(isInteger("isInteger"))
##/code-section custom-init-head

import Products

from Products.urban.content.licence import Article127  # noqa
from Products.urban.content.licence import BuildLicence  # noqa
from Products.urban.content.licence import CODT_Article127  # noqa
from Products.urban.content.licence import CODT_BuildLicence  # noqa
from Products.urban.content.licence import CODT_CommercialLicence  # noqa
from Products.urban.content.licence import CODT_IntegratedLicence  # noqa
from Products.urban.content.licence import CODT_ParcelOutLicence  # noqa
from Products.urban.content.licence import CODT_UniqueLicence  # noqa
from Products.urban.content.licence import CODT_UrbanCertificateBase  # noqa
from Products.urban.content.licence import CODT_UrbanCertificateTwo  # noqa
from Products.urban.content.licence import Declaration  # noqa
from Products.urban.content.licence import Division  # noqa
from Products.urban.content.licence import EnvClassThree  # noqa
from Products.urban.content.licence import EnvClassTwo  # noqa
from Products.urban.content.licence import EnvClassOne  # noqa
from Products.urban.content.licence import EnvClassBordering  # noqa
from Products.urban.content.licence import EnvironmentBase  # noqa
from Products.urban.content.licence import EnvironmentLicence  # noqa
from Products.urban.content.licence import GenericLicence  # noqa
from Products.urban.content.licence import Inspection  # noqa
from Products.urban.content.licence import IntegratedLicence  # noqa
from Products.urban.content.licence import MiscDemand  # noqa
from Products.urban.content.licence import ParcelOutLicence  # noqa
from Products.urban.content.licence import PatrimonyCertificate  # noqa
from Products.urban.content.licence import PreliminaryNotice  # noqa
from Products.urban.content.licence import ProjectMeeting  # noqa
from Products.urban.content.licence import Ticket  # noqa
from Products.urban.content.licence import UrbanCertificateBase  # noqa
from Products.urban.content.licence import UrbanCertificateTwo  # noqa
from Products.urban.content.licence import UniqueLicence  # noqa
from Products.urban.content.licence import ExplosivesPossession  # noqa
from Products.urban.content.licence import RoadDecree  # noqa
from Products.urban.content import CODT_Inquiry  # noqa
from Products.urban.content import CODT_UniqueLicenceInquiry  # noqa
from Products.urban.content import FollowUpEventType  # noqa
from Products.urban.content import Inquiry  # noqa
from Products.urban.content import UrbanEventAnnouncement  # noqa
from Products.urban.content import UrbanEventInquiry  # noqa
from Products.urban.content import UrbanEventInspectionReport  # noqa
from Products.urban.content import UrbanEventFollowUp  # noqa


def initialize(context):
    """initialize product (called by zope)"""
    ##code-section custom-init-top #fill in your manual code here
    ##/code-section custom-init-top
    # imports packages and types for registration
    import Applicant
    import City
    import Claimant
    import content.CODT_Inquiry
    import Contact
    import Corporation
    import Couple
    import EnvironmentRubricTerm
    import FolderManager
    import content.FollowUpEventType
    import content.Inquiry
    import LicenceConfig
    import Locality
    import OpinionRequestEventType
    import OrganisationTerm

    # [DX] TO DELETE > 2.5 [DX]
    import ParcellingTerm

    # [DX] TO DELETE > 2.5 [DX]
    import PcaTerm
    import PersonTitleTerm

    # [DX] TO DELETE > 2.5 [DX]
    import PortionOut

    # [DX] TO DELETE > 2.5 [DX]
    import Recipient
    import RecipientCadastre
    import SpecificFeatureTerm
    import Street
    import UrbanConfigurationValue
    import UrbanDelay
    import UrbanEvent
    import content.UrbanEventAnnouncement
    import content.UrbanEventInquiry
    import content.UrbanEventInspectionReport
    import content.UrbanEventFollowUp
    import UrbanEventOpinionRequest
    import UrbanEventType
    import UrbanTool
    import UrbanVocabularyTerm
    import content.licence.Article127
    import content.licence.BuildLicence
    import content.licence.CODT_Article127
    import content.licence.CODT_BuildLicence
    import content.licence.CODT_CommercialLicence
    import content.licence.CODT_IntegratedLicence
    import content.licence.CODT_ParcelOutLicence
    import content.licence.CODT_UniqueLicence
    import content.licence.CODT_UrbanCertificateTwo
    import content.licence.Declaration
    import content.licence.Division
    import content.licence.EnvClassThree
    import content.licence.EnvClassTwo
    import content.licence.EnvClassOne
    import content.licence.EnvClassBordering
    import content.licence.EnvironmentBase
    import content.licence.EnvironmentLicence
    import content.licence.GenericLicence
    import content.licence.IntegratedLicence
    import content.licence.MiscDemand
    import content.licence.ParcelOutLicence
    import content.licence.PatrimonyCertificate
    import content.licence.PreliminaryNotice
    import content.licence.ProjectMeeting
    import content.licence.UrbanCertificateBase
    import content.licence.UrbanCertificateTwo
    import content.licence.UniqueLicence
    import content.licence.ExplosivesPossession
    import content.licence.RoadDecree
    import ConfigTest

    # Initialize portal tools
    tools = [UrbanTool.UrbanTool]
    ToolInit(PROJECTNAME + " Tools", tools=tools, icon="tool.gif").initialize(context)

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME
    )

    cmfutils.ContentInit(
        PROJECTNAME + " Content",
        content_types=all_content_types,
        permission=DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors=all_constructors,
        fti=all_ftis,
    ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0, len(all_content_types)):
        klassname = all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(
            meta_type=all_ftis[i]["meta_type"],
            constructors=(all_constructors[i],),
            permission=ADD_CONTENT_PERMISSIONS[klassname],
        )

    ##code-section custom-init-bottom #fill in your manual code here
    ##/code-section custom-init-bottom


for licence_type in URBAN_TYPES + ["UrbanCertificateBase"]:
    if hasattr(content.licence, licence_type):
        alias_module(
            "Products.urban.{}".format(licence_type),
            getattr(content.licence, licence_type),
        )


def check_id(self, id, **kwargs):
    """
    'photo' id is reserved for image field 'photo'.
    """
    if id == "photo":
        return True  # MUST return True if id is invalid !! (and None if valid)
    if id in self.aq_parent.objectIds():
        return True


ATBlob.check_id = check_id
