# -*- coding: utf-8 -*-
#
# File: LicenceConfig.py
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

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from Products.Archetypes.public import DisplayList
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.FixedColumn import FixedColumn
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.urban.utils import getLicenceSchema
from zope.interface import Interface
from Products.PageTemplates.Expressions import getEngine
from Products.CMFCore.Expression import Expression
from plone import api
from DateTime import DateTime
##/code-section module-header

schema = Schema((

    StringField(
        name='licencePortalType',
        widget=StringField._properties['widget'](
            label='Licenceportaltype',
            label_msgid='urban_label_licencePortalType',
            i18n_domain='urban',
        ),
        mode='r',
    ),
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
        schemata='public_settings',
        multiValued=True,
        vocabulary='listUsedAttributes',
    ),
    DataGridField(
        name='tabsConfig',
        widget=DataGridWidget(
            columns={'display': CheckboxColumn('Display'), 'value': FixedColumn('Value'), 'display_name': Column('Name')},
            label='Tabsconfig',
            label_msgid='urban_label_tabsConfig',
            i18n_domain='urban',
        ),
        fixed_rows='getTabsConfigRows',
        allow_insert=False,
        allow_reorder=True,
        allow_oddeven=True,
        allow_delete=False,
        schemata='public_settings',
        columns=('display', 'value', 'display_name',),
    ),
    BooleanField(
        name='useTabbingForDisplay',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Usetabbingfordisplay',
            label_msgid='urban_label_useTabbingForDisplay',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    BooleanField(
        name='useTabbingForEdit',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Usetabbingforedit',
            label_msgid='urban_label_useTabbingForEdit',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    DataGridField(
        name='textDefaultValues',
        allow_oddeven=True,
        widget=DataGridWidget(
            columns={'fieldname' : SelectColumn('FieldName', 'listTextFields'), 'text' : TextAreaColumn('Text', rows=6, cols=60)},
            label='Textdefaultvalues',
            label_msgid='urban_label_textDefaultValues',
            i18n_domain='urban',
        ),
        schemata='public_settings',
        columns=('fieldname', 'text'),
        validators=('isTextFieldConfigured',),
    ),
    StringField(
        name='referenceTALExpression',
        default="python: obj.getLicenceTypeAcronym() + '/' + date.strftime('%Y') + '/' + numerotation + '/' + tool.getCurrentFolderManager(initials=True)",
        widget=StringField._properties['widget'](
            size=100,
            label='Referencetalexpression',
            label_msgid='urban_label_referenceTALExpression',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    StringField(
        name='numerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Numerotation',
            label_msgid='urban_label_numerotation',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

LicenceConfig_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
LicenceConfig_schema['licencePortalType'].widget.visible = False
for f in LicenceConfig_schema.filterFields(schemata='default'):
    f.widget.visible = {"edit": "invisible"}
for f in LicenceConfig_schema.filterFields(schemata='metadata'):
    f.widget.visible = {"edit": "invisible"}
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
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getEventTypesByInterface')
    def getEventTypesByInterface(self, interface):
        """
          Return all the UrbanEventTypes having interface 'interface'
          in their eventTypeType field
        """
        if issubclass(interface, Interface):
            interface = interface.__identifier__

        eventtypes = self.urbaneventtypes.objectValues()
        to_return = [uet for uet in eventtypes if interface in uet.getEventTypeType()]
        return to_return

    security.declarePrivate('listUsedAttributes')
    def listUsedAttributes(self):
        """
          Return the available optional fields
        """
        res = []
        abr = {
            'urban_peb': '(peb) ',
            'urban_location': '(urb) ',
            'urban_road': '(voi) ',
            'urban_investigation_and_advices': '(enq) ',
            'urban_description': '',
        }
        if not getLicenceSchema(self.getLicencePortalType()):
            return DisplayList()
        for field in getLicenceSchema(self.getLicencePortalType()).fields():
            if hasattr(field, 'optional'):
                tab = field.schemata
                if field.schemata in abr.keys() and field.widget.visible:
                    tab = abr[tab]
                    res.append(
                        (
                            field.getName(),
                            "%s%s" % (tab, self.utranslate(
                                field.widget.label_msgid,
                                domain=field.widget.i18n_domain,
                                default=field.widget.label)
                            )
                        )
                    )
        return DisplayList(tuple(res)).sortedByValue()

    def generateReference(self, licence, **kwargs):
        """
         Generates a reference based on the numerotationTALExpression
        """
        #we get a field like UrbanCertificateBaseNumerotation on self
        #to get the last numerotation for this kind of licence
        lastValue = self.getNumerotation()
        if str(lastValue).isdigit():
            lastValue = int(lastValue)
            lastValue = lastValue + 1

        #evaluate the numerotationTALExpression and pass it obj, lastValue and self
        data = {
            'obj': licence,
            'tool': api.portal.get_tool('portal_catalog'),
            'numerotation': str(lastValue),
            'portal': api.portal.getSite(),
            'date': DateTime(),
        }
        data.update(kwargs)
        res = ''
        try:
            ctx = getEngine().getContext(data)
            res = Expression(self.getReferenceTALExpression())(ctx)
        except Exception:
            pass
        return res

    security.declarePublic('getActiveTabs')
    def getActiveTabs(self):
        """
          Return the tabs in use
        """
        return [tab for tab in self.getTabsConfig() if tab['display']]

    security.declarePrivate('getTabsConfigRows')
    def getTabsConfigRows(self):
        """
        """
        default_names ={
                'description':'Récapitulatif',
                'road':'Voirie',
                'location':'Urbanisme',
                'investigation_and_advices':'Enquêtes et avis',
                'peb':'PEB',
                }
        minimum_tabs_config = ['description', 'road', 'location']
        inquiry_tabs_config = ['description', 'road', 'location', 'investigation_and_advices']
        full_tabs_config = ['description', 'road', 'location', 'investigation_and_advices', 'peb']

        types = {
                'buildlicence': full_tabs_config,
                'parceloutlicence': inquiry_tabs_config,
                'urbancertificatetwo': inquiry_tabs_config,
                'envclassthree': inquiry_tabs_config,
                }
        licence_type = self.id

        def makeRow(tabname):
            return FixedRow(
                keyColumn = 'value',
                initialData = {'display':'1', 'value':tabname, 'display_name':default_names[tabname]},
            )

        return [makeRow(tabname) for tabname in types.get(licence_type, minimum_tabs_config)]

    security.declarePublic('getIconURL')
    def getIconURL(self):
        portal_types = getToolByName(self, 'portal_types')
        if self.getLicencePortalType() and hasattr(portal_types, self.getLicencePortalType()):
            icon = "%s.png" % self.getLicencePortalType()
        else:
            icon = "LicenceConfig.png"
        portal_url = getToolByName(self, 'portal_url' )
        return portal_url() + '/' + icon

    security.declarePublic('listTextFields')
    def listTextFields(self):
        #we have to know from where the method has been called in order to know which text
        #fields to propose to be "default valued"
        licence_type = self.getLicencePortalType()
        licence_schema = getLicenceSchema(licence_type)
        abr = {
            'urban_peb': '(peb) ',
            'urban_location': '(urb) ',
            'urban_road': '(voi) ',
            'urban_investigation_and_advices': '(enq) ',
            'urban_description': '',
        }
        available_fields = [field for field in licence_schema.fields() if field.getType() == 'Products.Archetypes.Field.TextField' and field.getName() != 'rights']
        vocabulary_fields = [(field.getName(), '%s %s' % (translate(field.widget.label_msgid, 'urban', context=self.REQUEST), abr[field.schemata])) for field in available_fields]
        #return a vocabulary containing the names of all the text fields of the schema
        return DisplayList(sorted(vocabulary_fields, key=lambda name: name[1]))



registerType(LicenceConfig, PROJECTNAME)
# end of class LicenceConfig

##code-section module-footer #fill in your manual code here
##/code-section module-footer

