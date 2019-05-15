# -*- coding: utf-8 -*-
#
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.config import PROJECTNAME
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.Inquiry import Inquiry
from Products.urban.utils import setSchemataForInquiry
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from plone import api


schema = Schema((
    ReferenceField(
        name='bound_licence',
        widget=ReferenceBrowserWidget(
            allow_search=True,
            allow_browse=False,
            force_close_on_insert=True,
            startup_directory='urban',
            show_indexes=False,
            wild_card_search=True,
            restrict_browsing_to_startup_directory=True,
            label=_('urban_label_bound_licence', default='Bound licence'),
        ),
        allowed_types=[
            t for t in URBAN_CODT_TYPES
            if t not in [
                'Inspection',
                'ProjectMeeting',
                'PatrimonyCertificate',
                'CODT_NotaryLetter',
                'CODT_UrbanCertificateOne'
            ]
        ],
        schemata='urban_description',
        multiValued=False,
        relationship="bound_licence",
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

    def getApplicants(self):
        """
        """
        applicants = self.getCorporations()
        applicants.extend(super(Inspection, self).getApplicants())
        return applicants

    security.declarePublic('get_applicants_history')

    def get_applicants_history(self):
        applicants = self.get_corporations_history()
        applicants.extend(super(Inspection, self).get_applicants_history())
        return applicants

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')
                        if api.content.get_state(corp) == 'enabled']
        return corporations

    security.declarePublic('get_corporations_history')

    def get_corporations_history(self):
        return [corp for corp in self.objectValues('Corporation')
                if api.content.get_state(corp) == 'disabled']

    def getLastInspectionReport(self):
        return self.getLastEvent(interfaces.IInspectionReportEvent)


registerType(Inspection, PROJECTNAME)


def finalize_schema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    for field in schema.fields():
        if field.schemata not in [
                'urban_description',
                'urban_advices',
                'metadata',
                'default'
            ]:
            schema.delField(field.__name__)
    schema.delField('folderCategory')
    schema.moveField('description', after='inspection_context')
    return schema


finalize_schema(Inspection_schema)
