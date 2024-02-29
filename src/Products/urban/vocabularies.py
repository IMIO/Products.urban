# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 by CommunesPlone
# GNU General Public License (GPL)
from Products.CMFPlone.i18nl10n import utranslate

from plone import api
from Products.urban.config import URBAN_CWATUPE_TYPES
from Products.urban.config import URBAN_CODT_TYPES
from Products.urban.config import URBAN_ENVIRONMENT_TYPES
from Products.urban.config import URBAN_TYPES
from Products.urban.config import EMPTY_VOCAB_VALUE
from Products.urban.interfaces import IEventTypeType
from Products.urban.interfaces import IFolderManager
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import getCurrentFolderManager

from zope.component import getGlobalSiteManager
from zope.interface import implements
from zope.i18n import translate
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

import grokcore.component as grok


class EventTypeType(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name("eventTypeType")

    def __call__(self, context):
        gsm = getGlobalSiteManager()
        interfaces = gsm.getUtilitiesFor(IEventTypeType)
        items = []
        # we add an empty vocab value of type "choose a value"
        val = utranslate(
            domain="urban",
            msgid=EMPTY_VOCAB_VALUE,
            context=context,
            default=EMPTY_VOCAB_VALUE,
        )
        items.append(SimpleTerm("", val, val))
        items = items + [
            SimpleTerm(
                interfaceName,
                interface.__doc__,
                utranslate(
                    msgid=interface.__doc__,
                    domain="urban",
                    context=context,
                    default=interface.__doc__,
                ),
            )
            for interfaceName, interface in interfaces
        ]

        # sort elements by title
        def sort_function(x, y):
            z = cmp(x.title, y.title)
            return z

        items.sort(sort_function)
        return SimpleVocabulary(items)


class AvailableStreets(grok.GlobalUtility):
    grok.provides(IVocabularyFactory)
    grok.name("availableStreets")

    def __call__(self, context):
        voc = UrbanVocabulary(
            "streets",
            vocType=(
                "Street",
                "Locality",
            ),
            id_to_use="UID",
            sort_on="sortable_title",
            inUrbanConfig=False,
            allowedStates=["enabled", "disabled"],
        )
        vocDisplayList = voc.getDisplayList(context)
        items = vocDisplayList.sortedByValue().items()
        terms = [SimpleTerm(value, value, token) for value, token in items]
        return SimpleVocabulary(terms)


class folderManagersVocabulary:
    implements(IVocabularyFactory)

    def __call__(self, context):
        current_fm, foldermanagers = self.listFolderManagers(context)

        terms = []

        if current_fm:
            cfm_term = SimpleTerm(
                current_fm.UID(),
                current_fm.UID(),
                current_fm.Title().split("(")[0],
            )
            terms.append(cfm_term)

        for foldermanager in foldermanagers:
            fm_term = SimpleTerm(
                foldermanager.UID,
                foldermanager.UID,
                foldermanager.Title.split("(")[0],
            )
            terms.append(fm_term)

        vocabulary = SimpleVocabulary(terms)
        return vocabulary

    def listFolderManagers(self, context):
        """
        Returns the available folder managers
        """
        catalog = api.portal.get_tool("portal_catalog")

        current_foldermanager = getCurrentFolderManager()
        current_foldermanager_uid = (
            current_foldermanager and current_foldermanager.UID() or ""
        )
        foldermanagers = catalog(
            object_provides=IFolderManager.__identifier__,
            review_state="enabled",
            sort_on="sortable_title",
        )
        foldermanagers = [
            manager
            for manager in foldermanagers
            if manager.UID != current_foldermanager_uid
        ]

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

        wf_tool = api.portal.get_tool("portal_workflow")
        request = api.portal.get().REQUEST

        workfow = wf_tool.get(wf_tool.getChainForPortalType(portal_type)[0])
        voc_terms = [
            SimpleTerm(
                state_id, state_id, translate(state.title, "plone", context=request)
            )
            for state_id, state in workfow.states.items()
        ]
        # sort elements by title
        voc_terms.sort(lambda a, b: cmp(a.title, b.title))

        vocabulary = SimpleVocabulary(voc_terms)

        return vocabulary

    def get_portal_type(self, context):
        """ """
        if context.portal_type == "LicenceConfig":
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
        portal_urban = api.portal.get_tool("portal_urban")
        config = getattr(portal_urban, context.getProperty("urbanConfigId", ""), None)
        portal_type = config and config.getLicencePortalType() or None
        return portal_type


class ProcedureCategoryVocabulary(object):
    def __call__(self, context):
        terms = []
        codt_types = URBAN_ENVIRONMENT_TYPES + URBAN_CODT_TYPES
        cwatupe_types = URBAN_ENVIRONMENT_TYPES + URBAN_CWATUPE_TYPES

        terms = [
            SimpleTerm("codt", ",".join(codt_types), "CODT"),
            SimpleTerm("cwatupe", ",".join(cwatupe_types), "CWATUPE"),
        ]
        return SimpleVocabulary(terms)


ProcedureCategoryVocabularyFactory = ProcedureCategoryVocabulary()


class LicenceTypeVocabulary(object):
    def __call__(self, context):
        request = api.portal.get().REQUEST
        terms = [
            SimpleTerm(ltype, ltype, translate(ltype, "urban", context=request))
            for ltype in URBAN_TYPES
        ]

        return SimpleVocabulary(terms)


LicenceTypeVocabularyFactory = LicenceTypeVocabulary()


class DateIndexVocabulary(object):
    def __call__(self, context):
        request = api.portal.get().REQUEST
        terms = [
            SimpleTerm(
                "created",
                "created",
                translate("creation date", "urban", context=request),
            ),
            SimpleTerm(
                "modified",
                "modified",
                translate("modification date", "urban", context=request),
            ),
            SimpleTerm(
                "getDepositDate",
                "getDepositDate",
                translate("IDeposit type marker interface", "urban", context=request),
            ),
        ]

        return SimpleVocabulary(terms)


DateIndexVocabularyFactory = DateIndexVocabulary()
