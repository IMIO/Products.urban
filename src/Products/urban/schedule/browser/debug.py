# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from imio.schedule.interfaces import ICalculationDelay
from imio.schedule.interfaces import IStartDate
from plone import api
from zope.component import queryMultiAdapter
from datetime import date


class TaskDebugView(BrowserView):
    @property
    def licence(self):
        return self.context.get_container()

    @property
    def task_config(self):
        return self.context.get_task_config()

    @property
    def values(self):
        base = []
        base.extend(self.attributes)
        base.extend([("review state", api.content.get_state(self.context))])
        return base

    @property
    def attributes(self):
        keys = (
            "creation_date",
            "modification_date",
            "due_date",
            "assigned_group",
            "assigned_user",
        )
        return [(k, getattr(self.context, k, "")) for k in keys]

    @property
    def licence_values(self):
        licence = self.licence
        return [
            ("title", licence.Title()),
            ("url", licence.absolute_url()),
        ]

    def debug_infos(self):
        if hasattr(self.context, "_debug_data") and self.context._debug_data:
            debug_data = []
            for key, values in self.context._debug_data.items():
                category = {"title": key, "elements": []}
                for k, v in values.items():
                    if k == "status" and v is None:
                        v = False
                    if isinstance(v, date):
                        v = v.strftime("%Y-%m-%d")
                    if isinstance(v, bool):
                        v = v is True and _("Yes") or _("No")
                    if isinstance(v, set):
                        v = [e for e in v]
                    if v is None:
                        v = ""
                    category["elements"].append({"title": k, "value": v})
                debug_data.append(category)
            return debug_data

    @property
    def start_date_values(self):
        base = []
        adapter_name = self.task_config.start_date
        adapter = queryMultiAdapter(
            (self.licence, self.context), IStartDate, name=adapter_name
        )
        if not adapter:
            return base
        licence = adapter.task_container
        deposit = licence.getLastDeposit()
        deposit_date = deposit and deposit.getEventDate()
        has_modified_blueprints_attr = hasattr(licence, "getHasModifiedBlueprints")
        has_modified_blueprints = (
            hasattr(licence, "getHasModifiedBlueprints")
            and licence.getHasModifiedBlueprints()
            or False
        )
        ack = licence.getLastAcknowledgment(state="closed")
        announced_delay = queryMultiAdapter(
            (licence, self.context),
            ICalculationDelay,
            "urban.schedule.delay.annonced_delay",
        )
        announced_delay = (
            announced_delay
            and announced_delay.calculate_delay(with_modified_blueprints=False)
            or 0
        )

        base.extend(
            [
                ("adapter", adapter.__class__),
                ("start date", adapter.start_date()),
                ("task config", adapter.task_config.absolute_url()),
                ("last deposit event", deposit.absolute_url() or ""),
                ("last deposit date", deposit_date or ""),
                ("has modified blueprints attribute", has_modified_blueprints_attr),
                ("has modified blueprints", has_modified_blueprints),
                ("last acknowledgement event", ack and ack.absolute_url() or ""),
                ("last acknowledgement date", ack and ack.getEventDate() or ""),
                ("announced delay", announced_delay),
            ]
        )
        return base
