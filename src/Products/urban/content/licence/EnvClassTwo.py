# -*- coding: utf-8 -*-
#
# File: EnvClassTwo.py
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
from Products.urban.content.licence.EnvironmentLicence import EnvironmentLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban import UrbanMessage as _
from Products.urban.widget.urbanreferencewidget import UrbanBackReferenceWidget

##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((

    BooleanField(
        name='temporaryExploitation',
        default=False,
        widget=BooleanField._properties['widget'](
            label=_('urban_label_temporaryExploitation', default='Temporaryexploitation'),
        ),
        schemata='urban_description',
    ),
    StringField(
        name='explosive_possession_reference',
        widget=UrbanBackReferenceWidget(
            label=_('urban_label_explosive_reference',
                    default='Explosive Possession Reference'),
            portal_types=['ExplosivesPossession'],
        ),
        required=False,
        schemata='urban_description',
        default_method='getDefaultText',
        validators=('isReference', ),
    ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassTwo_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvClassTwo_schema['hasEnvironmentImpactStudy'].default = False
##/code-section after-schema

class EnvClassTwo(BaseFolder, EnvironmentLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassTwo)

    meta_type = 'EnvClassTwo'
    _at_rename_after_creation = True

    schema = EnvClassTwo_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def rubrics_base_query(self):
        base_query = super(EnvClassTwo, self).rubrics_base_query().copy()
        base_query['extraValue'] = ['0', '2', '3']
        return base_query

    def getProcedureDelays(self, *values):
        selection = [v['val'] for v in values if v['selected']]
        if 'simple' in selection:
            return '90j'
        elif 'temporary' in selection:
            return '40j'
        elif 'article65' in selection:
            return '50j'
        return ''


registerType(EnvClassTwo, PROJECTNAME)
# end of class EnvClassTwo

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('businessOldLocation', after='workLocations')
    schema.moveField('foldermanagers', after='businessOldLocation')
    schema.moveField('rubrics', after='folderCategory')
    schema.moveField('description', after='additionalLegalConditions')
    schema.moveField('temporaryExploitation', after='natura2000Details')
    return schema

finalizeSchema(EnvClassTwo_schema)
##/code-section module-footer

