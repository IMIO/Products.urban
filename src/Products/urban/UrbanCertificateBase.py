# -*- coding: utf-8 -*-
#
# File: UrbanCertificateBase.py
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
from Products.urban.GenericLicence import GenericLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.CheckboxColumn import CheckboxColumn
from Products.DataGridField.FixedColumn import FixedColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.UrbanDataGridColumns.FormFocusColumn import FormFocusColumn
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime

optional_fields = ['specificFeatures', 'roadSpecificFeatures', 'locationSpecificFeatures',
                   'customSpecificFeatures', 'townshipSpecificFeatures', 'opinionsToAskIfWorks',
                   'basement', 'ZIP', 'noteworthyTrees', 'pollution', 'annoncedDelay', 'annoncedDelayDetails']
##/code-section module-header

schema = Schema((

    ReferenceField(
        name='notaryContact',
        widget=ReferenceBrowserWidget(
            allow_search=1,
            allow_browse=1,
            force_close_on_insert=1,
            startup_directory='urban/notaries',
            restrict_browsing_to_startup_directory=1,
            popup_name='popup',
            wild_card_search=True,
            label='Notarycontact',
            label_msgid='urban_label_notaryContact',
            i18n_domain='urban',
        ),
        required=False,
        schemata='urban_description',
        multiValued=True,
        relationship="notary",
        allowed_types= ('Notary',),
    ),
    DataGridField(
        name='specificFeatures',
        widget=DataGridWidget(
            columns= {'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label='Specificfeatures',
            label_msgid='urban_label_specificFeatures',
            i18n_domain='urban',
        ),
        fixed_rows='getSpecificFeaturesRows',
        allow_insert= False,
        allow_reorder= False,
        allow_oddeven= True,
        allow_delete= False,
        schemata='urban_description',
        columns= ('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='roadSpecificFeatures',
        widget=DataGridWidget(
            columns= {'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label='Roadspecificfeatures',
            label_msgid='urban_label_roadSpecificFeatures',
            i18n_domain='urban',
        ),
        fixed_rows='getRoadFeaturesRows',
        allow_insert= False,
        allow_reorder= False,
        allow_oddeven= True,
        allow_delete= False,
        schemata='urban_road',
        columns= ('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='locationSpecificFeatures',
        widget=DataGridWidget(
            columns= {'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label='Locationspecificfeatures',
            label_msgid='urban_label_locationSpecificFeatures',
            i18n_domain='urban',
        ),
        fixed_rows='getLocationFeaturesRows',
        allow_insert= False,
        allow_reorder= False,
        allow_oddeven= True,
        allow_delete= False,
        schemata='urban_location',
        columns= ('id', 'check', 'value', 'text',),
    ),
    DataGridField(
        name='customSpecificFeatures',
        widget=DataGridWidget(
            columns={'text': TextAreaColumn("Feature", rows=1, cols=50)},
            label='Customspecificfeatures',
            label_msgid='urban_label_customSpecificFeatures',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('text',),
    ),
    DataGridField(
        name='townshipSpecificFeatures',
        widget=DataGridWidget(
            columns= {'id': FormFocusColumn('id'), 'check': CheckboxColumn('Select'), 'value': FixedColumn('Value'), 'text': TextAreaColumn('Text', rows=1, cols=50)},
            label='Townshipspecificfeatures',
            label_msgid='urban_label_townshipSpecificFeatures',
            i18n_domain='urban',
        ),
        fixed_rows='getTownshipFeaturesRows',
        allow_insert= False,
        allow_reorder= False,
        allow_oddeven= True,
        allow_delete= False,
        schemata='urban_description',
        columns= ('id', 'check', 'value', 'text',),
    ),
    LinesField(
        name='opinionsToAskIfWorks',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Opinionstoaskifworks',
            label_msgid='urban_label_opinionsToAskIfWorks',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('opinionstoaskifworks', vocType='OrganisationTerm'),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='basement',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Basement',
            label_msgid='urban_label_basement',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('basement'),
        default_method='getDefaultValue',
    ),
    BooleanField(
        name='pollution',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Pollution',
            label_msgid='urban_label_pollution',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    LinesField(
        name='ZIP',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Zip',
            label_msgid='urban_label_ZIP',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('zip'),
        default_method='getDefaultValue',
    ),
    LinesField(
        name='noteworthyTrees',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Noteworthytrees',
            label_msgid='urban_label_noteworthyTrees',
            i18n_domain='urban',
        ),
        schemata='urban_location',
        multiValued=True,
        vocabulary=UrbanVocabulary('noteworthytrees'),
        default_method='getDefaultValue',
    ),
    StringField(
        name='annoncedDelay',
        widget=SelectionWidget(
            label='Annonceddelay',
            label_msgid='urban_label_annoncedDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('folderdelays', vocType='UrbanDelay', with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='annoncedDelayDetails',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Annonceddelaydetails',
            label_msgid='urban_label_annoncedDelayDetails',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        default_method='getDefaultText',
        default_content_type='text/plain',
        default_output_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanCertificateBase_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanCertificateBase_schema['title'].required = False
##/code-section after-schema

class UrbanCertificateBase(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanCertificateBase)

    meta_type = 'UrbanCertificateBase'
    _at_rename_after_creation = True

    schema = UrbanCertificateBase_schema

    ##code-section class-header #fill in your manual code here
    schemata_order = ['urban_description', 'urban_road', 'urban_location']
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('attributeIsUsed')
    def attributeIsUsed(self, name):
        """
         Override the GenericLicence attributeIsUsed method to always return true.
         This is because we want to delegate the display of the field to licence edit view
         and not to archetype so we can hide the widget in a <div hidden=True> tag.
         This is needed for the specificFeature edit shortcut.
        """
        return True

    security.declarePublic('getSpecificFeaturesRows')
    def getSpecificFeaturesRows(self):
        return self._getSpecificFeaturesRows()

    security.declarePublic('getRoadFeaturesRows')
    def getRoadFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='road')

    security.declarePublic('getLocationFeaturesRows')
    def getLocationFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='location')

    security.declarePublic('getTownshipFeaturesRows')
    def getTownshipFeaturesRows(self):
        return self._getSpecificFeaturesRows(location='township')

    def _getSpecificFeaturesRows(self, location=''):
        portal_urban = getToolByName(self, 'portal_urban')
        vocname = '%sspecificfeatures' % location
        vocterms = [brain.getObject() for brain in portal_urban.listVocabularyBrains(vocToReturn=vocname, vocType=['SpecificFeatureTerm'], context=self)]

        rows = []
        for vocterm in vocterms:
            numbering = vocterm.getNumbering() and '%s - ' % vocterm.getNumbering() or ''
            value = '%s%s' % (numbering, vocterm.Title())
            row_data = {
                'check': vocterm.getIsDefaultValue() and '1' or '',
                'id': vocterm.id,
                'value': value,
                'text': vocterm.Description(),
            }
            row = FixedRow(keyColumn='id', initialData=row_data)
            rows.append(row)

        return rows

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to set a clearly identify the buildlicence
        """
        notary = ''
        proprietary = ''
        proprietaries = self.getProprietaries()
        if proprietaries:
            proprietary = proprietaries[0].Title()
        else:
            proprietary = translate('no_proprietary_defined', 'urban', context=self.REQUEST).encode('utf8')
        if self.getNotaryContact():
            notary = self.getNotaryContact()[0].Title()
        else:
            notary = translate('no_notary_defined', 'urban', context=self.REQUEST).encode('utf8')

        if proprietary and notary:
            title = "%s - %s - %s" % (self.getReference(), proprietary, notary)
        elif proprietary:
            title = "%s - %s" % (self.getReference(), proprietary)
        elif notary:
            title = "%s - %s" % (self.getReference(), notary)
        else:
            title = self.getReference()
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    security.declarePublic('getOpinionsToAskForWorks')
    def getOpinionsToAskForWorks(self, theObjects=False):
        """
          Returns the opinionsToAskIfWorks values or the OrganisationTerms if theObject=True
        """
        res = self.getField('opinionsToAskIfWorks').get(self)
        if res and theObjects:
            urbanConfig = self.getUrbanConfig()
            opinionsToAskIfWorksConfigFolder = urbanConfig.opinionstoaskifworks
            elts = res
            res = []
            for elt in elts:
                res.append(getattr(opinionsToAskIfWorksConfigFolder, elt))
        return res

    security.declarePublic('getLastDeposit')
    def getLastDeposit(self):
        return self._getLastEvent(interfaces.IDepositEvent)

    security.declarePublic('getLastTheLicence')
    def getLastTheLicence(self):
        return self._getLastEvent(interfaces.ITheLicenceEvent)

    security.declarePublic('getSpecificFeaturesForTemplate')
    def getSpecificFeaturesForTemplate(self, where=[''], active_style='', inactive_style='striked'):
        """
          Return formatted specific features (striked or not)
          Helper method used in templates
        """
        tool = getToolByName(self, 'portal_urban')
        #get all the specificfeatures vocabular terms from each config
        res=[]
        for location in where:
            specificfeature_accessor = "get%sSpecificFeatures" % location.capitalize()
            specificFeatures = getattr(self, specificfeature_accessor)()
            for specificfeature in specificFeatures:
                if specificfeature['check']:
                    #render the expressions
                    render = tool.renderText(text=specificfeature['text'], context=self)
                    if active_style:
                        render = tool.decorateHTML(active_style, render)
                    res.append(render)
                else:
                    #replace the expressions by a null value, aka "..."
                    render = tool.renderText(text=specificfeature['text'], context=self, renderToNull=True)
                    if inactive_style:
                        render = tool.decorateHTML(inactive_style, render)
                    res.append(render)
            #add customSpecificFeatures
            if location == '':
                for csf in self.getCustomSpecificFeatures():
                    res.append("<p>%s</p>" % "<br />".join(csf['feature']))
        return res

    security.declarePublic('getProprietaries')
    def getProprietaries(self):
        """
           Return the list of proprietaries for the certificate
        """
        res = []
        for obj in self.objectValues('Contact'):
            if obj.portal_type == 'Proprietary':
                res.append(obj)
        return res

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of proprietaries for the certificate
        """
        return self.getProprietaries()

    security.declarePublic('getBuildlicencesOfTheParcels')
    def getBuildlicencesOfTheParcels(self):
        limit_date = DateTime('1977/01/01')
        return self.getLicenceOfTheParcels('BuildLicence', limit_date)

    security.declarePublic('getUrbanCertificateOneOfTheParcels')
    def getUrbanCertificateOneOfTheParcels(self):
        #cu1 cannot be older than 2 years
        limit_date = self.getLastTheLicence().getEventDate() - 731
        return self.getLicenceOfTheParcels('UrbanCertificateOne', limit_date)

    security.declarePublic('getParceloutlicenceOfTheParcels')
    def getParceloutlicenceOfTheParcels(self):
        limit_date = DateTime('1977/01/01')
        return self.getLicenceOfTheParcels('ParcelOutLicence', limit_date)

    security.declarePublic('hasEventNamed')
    def hasEventNamed(self, title):
        """
        Tells if the licence contains an urbanEvent named 'title'
        """
        catalog = getToolByName(self, 'portal_catalog')
        if catalog(portal_type='UrbanEvent', path=self.absolute_url_path(), Title=title):
            return True
        return False

    security.declarePublic('hasNoEventNamed')
    def hasNoEventNamed(self, title):
        """
        Tells if the licence does not contain any urbanEvent named 'title'
        """
        return not self.hasEventNamed(title)



registerType(UrbanCertificateBase, PROJECTNAME)
# end of class UrbanCertificateBase

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('referenceDGATLP', after='reference')
    schema.moveField('notaryContact', after='workLocations')
    schema.moveField('foldermanagers', after='notaryContact')
    schema.moveField('description', after='opinionsToAskIfWorks')
    schema.moveField('basement', after='RCU')
    schema.moveField('ZIP', after='basement')
    schema.moveField('noteworthyTrees', after='ZIP')
    schema.moveField('pollution', after='noteworthyTrees')
    schema.moveField('folderCategoryTownship', after='pollution')
    return schema

finalizeSchema(UrbanCertificateBase_schema)
##/code-section module-footer

