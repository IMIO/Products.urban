# -*- coding: utf-8 -*-

from imio.schedule.utils import get_container_tasks


def reindex_tasks(licence, event):
    """
    Reindex some task indexes with licence values.
    """
    to_reindex = ("getReference", "StreetsUID", "StreetNumber", "applicantInfosIndex")

    for task in get_container_tasks(licence):
        task.reindexObject(idxs=to_reindex)
