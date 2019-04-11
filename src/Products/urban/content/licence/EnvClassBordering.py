# -*- coding: utf-8 -*-
#

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.content.licence.EnvClassOne import EnvClassOne

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from zope.i18n import translate


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

EnvClassBordering_schema = EnvClassOne.schema.copy() + schema.copy()


class EnvClassBordering(EnvClassOne):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IEnvClassBordering)

    meta_type = 'EnvClassBordering'

    schema = EnvClassBordering_schema

    def listEnvClassChoices(self):
        vocab = (
            ('ukn', 'Non determiné'),
            ('EnvClassOne', 'classe 1'),
            ('EnvClassTwo', 'classe 2'),
        )
        return DisplayList(vocab)

    security.declarePublic('getDefaultWorkLocationSignaletic')

    def getDefaultWorkLocationSignaletic(self, auto_back_to_the_line=False):
        """
          Returns a string reprensenting the different worklocations
        """
        signaletic = ''

        for wl in self.getWorkLocations():
            streetName = wl['street']
            number = wl['number']
            city = self.getCity()
            zipcode = self.getZipcode()
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            if number:
                signaletic += "%s %s à %s %s" % (streetName, number.encode('utf8'), zipcode, city)
            else:
                signaletic += "%s - %s %s" % (streetName, zipcode, city)
            if auto_back_to_the_line:
                signaletic += "\n"

        return signaletic

    security.declarePublic('getDefaultStreetAndNumber')

    def getDefaultStreetAndNumber(self):
        """
          Returns a string reprensenting the different streets and numbers
        """
        signaletic = ''

        for wl in self.getWorkLocations():
            street = wl['street']
            number = wl['number']
            if number:
                signaletic = '{} {} {}'.format(signaletic, street, number)
            else:
                signaletic = '{} {}'.format(signaletic, street)

        return signaletic


registerType(EnvClassBordering, PROJECTNAME)


def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('city', after='workLocations')
    schema.moveField('zipcode', after='city')
    schema.moveField('manualParcels', after='zipcode')
    schema.moveField('foldermanagers', after='manualParcels')
    schema.moveField('description', after='additionalLegalConditions')
    schema.moveField('missingPartsDetails', after='missingParts')
    to_remove_fields = (
        'annoncedDelay',
        'ftSolicitOpinionsTo',
    )
    for field in to_remove_fields:
        if field in schema:
            del schema[field]
    return schema


finalizeSchema(EnvClassBordering_schema)
