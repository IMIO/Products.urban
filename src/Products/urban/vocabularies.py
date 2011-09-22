# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 by CommunesPlone
# GNU General Public License (GPL)
import grokcore.component as grok
from zope.component import getGlobalSiteManager
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from Products.urban.interfaces import IEventTypeType
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary


class EventTypeType(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name('eventTypeType')

    def __call__(self, context):
        gsm = getGlobalSiteManager()
        interfaces = gsm.getUtilitiesFor(IEventTypeType)
        items = [SimpleTerm(interfaceName, interface.__doc__, interface.__doc__)
                 for interfaceName, interface in interfaces]
        return SimpleVocabulary(items)

class AvailableStreets(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name('availableStreets')

    def __call__(self, context):
        voc = UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", sort_on="sortable_title", inUrbanConfig=False, allowedStates=['enabled', 'disabled'])
        vocDisplayList = voc.getDisplayList(context)
        items = vocDisplayList.sortedByValue().items()
        terms = [SimpleTerm(value, value, token)
                 for value, token in items]
        return SimpleVocabulary(terms)
