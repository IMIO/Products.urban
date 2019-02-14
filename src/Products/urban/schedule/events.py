# -*- coding: utf-8 -*-

from imio.schedule.content.task import IAutomatedTask


def reindex_tasks(licence, event):
    """
    Reindex some task indexes with licence values.
    """
    to_reindex = (
        'getReference',
        'StreetsUID',
        'StreetNumber',
        'applicantInfosIndex'
    )

    to_explore = [licence]
    while to_explore:
        current = to_explore.pop()
        if IAutomatedTask.providedBy(current):
            current.reindexObject(idxs=to_reindex)
        if hasattr(current, 'objectValues'):
            to_explore.extend(current.objectValues())
