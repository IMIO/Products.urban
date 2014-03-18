# -*- coding: utf-8 -*-
#
# File: UrbanEvent.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
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
        optional= True,
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
        vocabulary=UrbanVocabulary('decisions', inUrbanConfig=False),
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
        default_output_type='text/html',
        optional= True,
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
            available_indexes={'getFirstname':'First name','getSurname': 'Surname'},
            wild_card_search=True,
            label_msgid='urban_label_eventRecipient',
            i18n_domain='urban',
        ),
        allowed_types= ('Recipient','Applicant','Architect'),
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
        default_content_type='text/plain',
        default_method='getDefaultText',
        default_output_type='text/html',
        optional=True,
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
        default_output_type='text/html',
        optional=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEvent_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEvent(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEvent)

    meta_type = 'UrbanEvent'
    _at_rename_after_creation = True

    schema = UrbanEvent_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

registerType(UrbanEvent, PROJECTNAME)
# end of class UrbanEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer

