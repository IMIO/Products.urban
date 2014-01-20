# -*- coding: utf-8 -*-
from Products.urban import UrbanMessage as _
from Products.urban.config import ORDERED_URBAN_TYPES
from Products.urban.interfaces import IUrbanEventType

from plone import api

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def licenceTypesVocabulary():
    terms = [SimpleTerm(licence, licence, _(licence))
             for licence in ORDERED_URBAN_TYPES]

    vocabulary = SimpleVocabulary(terms)
    return vocabulary


def getSchedulableEventsVocabulary(context, licence_type):
    urban_config = api.portal.get_tool('portal_urban')
    catalog = api.portal.get_tool('portal_catalog')
    licence_config = urban_config.get(licence_type, None)

    terms = [SimpleTerm('all', 'all', _(u'All'))]
    if licence_config:
        terms.append(SimpleTerm('all_opinions', 'all_opinions', _(u'All opinion requests')))
        eventtype_brains = catalog(
            object_provides=IUrbanEventType.__identifier__,
            path={'query': '/'.join(licence_config.getPhysicalPath()), 'depth': 2},
            last_key_event='schedulable',
        )
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
