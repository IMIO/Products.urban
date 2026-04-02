# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from Products.urban.interfaces import IGenericLicence

import unicodedata
import re
import logging
import transaction


STOPWORDS = {"et", "de", "le", "la", "les", "du", "des", "un", "une", "en", "a", "au", "aux"}


logger = logging.getLogger("Fix event link.py: ")


def _normalize(title):
    title = title.lower()
    title = unicodedata.normalize("NFD", title)
    title = "".join(c for c in title if unicodedata.category(c) != "Mn")
    words = set(re.findall(r"\w+", title))
    return words - STOPWORDS


def _similar(a, b, threshold=0.65):
    words_a = _normalize(a)
    words_b = _normalize(b)
    if not words_a or not words_b:
        return False

    a_in_b = len(words_a & words_b) / len(words_a)
    b_in_a = len(words_a & words_b) / len(words_b)

    return max(a_in_b, b_in_a) >= threshold


class FixEventLink(BrowserView):

    template = ViewPageTemplateFile("templates/fix_event_link.pt")

    def __call__(self):
        if self.request.form.get("form.submitted", False):
            self.fix_events()

        return self.template()

    @property
    def context_portal_type(self):
        if IGenericLicence.providedBy(self.context):
            return self.context.portal_type
        if self.context.hasProperty("urbanConfigId"):
            return self.context.getProperty("urbanConfigId")
        return None

    def check_broken_event(self, event):
        config = event.getUrbaneventtypes()
        if config is None:
            return True
        return False

    def get_events(self):
        events = {}
        if not IGenericLicence.providedBy(self.context):
            events_list = self.gather_events_across_licences()
        else:
            events_list = self.context.getAllEvents() 
        for event in events_list:
            event_key = event.title
            if self.check_broken_event(event):
                event_key = u"{}-broken".format(event_key)
            event_path = "/".join(
                event.getPhysicalPath()
            )
            if event_key in events:
                events[event_key]["path"].append(event_path)
                continue
            events[event_key] = {
                "path": [event_path],
                "id": event.getId(),
                "title": event.getRawTitle(),
                "url": event.absolute_url(),
                "urbaneventtypes": event.getField("urbaneventtypes").getRaw(event),
                "event_config_title": None,
                "event_config_path": None,
            }
            event_config = event.getUrbaneventtypes()
            if event_config:
                events[event_key]["event_config_title"] = event_config.title
                events[event_key]["event_config_path"] = "/".join(
                    event_config.getPhysicalPath()
                )
        return events

    def gather_events_across_licences(self):
        events = []
        for id, licence in self.context.contentItems():
            if IGenericLicence.providedBy(licence):
                events += licence.getAllEvents()
        return events

    def get_potential_config_fix(self, event_title):
        licence_type = self.context_portal_type
        if event_title is None or licence_type is None:
            return []
        event_title = safe_unicode(event_title)
        urban_config = api.portal.get_tool("portal_urban")
        licence_cfg = getattr(urban_config, licence_type.lower()).eventconfigs
        all_event_config = licence_cfg.objectValues()
        return [
            {
                "uid": event_config.UID(),
                "path": "/".join(event_config.getPhysicalPath()),
                "title": event_config.title,
                "url": event_config.absolute_url(),
                "state": api.content.get_state(event_config)
            }
            for event_config in all_event_config
            if (
                event_title == event_config.title
                or _similar(event_title, event_config.title)
            )
        ]

    def fix_events(self):
        form = self.request.form
        del form["form.submitted"]
        if "submit" in form:
            del form["submit"]
        for event_uids, config_uid in form.items():
            if isinstance(config_uid, list):
                config_uid = config_uid[-1]
            if config_uid == "":
                continue
            event_uids = event_uids.split("|")
            for event_uid in event_uids:
                event = api.content.get(path=event_uid)
                if event is None:
                    continue
                event.setUrbaneventtypes(config_uid)
        transaction.commit()
