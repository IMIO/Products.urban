# -*- coding: utf-8 -*-
#
# File: EnvironmentBase.py
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
from Products.urban.GenericLicence import GenericLicence
from Products.urban.Inquiry import Inquiry
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from Products.urban.utils import setOptionalAttributes, setSchemataForInquiry
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

optional_fields =['inadmissibilityReasons', 'roadTechnicalAdvice', 'locationTechnicalAdvice',
                  'additionalLegalConditions']

slave_fields_additionalconditions= (
    {'name': 'additionalConditions',
     'action': 'show',
     'hide_values': (True, ),
    },
)

##/code-section module-header

schema = Schema((

    TextField(
        name='businessDescription',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Businessdescription',
            label_msgid='urban_label_businessDescription',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    ReferenceField(
        name='rubrics',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=True,
            force_close_on_insert=True,
            startup_directory_method='getRubricsConfigPath',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory= True,
            label='Rubrics',
            label_msgid='urban_label_rubrics',
            i18n_domain='urban',
        ),
        allowed_types= ('EnvironmentRubricTerm',),
        schemata='urban_description',
        multiValued=True,
        relationship="rubric",
    ),
    StringField(
        name='applicationReasons',
        widget=SelectionWidget(
            format='checkbox',
            label='Applicationreasons',
            label_msgid='urban_label_applicationReasons',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary(path='applicationreasons', sort_on='getObjPositionInParent'),
        default_method='getDefaultValue',
    ),
    DataGridField(
        name='businessOldLocation',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number' : Column("Number"), 'street' : ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',))},
            helper_js=('datagridwidget.js', 'datagridautocomplete.js'),
            label='Businessoldlocation',
            label_msgid='urban_label_businessOldLocation',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
        validators=('isValidStreetName',),
    ),
    LinesField(
        name='inadmissibilityReasons',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Inadmissibilityreasons',
            label_msgid='urban_label_inadmissibilityReasons',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary(path='inadmissibilityreasons', sort_on='getObjPositionInParent'),
        default_method='getDefaultValue',
    ),
    ReferenceField(
        name='minimumLegalConditions',
        widget=ReferenceBrowserWidget(
            visible=False,
            label='Minimumlegalconditions',
            label_msgid='urban_label_minimumLegalConditions',
            i18n_domain='urban',
        ),
        schemata="urban_description",
        multiValued=True,
        relationship='minimumconditions',
    ),
    ReferenceField(
        name='additionalLegalConditions',
        widget=ReferenceBrowserWidget(
            allow_browse=True,
            allow_search=True,
            default_search_index='Title',
            startup_directory='portal_urban/exploitationconditions',
            restrict_browsing_to_startup_directory=True,
            wild_card_search=True,
            label='Additionallegalconditions',
            label_msgid='urban_label_additionalLegalConditions',
            i18n_domain='urban',
        ),
        schemata="urban_description",
        multiValued=True,
        relationship='additionalconditions',
    ),
    BooleanField(
        name='hasAdditionalConditions',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_additionalconditions,
            label='Hasadditionalconditions',
            label_msgid='urban_label_hasAdditionalConditions',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    TextField(
        name='additionalConditions',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Additionalconditions',
            label_msgid='urban_label_additionalConditions',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    TextField(
        name='roadTechnicalAdvice',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Roadtechnicaladvice',
            label_msgid='urban_label_roadTechnicalAdvice',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_road',
        default_output_type='text/html',
    ),
    TextField(
        name='locationTechnicalAdvice',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Locationtechnicaladvice',
            label_msgid='urban_label_locationTechnicalAdvice',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_location',
        default_output_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentBase_schema['title'].required = False
EnvironmentBase_schema['title'].widget.visible = False
#remove the annoncedDelays for Environments
del EnvironmentBase_schema['annoncedDelay']
del EnvironmentBase_schema['annoncedDelayDetails']
#remove the impactStudy field for Environments
del EnvironmentBase_schema['impactStudy']
EnvironmentBase_schema['solicitRoadOpinionsTo'].widget.visible=False
EnvironmentBase_schema['solicitLocationOpinionsTo'].widget.visible=False
setSchemataForInquiry(EnvironmentBase_schema)
def hidesInquiryFields(schema):
    inquiry_fields = [field for field in schema.filterFields(isMetadata=False)
                      if field.schemata == 'urban_investigation_and_advices' and field.getName() != 'solicitOpinionsTo']
    for field in inquiry_fields:
        field.widget.visible = False
hidesInquiryFields(EnvironmentBase_schema)
##/code-section after-schema

class EnvironmentBase(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvironmentBase)

    meta_type = 'EnvironmentBase'
    _at_rename_after_creation = True

    schema = EnvironmentBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location',\
                      'urban_investigation_and_advices']
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_create_script(self)

    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_edit_script(self)

    security.declarePublic('getAdditionalLayers')
    def getAdditionalLayers(self):
        """
          Return a list of additional layers that will be used
          when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues('Layer')
        except AttributeError:
            return None

    security.declarePublic('getProprietaries')
    def getProprietaries(self):
        """
           Return the list of proprietaries for the certificate
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Proprietary':
                res.append(obj)
        return res

    def getRubricsConfigPath(self):
        portal_urban = getToolByName(self, 'portal_urban')
        return '/'.join(portal_urban.envclassthree.rubrics.getPhysicalPath())[1:]

    security.declarePrivate('_getConditions')
    def _getConditions(self, restrict=['CI & CS', 'CI', 'CS']):
        all_conditions = self.getMinimumLegalConditions()
        all_conditions.extend(self.getAdditionalLegalConditions())
        return [cond for cond in all_conditions if cond.getExtraValue() in restrict]

    security.declarePublic('getIntegralConditions')
    def getIntegralConditions(self):
        """
         Return all the integral conditions,
        """
        return self._getConditions(restrict=['CI'])

    security.declarePublic('getSectorialConditions')
    def getSectorialConditions(self):
        """
         Return all the sectorial conditions,
        """
        return self._getConditions(restrict=['CS'])

    security.declarePublic('getIandSConditions')
    def getIandSConditions(self):
        """
         Return all the integral & sectorial conditions,
        """
        return self._getConditions(restrict=['CI & CS'])



registerType(EnvironmentBase, PROJECTNAME)
# end of class EnvironmentBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('foldermanagers', after='workLocations')
    schema.moveField('businessDescription', after='folderCategory')
    schema.moveField('rubrics', after='businessDescription')
    schema.moveField('missingParts', after='inadmissibilityReasons')
    schema.moveField('missingPartsDetails', after='missingParts')
    schema.moveField('description', after='additionalConditions')
    return schema

finalizeSchema(EnvironmentBase_schema)
##/code-section module-footer

