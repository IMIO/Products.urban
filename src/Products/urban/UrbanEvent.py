# -*- coding: utf-8 -*-
#
# File: UrbanEvent.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from DateTime import DateTime

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.ATContentTypes.interfaces.file import IATFile
from Products.CMFCore.utils import getToolByName

from Products.urban.interfaces import IUrbanDoc
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes

from plone import api

from zope.i18n import translate
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='eventDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label_method="eventDateLabel",
            starting_year=1960,
            label='Eventdate',
            label_msgid='urban_label_eventDate',
            i18n_domain='urban',
        ),
        default_method='getDefaultTime',
    ),
    StringField(
        name='depositType',
        widget=SelectionWidget(
            label='Deposittype',
            label_msgid='urban_label_depositType',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('deposittype', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    DateTimeField(
        name='transmitDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Transmitdate',
            label_msgid='urban_label_transmitDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='transmitToClaimantsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Transmittoclaimantsdate',
            label_msgid='urban_label_transmitToClaimantsDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='receiptDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Receiptdate',
            label_msgid='urban_label_receiptDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='receivedDocumentReference',
        widget=StringField._properties['widget'](
            label='Receiveddocumentreference',
            label_msgid='urban_label_receivedDocumentReference',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='auditionDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Auditiondate',
            label_msgid='urban_label_auditionDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='decisionDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Decisiondate',
            label_msgid='urban_label_decisionDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='decision',
        widget=SelectionWidget(
            label='Decision',
            label_msgid='urban_label_decision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('decisions', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='decisionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Decisiontext',
            label_msgid='urban_label_decisionText',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
    ),
    DateTimeField(
        name='recourseDecisionDisplayDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Recoursedecisiondisplaydate',
            label_msgid='urban_label_recourseDecisionDisplayDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='recourseDecision',
        widget=SelectionWidget(
            label='Recoursedecision',
            label_msgid='urban_label_recourseDecision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('recoursedecisions', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    StringField(
        name='adviceAgreementLevel',
        widget=SelectionWidget(
            format='select',
            label='Adviceagreementlevel',
            label_msgid='urban_label_adviceAgreementLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary='listAdviceAgreementLevels',
    ),
    BooleanField(
        name='isOptional',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isoptional',
            label_msgid='urban_label_isOptional',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='externalDecision',
        widget=SelectionWidget(
            label='Externaldecision',
            label_msgid='urban_label_externalDecision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('externaldecisions', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    TextField(
        name='opinionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Opiniontext',
            label_msgid='urban_label_opinionText',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
    ),
    TextField(
        name='analysis',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Analysisi',
            label_msgid='urban_label_analysis',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
    ),
    ReferenceField(
        name='eventRecipient',
        widget=ReferenceBrowserWidget(
            label='Destinataire',
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'getFirstname': 'First name', 'getSurname': 'Surname'},
            wild_card_search=True,
            label_msgid='urban_label_eventRecipient',
            i18n_domain='urban',
        ),
        allowed_types= ('Recipient', 'Applicant', 'Architect'),
        optional=True,
        relationship="recipients",
    ),
    ReferenceField(
        name='urbaneventtypes',
        widget=ReferenceBrowserWidget(
            visible=False,
            label='Urbaneventtypes',
            label_msgid='urban_label_urbaneventtypes',
            i18n_domain='urban',
        ),
        allowed_types=('UrbanEventType', 'OpinionRequestEventType'),
        multiValued=0,
        relationship='UrbanEventType',
    ),
    TextField(
        name='pmTitle',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Pmtitle',
            label_msgid='urban_label_pmTitle',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/plain',
        optional=True,
        pm_text_field=True,
    ),
    TextField(
        name='pmDescription',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pmdescription',
            label_msgid='urban_label_pmDescription',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
        pm_text_field=True,
    ),
    TextField(
        name='pmMotivation',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pmmotivation',
            label_msgid='urban_label_pmMotivation',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
        pm_text_field=True,
    ),
    TextField(
        name='pmDecision',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pmdecision',
            label_msgid='urban_label_pmDecision',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
        pm_text_field=True,
    ),
    TextField(
        name='officeCoordinate',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Officecoordinate',
            label_msgid='urban_label_officeCoordinate',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional= True,
    ),
    TextField(
        name='suspensionReason',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Suspensionreason',
            label_msgid='urban_label_suspensionReason',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/html',
        optional=True,
    ),
    DateTimeField(
        name='suspensionEndDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='suspensionEndDate',
            label_msgid='urban_label_suspensionEndDate',
            i18n_domain='urban',
        ),
        optional= True,
    ),
    StringField(
        name='delegateSignatures',
        widget=SelectionWidget(
            format='radio',
            label='Delegatesignatures',
            label_msgid='urban_label_delegateSignatures',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('delegatesignatures', inUrbanConfig=False),
        default_method='getDefaultValue',
    ),
    StringField(
        name='bank_account',
        widget=StringField._properties['widget'](
            label='Bank_account',
            label_msgid='urban_label_bank_account',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='bank_account_owner',
        widget=StringField._properties['widget'](
            label='Bank_account_owner',
            label_msgid='urban_label_bank_account_owner',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='amount_collected',
        widget=StringField._properties['widget'](
            label='Amount_collected',
            label_msgid='urban_label_amount_collected',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='displayDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Displaydate',
            label_msgid='urban_label_displayDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
optional_fields = [field.getName() for field in schema.filterFields(isMetadata=False) if field.getName() != 'eventDate']
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanEvent_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanEvent_schema['title'].widget.condition = "python:here.showTitle()"
##/code-section after-schema


class UrbanEvent(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEvent)

    meta_type = 'UrbanEvent'
    _at_rename_after_creation = True
    __ac_local_roles_block__ = True

    schema = UrbanEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getDefaultValue')

    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return ['']

        urban_tool = api.portal.get_tool('portal_urban')

        default_value = urban_tool.getVocabularyDefaultValue(
            vocabulary=field.vocabulary or field.vocabulary_factory,
            context=context,
            multivalued=field.multiValued
        )
        return default_value

    security.declarePublic('getDefaultText')

    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = getToolByName(self, 'portal_urban')
        return urban_tool.getTextDefaultValue(field.getName(), context, html=html, config=self.getUrbaneventtypes())

    def getKeyDate(self):
        return self.getEventDate()

    def getDefaultTime(self):
        return DateTime()

    security.declarePublic('getTemplates')
    def getTemplates(self):
        """
          Returns contained templates (File)
        """
        return self.getUrbaneventtypes().getTemplates()

    security.declarePublic('eventDateLabel')
    def eventDateLabel(self):
        """
         Returns the variable label
        """
        return self.getUrbaneventtypes().getEventDateLabel()

    security.declarePublic('listAdviceAgreementLevels')
    def listAdviceAgreementLevels(self):
        """
          Vocabulary for field 'adviceAgreementLevels'
        """
        lst=[
             ['agreementlevel_read_advice', translate('agreementlevel_read_advice', 'urban', context=self.REQUEST, default="Read advice")],
             ['agreementlevel_respect_charges', translate('agreementlevel_respect_charges', 'urban', context=self.REQUEST, default="Respect charges")],
            ]

        vocab = []
        #we add an empty vocab value of type "choose a value"
        val = translate('urban', EMPTY_VOCAB_VALUE, context=self, default=EMPTY_VOCAB_VALUE)
        vocab.append(('', val))
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('isInt')
    def isInt(self, s):
        """
          Check if 's' is an integer, return True or False...
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    security.declarePublic('parseCadastreStreet')
    def parseCadastreStreet(self, street):
        """
           Return a parsed version of data from Cadastre so we obtain something
           more beautiful to display
        """
        if street == None:
            return 'NO ADDRESS FOUND'
        print '\n\n Street: '+street
        i=0
        toreturn=''
        while (i < len(street)) and (street[i] !=','):
            toreturn=toreturn+street[i]
            i=i+1
        if i < len(street):
            while (i<len(street)) and (not self.isInt(street[i])):
                i=i+1
            toreturn=toreturn+' '
        while i < len(street):
            toreturn=toreturn+street[i]
            i=i+1
        return toreturn

    security.declarePublic('parseCadastreName')
    def parseCadastreName(self, name):
        """
        """
        print '\n\nName: '+name
        i=0
        nom1=''
        prenom1=''
        nom2=''
        prenom2=''
        toreturn=''
        if name.rfind(',') > 0:
            while (i<len(name)) and (name[i] != ','):
                nom1=nom1+name[i]
                i=i+1
            if i<len(name):
                i=i+1
            while (i<len(name)) and (name[i] != ' '):
                i=i+1
            if i<len(name):
                i=i+1
            while (i<len(name)) and (name[i] not in ['&', ' ']):
                prenom1=prenom1+name[i]
                i=i+1
            if i<len(name) and name[i] != '&':
                i=i+1
            toreturn=prenom1
            if prenom1!='':
                toreturn=toreturn+' '
            toreturn=toreturn+nom1
            if name.rfind('&') > 0 and i < name.rfind('&'):
                while (i<len(name)) and (name[i] != '&'):
                    i=i+1
                if name[i]=='&':
                    toreturn=toreturn+' - M. '
                    i=i+1
                while (i<len(name)) and (name[i] != ','):
                    nom2=nom2+name[i]
                    i=i+1
                if i<len(name):
                    i=i+1
                while (i<len(name)) and (name[i] != ' '):
                    i=i+1
                if i<len(name):
                    i=i+1
                while (i<len(name)) and (name[i] != ' '):
                    prenom2=prenom2+name[i]
                    i=i+1
                toreturn=toreturn+prenom2
                if prenom2 != '':
                    toreturn=toreturn+' '
                toreturn=toreturn+nom2
        else:
            toreturn=name
        return 'M. %s' % toreturn

    security.declarePublic('getDocuments')
    def getDocuments(self):
        """
          Return the documents (File) of the UrbanEvent
        """
        documents = [obj for obj in self.objectValues() if IUrbanDoc.providedBy(obj)]
        return documents

    security.declarePublic('getAttachments')
    def getAttachments(self):
        """
          Return the attachments (File) of the UrbanEvent
        """
        def is_attachment(obj):
            return IATFile.providedBy(obj) and not IUrbanDoc.providedBy(obj)

        attachments = [obj for obj in self.objectValues() if is_attachment(obj)]
        return attachments

    def getRecipients(self):
        """
          Returns a list of recipients
        """
        return self.objectValues('RecipientCadastre')

    security.declarePublic('RecipientsCadastreCSV')
    def RecipientsCadastreCSV(self):
        """
          Generates a fake CSV file used in POD templates
        """
        recipients=self.objectValues('RecipientCadastre')
        toreturn='[CSV]TitreNomPrenom|AdresseLigne1|AdresseLigne2'
        wft = getToolByName(self, 'portal_workflow')
        for recipient in recipients:
            #do not take "disabled" recipients into account
            if wft.getInfoFor(recipient, 'review_state') == 'disabled':
                continue
            street = recipient.getStreet() and recipient.getStreet() or ''
            address = recipient.getAdr1() and recipient.getAdr1() or ''
            toreturn=toreturn+'%'+recipient.getName()+'|'+street+'|'+address
        toreturn=toreturn+'[/CSV]'
        return toreturn

    security.declarePublic('getFormattedDate')
    def getFormattedDate(self, date=None, withCityNamePrefix=False, forDelivery=False, translatemonth=True):
        """
          Return the date
          withCityNamePrefix and forDelivery are exclusive in the logic here above
        """
        if not date:
            date = self.getEventDate()
        elif type(date) == str:
            date = self.getField(date).getAccessor(self)()
        tool = getToolByName(self, 'portal_urban')
        formattedDate = tool.formatDate(date, translatemonth=translatemonth)
        cityName = unicode(tool.getCityName(), 'utf-8')
        if withCityNamePrefix:
            return translate('formatted_date_with_cityname', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
        if forDelivery:
            return translate('formatted_date_for_delivery', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
        return formattedDate

    def attributeIsUsed(self, attrName):
        """
        """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return attrName in self.getUrbaneventtypes().getActivatedFields()
        else:
            return False

    def showTitle(self):
        """
        """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return urbanEventType.getShowTitle()
        else:
            return False

    security.declarePublic('getDecision')
    def getDecision(self, theObject=False):
        """
          Returns the decision value or the UrbanVocabularyTerm if theObject=True
        """
        res = self.getField('decision').get(self)
        if res and theObject:
            tool = getToolByName(self, 'portal_urban')
            res = getattr(tool.decisions, res)
        return res


registerType(UrbanEvent, PROJECTNAME)
# end of class UrbanEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer

