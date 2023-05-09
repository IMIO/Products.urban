# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import BaseFolder
from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import registerType
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from zope.i18n import translate
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.config import PROJECTNAME
from Products.urban.content.licence.EnvironmentLicence import EnvironmentLicence
from Products.urban.widget.urbanreferencewidget import UrbanReferenceWidget


schema = Schema((
    StringField(
        name='class',
        widget=SelectionWidget(
            label=_('urban_label_class', default='Class'),
        ),
        vocabulary='listExplosivesPossessionClass',
        required=True,
        schemata='urban_description',
        default_method='getDefaultValue',
    ),
    StringField(
        name='pe_reference',
        widget=UrbanReferenceWidget(
            label=_('urban_label_pe_reference', default='PE Reference'),
            portal_types=['EnvClassOne', 'EnvClassTwo'],
        ),
        required=False,
        schemata='urban_description',
        default_method='getDefaultText',
        validators=('isReference', ),
    ),
))


ExplosivesPossession_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentLicence, 'schema', Schema(())).copy() + \
    schema.copy()

ExplosivesPossession_schema['workLocations'].widget.label = _('urban_label_businessLocation')
ExplosivesPossession_schema['commentsOnSPWOpinion'].widget.label = _('urban_label_comments_on_decision_project')


class ExplosivesPossession(BaseFolder, EnvironmentLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IExplosivesPossession)

    meta_type = 'ExplosivesPossession'
    _at_rename_after_creation = True

    schema = ExplosivesPossession_schema
    schemata_order = [
        'urban_description',
        'urban_investigation_and_advices',
    ]

    security.declarePublic('getApplicantsSignaletic')

    def getApplicantsSignaletic(self, withaddress=False):
        """
        Returns a string representing the signaletic of every applicants
        """
        applicants = self.getApplicants()
        signaletic = ''
        for applicant in applicants:
            # if the signaletic is not empty, we are adding several applicants
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
            applicantTitle = ', '.join([applicant.Title() for applicant in self.getApplicants()])
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

    security.declarePublic('listExplosivesPossessionClass')

    def listExplosivesPossessionClass(self):
        """
        This vocabulary for field class return the list of classes
        """
        vocabulary = (
            ('first', _('1st class')),
            ('second', _('2nd class')),
        )
        return DisplayList(vocabulary)


registerType(ExplosivesPossession, PROJECTNAME)


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('description', after='pe_reference')
    to_remove_fields = (
        'referenceDGATLP',
        'authority',
        'rubricsDetails',
        'folderCategory',
        'applicationReasons',
        'procedureChoice',
        'bound_licences',
        'annoncedDelay',
        'validityDelay',
        'publicRoadModifications',
        'hasEnvironmentImpactStudy',
        'investigationArticles',
        'investigationArticlesText',
        'derogation',
        'derogationDetails',
        'divergence',
        'divergenceDetails',
        'demandDisplay',
        'inquiry_category',
        'investigationReasons',
        'investigationReasons',
        'roadModificationSubject',
    )
    for field in to_remove_fields:
        if field in schema:
            del schema[field]
    schema['pipelines'].schemata = 'urban_environment'
    schema['pipelinesDetails'].schemata = 'urban_environment'
    hidden_fields = (
        'businessOldLocation',
        'additionalLegalConditions',
        'rubrics',
    )
    for field in hidden_fields:
        schema[field].widget.visible = {'edit': 'invisible'}
    return schema

finalizeSchema(ExplosivesPossession_schema)
