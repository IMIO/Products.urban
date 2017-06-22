# -*- coding: utf-8 -*-
#
# File: Inquiry.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFCore.utils import getToolByName
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from collective.archetypes.select2.select2widget import Select2Widget

optional_fields = [
    'derogationDetails', 'investigationDetails', 'investigationReasons',
    'investigationArticlesText', 'investigationArticles', 'demandDisplay',
    'derogation', 'derogationDetails', 'roadModificationSubject'
]
##/code-section module-header

schema = Schema((

    LinesField(
        name='derogation',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Derogation',
            label_msgid='urban_label_derogation',
            i18n_domain='urban',
        ),
        multiValued=1,
        vocabulary=UrbanVocabulary('derogations'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='derogationDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Derogationdetails',
            label_msgid='urban_label_derogationDetails',
            i18n_domain='urban',
        ),
        default_output_type='text/plain',
        default_content_type='text/plain',
        default_method='getDefaultText',
    ),
    LinesField(
        name='investigationArticles',
        widget=MultiSelectionWidget(
            size=10,
            label='Investigationarticles',
            label_msgid='urban_label_investigationArticles',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary=UrbanVocabulary('investigationarticles'),
        default_method='getDefaultValue',
    ),
    TextField(
        name='investigationArticlesText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Investigationarticlestext',
            label_msgid='urban_label_investigationArticlesText',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        default_output_type='text/html',
    ),
    DateTimeField(
        name='demandDisplay',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label='Demanddisplay',
            label_msgid='urban_label_demandDisplay',
            i18n_domain='urban',
        ),
    ),
    TextField(
        name='investigationDetails',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Investigationdetails',
            label_msgid='urban_label_investigationDetails',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        default_output_type='text/html',
    ),
    TextField(
        name='investigationReasons',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Investigationreasons',
            label_msgid='urban_label_investigationReasons',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        default_output_type='text/html',
    ),
    TextField(
        name='roadModificationSubject',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Roadmodificationsubject',
            label_msgid='urban_label_roadModificationSubject',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        default_output_type='text/html',
    ),
    LinesField(
        name='solicitOpinionsTo',
        widget=Select2Widget(
            label='Solicitopinionsto',
            label_msgid='urban_label_solicitOpinionsTo',
            i18n_domain='urban',
            multiple=True,
        ),
        schemata='urban_advices',
        multiValued=1,
        vocabulary=UrbanVocabulary('urbaneventtypes', vocType="OpinionRequestEventType", value_to_use='extraValue'),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='solicitOpinionsToOptional',
        widget=Select2Widget(
            label='Solicitopinionstooptional',
            label_msgid='urban_label_solicitOpinionsToOptional',
            i18n_domain='urban',
            multiple=True,
        ),
        schemata='urban_advices',
        multiValued=1,
        vocabulary=UrbanVocabulary('urbaneventtypes', vocType="OpinionRequestEventType", value_to_use='extraValue'),
        default_method='getDefaultValue',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Inquiry_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Inquiry_schema['title'].widget.visible = False
#implicitly rmove the not used description field because it is defined with default
#values that are wrong for BuildLicence that heritates from self and GenericLicence
#GenericLicence redefines 'description' and self too...  See ticket #3502
del Inquiry_schema['description']
##/code-section after-schema

class Inquiry(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IInquiry)

    meta_type = 'Inquiry'
    _at_rename_after_creation = True

    schema = Inquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getDefaultValue')
    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return ['']
        urban_tool = getToolByName(self, 'portal_urban')

        default_value = urban_tool.getVocabularyDefaultValue(
            vocabulary=field.vocabulary or field.vocabulary_factory,
            context=context,
            multivalued=field.multiValued,
        )
        return default_value

    security.declarePublic('getDefaultText')
    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = getToolByName(self, 'portal_urban')
        return urban_tool.getTextDefaultValue(field.getName(), context, html=html)

    security.declarePrivate('manage_beforeDelete')
    def manage_beforeDelete(self, item, container):
        """
          We can not remove an Inquiry if a linked UrbanEventInquiry exists
        """
        linkedUrbanEventInquiry = self.getLinkedUrbanEventInquiry()
        if linkedUrbanEventInquiry:
            raise BeforeDeleteException, 'cannot_remove_inquiry_linkedurbaneventinquiry'
        BaseContent.manage_beforeDelete(self, item, container)

    security.declarePublic('getLinkedUrbanEventInquiry')
    def getLinkedUrbanEventInquiry(self):
        """
          Return the linked UrbanEventInquiry object if exists
        """
        brefs = self.getBRefs('linkedInquiry')
        if brefs:
            #linkedInquiry may come from a UrbanEventInquiry or an UrbanEventOpinionRequest
            for bref in brefs:
                if bref and bref.portal_type == 'UrbanEventInquiry':
                    return bref
        else:
            return None

    security.declarePublic('getCustomInvestigationArticles')
    def getCustomInvestigationArticles(self):
        items = []
        for article in self.getInvestigationArticles():
            if self.displayValue(UrbanVocabulary('investigationarticles').getDisplayList(self), article):
                items.append(self.displayValue(UrbanVocabulary('investigationarticles').getDisplayList(self), article))
        return items

    security.declarePublic('getLinkedUrbanEventOpinionRequest')
    def getLinkedUrbanEventOpinionRequest(self, organisation):
        """
          Return the linked UrbanEventOpinionRequest objects if exist
        """
        brefs = self.getBRefs('linkedInquiry')
        if brefs:
            #linkedInquiry may come from a UrbanEventInquiry or an UrbanEventOpinionRequest
            for bref in brefs:
                if bref.portal_type == 'UrbanEventOpinionRequest':
                    if bref.getLinkedOrganisationTermId() == organisation and bref.getLinkedInquiry() == self:
                        return bref
        return None

    def _getSelfPosition(self):
        """
          Return the position of the self between every Inquiry objects
        """
        #get the existing Inquiries
        #getInquiries is a method of GenericLicence
        #so by acquisition, we get it on the parent or we get it on self
        #as GenericLicence heritates from Inquiry
        inquiries = self.getInquiries()
        selfUID = self.UID()
        i = 0
        for inquiry in inquiries:
            if inquiry.UID() == selfUID:
                break
            i = i + 1
        return i

    security.declarePublic('generateInquiryTitle')
    def generateInquiryTitle(self):
        """
          Generates a title for the inquiry
        """
        #we need to generate the title as the number of the inquiry is into it
        position = self._getSelfPosition()
        return translate('inquiry_title_and_number', 'urban', mapping={'number': position + 1}, context=self.REQUEST)

    security.declarePublic('getInquiries')
    def getInquiries(self):
        """
        Returns the existing inquiries
        """
        return self._get_inquiry_objs(all_=False)

    security.declarePublic('getAllInquiries')
    def getAllInquiries(self):
        """
        Returns the existing inquiries
        """
        return self._get_inquiry_objs(all_=True)

    def _get_inquiry_objs(self, all_=False):
        """
        Returns the existing inquiries or announcements
        """
        all_inquiries = []
        other_inquiries = self.objectValues('Inquiry')
        if all_ or other_inquiries:
            all_inquiries.append(self)
        all_inquiries.extend(list(other_inquiries))
        return all_inquiries

    security.declarePublic('getUrbanEventInquiries')
    def getUrbanEventInquiries(self):
        """
          Returns the existing UrbanEventInquiries
        """
        return self.listFolderContents({'portal_type': 'UrbanEventInquiry'})

    def getLastInquiry(self, use_catalog=True):
        return self._getLastEvent(interfaces.IInquiryEvent, use_catalog=use_catalog)

    def getLastOpinionRequest(self):
        return self._getLastEvent(interfaces.IOpinionRequestEvent)

    def getAllTechnicalServiceOpinionRequests(self):
        return self._getAllEvents(interfaces.ITechnicalServiceOpinionRequestEvent)

    security.declarePublic('getSolicitOpinionValue')
    def getSolicitOpinionValue(self, opinionId):
        """
          Return the corresponding opinion value from the given opinionId
        """
        return self.Vocabulary('solicitOpinionsTo')[0].getValue(opinionId)

    security.declarePublic('getSolicitOpinionOptionalValue')
    def getSolicitOpinionOptionalValue(self, opinionId):
        """
          Return the corresponding opinion value from the given opinionId
        """
        return self.Vocabulary('solicitOpinionsToOptional')[0].getValue(opinionId)

    security.declarePublic('mayAddOpinionRequestEvent')
    def mayAddOpinionRequestEvent(self, organisation):
        """
           This is used as TALExpression for the UrbanEventOpinionRequest
           We may add an OpinionRequest if we asked one in an inquiry on the licence
           We may add another if another inquiry defined on the licence ask for it and so on
        """
        opinions = self.getSolicitOpinionsTo()
        opinions += self.getSolicitOpinionsToOptional()
        limit = organisation in opinions and 1 or 0
        inquiries = [inq for inq in self.getInquiries() if inq != self]
        for inquiry in inquiries:
            if organisation in inquiry.getSolicitOpinionsTo() or organisation in inquiry.getSolicitOpinionsToOptional():
                limit += 1
        limit = limit - len(self.getOpinionRequests(organisation))
        return limit > 0

    security.declarePublic('mayAddInquiryEvent')
    def mayAddInquiryEvent(self):
        """
           This is used as TALExpression for the UrbanEventInquiry
           We may add an inquiry if we defined one on the licence
           We may add another if another is defined on the licence and so on
        """
        #first of all, we can add an InquiryEvent if an inquiry is defined on the licence at least
        inquiries = self.getAllInquiries()
        urbanEventInquiries = self.getUrbanEventInquiries()
        #if we have only the inquiry defined on the licence and no start date is defined
        #it means that no inquiryEvent can be added because no inquiry is defined...
        #or if every UrbanEventInquiry have already been added
        if len(urbanEventInquiries) >= len(inquiries):
            return False
        return True

    def getAllTechnicalServiceOpinionRequestsNoDup(self):
        allOpinions = self.getAllTechnicalServiceOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor] = opinion
        return allOpinionsNoDup.values()

    def getAllOpinionRequests(self, organisation=""):
        if organisation == "":
            return self._getAllEvents(interfaces.IOpinionRequestEvent)
        catalog = getToolByName(self, 'portal_catalog')
        query = {'path': {'query': self.absolute_url_path(),
                          'depth': 1},
                 'object_provides': IOpinionRequestEvent.__identifier__,
                 'sort_on': 'getObjPositionInParent',
                 'id': organisation.lower()}
        return [brain.getObject() for brain in catalog(**query)]

    def getAllOpinionRequestsNoDup(self):
        allOpinions = self.getAllOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor] = opinion
        return allOpinionsNoDup.values()

    def getAllInquiryEvents(self):
        return self._getAllEvents(interfaces.IInquiryEvent)

    def getAllClaimsTexts(self):
        claimsTexts = []
        for inquiry in self.getAllInquiryEvents():
            text = inquiry.getClaimsText()
            if text is not "":
                claimsTexts.append(text)
        return claimsTexts

    security.declarePublic('getFolderMakersCSV')
    def getFolderMakersCSV(self):
        """
          Returns a formatted version of the folder maker address to be used in POD templates
        """
        urban_tool = getToolByName(self, 'portal_urban')
        foldermakers_config = urban_tool.getUrbanConfig(self).urbaneventtypes
        foldermakers = [fm for fm in foldermakers_config.objectValues('OpinionRequestEventType') if fm.id in self.getSolicitOpinionsTo()]
        toreturn = '[CSV]Nom|Description|AdresseLigne1|AdresseLigne2'
        for foldermaker in foldermakers:
            toreturn = toreturn + '%' + foldermaker.getAddressCSV()
        toreturn = toreturn + '[/CSV]'
        return toreturn



registerType(Inquiry, PROJECTNAME)
# end of class Inquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer

