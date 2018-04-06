# -*- coding: utf-8 -*-
#
# File: EnvironmentLicence.py
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

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *
from Products.urban import UrbanMessage as _

##code-section module-header #fill in your manual code here
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import ILicenceDeliveryEvent
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn

from zope.i18n import translate

optional_fields = [
    'publicRoadModifications',
    'referenceSPE', 'referenceFT', 'environmentTechnicalRemarks',
    'claimsSynthesis', 'conclusions', 'commentsOnSPWOpinion',
]
##/code-section module-header

schema = Schema((

    StringField(
        name='authority',
        widget=SelectionWidget(
            label='Authority',
            label_msgid='urban_label_authority',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('authority', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    ReferenceField(
        name='previousLicences',
        widget=ReferenceBrowserWidget(
            label='Previouslicences',
            label_msgid='urban_label_previousLicences',
            i18n_domain='urban',
        ),
        allowed_types=('EnvClassThree', 'EnvClassTwo', 'EnvClassOne'),
        schemata='urban_description',
        multiValued=True,
        relationship='previousLicences',
    ),
    DataGridField(
        name='publicRoadModifications',
        allow_oddeven=True,
        widget=DataGridWidget(
            columns={'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',)), 'modification': TextAreaColumn('Modification'), 'justification': TextAreaColumn('Justification')},
            label='Publicroadmodifications',
            label_msgid='urban_label_publicRoadModifications',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('street', 'modification', 'justification'),
    ),
    BooleanField(
        name='hasEnvironmentImpactStudy',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Hasenvironmentimpactstudy',
            label_msgid='urban_label_hasEnvironmentImpactStudy',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isSeveso',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isseveso',
            label_msgid='urban_label_isSeveso',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    LinesField(
        name='ftSolicitOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Ftsolicitopinionsto',
            label_msgid='urban_label_ftSolicitOpinionsTo',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('ftSolicitOpinionsTo', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='claimsSynthesis',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_claimsSynthesis', default='Claimssynthesis'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='environmentTechnicalAdviceAfterInquiry',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_environmentTechnicalAdviceAfterInquiry',
                    default='Environmenttechnicaladviceafterinquiry'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='commentsOnSPWOpinion',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_commentsOnSPWOpinion',
                    default='Commentsonspwopinion'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='conclusions',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_conclusions', default='Conclusions'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),
    TextField(
        name='environmentTechnicalRemarks',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_environmentTechnicalRemarks',
                    default='Environmenttechnicalremarks'),
        ),
        default_content_type='text/html',
        default_method='getDefaultText',
        schemata='urban_environment',
        default_output_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentLicence_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
EnvironmentLicence_schema['roadMissingPartsDetails'].widget.label_msgid = 'urban_label_complement'
EnvironmentLicence_schema['investigationDetails'].widget.label_msgid = 'urban_label_investigationSubject'
##/code-section after-schema

class EnvironmentLicence(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentLicence)

    meta_type = 'EnvironmentLicence'
    _at_rename_after_creation = True

    schema = EnvironmentLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    def getProcedureDelays(self, *values):
        """
        To implements in subclasses
        """

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
        """
        applicants = self.getCorporations() or super(EnvironmentLicence, self).getApplicants()
        return applicants

    security.declarePublic('getCorporations')
    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')]
        return corporations

    security.declarePublic('getFtSolicitOpinionsTo')
    def getFtSolicitOpinionsTo(self, get_obj=False):
        """
        add 'get_obj' parameter returning the vocabulary objects if set to True
        """

        if not get_obj:
            return self.ftSolicitOpinionsTo
        else:
            field = self.schema.get('ftSolicitOpinionsTo')
            all_opinions = field.vocabulary.getAllVocTerms(self)
            selected_opinions = tuple([all_opinions[selected] for selected in self.ftSolicitOpinionsTo])
            return selected_opinions

    security.declarePublic('getApplicantsSignaletic')
    def getApplicantsSignaletic(self, withaddress=False):
        """
          Returns a string representing the signaletic of every applicants
        """
        applicants = self.getApplicants()
        signaletic = ''
        for applicant in applicants:
            #if the signaletic is not empty, we are adding several applicants
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += applicant.getSignaletic(withaddress=withaddress)
        return signaletic

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        applicants = self.getCorporations() or self.getApplicants()
        if applicants:
            applicantTitle = applicants[0].Title()
        else:
            applicantTitle = translate('no_applicant_defined', 'urban', context=self.REQUEST).encode('utf8')
        title = "%s - %s - %s" % (self.getReference(), self.getLicenceSubject(), applicantTitle)
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    security.declarePublic('listLicenceParcels')
    def listLicenceParcels(self):
        parcels = self.objectValues('PortionOut')
        vocabulary = [(parcel.UID(), parcel.Title()) for parcel in parcels]
        return DisplayList(sorted(vocabulary, key=lambda name: name[1]))

    security.declarePublic('previouslicencesBaseQuery')
    def previouslicencesBaseQuery(self):
        return {'object_provides': IEnvironmentBase.__identifier__}

    def getLastLicenceDelivery(self):
        return self.getLastEvent(ILicenceDeliveryEvent)

    def getLastMissingPart(self):
        return self.getLastEvent(interfaces.IMissingPartEvent)

    security.declarePublic('getFTOpinionRequestAddresses')
    def getFTOpinionRequestAddresses(self):
        """
          Returns a formatted version of the applicants to be used in POD templates
        """
        opinion_requests = self.getFtSolicitOpinionsTo(get_obj=True)

        addresses = []
        for opinion_request in opinion_requests:
            name = opinion_request.Title()
            lines = opinion_request.Description()[3:-4].split('<br />')
            description = lines[:-2]
            address = lines[-2:]
            address = '%{name}|{description}|{street}|{city}'.format(
                name=name,
                description=' '.join(description),
                street=address[0],
                city=address[1]
            )
            addresses.append(address)
        addresses = ''.join(addresses)

        csv_adresses = '[CSV]Nom|Description|AdresseLigne1|AdresseLigne2{body}[/CSV]'.format(
            body=addresses
        )
        return csv_adresses



registerType(EnvironmentLicence, PROJECTNAME)
# end of class EnvironmentLicence

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('authority', after='referenceDGATLP')
    schema.moveField('natura2000', after='isSeveso')
    schema.moveField('natura2000location', after='natura2000')
    schema.moveField('natura2000Details', after='natura2000location')
    schema.moveField('description', after='validityDelay')

finalizeSchema(EnvironmentLicence_schema)
##/code-section module-footer

