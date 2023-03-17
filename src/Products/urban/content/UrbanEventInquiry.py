# -*- coding: utf-8 -*-
#
# File: UrbanEventInquiry.py
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
from Products.urban import interfaces
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from OFS.ObjectManager import BeforeDeleteException
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from plone import api

suspension_slave_fields = (
    {
        'name': 'suspension_period',
        'action': 'show',
        'hide_values': (True,),
    },
)
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='investigationStart',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1930,
            label=_('urban_label_investigationStart',
                    default='Investigationstart'),
        ),
    ),
    DateTimeField(
        name='investigationEnd',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1930,
            label=_('urban_label_investigationEnd',
                    default='Investigationend'),
        ),
        validators=('isValidInvestigationEnd',),
    ),
    DateTimeField(
        name='explanationStartSDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            format="%d/%m/%Y %H:%M",
            starting_year=1930,
            label=_('urban_label_explanationStartSDate',
                    default='Explanationstartsdate'),
        ),
        optional=True,
    ),
    DateTimeField(
        name='explanationEndSDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            format="%d/%m/%Y %H:%M",
            starting_year=1930,
            label=_('urban_label_explanationEndSDate',
                    default='Explanationendsdate'),
        ),
        optional=True,
    ),
    DateTimeField(
        name='claimsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            format="%d/%m/%Y %H:%M",
            starting_year=1930,
            label=_('urban_label_claimsDate', default='Claimsdate'),
        ),
        optional=True,
    ),
    DateTimeField(
        name='claimEndSDate',
        widget=DateTimeField._properties['widget'](
            show_hm=True,
            format="%d/%m/%Y %H:%M",
            starting_year=1930,
            label=_('urban_label_claimEndSDate', default='Claimendsdate'),
        ),
        optional=True,
    ),
    TextField(
        name='claimsText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_claimsText', default='Claimstext'),
        ),
        default_method='getDefaultText',
        default_output_type='text/x-html-safe',
        optional=True,
    ),
    DateTimeField(
        name='concertationDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1930,
            label=_('urban_label_concertationDate',
                    default='Concertationdate'),
        ),
        optional=True,
    ),
    BooleanField(
        name='suspension',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=suspension_slave_fields,
            label=_('urban_label_suspension', default='Suspension'),
        ),
        optional=True,
    ),
    StringField(
        name='suspension_period',
        widget=SelectionWidget(
            format='select',
            label=_('urban_label_suspension_period',
                    default='Suspension_period'),
        ),
        optional=True,
        vocabulary=UrbanVocabulary(
            'inquiry_suspension',
            vocType="UrbanVocabularyTerm",
            inUrbanConfig=False,
            with_empty_value=True
        ),
        default_method='getDefaultValue',
    ),
    ReferenceField(
        name='linkedInquiry',
        widget=ReferenceBrowserWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
            label=_('urban_label_linkedInquiry',
                    default='Linkedinquiry'),
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
UrbanEventInquiry_schema['eventDate'].widget.visible['edit'] = 'invisible'
UrbanEventInquiry_schema['eventDate'].widget.visible['view'] = 'invisible'
##/code-section after-schema


class UrbanEventInquiry(BaseFolder, UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventInquiry)

    meta_type = 'UrbanEventInquiry'
    _at_rename_after_creation = False

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
            'portal_type': 'Parcel',
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

    def getKeyDate(self):
        return self.getInvestigationStart()

    def getNumberOfOralComplaint(self):
        claimants = self.getClaimants()
        number = 0
        for claimant in claimants:
            if claimant.isOralComplaint():
                number += 1
        return number

    def getNumberOfWrittenComplaint(self):
        claimants = self.getClaimants()
        number = 0
        for claimant in claimants:
            if claimant.isWrittenComplaint():
                number += 1
        return number

    def getNumberOfPetition(self):
        claimants = self.getClaimants()
        number = 0
        for claimant in claimants:
            if claimant.isPetition():
                number += 1
        return number

    def getNumberOfSignature(self):
        claimants = self.getClaimants()
        number = 0
        for claimant in claimants:
            if claimant.hasSignatureComplaint():
                number += claimant.getSignatureNumber()
        return number


registerType(UrbanEventInquiry, PROJECTNAME)
# end of class UrbanEventInquiry
