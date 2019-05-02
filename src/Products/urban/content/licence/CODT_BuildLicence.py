# -*- coding: utf-8 -*-
#
# File: CODT_BuildLicence.py
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
from Products.urban.content.licence.CODT_BaseBuildLicence import CODT_BaseBuildLicence
from Products.urban.utils import setOptionalAttributes
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.widget.urbanreferencewidget import UrbanBackReferenceWidget


##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
optional_fields = ['limitedImpact', 'SDC_divergence']

full_patrimony_slave_fields = (
        {
            'name': 'archeological_site',
            'action': 'hide',
            'hide_values': ('none',),
        },
        {
            'name': 'protection_zone',
            'action': 'hide',
            'hide_values': ('none',),
        },
        {
            'name': 'regional_inventory_building',
            'action': 'hide',
            'hide_values': ('none',),
        },
        {
            'name': 'small_popular_patrimony',
            'action': 'hide',
            'hide_values': ('none',),
        },
        {
            'name': 'communal_inventory',
            'action': 'hide',
            'hide_values': ('none',),
        },

)
##/code-section module-header

schema = Schema((

    BooleanField(
        name='limitedImpact',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_limitedImpact', default='Limitedimpact'),
        ),
        schemata='urban_analysis',
    ),
    BooleanField(
        name='SDC_divergence',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_SDC_divergence', default='SDC_divergence'),
        ),
        schemata='urban_analysis',
    ),
    StringField(
        name='road_decree_reference',
        widget=UrbanBackReferenceWidget(
            label=_('road_decree_reference', default='road_decree_reference'),
            portal_types=['RoadDecree'],
        ),
        required=False,
        schemata='urban_description',
        default_method='getDefaultText',
        validators=('isReference',),
    ),
    StringField(
        name='patrimony',
        widget=MasterSelectWidget(
            slave_fields=full_patrimony_slave_fields,
            label=_('urban_label_patrimony', default='Patrimony'),
        ),
        vocabulary='list_patrimony_types',
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='archeological_site',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_archeological_site', default='Archeological_site'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='protection_zone',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_protection_zone', default='Protection_zone'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='regional_inventory_building',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_regional_inventory_building', default='Regional_inventory_building'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='small_popular_patrimony',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_small_popular_patrimony', default='Small_popular_patrimony'),
        ),
        schemata='urban_patrimony',
    ),
    BooleanField(
        name='communal_inventory',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_communal_inventory', default='Communal_inventory'),
        ),
        schemata='urban_patrimony',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

CODT_BuildLicence_schema = BaseFolderSchema.copy() + \
    getattr(CODT_BaseBuildLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema


class CODT_BuildLicence(BaseFolder, CODT_BaseBuildLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICODT_BuildLicence)

    meta_type = 'CODT_BuildLicence'
    _at_rename_after_creation = True

    schema = CODT_BuildLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def list_patrimony_types(self):
        """
        """
        vocabulary = (
                ('none', 'aucune incidence'),
                ('patrimonial', 'incidence patrimoniale'),
                ('classified', 'bien classé'),
        )
        return DisplayList(vocabulary)

registerType(CODT_BuildLicence, PROJECTNAME)
# end of class CODT_BuildLicence

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('roadAdaptation', before='roadTechnicalAdvice')
    schema.moveField('architects', after='workLocations')
    schema.moveField('foldermanagers', after='architects')
    schema.moveField('workType', after='folderCategory')
    schema.moveField('parcellings', after='isInSubdivision')
    schema.moveField('description', after='usage')
    schema.moveField('roadMiscDescription', after='roadEquipments')
    schema.moveField('locationTechnicalRemarks', after='locationTechnicalConditions')
    schema.moveField('areParcelsVerified', after='folderCategoryTownship')
    schema.moveField('requirementFromFD', before='annoncedDelay')
    schema.moveField('townshipCouncilFolder', after='futureRoadCoating')
    schema.moveField('annoncedDelayDetails', after='annoncedDelay')
    schema.moveField('impactStudy', after='annoncedDelayDetails')
    schema.moveField('procedureChoice', before='description')
    schema.moveField('exemptFDArticle', after='procedureChoice')
    schema.moveField('water', after='futureRoadCoating')
    schema.moveField('electricity', before='water')
    schema['missingParts'].widget.format = None
    return schema


def finalizeSpecificSchema(schema):
    """
       Finalizes the type schema to alter some fields specific to BuildLicence schema
    """
    schema.moveField('limitedImpact', after='prorogation')
    schema.moveField('SDC_divergence', after='limitedImpact')

finalizeSchema(CODT_BuildLicence_schema)
finalizeSpecificSchema(CODT_BuildLicence_schema)
##/code-section module-footer
