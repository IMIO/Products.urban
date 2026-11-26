# -*- coding: utf-8 -*-
"""
Tick/untick "isKeyEvent" on an EventConfig when the edit form crashes with
"'NoneType' object has no attribute 'getSourceObject'" (stale reference).

Same as urbanEventTypesEvents.updateKeyEvent, but broken references are skipped.

External Method: module "urban.check_eventconfig_references",
function "set_eventconfig_key_event", called on the EventConfig:
    .../set_eventconfig_key_event?is_key_event=1             (dry run)
    .../set_eventconfig_key_event?is_key_event=1&dry_run=0   (apply)
"""

from AccessControl import Unauthorized
from plone import api
from zope.annotation import IAnnotations


def set_eventconfig_key_event(self, is_key_event, dry_run="1"):
    if not api.user.has_permission("Manage portal", obj=self):
        raise Unauthorized("set_eventconfig_key_event requires the 'Manage portal' permission")
    new_value = is_key_event == "1"
    ref_catalog = api.portal.get_tool("reference_catalog")

    licences = {}
    skipped = 0
    for brain in ref_catalog(targetUID=self.UID()):
        ref = brain.getObject()
        event = ref.getSourceObject() if ref is not None else None
        if event is None:
            skipped += 1
            continue
        licences[event.aq_parent.UID()] = event.aq_parent

    if dry_run == "0":
        self.isKeyEvent = new_value
        IAnnotations(self)["urban.is_key_event"] = new_value
        for licence in licences.values():
            licence.reindexObject(["last_key_event"])

    return "%s: isKeyEvent=%s, %d licences reindexed, %d broken references skipped" % (
        "APPLIED" if dry_run == "0" else "DRY RUN",
        new_value,
        len(licences),
        skipped,
    )
