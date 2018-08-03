# -*- coding: utf-8 -*-
#

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.EnvironmentLicence import EnvironmentLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.content.licence.EnvClassOne import EnvClassOne

from Products.urban.config import *
from Products.urban import UrbanMessage as _


##code-section module-header #fill in your manual code here
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
##/code-section module-header

schema = Schema((
    DataGridField(
        name='workLocations',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number': Column("Number"), 'street': Column("Street")},
            label=_('urban_label_workLocations', default='Work locations'),
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
    ),
    StringField(
        name='zipcode',
        schemata="urban_description",
        widget=StringField._properties['widget'](
            label=_('urban_label_zipcode', default='Zipcode'),
        ),
    ),
    StringField(
        name='city',
        schemata="urban_description",
        widget=StringField._properties['widget'](
            label=_('urban_label_city', default='City'),
        ),
    ),
    DataGridField(
        name='manualParcels',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'ref': Column("Référence cadastrale"), 'capakey': Column("Capakey")},
            label=_('urban_label_manualParcels', default='Manualparcels'),
        ),
        allow_oddeven=True,
        columns=('ref', 'capakey'),
    ),
    DataGridField(
        name='businessOldLocation',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number': Column("Number"), 'street': Column("Street")},
            label=_('urban_label_businessOldLocation', default='Businessoldlocation'),
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
        validators=('isValidStreetName',),
    ),
    DataGridField(
        name='manualOldParcels',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'ref': Column("Référence cadastrale"), 'capakey': Column("Capakey")},
            label=_('urban_label_manualOldParcels', default='Manualoldparcels'),
        ),
        allow_oddeven=True,
        columns=('ref', 'capakey'),
    ),
    StringField(
            name='envclasschoices',
            default='ukn',
            widget=MasterSelectWidget(
                    label='Type de classe d\'environement',
                    label_msgid='urban_label_listenvclasschoices',
                    i18n_domain='urban',
            ),
            schemata='urban_description',
            multiValued=1,
            vocabulary='listEnvClassChoices',
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassBordering_schema = EnvClassOne.schema.copy() + schema.copy()


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvClassBordering(EnvClassOne):
  """
  """
  implements(interfaces.IEnvClassBordering)

  meta_type = 'EnvClassBordering'

  schema = EnvClassBordering_schema
  ##code-section class-header #fill in your manual code here
  ##/code-section class-header



  def listEnvClassChoices(self):
    vocab = (
      ('ukn', 'Non determiné'),
      ('EnvClassOne', 'classe 1'),
      ('EnvClassTwo', 'classe 2'),
    )
    return DisplayList(vocab)


registerType(EnvClassBordering, PROJECTNAME)


# end of class EnvClassOne

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('city', after='workLocations')
    schema.moveField('zipcode', after='city')
    schema.moveField('manualParcels', after='zipcode')
    schema.moveField('businessOldLocation', after='manualParcels')
    schema.moveField('manualOldParcels', after='businessOldLocation')
    schema.moveField('foldermanagers', after='manualOldParcels')
    schema.moveField('description', after='additionalLegalConditions')
    schema.moveField('missingPartsDetails', after='missingParts')
    return schema


finalizeSchema(EnvClassBordering_schema)
##/code-section module-footer
