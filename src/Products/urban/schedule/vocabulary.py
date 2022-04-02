# -*- coding: utf-8 -*-

from Products.urban import interfaces
from Products.urban import UrbanMessage

from imio.schedule.content.vocabulary import ScheduledContentTypeVocabulary

from plone import api

from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


URBAN_TYPES_INTERFACES = {
    'CODT_Article127': interfaces.ICODT_Article127,
    'CODT_BaseBuildLicence': interfaces.ICODT_BaseBuildLicence,
    'CODT_BuildLicence': interfaces.ICODT_BuildLicence,
    'CODT_CommercialLicence': interfaces.ICODT_CommercialLicence,
    'CODT_IntegratedLicence': interfaces.ICODT_IntegratedLicence,
    'CODT_NotaryLetter': interfaces.ICODT_NotaryLetter,
    'CODT_ParcelOutLicence': interfaces.ICODT_ParcelOutLicence,
    'CODT_UniqueLicence': interfaces.ICODT_UniqueLicence,
    'CODT_UrbanCertificateOne': interfaces.ICODT_UrbanCertificateOne,
    'CODT_UrbanCertificateTwo': interfaces.ICODT_UrbanCertificateTwo,
    'Article127': interfaces.IArticle127,
    'Base BuildLicence (PU, 127, CU2)': interfaces.IBaseBuildLicence,
    'All Base BuildLicence (PU, 127, CU2 CWATUP and CODT)': interfaces.IBaseAllBuildLicence,
    'Urban and environment BuildLicences (PU, 127, CU2 CWATUP/CODT, PE1, PE2)':
        (interfaces.IBaseAllBuildLicence, interfaces.IEnvironmentLicence),
    'BuildLicence': interfaces.IBuildLicence,
    'Declaration': interfaces.IDeclaration,
    'Division': interfaces.IDivision,
    'EnvClassOne': interfaces.IEnvClassOne,
    'EnvClassTwo': interfaces.IEnvClassTwo,
    'EnvClassThree': interfaces.IEnvClassThree,
    'EnvClassBordering': interfaces.IEnvClassBordering,
    'GenericLicence': interfaces.IGenericLicence,
    'Inspection': interfaces.IInspection,
    'IntegratedLicence': interfaces.IIntegratedLicence,
    'MiscDemand': interfaces.IMiscDemand,
    'NotaryLetter': interfaces.INotaryLetter,
    'ParcelOutLicence': interfaces.IParcelOutLicence,
    'PatrimonyCertificate': interfaces.IPatrimonyCertificate,
    'PreliminaryNotice': interfaces.IPreliminaryNotice,
    'ProjectMeeting': interfaces.IProjectMeeting,
    'Ticket': interfaces.ITicket,
    'UniqueLicence': interfaces.IUniqueLicence,
    'UrbanCertificateOne': interfaces.IUrbanCertificateOne,
    'UrbanCertificateTwo': interfaces.IUrbanCertificateTwo,
    'UrbanEventOpinionRequest': interfaces.IUrbanEventOpinionRequest,
    'ExplosivesPossession': interfaces.IExplosivesPossession,
    'RoadDecree': interfaces.IRoadDecree,
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
