# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

import logging


logger = logging.getLogger("Fix event link.py: ")


class FixEventLink(BrowserView):

    template = ViewPageTemplateFile("templates/fix_event_link.pt")

    def __call__(self):
        if self.request.form.get("form.submitted", False):
            self.fix_events()

        return self.template()

    def get_events(self):
        events = []
        for event in self.context.getAllEvents():
            event_dict = {
                "id": event.getId(),
                "title": event.getRawTitle(),
                "url": event.absolute_url(),
                "urbaneventtypes": event.getField("urbaneventtypes").getRaw(event),
                "event_config_title": None,
                "event_config_path": None,
            }
            event_config = event.getUrbaneventtypes()
            if event_config:
                event_dict["event_config_title"] = event_config.title
                event_dict["event_config_path"] = "/".join(
                    event_config.getPhysicalPath()
                )
            events.append(event_dict)
        return events

    def get_potential_config_fix(self, event_title):
        urban_config = api.portal.get_tool("portal_urban")
        licence_type = self.context.portal_type
        licence_cfg = getattr(urban_config, licence_type.lower()).eventconfigs
        all_event_config = licence_cfg.objectValues()
        return [
            {
                "uid": event_config.UID,
                "path": "/".join(event_config.getPhysicalPath()),
                "title": event_config.title,
                "url": event_config.absolute_url(),
            }
            for event_config in all_event_config
            if event_config.title == event_title
        ]

    def fix_events(self):
        form = self.request.form
        del form["form.submitted"]
        if "submit" in form:
            del form["submit"]
        for event_id, config_uid in form.items():
            if isinstance(config_uid, list):
                config_uid = config_uid[-1]
            if config_uid == "":
                continue
            event = self.context.get(event_id, None)
            if event is None:
                continue
            event.setUrbaneventtypes(config_uid)
