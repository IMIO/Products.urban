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

from datetime import datetime
from mock import Mock
from DateTime import DateTime

from urban.schedule.conditions.delay import CalculationDelayOpinionFd
from imio.schedule.testing import ExampleScheduleFunctionalTestCase
from imio.schedule.tests.due_date import ContainerCreationDate

import unittest

CODT_BUILDLICENCE_WORKFLOWS = {
    "ask_address_validation": None,
    "validate_address":["AddressEditor"],
    "check_completion": None,
    "propose_procedure_choice": ["Editor", "Contributor","AddressEditor"],
    "validate_procedure_choice": ["Contributor"]
}


class TestCalculationDelayOpinionFD(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def _get_due_date(self, task):
        """"Return the due date for a given task"""
        container = task.get_container()
        config = task.get_task_config()
        return config.compute_due_date(container, task)

    def _pass_workflow(self, licence):
        api.user.grant_roles(obj=licence,roles=["Manager"], username=self.layer.default_user)
        for workflow, roles in CODT_BUILDLICENCE_WORKFLOWS.items():
            api.content.transition(obj=licence, transition=workflow)

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
        self.licence_1.setProcedureChoice("FD")
        event = self.licence_1.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 3, 31))
        notify(ObjectModifiedEvent(self.licence_1))
        self._pass_workflow(self.licence_1)
        __import__('pdb').set_trace()

        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("FD")
        event = self.licence_2.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 4, 1))
        notify(ObjectModifiedEvent(self.licence_2))
        self._pass_workflow(self.licence_2)

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, self.layer.default_user)
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_2)

    def test_delay_opinion_fd(self):
        # 35 days
        self.assertTrue("TASK_avis_fd" in self.licence_1)
        self.assertTrue("TASK_envoyer_avis_FD" in self.licence_1.TASK_avis_fd)
        task = self.licence_1.TASK_avis_fd.TASK_envoyer_avis_FD
        self.assertEqual(datetime(2024, 5, 5).date(), self._get_due_date(task))

        # 30 days
        self.assertTrue("TASK_avis_fd" in self.licence_2)
        self.assertTrue("TASK_envoyer_avis_FD" in self.licence_2.TASK_avis_fd)
        task = self.licence_2.TASK_avis_fd.TASK_envoyer_avis_FD
        self.assertEqual(datetime(2024, 5, 1).date(), self._get_due_date(task))
