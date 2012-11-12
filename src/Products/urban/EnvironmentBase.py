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
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

optional_fields =['inadmissibilityReasons']

slave_fields_oldlocation= (
    {'name': 'businessOldLocation',
     'action': 'show',
     'hide_values': ('location_move', ),
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
    StringField(
        name='applicationReasons',
        widget=MasterSelectWidget(
            slave_fields=slave_fields_oldlocation,
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
        name='sectorialCondition',
        widget=ReferenceBrowserWidget(
            visible=True,
            allow_browse=True,
            allow_search=True,
            show_indexes=True,
            available_indexes={'Title':'Nom'},
            show_index_selector=True,
            startup_directory='portal_urban/sectorialconditions',
            restrict_browsing_to_startup_directory=True,
            default_search_index='Title',
            wild_card_search=True,
            label='Sectorialcondition',
            label_msgid='urban_label_sectorialCondition',
            i18n_domain='urban',
        ),
        schemata="urban_description",
        multiValued=True,
        relationship='sectorialconditions',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentBase_schema['title'].required = False
EnvironmentBase_schema['title'].widget.visible = False
#remove the annoncedDelays for Environments
del EnvironmentBase_schema['annoncedDelay']
del EnvironmentBase_schema['annoncedDelayDetails']
#remove the impactStudy field for Environments
del EnvironmentBase_schema['impactStudy']
#hide the solicit opinions to fields for EnvironmentOne
EnvironmentBase_schema['solicitRoadOpinionsTo'].widget.visible=False
EnvironmentBase_schema['solicitLocationOpinionsTo'].widget.visible=False
##/code-section after-schema

class EnvironmentBase(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvironmentBase)

    meta_type = 'EnvironmentBase'
    _at_rename_after_creation = True

    schema = EnvironmentBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
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



registerType(EnvironmentBase, PROJECTNAME)
# end of class EnvironmentBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('foldermanagers', after='workLocations')
    schema.moveField('businessDescription', after='foldermanagers')
    schema.moveField('missingParts', after='inadmissibilityReasons')
    schema.moveField('missingPartsDetails', after='missingParts')
    schema.moveField('description', after='missingPartsDetails')
    return schema

finalizeSchema(EnvironmentBase_schema)
##/code-section module-footer

