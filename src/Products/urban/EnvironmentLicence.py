# -*- coding: utf-8 -*-
#
# File: EnvironmentLicence.py
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
from Products.urban.EnvironmentBase import EnvironmentBase
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.utils import setOptionalAttributes

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn

optional_fields =['areaDescriptionText', 'hasConfidentialData', 'isTemporaryProject', 'isEssayProject', 'isMobileProject']
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='previousLicences',
        widget=ReferenceBrowserWidget(
            label='Previouslicences',
            label_msgid='urban_label_previousLicences',
            i18n_domain='urban',
        ),
        allowed_types=('EnvClassThree', 'EnvClassTwo', 'EnvClassOne'),
        schemata='urban_description',
        multiValued=True,
        relationship='previousLicences',
    ),
    ReferenceField(
        name='additionalPreviousLicences',
        widget=ReferenceBrowserWidget(
            allow_browse=False,
            allow_search=False,
            show_results_without_query=True,
            wild_card_search=True,
            base_query='previouslicencesBaseQuery',
            label='Additionalpreviouslicences',
            label_msgid='urban_label_additionalPreviousLicences',
            i18n_domain='urban',
        ),
        allowed_types=('EnvClassThree', 'EnvClassTwo', 'EnvClassOne'),
        schemata='urban_description',
        multiValued=True,
        relationship='additionalPreviousLicences',
    ),
    TextField(
        name='areaDescriptionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Areadescriptiontext',
            label_msgid='urban_label_areaDescriptionText',
            i18n_domain='urban',
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_description',
        default_output_type='text/html',
    ),
    DataGridField(
        name='servitudesListing',
        allow_oddeven=True,
        widget=DataGridWidget(
            columns={'parcel_number': Column('ParcelLabel'), 'parcel_reference': SelectColumn('ParcelReference', 'listLicenceParcels'), 'description': TextAreaColumn('ServitudeDescription'), 'constraints': TextAreaColumn('ServitudeConstraints')},
            label='Servitudeslisting',
            label_msgid='urban_label_servitudesListing',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('parcel_number', 'parcel_reference', 'description', 'constraints'),
    ),
    DataGridField(
        name='publicRoadModifications',
        allow_oddeven=True,
        widget=DataGridWidget(
            columns={'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',)), 'modification': TextAreaColumn('Modification'), 'justification': TextAreaColumn('Justification')},
            label='Publicroadmodifications',
            label_msgid='urban_label_publicRoadModifications',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('street', 'modification', 'justification'),
    ),
    BooleanField(
        name='hasConfidentialData',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Hasconfidentialdata',
            label_msgid='urban_label_hasConfidentialData',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isTemporaryProject',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Istemporaryproject',
            label_msgid='urban_label_isTemporaryProject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isEssayProject',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isessayproject',
            label_msgid='urban_label_isEssayProject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isMobileProject',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Ismobileproject',
            label_msgid='urban_label_isMobileProject',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='hasEnvironmentImpactStudy',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Hasenvironmentimpactstudy',
            label_msgid='urban_label_hasEnvironmentImpactStudy',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isSeveso',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isseveso',
            label_msgid='urban_label_isSeveso',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    IntegerField(
        name='validityDelay',
        default=20,
        widget=IntegerField._properties['widget'](
            label='Validitydelay',
            label_msgid='urban_label_validityDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentLicence_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
for field in EnvironmentLicence_schema.filterFields(isMetadata=False):
    field.widget.visible = True
##/code-section after-schema

class EnvironmentLicence(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentLicence)

    meta_type = 'EnvironmentLicence'
    _at_rename_after_creation = True

    schema = EnvironmentLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listLicenceParcels')
    def listLicenceParcels(self):
        parcels = self.objectValues('PortionOut')
        vocabulary = [(parcel.UID(), parcel.Title()) for parcel in parcels]
        return DisplayList(sorted(vocabulary, key=lambda name: name[1]))

    security.declarePublic('previouslicencesBaseQuery')
    def previouslicencesBaseQuery(self):
        return {'object_provides': IEnvironmentBase.__identifier__}



registerType(EnvironmentLicence, PROJECTNAME)
# end of class EnvironmentLicence

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('areaDescriptionText', after='missingPartsDetails')
    schema.moveField('natura2000', after='isSeveso')
    schema.moveField('natura2000Details', after='natura2000')
    schema.moveField('hasAdditionalConditions', after='natura2000Details')
    schema.moveField('additionalConditions', after='hasAdditionalConditions')
    schema.moveField('description', after='validityDelay')

finalizeSchema(EnvironmentLicence_schema)
##/code-section module-footer

