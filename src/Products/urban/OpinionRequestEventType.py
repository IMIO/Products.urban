# -*- coding: utf-8 -*-
#
# File: OpinionRequestEventType.py
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
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanEventType import UrbanEventType
from Products.urban.UrbanVocabularyTerm import UrbanVocabularyTerm
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

##code-section module-header #fill in your manual code here

slave_field_internal_service = (
    # applicant is either represented by a society or by another contact but not both at the same time
    {
        'name': 'internal_service',
        'action': 'show',
        'hide_values': (True, ),
    },
)
##/code-section module-header

schema = Schema((


    StringField(
        name='recipientSName',
        widget=StringField._properties['widget'](
            label='Recipientsname',
            label_msgid='urban_label_recipientSName',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='function_department',
        widget=StringField._properties['widget'](
            label='Function_department',
            label_msgid='urban_label_function_department',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='organization',
        widget=StringField._properties['widget'](
            label='Organization',
            label_msgid='urban_label_organization',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='dispatchSInformation',
        widget=StringField._properties['widget'](
            label='Dispatchsinformation',
            label_msgid='urban_label_dispatchSInformation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='typeAndStreetName_number_box',
        widget=StringField._properties['widget'](
            label='Typeandstreetname_number_box',
            label_msgid='urban_label_typeAndStreetName_number_box',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='postcode_locality',
        widget=StringField._properties['widget'](
            label='Postcode_locality',
            label_msgid='urban_label_postcode_locality',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='country',
        widget=StringField._properties['widget'](
            label='Country',
            label_msgid='urban_label_country',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='is_internal_service',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_field_internal_service,
            label='Is_internal_service',
            label_msgid='urban_label_is_internal_service',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='internal_service',
        widget=SelectionWidget(
            format='select',
            label='Internal_service',
            label_msgid='urban_label_internal_service',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        vocabulary='listInternalServices',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

OpinionRequestEventType_schema = OrderedBaseFolderSchema.copy() + schema.copy() + \
    getattr(UrbanEventType, 'schema', Schema(())).copy() + \
    getattr(UrbanVocabularyTerm, 'schema', Schema(())).copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class OpinionRequestEventType(OrderedBaseFolder, UrbanEventType, UrbanVocabularyTerm, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IOpinionRequestEventType)

    meta_type = 'OpinionRequestEventType'
    _at_rename_after_creation = True

    schema = OpinionRequestEventType_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listInternalServices')

    def listInternalServices(self):
        registry = api.portal.get_tool('portal_registry')
        registry_field = registry['Products.urban.interfaces.IInternalOpinionServices.services']
        voc_terms = [(key, value['full_name'][0]) for key, value in registry_field.iteritems()]
        vocabulary = DisplayList(voc_terms)
        return vocabulary


    security.declarePublic('getAddressCSV')
    def getAddressCSV(self):
        name = self.Title()
        lines = self.Description()[3:-4].split('<br />')
        description = lines[:-2]
        address = lines[-2:]
        return '%s|%s|%s|%s' % (name, ' '.join(description), address[0], address[1])



registerType(OpinionRequestEventType, PROJECTNAME)
# end of class OpinionRequestEventType

##code-section module-footer #fill in your manual code here
##/code-section module-footer

