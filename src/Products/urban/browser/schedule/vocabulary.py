# -*- coding: utf-8 -*-
from Products.urban import UrbanMessage as _
from Products.urban.interfaces import IUrbanEventType
from Products.urban.interfaces import IFolderManager

from plone import api

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class folderManagersVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        current_fm, foldermanagers = self.listFolderManagers(context)

        terms = []

        if current_fm:
            cfm_term = SimpleTerm(
                'me',
                'me',
                current_fm.Title().split('(')[0],
            )
            terms.append(cfm_term)

        terms.append(SimpleTerm('all', 'all', _('All')))

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
        urban_tool = api.portal.get_tool('portal_urban')
        catalog = api.portal.get_tool('portal_catalog')

        current_foldermanager = urban_tool.getCurrentFolderManager(initials=False)
        current_foldermanager_uid = current_foldermanager and current_foldermanager.UID() or ''
        foldermanagers = catalog(
            object_provides=IFolderManager.__identifier__,
            sort_on='sortable_title',
        )
        foldermanagers = [manager for manager in foldermanagers if manager.UID != current_foldermanager_uid]

        return current_foldermanager, foldermanagers

folderManagersVocabularyFactory = folderManagersVocabulary()


def getSchedulableEventsVocabulary(context, licence_type):
    urban_config = api.portal.get_tool('portal_urban')
    licence_config = urban_config.get(licence_type, None)

    terms = [SimpleTerm('all', 'all', _(u'All events'))]
    if licence_config:
        terms.append(SimpleTerm('all_opinions', 'all_opinions', _(u'All opinion requests')))

        eventtype_brains = _getAllSchedulableEventTypes(licence_config)

        for event_type in eventtype_brains:
            title = event_type.Title
            short_title = len(title) > 40 and '{title}...'.format(title=title[:39]) or title
            terms.append(SimpleTerm(
                event_type.UID,
                event_type.UID,
                short_title
            ))

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


def _getAllSchedulableEventTypes(licence_config):
    catalog = api.portal.get_tool('portal_catalog')
    eventtype_brains = catalog(
        object_provides=IUrbanEventType.__identifier__,
        path={'query': '/'.join(licence_config.getPhysicalPath()), 'depth': 2},
        last_key_event='schedulable',
        review_state='enabled',
    )

    return eventtype_brains


class buildlicenceEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'buildlicence')
buildlicenceEventsVocabularyFactory = buildlicenceEventsVocabulary()


class parceloutlicenceEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'parceloutlicence')
parceloutlicenceEventsVocabularyFactory = parceloutlicenceEventsVocabulary()


class declarationEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'declaration')
declarationEventsVocabularyFactory = declarationEventsVocabulary()


class divisionEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'division')
divisionEventsVocabularyFactory = divisionEventsVocabulary()


class urbancertificateoneEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'urbancertificateone')
urbancertificateoneEventsVocabularyFactory = urbancertificateoneEventsVocabulary()


class urbancertificatetwoEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'urbancertificatetwo')
urbancertificatetwoEventsVocabularyFactory = urbancertificatetwoEventsVocabulary()


class notaryletterEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'notaryletter')
notaryletterEventsVocabularyFactory = notaryletterEventsVocabulary()


class envclassthreeEventsVocabulary():
    implements(IVocabularyFactory)

    def __call__(self, context):
        return getSchedulableEventsVocabulary(context, 'envclassthree')
envclassthreeEventsVocabularyFactory = envclassthreeEventsVocabulary()
