# -*- coding: utf-8 -*-
#
# File: LicenceConfig.py
#
# Copyright (c) 2012 by CommunesPlone
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
##/code-section module-header

schema = Schema((

    LinesField(
        name='usedAttributes',
        widget=MultiSelectionWidget(
            description="Select the optional fields you want to use. Multiple selection or deselection when clicking with CTRL",
            description_msgid="urban_descr_usedAttributes",
            size=10,
            label='Usedattributes',
            label_msgid='urban_label_usedAttributes',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listUsedAttributes',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LicenceConfig_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
from BuildLicence import BuildLicence_schema
from ParcelOutLicence import ParcelOutLicence_schema
from Declaration import Declaration_schema
from Division import Division_schema
from UrbanCertificateBase import UrbanCertificateBase_schema
from UrbanCertificateTwo import UrbanCertificateTwo_schema
from EnvironmentalDeclaration import EnvironmentalDeclaration_schema
from MiscDemand import MiscDemand_schema
FTI_SCHEMAS = {
    'BuildLicence' : BuildLicence_schema,
    'ParcelOutLicence' : ParcelOutLicence_schema,
    'Declaration' : Declaration_schema,
    'Division' : Division_schema,
    'UrbanCertificateOne' : UrbanCertificateBase_schema,
    'UrbanCertificateTwo' : UrbanCertificateTwo_schema,
    'NotaryLetter' : UrbanCertificateBase_schema,
    'EnvironmentalDeclaration' : EnvironmentalDeclaration_schema,
    'MiscDemand' : MiscDemand_schema,
}

##/code-section after-schema

class LicenceConfig(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ILicenceConfig)

    meta_type = 'LicenceConfig'
    _at_rename_after_creation = True

    schema = LicenceConfig_schema

    ##code-section class-header #fill in your manual code here
    licence_portal_type = ''  #must be set on creation
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('listUsedAttributes')
    def listUsedAttributes(self):
        """
          Return the available optional fields
        """
        res = []
        abr = {
            'urban_peb':'(peb) ',
            'urban_location':'(urb) ',
            'urban_road':'(voi) ',
            'urban_investigation_and_advices':'(enq) ',
            'urban_description':'',
        }
        if not FTI_SCHEMAS.has_key(self.licence_portal_type):
            return DisplayList()
        for field in FTI_SCHEMAS[self.licence_portal_type].fields():
            if hasattr(field, 'optional'):
                tab = field.schemata
                if field.schemata in abr.keys():
                   tab = abr[tab]
                res.append((field.getName(), "%s%s" %(tab,
                    self.utranslate(field.widget.label_msgid, domain=field.widget.i18n_domain, default=field.widget.label))))
        return DisplayList(tuple(res)).sortedByValue()

    security.declarePublic('getIconURL')
    def getIconURL(self):
        portal_types = getToolByName(self, 'portal_types')
        if self.licence_portal_type and hasattr(portal_types, self.licence_portal_type):
            icon = "%s.png" % self.licence_portal_type
        else:
            icon = "LicenceConfig.png"
        portal_url = getToolByName( self, 'portal_url' )
        return portal_url() + '/' + icon



registerType(LicenceConfig, PROJECTNAME)
# end of class LicenceConfig

##code-section module-footer #fill in your manual code here
##/code-section module-footer

