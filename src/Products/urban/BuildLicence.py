# -*- coding: utf-8 -*-
#
# File: BuildLicence.py
#
# Copyright (c) 2011 by CommunesPlone
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

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from GenericLicence import GenericLicence
from GenericLicence import GenericLicence_schema
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService

slave_fields_subdivision = (
    # if in subdivision, display a textarea the fill some details
    {'name': 'subdivisionDetails',
     'action': 'show',
     'hide_values': (True, ),
    },
    {'name': 'parcellings',
     'action': 'show',
     'hide_values': (True, ),
     'hide_values': (True, ),
    },
)
slave_fields_pca= (
    # if in a pca, display a selectbox
    {'name': 'pca',
     'action': 'show',
     'hide_values': (True, ),
    },
)
##/code-section module-header

schema = Schema((

    StringField(
        name='workType',
        widget=SelectionWidget(
            label='Worktype',
            label_msgid='urban_label_workType',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary='listBuildWorkTypeTerms',
    ),
    StringField(
        name='usage',
        widget=SelectionWidget(
            label='Usage',
            label_msgid='urban_label_usage',
            i18n_domain='urban',
        ),
        required= True,
        schemata='urban_description',
        vocabulary='listUsages',
    ),
    BooleanField(
        name='isInSubdivision',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_subdivision,
            label='Isinsubdivision',
            label_msgid='urban_label_isInSubdivision',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    TextField(
        name='subdivisionDetails',
        widget=TextAreaWidget(
            description='Number of the lots, ...',
            description_msgid="urban_descr_subdivisionDetails",
            label='Subdivisiondetails',
            label_msgid='urban_label_subdivisionDetails',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    BooleanField(
        name='isInPCA',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_pca,
            label='Isinpca',
            label_msgid='urban_label_isInPCA',
            i18n_domain='urban',
        ),
        schemata='urban_location',
    ),
    StringField(
        name='roadAdaptation',
        default='no',
        widget=SelectionWidget(
            label='Roadadaptation',
            label_msgid='urban_label_roadAdaptation',
            i18n_domain='urban',
        ),
        schemata='urban_road',
        vocabulary='listRoadAdaptations',
    ),
    BooleanField(
        name='implantation',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Implantation',
            label_msgid='urban_label_implantation',
            i18n_domain='urban',
        ),
        schemata='urban_road',
    ),
    ReferenceField(
        name='architects',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=1,
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'Title':'Nom'},
            base_query="architectsBaseQuery",
            label='Architects',
            label_msgid='urban_label_architects',
            i18n_domain='urban',
        ),
        required= True,
        schemata='urban_description',
        multiValued=1,
        relationship='licenceArchitects',
        allowed_types=('Architect',),
    ),
    ReferenceField(
        name='parcellings',
        widget=ReferenceBrowserWidget(
            force_close_on_insert=True,
            allow_search=True,
            allow_browse=False,
            show_indexes=True,
            available_indexes={'subdividerName':'Nom'},
            show_index_selector=True,
            label='Parcellings',
            label_msgid='urban_label_parcellings',
            i18n_domain='urban',
        ),
        allowed_types=('ParcellingTerm',),
        schemata='urban_location',
        multiValued=1,
        relationship='licenceParcelling',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

BuildLicence_schema = GenericLicence_schema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
BuildLicence_schema['title'].required = False
##/code-section after-schema

class BuildLicence(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IBuildLicence)

    meta_type = 'BuildLicence'
    _at_rename_after_creation = True

    schema = BuildLicence_schema

    ##code-section class-header #fill in your manual code here
    #implements(interfacesToImplement)
    archetype_name = 'BuildLicence'

    ##/code-section class-header

    # Methods

    security.declarePublic('listBuildWorkTypeTerms')
    def listBuildWorkTypeTerms(self):
        """
         Return the list of worktypesterm defined in portal_urban
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('folderbuildworktypes', self))

    security.declarePublic('listRoadAdaptations')
    def listRoadAdaptations(self):
        """
          This vocabulary for field roadAdaptation returns a list of
          road adaptations : no, yes modify, yes create
        """
        service = getGlobalTranslationService()
        _ = service.translate
        lst=[
             ['no', _("urban", 'road_adaptation_no', context=self, default="No")],
             ['modify', _("urban", 'road_adaptation_modify', context=self, default="Yes, modification")],
             ['create', _("urban", 'road_adaptation_create', context=self, default="Yes, creation")],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('listUsages')
    def listUsages(self):
        """
          This vocabulary for field usage returns a list of
          building usage : for habitation, not for habitation
        """
        service = getGlobalTranslationService()
        _ = service.translate
        lst=[
             ['for_habitation', _("urban", 'usage_for_habitation', context=self, default="For habitation")],
             ['not_for_habitation', _("urban", 'usage_not_for_habitation', context=self, default="Not for habitation")],
             ['not_applicable', _("urban", 'usage_not_applicable', context=self, default="Not applicable")],
              ]
        vocab = []
        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    # Manually created methods

    security.declarePublic('architectsBaseQuery')
    def architectsBaseQuery(self):
        """
          Do add some details for the base query
          Here, we want to be sure that architects are alphabetically sorted
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        rootPath = '/'.join(portal.getPhysicalPath())
        dict = {}
        dict['path'] = {'query':'%s/urban/architects' % (rootPath)}
        dict['sort_on'] = 'sortable_title'
        return dict

    security.declarePublic('askFD')
    def askFD(self):
        """
        """
        if self.getFolderCategory() in ['udc', 'uap', 'cu2', 'lap', 'lapm']:
            return True
        else:
            return False

    security.declarePublic('getUrbanEvents')
    def getUrbanEvents(self):
        """
          Return contained UrbanEvents...
        """
        return self.objectValues("UrbanEvent")

    security.declarePublic('getAdditionalLayers')
    def getAdditionalLayers(self):
        """
          Return a list of additional layers that will be used
          when generating the mapfile
        """
        try:
            additionalLayersFolder = getattr(self, ADDITIONAL_LAYERS_FOLDER)
            return additionalLayersFolder.objectValues('Layer')
        except AttributeError:
            return None

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_create_script(self)

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        super(GenericLicence).__thisclass__.at_post_edit_script(self)



registerType(BuildLicence, PROJECTNAME)
# end of class BuildLicence

##code-section module-footer #fill in your manual code here
# Make sure the schema is correctly finalized
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('pca', after='isInPCA')
    schema.moveField('roadAdaptation', after='architects')
    schema.moveField('licenceSubject', after='title')
    schema.moveField('reference', after='licenceSubject')
    schema.moveField('architects', after='reference')
    schema.moveField('referenceDGATLP', after='reference')
    schema.moveField('foldermanagers', after='architects')
    schema.moveField('workType', after='folderCategory')
    schema.moveField('isInSubdivision', after='derogationDetails')
    schema.moveField('parcellings', after='isInSubdivision')
    schema.moveField('subdivisionDetails', after='parcellings')
    schema.moveField('isInPCA', after='subdivisionDetails')
    schema.moveField('pca', after='isInPCA')
    schema.moveField('description', after='usage')
    schema.moveField('pash', after='description')
    return schema

finalizeSchema(BuildLicence_schema)
##/code-section module-footer

