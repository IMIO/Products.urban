# -*- coding: utf-8 -*-

from Products.urban.interfaces import IArticle127
from Products.urban.interfaces import IBaseBuildLicence
from Products.urban.interfaces import ICODT_Article127
from Products.urban.interfaces import ICODT_BaseBuildLicence
from Products.urban.interfaces import ICODT_BuildLicence
from Products.urban.interfaces import ICODT_IntegratedLicence
from Products.urban.interfaces import ICODT_NotaryLetter
from Products.urban.interfaces import ICODT_UniqueLicence
from Products.urban.interfaces import ICODT_UrbanCertificateOne
from Products.urban.interfaces import ICODT_UrbanCertificateTwo
from Products.urban.interfaces import IBuildLicence
from Products.urban.interfaces import IDeclaration
from Products.urban.interfaces import IDivision
from Products.urban.interfaces import IEnvClassOne
from Products.urban.interfaces import IEnvClassThree
from Products.urban.interfaces import IEnvClassTwo
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IIntegratedLicence
from Products.urban.interfaces import IMiscDemand
from Products.urban.interfaces import INotaryLetter
from Products.urban.interfaces import IParcelOutLicence
from Products.urban.interfaces import IPatrimonyCertificate
from Products.urban.interfaces import IPreliminaryNotice
from Products.urban.interfaces import IProjectMeeting
from Products.urban.interfaces import IUniqueLicence
from Products.urban.interfaces import IUrbanCertificateOne
from Products.urban.interfaces import IUrbanCertificateTwo
from Products.urban.interfaces import IUrbanEventOpinionRequest

from imio.schedule.content.vocabulary import ScheduledContentTypeVocabulary

from Products.urban import UrbanMessage

URBAN_TYPES_INTERFACES = {
    'CODT_Article127': ICODT_Article127,
    'CODT_BaseBuildLicence': ICODT_BaseBuildLicence,
    'CODT_BuildLicence': ICODT_BuildLicence,
    'CODT_IntegratedLicence': ICODT_IntegratedLicence,
    'CODT_NotaryLetter': ICODT_NotaryLetter,
    'CODT_UniqueLicence': ICODT_UniqueLicence,
    'CODT_UrbanCertificateOne': ICODT_UrbanCertificateOne,
    'CODT_UrbanCertificateTwo': ICODT_UrbanCertificateTwo,
    'Article127': IArticle127,
    'Base BuildLicence (PU, 127, CU2)': IBaseBuildLicence,
    'BuildLicence': IBuildLicence,
    'Declaration': IDeclaration,
    'Division': IDivision,
    'EnvClassOne': IEnvClassOne,
    'EnvClassTwo': IEnvClassTwo,
    'EnvClassThree': IEnvClassThree,
    'GenericLicence': IGenericLicence,
    'IntegratedLicence': IIntegratedLicence,
    'MiscDemand': IMiscDemand,
    'NotaryLetter': INotaryLetter,
    'ParcelOutLicence': IParcelOutLicence,
    'PatrimonyCertificate': IPatrimonyCertificate,
    'PreliminaryNotice': IPreliminaryNotice,
    'ProjectMeeting': IProjectMeeting,
    'UniqueLicence': IUniqueLicence,
    'UrbanCertificateOne': IUrbanCertificateOne,
    'UrbanCertificateTwo': IUrbanCertificateTwo,
    'UrbanEventOpinionRequest': IUrbanEventOpinionRequest,
}


class UrbanScheduledTypeVocabulary(ScheduledContentTypeVocabulary):
    """
    Adapts a TaskConfig fti to return a specific
    vocabulary for the 'task_container' field.
    """

    def content_types(self):
        """
        - The key of a voc term is the class of the content type
        - The display value is the translation of the content type
        """
        return URBAN_TYPES_INTERFACES

    def get_message_factory(self):
        return UrbanMessage
