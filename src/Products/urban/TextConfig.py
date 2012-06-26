# -*- coding: utf-8 -*-
#
# File: TextConfig.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.Archetypes.public import DisplayList
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.LinesColumn import LinesColumn
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
##/code-section module-header

schema = Schema((

    DataGridField(
        name='texts',
        widget=DataGridWidget(
            columns={'fieldname' : SelectColumn("FieldName", 'getVoc'), 'text' : LinesColumn("Text")},
            label='Texts',
            label_msgid='urban_label_texts',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('fieldname', 'text'),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

TextConfig_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TextConfig(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ITextConfig)

    meta_type = 'TextConfig'
    _at_rename_after_creation = True

    schema = TextConfig_schema

    ##code-section class-header #fill in your manual code here

    def getVoc(self):
        #we have to know from where the method has been called in order to know which text
        #fields to propose to be "default valued"
        licence_type = self.aq_parent.id
        #dynamical import of the correct shema
        licence_modules = {
            'buildlicence' : 'BuildLicence',
            'parceloutlicence' : 'ParcelOutLicence',
            'declaration' : 'Declaration',
            'division' : 'Division',
            'urbancertificateone' : 'UrbanCertificateBase',
            'urbancertificatetwo' : 'UrbanCertificateTwo',
            'notaryletter' : 'UrbanCertificateBase',
            'environmentaldeclaration' : 'EnvironmentalDeclaration',
            'miscdemand' : 'MiscDemand',
        }
        module_name = 'Products.urban.%s' % licence_modules[licence_type]
        attribute = "%s_schema" % licence_modules[licence_type]
        module = __import__(module_name, fromlist=[attribute])
        licence_schema = getattr(module, attribute)
        return DisplayList([(field.getName(), translate(field.widget.label_msgid,'urban', context=self.REQUEST))
            for field in licence_schema.fields() if field.getType() == 'Products.Archetypes.Field.TextField' and field.getName() != 'rights'])
    ##/code-section class-header

    # Methods


registerType(TextConfig, PROJECTNAME)
# end of class TextConfig

##code-section module-footer #fill in your manual code here
##/code-section module-footer

