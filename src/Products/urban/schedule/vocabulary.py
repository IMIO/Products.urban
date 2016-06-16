# -*- coding: utf-8 -*-

from Products.urban.interfaces import IArticle127
from Products.urban.interfaces import IBuildLicence
from Products.urban.interfaces import IDeclaration
from Products.urban.interfaces import IDivision
from Products.urban.interfaces import IEnvClassOne
from Products.urban.interfaces import IEnvClassThree
from Products.urban.interfaces import IEnvClassTwo
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IMiscDemand
from Products.urban.interfaces import INotaryLetter
from Products.urban.interfaces import IParcelOutLicence
from Products.urban.interfaces import IPatrimonyCertificate
from Products.urban.interfaces import IPreliminaryNotice
from Products.urban.interfaces import IUrbanCertificateOne
from Products.urban.interfaces import IUrbanCertificateTwo
from Products.urban.interfaces import IUrbanEventOpinionRequest

from imio.schedule.content.vocabulary import ScheduledContentTypeVocabulary

from Products.urban import UrbanMessage

URBAN_TYPES_INTERFACES = {
    'UrbanEventOpinionRequest': IUrbanEventOpinionRequest,
    'GenericLicence': IGenericLicence,
    'BuildLicence': IBuildLicence,
    'Article127': IArticle127,
    'ParcelOutLicence': IParcelOutLicence,
    'Declaration': IDeclaration,
    'Division': IDivision,
    'UrbanCertificateOne': IUrbanCertificateOne,
    'UrbanCertificateTwo': IUrbanCertificateTwo,
    'NotaryLetter': INotaryLetter,
    'MiscDemand': IMiscDemand,
    'PatrimonyCertificate': IPatrimonyCertificate,
    'PreliminaryNotice': IPreliminaryNotice,
    'EnvClassOne': IEnvClassOne,
    'EnvClassTwo': IEnvClassTwo,
    'EnvClassThree': IEnvClassThree,
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
