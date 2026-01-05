# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.contentmigration.basemigrator.walker import registerWalker
from Products.contentmigration.walker import CustomQueryWalker
from Products.urban.interfaces import IGenericLicence
from datetime import date
from datetime import datetime
from plone import api
from plone.app import textfield
from plone.app.contenttypes.migration.migration import makeCustomATMigrator
from plone.app.uuid.utils import uuidToObject
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.interfaces import IDexterityFTI
from plone.registry import Record
from plone.registry.field import Dict
from plone.registry.interfaces import IRegistry
from zExceptions import NotFound
from zope.component import getUtility
from zope.component.hooks import getSite

import logging
import os
import transaction


logger = logging.getLogger("urban: migrations utils")


def migrate_date(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_date = src_obj.getField(src_fieldname).getRaw(src_obj)
    if old_date:
        new_date = date(old_date.year(), old_date.month(), old_date.day())
        setattr(dst_obj, dst_fieldname, new_date)


def migrate_to_tuple(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_value = src_obj.getField(src_fieldname).getRaw(src_obj)
    new_value = old_value
    if type(old_value) in [str, unicode]:
        new_value = (old_value,)
    elif type(old_value) is list:
        new_value = tuple(old_value)
    setattr(dst_obj, dst_fieldname, new_value)


def migrate_to_richtext(src_obj, dst_obj, src_fieldname, dst_fieldname):
    old_value = src_obj.getField(src_fieldname).getRaw(src_obj)
    new_value = old_value
    if type(old_value) is unicode:
        new_value = textfield.RichTextValue(old_value.encode("utf-8"))
    if type(old_value) is str:
        new_value = textfield.RichTextValue(old_value)
    setattr(dst_obj, dst_fieldname, new_value)

def migrate_to_shore(src_obj, dst_obj, src_fieldname, dst_fieldname):
    value = src_obj.shore
    setattr(dst_obj, "shore", value)

def clean_obsolete_portal_type(portal_type_to_remove=None, report="print"):

    if not portal_type_to_remove:
        return
    portal_types_tool = api.portal.get_tool("portal_types")
    logger.info("***Clean Obsolete Portal Type ***")
    logger.info(
        "***Step 1 Check if portal type '{}' exists ***".format(portal_type_to_remove)
    )

    catalog = api.portal.get_tool("portal_catalog")
    portal_types_objects = [
        brain.getObject() for brain in catalog(portal_type=portal_type_to_remove)
    ]

    if portal_types_objects:
        if report == "print":
            for portal_type in portal_types_objects:
                logger.info(portal_type.absolute_url())
            logger.info("Portal type found : {}".format(len(portal_types_objects)))
        if report == "csv":
            with open(
                "{}_{}.csv".format(
                    portal_type_to_remove,
                    datetime.today().strftime("%Y_%m_%d_%H_%M_%S"),
                ),
                "a",
            ) as file:
                for portal_type in portal_types_objects:
                    file.write(portal_type.absolute_url() + "\n")
        logger.info("Portal type object found : stop the process")
    else:
        logger.info("Portal type not found in linked catalog : next step!")
        logger.info(
            "***Step 2: Remove the possibility to add the {} portal type object to another portal type ***".format(
                portal_type_to_remove
            )
        )
        for portal_type in portal_types_tool:
            if hasattr(portal_types_tool.get(portal_type), "allowed_content_types"):
                if (
                    portal_type_to_remove
                    in portal_types_tool.get(portal_type).allowed_content_types
                ):
                    allowed_content_types_list = list(
                        portal_types_tool.get(portal_type).allowed_content_types
                    )
                    allowed_content_types_list.remove(portal_type_to_remove)
                    portal_types_tool.get(portal_type).allowed_content_types = tuple(
                        allowed_content_types_list
                    )

        logger.info(
            "***Step 3: Delete the {} portal type ***".format(portal_type_to_remove)
        )
        if hasattr(portal_types_tool, portal_type_to_remove):
            portal_type_obj = getattr(portal_types_tool, portal_type_to_remove)
            portal_type_obj.manage_delObjects([portal_type_obj.getId()])
        logger.info("***Done ***")


def delete_plone_objects(portal_type_object_to_delete):
    logger.info(
        "***Delete all {} portal type objects ***".format(portal_type_object_to_delete)
    )

    catalog = api.portal.get_tool("portal_catalog")
    items = [
        brain.getObject() for brain in catalog(portal_type=portal_type_object_to_delete)
    ]
    logger.info("Found {} items to be deleted".format(len(items)))
    api.content.delete(objects=items)
    logger.info("***Done ***")


def uid_catalog_reindex_objects(objects=[]):
    """
    Reindex the given objects the the UID catalog.
    """
    uid_catalog = api.portal.get_tool("uid_catalog")
    for obj in objects:
        uid_catalog.catalog_object(obj, "/".join(obj.getPhysicalPath()))


# reimplements migration method to be able to define savepoints threshold (transaction_size)
def migrateCustomAT(
    fields_mapping, src_type, dst_type, transaction_size=20, dry_run=False, full_transaction=False, use_savepoint=False
):
    """
    Try to get types infos from archetype_tool, then set a migrator an pass it
    given values. There is a dry_run mode that allows to check the success of
    a migration without committing.
    """
    portal = getSite()

    # if the type still exists get the src_meta_type from the portal_type
    portal_types = getToolByName(portal, "portal_types")
    fti = portal_types.get(src_type, None)
    # Check if the fti was removed or replaced by a DX-implementation
    if fti is None or IDexterityFTI.providedBy(fti):
        # Get the needed info from an instance of the type
        catalog = portal.portal_catalog
        brains = catalog(portal_type=src_type, sort_limit=1)
        if not brains:
            # no item? assume stuff
            is_folderish = False
            src_meta_type = src_type
        else:
            try:
                src_obj = brains[0].getObject()
            except (KeyError, NotFound):
                logger.error(
                    "Could not find the object for brain at %s", brains[0].getURL()
                )
                return
            if IDexterityContent.providedBy(src_obj):
                logger.error(
                    "%s should not be dexterity object!" % src_obj.absolute_url()
                )
            is_folderish = getattr(src_obj, "isPrincipiaFolderish", False)
            src_meta_type = src_obj.meta_type
    else:
        # Get info from at-fti
        src_meta_type = fti.content_meta_type
        archetype_tool = getToolByName(portal, "archetype_tool", None)
        for info in archetype_tool.listRegisteredTypes():
            # lookup registered type in archetype_tool with meta_type
            # because several portal_types can use same meta_type
            if info.get("meta_type") == src_meta_type:
                klass = info.get("klass", None)
                is_folderish = klass.isPrincipiaFolderish

    migrator = makeCustomATMigrator(
        context=portal,
        src_type=src_type,
        dst_type=dst_type,
        fields_mapping=fields_mapping,
        is_folderish=is_folderish,
        dry_run=dry_run,
    )
    if migrator:
        migrator.src_meta_type = src_meta_type
        migrator.dst_meta_type = ""
        walker_settings = {
            "portal": portal,
            "migrator": migrator,
            "src_portal_type": src_type,
            "dst_portal_type": dst_type,
            "src_meta_type": src_meta_type,
            "dst_meta_type": "",
            "transaction_size": transaction_size,
            "full_transaction": full_transaction,
            "use_savepoint": use_savepoint,
        }
        if dry_run:
            walker_settings["limit"] = 1
        walker = CustomQueryWalker(**walker_settings)
        walker.go()
        walker_infos = {
            "errors": walker.errors,
            "msg": walker.getOutput().splitlines(),
            "counter": walker.counter,
        }
        for error in walker.errors:
            logger.error(error.get("message"))
        if dry_run:
            transaction.abort()
        return walker_infos


class UrbanLicenceWalker(CustomQueryWalker):
    def walk(self):
        catalog = self.catalog

        for brain in catalog(object_provides=IGenericLicence.__identifier__):
            licence_obj = uuidToObject(brain.UID)
            objs = licence_obj.listFolderContents(
                contentFilter={"portal_type": self.src_portal_type}
            )
            for obj in objs:
                if self.callBefore is not None and callable(self.callBefore):
                    if self.callBefore(obj, **self.kwargs) == False:
                        continue
                try:
                    state = obj._p_changed
                except:
                    state = 0
                if obj is not None:
                    yield obj
                    # safe my butt
                    if state is None:
                        obj._p_deactivate()

registerWalker(UrbanLicenceWalker)

class UrbanLicenceToFileWalker(CustomQueryWalker):
    index_key = "Products.urban.interfaces.IMigrationIndex.indexes"
    last_modified_key = "Products.urban.interfaces.IMigrationIndex.last_modified"

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

    def check_if_path_already_register(self, path):
        with open(self.file, "r") as f:
            for line in f:
                if path in line:
                    return True
        return False

    def make_file(self, update=False):
        catalog = self.catalog
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

    def get_elements(self):
        update = False
        if os.path.isfile(self.file):
            update = True
        self.make_file(update)
        with open(self.file, "r") as f:
            for count, line in enumerate(f):
                if count >= self.get_index():
                    yield line.rstrip("\n")

    def init_registry_indexes(self):
        registry = getUtility(IRegistry)
        if self.index_key in registry:
            return
        attributes = {"title": u"index migration"}
        registry_field = Dict(**attributes)
        registry_record = Record(registry_field)
        registry_record.value = {}
        registry.records[self.index_key] = registry_record
        logger.info("index registry init")

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

    def get_index(self):
        values = api.portal.get_registry_record(
            self.index_key,
            default=None,
        )
        if values is None:
            values = {}
        return values.get(self.src_portal_type, 0)

    def set_index(self, index):
        values = api.portal.get_registry_record(
            self.index_key,
            default=None,
        )
        if values is None:
            values = {}
        values[self.src_portal_type] = index
        api.portal.set_registry_record(
            self.index_key,
            values
        )
        logger.info("index: {} added in registry".format(str(index)))
        transaction.commit()

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
            values
        )
        logger.info("date: {} added in registry".format(str(last_modified)))
        transaction.commit()

    def commit(self, current_index):
        self.init_registry_indexes()
        self.set_index(current_index + 1)

    def clear(self):
        registry = getUtility(IRegistry)
        if self.index_key in registry:
            del registry.records[self.index_key]
        if self.last_modified_key in registry:
            del registry.records[self.last_modified_key]
        if os.path.isfile(self.file):
            os.remove(self.file)

    def walk(self):
        start = self.get_index()
        for local_count, element in enumerate(self.get_elements()):
            global_count = start + local_count

            obj = api.content.get(path=element)

            if self.callBefore is not None and callable(self.callBefore):
                if self.callBefore(obj, **self.kwargs) == False:
                    continue
            try:
                state = obj._p_changed
            except:
                state = 0
            if obj is not None:
                yield obj
                # safe my butt
                if state is None:
                    obj._p_deactivate()

                if global_count != 0 and global_count % self.transaction_size == 0:
                    self.commit(global_count)

registerWalker(UrbanLicenceToFileWalker)

# reimplements migration method to be able to define savepoints threshold (transaction_size)
def migrateCustomAT_trough_licences(
    fields_mapping, src_type, dst_type, transaction_size=20, dry_run=False, full_transaction=False, use_savepoint=False
):
    """
    Try to get types infos from archetype_tool, then set a migrator an pass it
    given values. There is a dry_run mode that allows to check the success of
    a migration without committing.
    """
    portal = getSite()

    # if the type still exists get the src_meta_type from the portal_type
    portal_types = getToolByName(portal, "portal_types")
    fti = portal_types.get(src_type, None)
    # Check if the fti was removed or replaced by a DX-implementation
    if fti is None or IDexterityFTI.providedBy(fti):
        # Get the needed info from an instance of the type
        catalog = portal.portal_catalog
        brains = catalog(portal_type=src_type, sort_limit=1)
        if not brains:
            # no item? assume stuff
            is_folderish = False
            src_meta_type = src_type
        else:
            try:
                src_obj = brains[0].getObject()
            except (KeyError, NotFound):
                logger.error(
                    "Could not find the object for brain at %s", brains[0].getURL()
                )
                return
            if IDexterityContent.providedBy(src_obj):
                logger.error(
                    "%s should not be dexterity object!" % src_obj.absolute_url()
                )
            is_folderish = getattr(src_obj, "isPrincipiaFolderish", False)
            src_meta_type = src_obj.meta_type
    else:
        # Get info from at-fti
        src_meta_type = fti.content_meta_type
        archetype_tool = getToolByName(portal, "archetype_tool", None)
        for info in archetype_tool.listRegisteredTypes():
            # lookup registered type in archetype_tool with meta_type
            # because several portal_types can use same meta_type
            if info.get("meta_type") == src_meta_type:
                klass = info.get("klass", None)
                is_folderish = klass.isPrincipiaFolderish

    migrator = makeCustomATMigrator(
        context=portal,
        src_type=src_type,
        dst_type=dst_type,
        fields_mapping=fields_mapping,
        is_folderish=is_folderish,
        dry_run=dry_run,
    )
    if migrator:
        migrator.src_meta_type = src_meta_type
        migrator.dst_meta_type = ""
        walker_settings = {
            "portal": portal,
            "migrator": migrator,
            "src_portal_type": src_type,
            "dst_portal_type": dst_type,
            "src_meta_type": src_meta_type,
            "dst_meta_type": "",
            "transaction_size": transaction_size,
            "full_transaction": full_transaction,
            "use_savepoint": use_savepoint,
        }
        if dry_run:
            walker_settings["limit"] = 1
        walker = UrbanLicenceToFileWalker(**walker_settings)
        walker.go()
        walker.clear()
        walker_infos = {
            "errors": walker.errors,
            "msg": walker.getOutput().splitlines(),
            "counter": walker.counter,
        }
        for error in walker.errors:
            logger.error(error.get("message"))
        if dry_run:
            transaction.abort()
        return walker_infos
