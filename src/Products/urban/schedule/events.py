# -*- coding: utf-8 -*-

from imio.schedule.content.task import IAutomatedTask

from plone import api


def reindex_tasks(licence, event):
    """
    Reindex some task indexes with licence values.
    """
    catalog = api.portal.get_tool('portal_catalog')
    to_reindex = ('StreetsUID', 'getReference', 'StreetNumber ')

    tasks_brains = catalog(
        object_provides=IAutomatedTask.__identifier__,
        path={'query': '/'.join(licence.getPhysicalPath())}
    )
    all_tasks = [brain.getObject() for brain in tasks_brains]
    for task in all_tasks:
        task.reindexObject(idxs=to_reindex)
