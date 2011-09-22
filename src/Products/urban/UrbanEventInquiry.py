# -*- coding: utf-8 -*-
#
# File: UrbanEventInquiry.py
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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFPlone import PloneMessageFactory as _
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
        default=claimsTextDefaultValue,
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
        allowed_types=('Inquiry', 'GenericLicence', 'UrbanCertificateTwo'),
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

    # Manually created methods

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """
          We can only remove the last UrbanEventInquiry to avoid mismatch between
          existing inquiries and UrbanEventInquiries
        """
        existingUrbanEventInquiries = self.getUrbanEventInquiries()
        lastUrbanEventInquiry = existingUrbanEventInquiries[-1]
        #if the user is not removing the last UrbanEventInquiry, we raise!
        if not lastUrbanEventInquiry.UID() == self.UID():
            raise BeforeDeleteException, _('cannot_remove_urbaneventinquiry_notthelast', mapping={'lasturbaneventinquiryurl': lastUrbanEventInquiry.absolute_url()}, default="You can not delete an UrbanEventInquiry if it is not the last!  Remove the last UrbanEventInquiries before being able to remove this one!")
        BaseFolder.manage_beforeDelete(self, item, container)

    security.declarePublic('getClaimants')
    def getClaimants(self):
        """
          Return the claimants for this UrbanEventInquiry
        """
        return self.listFolderContents({'portal_type': 'Claimant'})

    security.declarePublic('getMultipleClaimantsCSV')
    def getMultipleClaimantsCSV(self):
        """
          Returns a formatted version of the claimants to be used in POD templates
        """
        claimants = self.getClaimants()
        toreturn = '<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for claimant in claimants:
            toreturn = toreturn + '%' + claimant.getPersonTitleValue() + '|' + claimant.getName1() + '|' +\
                    claimant.getName2() + '|' + claimant.getNumber() + ', ' + claimant.getStreet() + '|' +\
                    claimant.getZipcode() + ' ' + claimant.getCity()
        toreturn = toreturn + '</CSV>'
        return toreturn



registerType(UrbanEventInquiry, PROJECTNAME)
# end of class UrbanEventInquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

