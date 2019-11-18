# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import PROJECTNAME
from Products.urban.config import URBAN_TYPES
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from plone import api

slave_fields_bound_inspection = (
    {
        'name': 'workLocations',
        'action': 'hide',
        'hide_values': (True, ),
    },
)

schema = Schema((
    StringField(
        name='referenceProsecution',
        widget=StringField._properties['widget'](
            size=60,
            label=_('urban_label_referenceProsecution', default='Referenceprosecution'),
        ),
        schemata='urban_description',
    ),
    ReferenceField(
        name='bound_inspection',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=False,
            force_close_on_insert=True,
            startup_directory='urban',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            label=_('urban_label_bound_inspection', default='Bound inspection'),
        ),
        allowed_types=['Inspection'],
        schemata='urban_description',
        multiValued=False,
        relationship="bound_inspection",
    ),
    BooleanField(
        name='use_bound_inspection_infos',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_bound_inspection,
            label=_('urban_label_use_bound_inspection_infos', default='Use_bound_inspection_infos'),
        ),
        schemata='urban_description',
    ),
    ReferenceField(
        name='bound_licences',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=False,
            force_close_on_insert=True,
            startup_directory='urban',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            label=_('urban_label_bound_licences', default='Bound licences'),
        ),
        allowed_types=[
            t for t in URBAN_TYPES
            if t not in [
                'Ticket',
                'Inspection',
                'ProjectMeeting',
                'PatrimonyCertificate',
                'CODT_NotaryLetter',
                'CODT_UrbanCertificateOne'
                'NotaryLetter',
                'UrbanCertificateOne',
            ]
        ],
        schemata='urban_description',
        multiValued=True,
        relationship="bound_licences",
    ),
),
)
Ticket_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    schema.copy()


class Ticket(BaseFolder, GenericLicence, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ITicket)

    meta_type = 'Ticket'
    _at_rename_after_creation = True
    schema = Ticket_schema

    security.declarePublic('getApplicants')

    def getWorkLocations(self):
        if self.getUse_bound_inspection_infos():
            bound_licence = self.getBound_inspection()
            if bound_licence:
                return bound_licence.getWorkLocations()

        field = self.getField('workLocations')
        worklocations = field.get(self)
        return worklocations

    def getParcels(self):
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                return bound_inspection.getParcels()

        return super(Ticket, self).getParcels()

    security.declarePublic('getOfficialParcels')

    def getOfficialParcels(self):
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                return bound_inspection.getOfficialParcels()

        return super(Ticket, self).getOfficialParcels()

    security.declarePublic('getApplicants')

    def getApplicants(self):
        """
        """
        applicants = super(Ticket, self).getApplicants()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                applicants.extend(bound_inspection.getApplicants())

        return list(set(applicants))

    security.declarePublic('get_applicants_history')

    def get_applicants_history(self):
        applicants = super(Ticket, self).get_applicants_history()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                applicants.extend(bound_inspection.get_applicants_history())

        return list(set(applicants))

    security.declarePublic('getProprietaries')

    def getProprietaries(self):
        """
        """
        proprietaries = super(Ticket, self).getProprietaries()
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                proprietaries.extend(bound_inspection.getProprietaries())

        return proprietaries

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'enabled']
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                corporations.extend(bound_inspection.getCorporations())
        return list(set(corporations))

    security.declarePublic('get_corporations_history')

    def get_corporations_history(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'disabled']
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                corporations.extend(bound_inspection.get_corporations_history())
        return list(set(corporations))

    security.declarePublic('getTenants')

    def getTenants(self):
        """
           Return the list of plaintiffs for the Licence
        """
        tenants = [app for app in self.objectValues('Applicant')
                   if app.portal_type == 'Tenant']
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                tenants.extend(bound_inspection.getTenants())
        return list(set(tenants))

    security.declarePublic('getPlaintiffs')

    def getPlaintiffs(self):
        """
           Return the list of plaintiffs for the Licence
        """
        plaintiffs = [app for app in self.objectValues('Applicant')
                      if app.portal_type == 'Plaintiff']
        corporations = self.getCorporationPlaintiffs()
        plaintiffs.extend(corporations)
        if self.getUse_bound_inspection_infos():
            bound_inspection = self.getBound_inspection()
            if bound_inspection:
                plaintiffs.extend(bound_inspection.getPlaintiffs())
        return plaintiffs

    security.declarePublic('getCorporationPlaintiffs')

    def getCorporationPlaintiffs(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'CorporationPlaintiff']
        return corporations


registerType(Ticket, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    for field in schema.fields():
        allowed_schematas = [
            'urban_description',
            'urban_inspection',
            'urban_location',
            'metadata',
            'default'
        ]
        if field.schemata not in allowed_schematas:
            schema.delField(field.__name__)
    schema.delField('folderCategory')
    schema.moveField('referenceProsecution', after='reference')
    schema.moveField('bound_inspection', before='workLocations')
    schema.moveField('use_bound_inspection_infos', after='bound_inspection')
    schema.moveField('bound_licences', after='use_bound_inspection_infos')
    schema.moveField('description', after='foldermanagers')
    return schema


finalize_schema(Ticket_schema)
