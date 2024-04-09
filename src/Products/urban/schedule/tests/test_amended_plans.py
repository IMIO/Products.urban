# -*- coding: utf-8 -*-

from Products.urban.browser.actionspanel import LicenceActionsPanelView
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from datetime import datetime
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify

import unittest


class TestAmendedPlansStartDate(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def _get_due_date(self, task):
        """"Return the due date for a given task"""
        container = task.get_container()
        config = task.get_task_config()
        return config.compute_due_date(container, task)

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        api.user.grant_roles(username="urbanmanager", roles=["Member", "Manager"])
        login(self.portal, "urbanmanager")
        self.portal_urban = portal.portal_urban
        event_config = self.portal_urban.codt_buildlicence.urbaneventtypes["intention-de-depot-de-plans-modifies"]

        # receipt date + ultimatum date
        self.licence_1 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1",
        )
        self.licence_1.setProcedureChoice("simple")
        event = self.licence_1.createUrbanEvent(event_config)
        event.setReceiptDate(datetime(2024, 1, 1))
        event.setUltimeDate(datetime(2024, 3, 1))
        api.content.transition(self.licence_1, transition="ask_address_validation")
        api.content.transition(self.licence_1, transition="validate_address")
        api.content.transition(self.licence_1, transition="propose_complete")
        freeze_view = LicenceActionsPanelView(self.licence_1, self.layer["request"])
        freeze_view.triggerTransition("suspend_freeze", comment="", redirect=False)
        notify(ObjectModifiedEvent(self.licence_1))

        # receipt date only
        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("simple")
        event = self.licence_2.createUrbanEvent(event_config)
        event.setReceiptDate(datetime(2024, 1, 1))
        api.content.transition(self.licence_2, transition="ask_address_validation")
        api.content.transition(self.licence_2, transition="validate_address")
        api.content.transition(self.licence_2, transition="propose_complete")
        freeze_view = LicenceActionsPanelView(self.licence_2, self.layer["request"])
        freeze_view.triggerTransition("suspend_freeze", comment="", redirect=False)
        notify(ObjectModifiedEvent(self.licence_2))

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, self.layer.default_user)
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_2)

    def test_start_date(self):
        self.assertTrue("TASK_attente_plans_modifies" in self.licence_1)
        task = self.licence_1.TASK_attente_plans_modifies
        self.assertEqual(datetime(2024, 3, 1).date(), self._get_due_date(task))

        self.assertTrue("TASK_attente_plans_modifies" in self.licence_2)
        task = self.licence_2.TASK_attente_plans_modifies
        self.assertEqual(datetime(2024, 6, 29).date(), self._get_due_date(task))
