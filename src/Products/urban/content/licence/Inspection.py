# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import PROJECTNAME
from Products.urban.config import URBAN_TYPES
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.Inquiry import Inquiry
from Products.urban.utils import setSchemataForInquiry
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from plone import api

from zope.annotation import IAnnotations

slave_fields_bound_licence = (
    {
        'name': 'workLocations',
        'action': 'hide',
        'hide_values': (True, ),
    },
)

schema = Schema((
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
                'Inspection',
                'Ticket',
                'ProjectMeeting',
                'PatrimonyCertificate',
                'CODT_UrbanCertificateOne',
                'UrbanCertificateOne',
            ]
        ],
        schemata='urban_description',
        multiValued=True,
        relationship="bound_licences",
    ),
    BooleanField(
        name='use_bound_licence_infos',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_bound_licence,
            label=_('urban_label_use_bound_licence_infos', default='Use_bound_licence_infos'),
        ),
        schemata='urban_description',
    ),
    StringField(
        name='inspection_context',
        widget=SelectionWidget(
            format='select',
            label=_('urban_label_inspection_context', default='Inspection_context'),
        ),
        enforceVocabulary=True,
        schemata='urban_description',
        vocabulary=UrbanVocabulary('inspectioncontexts', with_empty_value=True),
        default_method='getDefaultValue',
    ),
    TextField(
        name='inspectionDescription',
        widget=RichWidget(
            label=_('urban_label_inspectionDescription', default='Inspectiondescription'),
        ),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        schemata='urban_inspection',
        default_method='getDefaultText',
        default_output_type='text/x-html-safe',
    ),
),
)
Inspection_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema', Schema(())).copy() + \
    getattr(Inquiry, 'schema', Schema(())).copy() + \
    schema.copy()

setSchemataForInquiry(Inspection_schema)


class Inspection(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IInspection)

    meta_type = 'Inspection'
    _at_rename_after_creation = True
    schema = Inspection_schema

    security.declarePublic('getApplicants')

    def getWorkLocations(self):
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                return bound_licences[0].getWorkLocations()

        field = self.getField('workLocations')
        worklocations = field.get(self)
        return worklocations

    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        proprietary = ''
        if self.getProprietaries():
            proprietary = ', '.join([app.Title() for app in self.getProprietaries()])
        title = "{}{} - {}".format(
            self.getReference(),
            proprietary and ' - {}'.format(proprietary) or '',
            self.getLicenceSubject()
        )
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'sortable_title',))

    def getParcels(self):
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                return bound_licences[0].getParcels()

        return super(Inspection, self).getParcels()

    security.declarePublic('getOfficialParcels')

    def getOfficialParcels(self):
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                return bound_licences[0].getOfficialParcels()

        return super(Inspection, self).getOfficialParcels()

    def getApplicants(self):
        """
        """
        applicants = super(Inspection, self).getApplicants()
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                applicants.extend(bound_licences[0].getApplicants())
        return list(set(applicants))

    security.declarePublic('get_applicants_history')

    def get_applicants_history(self):
        applicants = super(Inspection, self).get_applicants_history()
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                applicants.extend(bound_licences[0].get_applicants_history())
        return list(set(applicants))

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'enabled']
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                corporations.extend(bound_licences[0].getCorporations())
        return list(set(corporations))

    security.declarePublic('get_corporations_history')

    def get_corporations_history(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'Corporation' and
                        api.content.get_state(corp) == 'disabled']
        if self.getUse_bound_licence_infos():
            bound_licences = self.getBound_licences()
            if bound_licences:
                corporations.extend(bound_licences[0].get_corporations_history())
        return list(set(corporations))

    security.declarePublic('getTenants')

    def getTenants(self):
        """
           Return the list of tenants for the Licence
        """
        tenants = [app for app in self.objectValues('Applicant')
                   if app.portal_type == 'Tenant']
        return tenants

    security.declarePublic('getPlaintiffs')

    def getPlaintiffs(self):
        """
           Return the list of plaintiffs for the Licence
        """
        plaintiffs = [app for app in self.objectValues('Applicant')
                      if app.portal_type == 'Plaintiff']
        corporations = self.getCorporationPlaintiffs()
        plaintiffs.extend(corporations)
        return plaintiffs

    security.declarePublic('getCorporationPlaintiffs')

    def getCorporationPlaintiffs(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if corp.portal_type == 'CorporationPlaintiff']
        return corporations

    security.declarePublic('getLastReportEvent')

    def getLastReportEvent(self):
        return self.getLastEvent(interfaces.IUrbanEventInspectionReport)

    security.declarePublic('getAllReportEvents')

    def getAllReportEvents(self):
        return self.getAllEvents(interfaces.IUrbanEventInspectionReport)

    security.declarePublic('getCurrentReportEvent')

    def getCurrentReportEvent(self):
        last_analysis_date = None
        for action in self.workflow_history.values()[0][::-1]:
            if action['review_state'] == 'analysis':
                last_analysis_date = action['time']
                break

        if not last_analysis_date:
            return

        report_events = self.getAllReportEvents()
        for report in report_events:
            workflow_history = report.workflow_history.values()[0]
            creation_date = workflow_history[0]['time']
            if creation_date > last_analysis_date:
                return report

    security.declarePublic('getFollowUpEventsById')

    def getFollowUpEventsById(self, followup_id):
        followup_events = self.objectValues('UrbanEventFollowUp')
        if followup_id == '':
            return followup_events
        res = []
        for followup_event in followup_events:
            if followup_event.getFollowUpId() == followup_id:
                res.append(followup_event)
        return res

    security.declarePublic('getLastFollowUpEvent')

    def getLastFollowUpEvent(self):
        return self.getLastEvent(interfaces.IUrbanEventFollowUp)

    security.declarePublic('getAllFollowUpEvents')

    def getAllFollowUpEvents(self):
        return self.getAllEvents(interfaces.IUrbanEventFollowUp)

    security.declarePublic('getCurrentFollowUpEvents')

    def getCurrentFollowUpEvents(self):
        last_answer_date = None
        for action in self.workflow_history.values()[0][::-1]:
            if action['review_state'] == 'administrative_answer':
                last_answer_date = action['time']
                break
        if not last_answer_date:
            return []

        report = self.getCurrentReportEvent()
        if not report:
            return []
        ignore = ['ticket', 'close']
        selected_follow_ups = [fw_up for fw_up in report.getFollowup_proposition() if fw_up not in ignore]
        if not selected_follow_ups:
            return []

        followup_events = self.getAllFollowUpEvents()
        to_return = []
        for followup in followup_events:
            workflow_history = followup.workflow_history.values()[0]
            creation_date = workflow_history[0]['time']
            if creation_date > last_answer_date:
                uet = followup.getUrbaneventtypes()
                if uet and uet.id in selected_follow_ups:
                    to_return.append(followup)
        return to_return

    security.declarePublic('getLastFollowUpEventWithDelay')

    def getLastFollowUpEventWithDelay(self):
        return self.getLastEvent(interfaces.IUrbanEventFollowUpWithDelay)

    security.declarePublic('mayAddInspectionReportEvent')

    def mayAddInspectionReportEvent(self):
        """
           This is used as TALExpression for the UrbanEventInspectionReport
           We may add an InspectionReport only if the previous one is closed
        """
        report_events = self.getAllReportEvents()
        for report_event in report_events:
            if api.content.get_state(report_event) != 'closed':
                return False

        return True

    security.declarePublic('mayAddFollowUpEvent')

    def mayAddFollowUpEvent(self, followup_id):
        """
           This is used as TALExpression for the UrbanEventFollowUp
           We may add an UrbanEventFollowUp only if the previous one is closed
        """
        report_events = self.getAllReportEvents()
        if not report_events:
            return False

        limit = 0
        for report_event in report_events:
            if followup_id in report_event.getFollowup_proposition():
                limit += 1
        limit = limit - len(self.getFollowUpEventsById(followup_id))
        return limit > 0

    security.declarePublic('getBoundTickets')

    def getBoundTickets(self):
        """
        Return tickets referring this inspection.
        """
        annotations = IAnnotations(self)
        ticket_uids = annotations.get('urban.bound_tickets')
        if ticket_uids:
            ticket_uids = list(ticket_uids)
            uid_catalog = api.portal.get_tool('uid_catalog')
            tickets = [b.getObject() for b in uid_catalog(UID=ticket_uids)]
            return tickets


registerType(Inspection, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema['folderCategory'].widget.visible = {'edit': 'invisible', 'view': 'invisible'}
    schema.moveField('description', after='inspection_context')
    schema.moveField('bound_licences', before='workLocations')
    schema.moveField('use_bound_licence_infos', after='bound_licences')
    schema['parcellings'].widget.label = _('urban_label_parceloutlicences')
    schema['isInSubdivision'].widget.label = _('urban_label_is_in_parceloutlicences')
    schema['subdivisionDetails'].widget.label = _('urban_label_parceloutlicences_details')
    schema['pca'].vocabulary = UrbanVocabulary('sols', vocType="PcaTerm", inUrbanConfig=False)
    schema['pca'].widget.label = _('urban_label_sol')
    schema['pcaZone'].vocabulary_factory = 'urban.vocabulary.SOLZones'
    schema['pcaZone'].widget.label = _('urban_label_solZone')
    schema['isInPCA'].widget.label = _('urban_label_is_in_sol')
    schema['pcaDetails'].widget.label = _('urban_label_sol_details')
    return schema


finalize_schema(Inspection_schema)
