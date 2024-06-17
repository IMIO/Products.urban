# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from plone.app.testing import login, logout
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest

CODT_BUILDLICENCE_TRANSITIONS_LIST = [
    "ask_address_validation",
    "validate_address",
    "propose_complete",
    "propose_procedure_choice",
    "validate_procedure_choice",
]


class TestCalculationDelayOpinionFD(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def _get_due_date(self, task):
        """ "Return the due date for a given task"""
        container = task.get_container()
        config = task.get_task_config()
        return config.compute_due_date(container, task)

    def _pass_workflow(self, licence):
        api.user.grant_roles(
            obj=licence, roles=["Manager"], username=self.layer.default_user
        )
        for transition in CODT_BUILDLICENCE_TRANSITIONS_LIST:
            api.content.transition(obj=licence, transition=transition)

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        login(self.portal, self.layer.default_user)
        self.portal_urban = portal.portal_urban
        depot_event_config = self.portal_urban.codt_buildlicence.urbaneventtypes[
            "depot-de-la-demande"
        ]
        rw_event_config = self.portal_urban.codt_buildlicence.urbaneventtypes[
            "transmis-2eme-dossier-rw"
        ]

        self.licence_1 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1",
        )
        self.licence_1.setProcedureChoice("FD")
        event_depot = self.licence_1.createUrbanEvent(depot_event_config)
        event_depot.setEventDate(datetime(2024, 3, 31))
        notify(ObjectModifiedEvent(self.licence_1))
        self._pass_workflow(self.licence_1)
        event_rw = self.licence_1.createUrbanEvent(rw_event_config)
        event_rw.setEventDate(datetime(2024, 3, 31))

        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("FD")
        event_depot = self.licence_2.createUrbanEvent(depot_event_config)
        event_depot.setEventDate(datetime(2024, 4, 1))
        notify(ObjectModifiedEvent(self.licence_2))
        self._pass_workflow(self.licence_2)
        event_rw = self.licence_2.createUrbanEvent(rw_event_config)
        event_rw.setEventDate(datetime(2024, 4, 1))

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, self.layer.default_user)
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_2)

    def test_delay_opinion_fd(self):
        # 35 days
        self.assertTrue("TASK_avis-fd" in self.licence_1)
        self.assertTrue("TASK_envoyer-avis-FD" in self.licence_1["TASK_avis-fd"])
        task = self.licence_1["TASK_avis-fd"]["TASK_envoyer-avis-FD"]
        self.assertEqual(datetime(2024, 5, 5).date(), self._get_due_date(task))

        # 30 days
        self.assertTrue("TASK_avis-fd" in self.licence_2)
        self.assertTrue("TASK_envoyer-avis-FD" in self.licence_2["TASK_avis-fd"])
        task = self.licence_2["TASK_avis-fd"]["TASK_envoyer-avis-FD"]
        self.assertEqual(datetime(2024, 5, 1).date(), self._get_due_date(task))
