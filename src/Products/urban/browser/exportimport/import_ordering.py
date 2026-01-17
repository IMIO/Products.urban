# -*- coding: utf-8 -*-

from OFS.interfaces import IOrderedContainer
from collective.exportimport.import_other import ImportOrdering
from operator import itemgetter
from plone import api
from plone.uuid.interfaces import IUUID
import logging


logger = logging.getLogger(__name__)


class UrbanConfigImportOrdering(ImportOrdering):
    def import_ordering(self, data):
        results = 0
        total = len(data)
        for index, item in enumerate(data, start=1):
            obj = api.content.get(UID=item["uuid"])
            if not obj and "path" in item:
                obj = api.content.get(path=item["path"])
            if not obj:
                continue
            ordered = IOrderedContainer(obj.__parent__, None)
            if not ordered:
                continue
            ordered.moveObjectToPosition(obj.getId(), item["order"])
            if not index % 1000:
                logger.info(
                    u"Ordered {} ({}%) of {} items".format(
                        index, round(index / total * 100, 2), total
                    )
                )
            results += 1
        return results
