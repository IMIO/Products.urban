# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

import logging
import transaction


logger = logging.getLogger("Reindex specific content types")


class ReindexContentType(BrowserView):
    """View used to reindex a specific content type."""

    template = ViewPageTemplateFile("templates/reindex.pt")

    @property
    def portal_type(self):
        return self.request.get("portal_type", None)

    @property
    def transaction_size(self):
        size = self.request.get("transaction_size", "1000")
        try:
            size = int(size)
        except ValueError:
            size = 1000
        if size < 10:
            size = 10
        if size > 10000:
            size = 10000
        return size

    def __call__(self):
        self.reindexed = []
        if not self.portal_type:
            return self.template()
        self._reindex()
        return self.template()

    def get_brains(self):
        brains = api.content.find(portal_type=self.portal_type)
        for brain in brains:
            yield brain

    def _reindex(self):
        transaction_size = self.transaction_size
        idx = 0
        for brain in self.get_brains():
            brain.getObject().reindexObject()
            path = brain.getPath()
            logger.info("Reindex {0}".format(path))
            self.reindexed.append(path)
            idx += 1
            if idx >= transaction_size:
                logger.info("Commit {0} objects".format(str(idx)))
                transaction.commit()
                idx = 0
        if idx > 0:
            logger.info("Commit {0} objects".format(str(idx)))
            transaction.commit()