# -*- coding: utf-8 -*-

from Products.urban.interfaces import IArticle127
from Products.urban.interfaces import IBaseBuildLicence
from Products.urban.interfaces import IBaseAllBuildLicence
from Products.urban.interfaces import ICODT_Article127
from Products.urban.interfaces import ICODT_BaseBuildLicence
from Products.urban.interfaces import ICODT_BuildLicence
from Products.urban.interfaces import ICODT_CommercialLicence
from Products.urban.interfaces import ICODT_IntegratedLicence
from Products.urban.interfaces import ICODT_NotaryLetter
from Products.urban.interfaces import ICODT_ParcelOutLicence
from Products.urban.interfaces import ICODT_UniqueLicence
from Products.urban.interfaces import ICODT_UrbanCertificateOne
from Products.urban.interfaces import ICODT_UrbanCertificateTwo
from Products.urban.interfaces import IBuildLicence
from Products.urban.interfaces import IDeclaration
from Products.urban.interfaces import IDivision
from Products.urban.interfaces import IEnvClassOne
from Products.urban.interfaces import IEnvClassThree
from Products.urban.interfaces import IEnvClassTwo
from Products.urban.interfaces import IEnvClassBordering
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
from Products.urban.interfaces import IExplosivesPossession
from Products.urban.interfaces import IRoadDecree


from Products.urban import UrbanMessage

from imio.schedule.content.vocabulary import ScheduledContentTypeVocabulary

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


URBAN_TYPES_INTERFACES = {
    'CODT_Article127': ICODT_Article127,
    'CODT_BaseBuildLicence': ICODT_BaseBuildLicence,
    'CODT_BuildLicence': ICODT_BuildLicence,
    'CODT_CommercialLicence': ICODT_CommercialLicence,
    'CODT_IntegratedLicence': ICODT_IntegratedLicence,
    'CODT_NotaryLetter': ICODT_NotaryLetter,
    'CODT_ParcelOutLicence': ICODT_ParcelOutLicence,
    'CODT_UniqueLicence': ICODT_UniqueLicence,
    'CODT_UrbanCertificateOne': ICODT_UrbanCertificateOne,
    'CODT_UrbanCertificateTwo': ICODT_UrbanCertificateTwo,
    'Article127': IArticle127,
    'Base BuildLicence (PU, 127, CU2)': IBaseBuildLicence,
    'All Base BuildLicence (PU, 127, CU2 CWATUP and CODT)': IBaseAllBuildLicence,
    'Urban and environment BuildLicences (PU, 127, CU2 CWATUP/CODT, PE1, PE2)': (IBaseAllBuildLicence, IEnvironmentLicence),
    'BuildLicence': IBuildLicence,
    'Declaration': IDeclaration,
    'Division': IDivision,
    'EnvClassOne': IEnvClassOne,
    'EnvClassTwo': IEnvClassTwo,
    'EnvClassThree': IEnvClassThree,
    'EnvClassBordering': IEnvClassBordering,
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
    'ExplosivesPossession': IExplosivesPossession,
    'RoadDecree': IRoadDecree,
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


class UsersFromGroupsVocabularyFactory(object):
    """
    Vocabulary factory listing all the users of a group.
    """

    group_ids = ['urban_managers', 'urban_editors']  # to override
    me_value = False  # set to True to add a value representing the current user

    def __call__(self, context):
        """
        List users from a group as a vocabulary.
        """
        base_terms = []
        me_id = ''
        user_ids = set()
        if self.me_value:
            me = api.user.get_current()
            me_id = me.id
            base_terms.append(SimpleTerm(me_id, me_id, 'Moi'))
            base_terms.append(SimpleTerm('to_assign', 'to_assign', 'À ASSIGNER'))

        voc_terms = []
        for group_id in self.group_ids:
            group = api.group.get(group_id)

            for user in api.user.get_users(group=group):
                if user.id != me_id and user.id not in user_ids:
                    user_ids.add(user.id)
                    voc_terms.append(
                        SimpleTerm(
                            user.id,
                            user.id,
                            user.getProperty('fullname') or user.getUserName()
                        )
                    )

        vocabulary = SimpleVocabulary(base_terms + sorted(voc_terms, key=lambda term: term.title))
        return vocabulary


class OpinionUsersVocabularyFactory(UsersFromGroupsVocabularyFactory):
    """
    Vocabulary factory listing all the users of the survey group.
    """
    group_ids = ['opinions_editors']
