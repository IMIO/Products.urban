# -*- coding: utf-8 -*-
#
# File: UrbanVocabularyTerm.py
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
from Products.urban.UrbanConfigurationValue import UrbanConfigurationValue
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from plone import api
from plone.app.referenceintegrity.interfaces import IReferenceableVocabulary

import re
import logging

logger = logging.getLogger('urban: UrbanVocabularyTerm')
##/code-section module-header

schema = Schema((

    TextField(
        name='description',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            description="""If this field is used, you can insert special expressions between [[]] that will be rendered.  This can be something like "My text [[object/getMyAttribute]] end of the text".  Object is the licence the term is used in.""",
            label='Description',
            label_msgid='urban_label_description',
            description_msgid='urban_help_description',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        accessor="Description",
    ),
    StringField(
        name='numbering',
        widget=StringField._properties['widget'](
            description="Use this field to add a custom numbering that will be shown in edit forms but not on document render.",
            label='Numbering',
            label_msgid='urban_label_numbering',
            description_msgid='urban_help_numbering',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='extraValue',
        widget=StringField._properties['widget'](
            description="This field is made to store extra value if needed.",
            label='Extravalue',
            label_msgid='urban_label_extraValue',
            description_msgid='urban_help_extraValue',
            i18n_domain='urban',
        ),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanVocabularyTerm_schema = BaseSchema.copy() + \
    getattr(UrbanConfigurationValue, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanVocabularyTerm_schema['title'].label_msgid = "urban_label_termTitle"
UrbanVocabularyTerm_schema['title'].i18n_domain = "urban"
##/code-section after-schema

class UrbanVocabularyTerm(BaseContent, UrbanConfigurationValue, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanVocabularyTerm)

    meta_type = 'UrbanVocabularyTerm'
    _at_rename_after_creation = True

    schema = UrbanVocabularyTerm_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getFormattedDescription')
    def getAddress(self):
        """
          get the address
        """
        address = ''
        if self.getRecipientSName():
            address += self.getRecipientSName()
        if self.getFunction_department():
            address += '\n' + self.getFunction_department()
        if self.getOrganization():
            address += '\n' + self.getOrganization()
        if self.getDispatchSInformation():
            address += '\n' + self.getDispatchSInformation()
        if self.getTypeAndStreetName_number_box():
            address += '\n' + self.getTypeAndStreetName_number_box()
        if self.getPostcode_locality():
            address += '\n' + self.getPostcode_locality()
        if self.getCountry():
            address += '\n' + self.getCountry()
        return address

    security.declarePublic('getFormattedDescription')
    def getFormattedDescription(self, linebyline=True, prefix=''):
        """
          This method can get the description in different formats
        """
        descr = self.Description().strip()
        #add prefix only if description isn't empty
        #    or is different from code like "<p> </p>" ??
        if descr and prefix:
            descr = prefix + descr
        if linebyline:
            return descr
        else:
            #we need to make a single string with everything we have in the HTML description
            return re.sub(r'<[^>]*?>', ' ', descr).replace('  ', ' ')

    security.declarePublic('getRenderedDescription')
    def getRenderedDescription(self, obj, renderToNull=False):
        """
          see renderText method of UrbanTool
        """
        portal_urban = api.portal.get_tool('portal_urban')
        return portal_urban.renderText(text=self.Description(), context=obj, renderToNull=renderToNull)



registerType(UrbanVocabularyTerm, PROJECTNAME)
# end of class UrbanVocabularyTerm

##code-section module-footer #fill in your manual code here
class UrbanVocabulary(object):

    implements(IReferenceableVocabulary)

    def __init__(self, path, vocType="UrbanVocabularyTerm", id_to_use="id", value_to_use="Title", sort_on="getObjPositionInParent", inUrbanConfig=True, allowedStates=['enabled'], with_empty_value=False, datagridfield_key='street'):
        self.path = path
        self.vocType = vocType
        self.id_to_use = id_to_use
        self.value_to_use = value_to_use
        self.sort_on = sort_on
        self.inUrbanConfig = inUrbanConfig
        self.allowedStates = allowedStates
        self.with_empty_value = with_empty_value
        self.datagridfield_key = datagridfield_key

    def getDisplayList(self, content_instance):
        portal_urban = api.portal.get_tool('portal_urban')
        result = DisplayList(portal_urban.listVocabulary(self.path,
            content_instance, vocType=self.vocType, id_to_use=self.id_to_use, value_to_use=self.value_to_use, sort_on=self.sort_on,\
            inUrbanConfig=self.inUrbanConfig, allowedStates=self.allowedStates, with_empty_value=self.with_empty_value))
        return result

    def getDisplayListForTemplate(self, content_instance):
        portal_urban = api.portal.get_tool('portal_urban')
        result = DisplayList(portal_urban.listVocabulary(self.path,
            content_instance, vocType=self.vocType, id_to_use=self.id_to_use, value_to_use=self.value_to_use, sort_on=self.sort_on,\
            inUrbanConfig=self.inUrbanConfig, allowedStates=self.allowedStates, with_empty_value=self.with_empty_value, with_numbering=False))
        return result

    def getObjectsSet(self, content_instance, values):
        if isinstance(values, str):
            values = (values,)
        objects = self.getAllVocTerms(content_instance)
        result = set()
        for value in values:
            if type(value) == dict:
                value = value[self.datagridfield_key]
            obj = objects.get(value, None)
            if obj is not None:
                result.add(obj)
        return result

    def getAllVocTerms(self, content_instance):
        portal_urban = api.portal.get_tool('portal_urban')
        voc_terms = portal_urban.listVocabularyObjects(
            self.path,
            content_instance,
            sort_on=self.sort_on,
            id_to_use=self.id_to_use,
            vocType=self.vocType,
            inUrbanConfig=self.inUrbanConfig,
            allowedStates=self.allowedStates,
            with_empty_value=self.with_empty_value
        )
        return voc_terms

    def listAllVocTerms(self, content_instance):
        portal_urban = api.portal.get_tool('portal_urban')
        voc_brains = portal_urban.listVocabularyBrains(
            self.path,
            content_instance,
            sort_on=self.sort_on,
            vocType=self.vocType,
            inUrbanConfig=self.inUrbanConfig,
            allowedStates=self.allowedStates,
        )
        voc_terms = [brain.getObject() for brain in voc_brains]
        return voc_terms


##/code-section module-footer

