# -*- coding: utf-8 -*-
#
# File: LicenceConfig.py
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
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from Products.Archetypes.public import DisplayList
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.validators.validator import isTextFieldConfiguredValidator
from Products.validation import V_REQUIRED
##/code-section module-header

schema = Schema((

    LinesField(
        name='usedAttributes',
        widget=MultiSelectionWidget(
            description="Select the optional fields you want to use. Multiple selection or deselection when clicking with CTRL",
            description_msgid="urban_descr_usedAttributes",
            size=10,
            label='Usedattributes',
            label_msgid='urban_label_usedAttributes',
            i18n_domain='urban',
        ),
        multiValued=True,
        vocabulary='listUsedAttributes',
    ),
    DataGridField(
        name='textDefaultValues',
        widget=DataGridWidget(
            columns={'fieldname' : SelectColumn('FieldName', 'getVoc'), 'text' : TextAreaColumn('Text', rows=6, cols=60)},
            label='Textdefaultvalues',
            label_msgid='urban_label_textDefaultValues',
            i18n_domain='urban',
        ),
        allow_oddeven=True,
        columns=('fieldname', 'text'),
        validators=('isTextFieldConfigured',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LicenceConfig_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class LicenceConfig(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.ILicenceConfig)

    meta_type = 'LicenceConfig'
    _at_rename_after_creation = True

    schema = LicenceConfig_schema

    ##code-section class-header #fill in your manual code here
    licence_portal_type = ''  #must be set on creation
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePrivate('listUsedAttributes')
    def listUsedAttributes(self):
        """
          Return the available optional fields
        """
        res = []
        abr = {
            'urban_peb':'(peb) ',
            'urban_location':'(urb) ',
            'urban_road':'(voi) ',
            'urban_investigation_and_advices':'(enq) ',
            'urban_description':'',
        }
        if not self._getSchema(self.licence_portal_type):
            return DisplayList()
        for field in self._getSchema(self.licence_portal_type).fields():
            if hasattr(field, 'optional'):
                tab = field.schemata
                if field.schemata in abr.keys():
                   tab = abr[tab]
                res.append((field.getName(), "%s%s" %(tab,
                    self.utranslate(field.widget.label_msgid, domain=field.widget.i18n_domain, default=field.widget.label))))
        return DisplayList(tuple(res)).sortedByValue()

    security.declarePublic('getIconURL')
    def getIconURL(self):
        portal_types = getToolByName(self, 'portal_types')
        if self.licence_portal_type and hasattr(portal_types, self.licence_portal_type):
            icon = "%s.png" % self.licence_portal_type
        else:
            icon = "LicenceConfig.png"
        portal_url = getToolByName( self, 'portal_url' )
        return portal_url() + '/' + icon

    def getVoc(self):
        #we have to know from where the method has been called in order to know which text
        #fields to propose to be "default valued"
        licence_type = self.licence_portal_type
        licence_schema = self._getSchema(licence_type)
        abr = {
            'urban_peb':'(peb) ',
            'urban_location':'(urb) ',
            'urban_road':'(voi) ',
            'urban_investigation_and_advices':'(enq) ',
            'urban_description':'',
        }
        available_fields = [field for field in licence_schema.fields() if field.getType() == 'Products.Archetypes.Field.TextField' and field.getName() != 'rights']
        vocabulary_fields = [(field.getName(), '%s %s' % (translate(field.widget.label_msgid,'urban', context=self.REQUEST), abr[field.schemata])) for field in available_fields]
        #return a vocabulary containing the names of all the text fields of the schema
        return DisplayList(sorted(vocabulary_fields, key=lambda name:name[1]))

    def _getSchema(self, licencetype):
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
        licence_type = licencetype.lower()
        if licence_type not in licence_modules.keys():
            return None
        module_name = 'Products.urban.%s' % licence_modules[licence_type]
        attribute = "%s_schema" % licence_modules[licence_type]
        module = __import__(module_name, fromlist=[attribute])
        return getattr(module, attribute)



registerType(LicenceConfig, PROJECTNAME)
# end of class LicenceConfig

##code-section module-footer #fill in your manual code here
##/code-section module-footer

