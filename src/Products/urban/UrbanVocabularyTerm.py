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
from Products.Archetypes.interfaces import IVocabulary

from Products.urban.config import *
from zope.globalrequest import getRequest
from zope.i18n import translate

##code-section module-header #fill in your manual code here
from plone import api

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
        default_output_type='text/x-html-safe',
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
    StringField(
        name='coring_id',
        widget=StringField._properties['widget'](
            description="This field is made to store the coring id.",
            label='CoringId',
            label_msgid='urban_label_coring_id',
            description_msgid='urban_help_coring_id',
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

    def __str__(self):
        return self.Title()

    def __unicode__(self):
        return self.__str__().decode('utf-8')


registerType(UrbanVocabularyTerm, PROJECTNAME)
# end of class UrbanVocabularyTerm

##code-section module-footer #fill in your manual code here
class UrbanVocabulary(object):

    implements(IVocabulary)

    def __init__(self, path, vocType="UrbanVocabularyTerm", id_to_use="id", value_to_use="title", sort_on="getObjPositionInParent", inUrbanConfig=True, allowedStates=['enabled'], with_empty_value=False, datagridfield_key='street', _filter=None):
        self.path = path
        self.vocType = vocType
        self.id_to_use = id_to_use
        self.value_to_use = value_to_use
        self.sort_on = sort_on
        self.inUrbanConfig = inUrbanConfig
        self.allowedStates = allowedStates
        self.with_empty_value = with_empty_value
        self.datagridfield_key = datagridfield_key
        self._filter = _filter

    def get_raw_voc(self, context, licence_type='', _filter=None):
        portal_urban = api.portal.get_tool('portal_urban')
        raw_voc = portal_urban.get_vocabulary(
            in_urban_config=self.inUrbanConfig,
            context=context,
            licence_type=licence_type,
            name=self.path
        )
        voc = [v for v in raw_voc if v['portal_type'] in self.vocType]
        if self._filter:
            voc = [v for v in voc if self._filter(v)]
        return voc

    def get_default_values(self, context):
        raw_voc = self.get_raw_voc(context)
        default_values = [v['id'] for v in raw_voc if v['isDefaultValue']]
        return default_values

    def getDisplayList(self, context=None, licence_type=''):
        raw_voc = self.get_raw_voc(context, licence_type)
        url = getRequest() and getRequest().getURL()
        if url and (url.endswith('edit') or url.endswith('@@fieldeditoverlay')):
            result = [(v['id'], u'{}{}'.format(v.get('numbering', ''), v[self.value_to_use])) for v in raw_voc if v['enabled']]
        else:
            result = [(v['id'], v[self.value_to_use]) for v in raw_voc]
        if self.with_empty_value:
            val = translate(
                EMPTY_VOCAB_VALUE,
                'urban',
                context=context.REQUEST,
                default=EMPTY_VOCAB_VALUE
            )
            result = [('', val)] + result
        return DisplayList(result)

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

