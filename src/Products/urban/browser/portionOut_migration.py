# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.urban.interfaces import IGenericLicence
from plone import api
from plone.app.uuid.utils import uuidToObject
from plone.registry import Record
from plone.registry.field import Dict
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import logging
import os
import transaction


logger = logging.getLogger("urban: portionOut migration")


class GenerateCotentTypeList(BrowserView):
    index_key = "Products.urban.interfaces.IMigrationIndex.indexes"
    last_modified_key = "Products.urban.interfaces.IMigrationIndex.last_modified"
    src_portal_type = None

    def __call__(self):
        update = False
        if os.path.isfile(self.file):
            update = True
        self.make_file(update=update)

    @property
    def file(self):
        instance_home = os.environ.get("INSTANCE_HOME", "")
        if instance_home != "":
            instance_home = "{}/var/".format(instance_home)
        return "{}migration_{}.txt".format(instance_home, self.src_portal_type)

    def write_element(self, element, update=False):
        flag = "w"
        if update:
            flag = "a"
        with open(self.file, flag) as f:
            f.write("{}\n".format(element))

    def make_file(self, update=False):
        catalog = api.portal.get_tool("portal_catalog")
        paths = []
        portion_out_count = 0
        for count, brain in enumerate(catalog(
            object_provides=IGenericLicence.__identifier__,
            sort_on="modified",
            sort_order="descending",
        )):
            if (not update) and count == 0:
                self.init_registry_last_modified()
                self.set_last_modified(brain.modified)
            if update and (brain.modified < self.get_last_modified()):
                break
            if update and self.check_if_path_already_register(brain.getPath()):
                continue
            if count > 0 and count % 100 == 0:
                logger.info("licence : {}".format(count))
            licence_obj = uuidToObject(brain.UID)
            for obj in licence_obj.objectValues():
                if obj.portal_type == self.src_portal_type:
                    if portion_out_count > 0 and portion_out_count % 10 == 0:
                        logger.info("PortionOut : {}".format(portion_out_count))
                    paths.append('/'.join(obj.getPhysicalPath()))
                    portion_out_count += 1
        self.write_element('\n'.join(paths), update)

    def init_registry_last_modified(self):
        registry = getUtility(IRegistry)
        if self.last_modified_key in registry:
            return
        attributes = {"title": u"last modified migration"}
        registry_field = Dict(**attributes)
        registry_record = Record(registry_field)
        registry_record.value = {}
        registry.records[self.last_modified_key] = registry_record
        logger.info("last_modified registry init")

    def get_last_modified(self):
        values = api.portal.get_registry_record(
            self.last_modified_key,
            default=None,
        )
        if values is None:
            values = {}
        return values.get(self.src_portal_type, 0)

    def set_last_modified(self, last_modified):
        values = api.portal.get_registry_record(
            self.last_modified_key,
            default=None,
        )
        if values is None:
            values = {}
        values[self.src_portal_type] = last_modified
        api.portal.set_registry_record(
            self.last_modified_key,
            values,
        )
        logger.info("date: {} added in registry".format(str(last_modified)))
        transaction.commit()


class GeneratePortioOutList(GenerateCotentTypeList):
    src_portal_type = "PortionOut"
