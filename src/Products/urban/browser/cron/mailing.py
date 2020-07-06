# -*- coding: utf-8 -*-

from plone import api

from Products.Five import BrowserView

import transaction


class Mailings(BrowserView):
    """
    Browser view to call with cron to automatically
    execute all mailings registered.
    """

    def __call__(self):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        planned_mailings = (
            api.portal.get_registry_record(
                "Products.urban.interfaces.IAsyncMailing.mailings_to_do"
            )
            or {}
        )

        for event_UID in planned_mailings.keys():
            document_path = planned_mailings.pop(event_UID)
            event = catalog.unrestrictedSearchResults(UID=event_UID)[0].getObject()
            mailing_view = event.restrictedTraverse(
                "@@mailing-loop-persistent-document-generation"
            )
            mailing_view(document_url_path=document_path, force=True)
            api.portal.set_registry_record(
                "Products.urban.interfaces.IAsyncMailing.mailings_to_do",
                planned_mailings,
            )
            transaction.commit()
