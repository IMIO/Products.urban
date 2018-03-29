# -*- coding: utf-8 -*-
#
# File: EnvClassThree.py
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
from Products.urban.content.licence.EnvironmentBase import EnvironmentBase
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

slave_fields_additionalconditions = (
    {
        'name': 'additionalConditions',
        'action': 'show',
        'hide_values': (True, ),
    },
)

optional_fields =['inadmissibilityReasons']

##/code-section module-header

schema = Schema((

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
    FileField(
        name='additionalConditions',
        schemata='urban_description',
        widget=FileField._properties['widget'](
            label='Additionalconditions',
            label_msgid='urban_label_additionalConditions',
            i18n_domain='urban',
        ),
        storage=AnnotationStorage(),
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

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassThree_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvClassThree(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvClassThree)

    meta_type = 'EnvClassThree'
    _at_rename_after_creation = True

    schema = EnvClassThree_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getValidityDelay(self):
        return 10

    def rubrics_base_query(self):
        return {'extraValue': ['0', '3']}



registerType(EnvClassThree, PROJECTNAME)
# end of class EnvClassThree

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('businessOldLocation', after='workLocations')
    schema.moveField('foldermanagers', after='businessOldLocation')
    schema.moveField('rubrics', after='folderCategory')
    schema.moveField('description', after='additionalLegalConditions')
    schema.moveField('missingParts', after='inadmissibilityReasons')
    schema.moveField('missingPartsDetails', after='missingParts')
    return schema

finalizeSchema(EnvClassThree_schema)
##/code-section module-footer

