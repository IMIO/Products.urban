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


class EventTypeType(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name('eventTypeType')

    def __call__(self, context):
        gsm = getGlobalSiteManager()
        interfaces = gsm.getUtilitiesFor(IEventTypeType)
        items = [SimpleTerm(interfaceName, interface.__doc__, interface.__doc__)
                 for interfaceName, interface in interfaces]
        return SimpleVocabulary(items)
