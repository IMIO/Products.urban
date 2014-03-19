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
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.cfg.UrbanVocabularyTerm import UrbanVocabulary
from plone import api
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

    def getRecipients(self, theObjects=True, onlyActive=False):
        """
         Return the recipients of the UrbanEvent
        """
        queryString = {'portal_type': 'RecipientCadastre',
                       'path': '/'.join(self.getPhysicalPath())}
        if onlyActive:
            queryString['review_state'] = 'enabled'
        brains = self.portal_catalog(**queryString)
        if theObjects:
            return [brain.getObject() for brain in brains]
        return brains

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

    security.declarePublic('getParcels')
    def getParcels(self, onlyActive=False):
        """
          Returns the contained parcels
          Parcels in this container are created while calculating the "rayon de 50m"
          We can specify here that we only want active parcels because we can deactivate some proprietaries
        """
        catalog = api.portal.get_tool('portal_catalog')
        urban_tool = api.portal.get_tool('portal_urban')
        queryString = {
            'portal_type': 'PortionOut',
            'path': {'query': '/'.join(urban_tool.getPhysicalPath()), 'depth': 2},
            'sort_on': 'getObjPositionInParent'
        }
        if onlyActive:
            #only take active RecipientCadastre paths into account
            activeRecipients = self.getRecipients(theObjects=False, onlyActive=True)
            paths = [activeRecipient.getPath() for activeRecipient in activeRecipients]
            queryString.update({'path': {'query': paths, 'depth': 2}})

        parcel_brains = catalog(**queryString)
        parcels = [brain.getObject() for brain in parcel_brains]

        return parcels

    security.declarePublic('getAbbreviatedArticles')
    def getAbbreviatedArticles(self):
        """
          As we have a short version of the article in the title, if we need just
          the list of articles (330 1°, 330 2°, ...) we will use the extraValue of the Vocabulary term
        """
        return self.displayValue(UrbanVocabulary('investigationarticles', value_to_use="extraValue").getDisplayList(self), self.getLinkedInquiry().getInvestigationArticles())



registerType(UrbanEventInquiry, PROJECTNAME)
# end of class UrbanEventInquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

