# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from Products.urban.tests.helpers import SchemaFieldsTestCase
from datetime import datetime
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify

import unittest


class TestScheduleModifiedBluePrint(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def _get_due_date(self, task):
        """"Return the due date for a given task"""
        container = task.get_container()
        config = task.get_task_config()
        return config.compute_due_date(container, task)

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        login(self.portal, self.layer.default_user)
        self.portal_urban = portal.portal_urban
        event_config = self.portal_urban.codt_buildlicence.urbaneventtypes["depot-de-la-demande"]

        self.licence_1 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1",
        )
        self.licence_1.setProcedureChoice("simple")
        event = self.licence_1.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 3, 31))
        notify(ObjectModifiedEvent(self.licence_1))

        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("simple")
        event = self.licence_2.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 4, 1))
        notify(ObjectModifiedEvent(self.licence_2))

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, self.layer.default_user)
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_2)

    def test_no_modified_blueprint_completion(self):
        # 20 days
        self.assertTrue("TASK_reception" in self.licence_1)
        self.assertTrue("TASK_check_completion" in self.licence_1.TASK_reception)
        task = self.licence_1.TASK_reception.TASK_check_completion
        self.assertEqual(datetime(2024, 4, 20).date(), self._get_due_date(task))

        # 30 days
        self.assertTrue("TASK_reception" in self.licence_2)
        self.assertTrue("TASK_check_completion" in self.licence_2.TASK_reception)
        task = self.licence_2.TASK_reception.TASK_check_completion
        self.assertEqual(datetime(2024, 5, 1).date(), self._get_due_date(task))