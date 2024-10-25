# -*- coding: utf-8 -*-

from OFS.interfaces import IOrderedContainer
from collective.exportimport.export_other import ExportOrdering
from operator import itemgetter
from plone import api
from plone.uuid.interfaces import IUUID


class UrbanConfigExportOrdering(ExportOrdering):
    def all_orders(self):
        results = []

        def get_position_in_parent(obj, path):
            uid = IUUID(obj, None)
            if not uid:
                return
            parent = obj.__parent__
            ordered = IOrderedContainer(parent, None)
            if ordered is not None:
                order = ordered.getObjectPosition(obj.getId())
                if order is not None:
                    results.append({"uuid": uid, "order": order})
            return

        portal = api.portal.get()
        portal.ZopeFindAndApply(
            self.context, search_sub=True, apply_func=get_position_in_parent
        )
        return sorted(results, key=itemgetter("order"))
