import importlib
import logging

from plone import api

logger = logging.getLogger('urban: fix moved class')


def set_new_class(obj, new_class_name):
    module_name, class_name = new_class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    new_class = getattr(module, class_name)

    obj_id = obj.getId()
    parent = obj.__parent__

    parent._delOb(obj_id)
    obj.__class__ = new_class
    parent._setOb(obj_id, obj)


def reindex_object(obj):
    obj.reindexObject()
    for child in obj.objectValues():
        try:
            child.reindexObject()
        except Exception:
            pass


def fix_labruyere_envclassthrees():
    """
    steps to run this fix:
    1) add `wildcard.fixmissing` (version 1.0) package to instance eggs and zcml
    2) add an environment variable:
        MISSING_EnvironmentBase Products.urban.EnvironmentBase=Products.urban.content.licence.EnvironmentBase
    3) add this function as an external method at Plone site root
         Module Name:    Products.urban.fix_moved_class
         Function Name:  fix_labruyere_envclassthrees
    4) run it
    5) undo steps 1 - 3

    It can be run via instance-debug.
    Restart instances to purge "old" object version from memory.
    """

    portal = api.portal.get()
    folder = portal.urban.envclassthrees

    # in this case, the broken objects are not in the catalog, it's an easy way to find them
    cat = api.portal.get_tool('portal_catalog')
    path = {'query': '/'.join(folder.getPhysicalPath()), 'depth': 1}
    brains = cat(path=path)
    working_ids = [brain.id for brain in brains]
    missing_ids = set(folder.objectIds()).difference(working_ids)

    for obj_id in sorted(missing_ids):
        obj = folder[obj_id]
        logger.info('fixing & reindexing {} ...'.format(obj_id))
        set_new_class(obj, 'Products.urban.content.licence.EnvClassThree.EnvClassThree')
        reindex_object(obj)

    logger.info("finished.")
