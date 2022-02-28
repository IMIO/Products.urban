# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 by CommunesPlone
# GNU General Public License (GPL)

from plone import api
from Products.urban.config import URBAN_CWATUPE_TYPES
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.config import URBAN_ENVIRONMENT_TYPES
from Products.urban.config import URBAN_TYPES
from Products.urban.interfaces import IFolderManager
from Products.urban.interfaces import IGenericLicence
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import getCurrentFolderManager

from zope.interface import implements
from zope.i18n import translate
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

import grokcore.component as grok


class AvailableStreets(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name('availableStreets')

    def __call__(self, context):
        voc = UrbanVocabulary(
            'streets',
            vocType=("Street", "Locality", ),
            id_to_use="UID",
            sort_on="sortable_title",
            inUrbanConfig=False,
            allowedStates=['enabled', 'disabled']
        )
        vocDisplayList = voc.getDisplayList(context)
        items = vocDisplayList.sortedByValue().items()
        terms = [SimpleTerm(value, value, token)
                 for value, token in items]
        return SimpleVocabulary(terms)


class folderManagersVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        current_fm, foldermanagers = self.listFolderManagers(context)

        terms = []

        if current_fm:
            cfm_term = SimpleTerm(
                current_fm.UID(),
                current_fm.UID(),
                current_fm.Title().split('(')[0],
            )
            terms.append(cfm_term)

        for foldermanager in foldermanagers:
            fm_term = SimpleTerm(
                foldermanager.UID,
                foldermanager.UID,
                foldermanager.Title.split('(')[0],
            )
            terms.append(fm_term)

        vocabulary = SimpleVocabulary(terms)
        return vocabulary

    def listFolderManagers(self, context):
        """
          Returns the available folder managers
        """
        catalog = api.portal.get_tool('portal_catalog')

        current_foldermanager = getCurrentFolderManager()
        current_foldermanager_uid = current_foldermanager and current_foldermanager.UID() or ''
        foldermanagers = catalog(
            object_provides=IFolderManager.__identifier__,
            review_state='enabled',
            sort_on='sortable_title',
        )
        foldermanagers = [manager for manager in foldermanagers if manager.UID != current_foldermanager_uid]

        return current_foldermanager, foldermanagers


folderManagersVocabularyFactory = folderManagersVocabulary()


class LicenceStateVocabularyFactory(object):
    """
    Vocabulary factory for 'container_state' field.
    """

    def __call__(self, context):
        """
        Return workflow states vocabulary of a licence.
        """
        portal_type = self.get_portal_type(context)

        wf_tool = api.portal.get_tool('portal_workflow')
        request = api.portal.get().REQUEST

        workfow = wf_tool.get(wf_tool.getChainForPortalType(portal_type)[0])
        voc_terms = [
            SimpleTerm(state_id, state_id, translate(state.title, 'plone', context=request))
            for state_id, state in workfow.states.items()
        ]
        # sort elements by title
        voc_terms.sort(lambda a, b: cmp(a.title, b.title))

        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary

    def get_portal_type(self, context):
        """
        """
        if context.portal_type == 'LicenceConfig':
            return context.licencePortalType
        return context.portal_type


class UrbanRootLicenceStateVocabularyFactory(LicenceStateVocabularyFactory):
    """
    Vocabulary factory for 'container_state' field.
    """

    def get_portal_type(self, context):
        """
        Return workflow states vocabulary of a licence.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        config = getattr(portal_urban, context.getProperty('urbanConfigId', ''), None)
        portal_type = config and config.getLicencePortalType() or None
        return portal_type


class ProcedureCategoryVocabulary(object):

    def __call__(self, context):
        terms = []
        codt_types = URBAN_ENVIRONMENT_TYPES + URBAN_CODT_TYPES
        cwatupe_types = URBAN_ENVIRONMENT_TYPES + URBAN_CWATUPE_TYPES

        terms = [
            SimpleTerm('codt', ','.join(codt_types), 'CODT'),
            SimpleTerm('cwatupe', ','.join(cwatupe_types), 'CWATUPE'),
        ]
        return SimpleVocabulary(terms)


ProcedureCategoryVocabularyFactory = ProcedureCategoryVocabulary()


class LicenceTypeVocabulary(object):

    def __call__(self, context):
        request = api.portal.get().REQUEST
        terms = [SimpleTerm(ltype, ltype, translate(ltype, 'urban', context=request)) for ltype in URBAN_TYPES]

        return SimpleVocabulary(terms)


LicenceTypeVocabularyFactory = LicenceTypeVocabulary()


class DateIndexVocabulary(object):

    def __call__(self, context):
        request = api.portal.get().REQUEST
        terms = [
            SimpleTerm(
                'created',
                'created',
                translate('creation date', 'urban', context=request)
            ),
            SimpleTerm(
                'modified',
                'modified',
                translate('modification date', 'urban', context=request)
            ),
            SimpleTerm(
                'getDepositDate',
                'getDepositDate',
                translate('IDeposit type marker interface', 'urban', context=request)
            ),
        ]

        return SimpleVocabulary(terms)


DateIndexVocabularyFactory = DateIndexVocabulary()


class DivisionNamesVocabulary(object):
    """
    Vocabulary factory for division names.
    """
    name = 'name'

    def __call__(self, context):
        urban_tool = api.portal.get_tool('portal_urban')
        divisions = urban_tool.getDivisionsRenaming()
        vocabulary = SimpleVocabulary(
            [SimpleTerm(
                str(div['division']),
                str(div['division']),
                unicode(div[self.name].decode('utf-8')))
                for div in divisions]
        )
        return vocabulary


DivisionNamesVocabularyFactory = DivisionNamesVocabulary()


class DivisionAlternativesNamesVocabulary(DivisionNamesVocabulary):
    """
    Vocabulary factory for alternative division names.
    """
    name = 'alternative_name'


DivisionAlternativeNamesVocabularyFactory = DivisionAlternativesNamesVocabulary()


class OffDaysTypeVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        request = api.portal.get().REQUEST
        term_ids = ['holydays', 'other']
        terms = [SimpleTerm(t_id, t_id, translate(t_id, 'urban', context=request)) for t_id in term_ids]
        return SimpleVocabulary(terms)


OffDaysTypeVocabularyFactory = OffDaysTypeVocabulary()


class OffDaysPeriodTypeVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        request = api.portal.get().REQUEST
        term_ids = ['inquiry_suspension', 'college_holydays', 'other']
        terms = [SimpleTerm(t_id, t_id, translate(t_id, 'urban', context=request)) for t_id in term_ids]
        return SimpleVocabulary(terms)


OffDaysPeriodTypeVocabularyFactory = OffDaysPeriodTypeVocabulary()


class WeekDaysVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        request = api.portal.get().REQUEST
        term_ids = [
            'weekday_mon',
            'weekday_tue',
            'weekday_wed',
            'weekday_thu',
            'weekday_fri',
            'weekday_sat',
            'weekday_sun',
        ]
        terms = [SimpleTerm(i, i, translate(t_id, 'plonelocales', context=request)) for i, t_id in enumerate(term_ids)]
        return SimpleVocabulary(terms)


WeekDaysVocabularyFactory = WeekDaysVocabulary()


class LicenceTabsVocabulary(object):

    def __call__(self, context):
        if IGenericLicence.providedBy(context):
            licence_cfg = context.getLicenceConfig()
            terms = [SimpleTerm('urban_' + tab['value'], 'urban_' + tab['value'], tab['display_name'].decode('utf-8'))
                     for tab in licence_cfg.getTabsConfig() if tab['display'] == '1']
            return SimpleVocabulary(terms)
        return []


LicenceTabsVocabularyFactory = LicenceTabsVocabulary()


class OpinionsToAskVocabulary(object):

    def __call__(self, context):
        portal_type = self.get_licence_type(context)
        vocabulary = UrbanVocabulary('eventconfigs', vocType="OpinionEventConfig", value_to_use='abbreviation')
        terms = vocabulary.get_raw_voc(context, licence_type=portal_type)
        terms = list(set([t['abbreviation'].encode('utf-8') for t in terms if t['enabled']]))
        voc_terms = [SimpleTerm(t, t, t) for t in terms]
        # sort elements by title
        voc_terms.sort(lambda a, b: cmp(a.title, b.title))
        return SimpleVocabulary(voc_terms)

    def get_licence_type(self, context):
        """
        Return workflow states vocabulary of a licence.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        config = getattr(portal_urban, context.getProperty('urbanConfigId', ''), None)
        portal_type = config and config.getLicencePortalType() or None
        return portal_type


OpinionsToAskVocabularyFactory = OpinionsToAskVocabulary()


class WorkTypesVocabulary(object):

    def __call__(self, context):
        portal_type = self.get_licence_type(context)
        vocabulary = UrbanVocabulary('folderbuildworktypes')
        terms = vocabulary.get_raw_voc(context, licence_type=portal_type)
        voc_terms = [
            SimpleTerm(t['id'], t['id'], t['title'])
            for t in terms if t['enabled']
        ]
        # sort elements by title
        voc_terms.sort(lambda a, b: cmp(a.title, b.title))
        return SimpleVocabulary(voc_terms)

    def get_licence_type(self, context):
        """
        Return workflow states vocabulary of a licence.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        config = getattr(portal_urban, context.getProperty('urbanConfigId', ''), None)
        portal_type = config and config.getLicencePortalType() or 'CODT_Buildlicence'
        return portal_type


WorkTypesVocabularyFactory = WorkTypesVocabulary()


class GigCoringUserIdVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_membership = api.portal.get_tool('portal_membership')
        users = portal_membership.searchForMembers()
        terms = [SimpleTerm(t_id._id, t_id._id, t_id._id + ' ' + (t_id.getProperty('email') or '')) for t_id in users]

        return SimpleVocabulary(terms)


GigCoringUserIdVocabularyFactory = GigCoringUserIdVocabulary()
