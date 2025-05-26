# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from datetime import datetime
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from dateutil.relativedelta import relativedelta

import unittest


class TestAmendedPlansStartDate(unittest.TestCase):
    maxDiff = 9999
    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def _get_due_date(self, task):
        """ "Return the due date for a given task"""
        container = task.get_container()
        config = task.get_task_config()
        return config.compute_due_date(container, task)

    def _create_recepisse_plans_modificatifs(self, licence, event_date):
        event_config = self.portal_urban.codt_buildlicence.eventconfigs[
            "recepisse-de-plans-modificatifs"
        ]
        event = licence.createUrbanEvent(event_config)
        event.setEventDate(event_date)
        notify(ObjectModifiedEvent(licence))

    def setUp(self):
        portal = self.layer["portal"]
        self.portal = portal
        api.user.grant_roles(username="urbanmanager", roles=["Member", "Manager"])
        api.group.add_user(username="urbanmanager", groupname="urban_editors")
        login(self.portal, "urbanmanager")
        self.portal_urban = portal.portal_urban
        event_config_deposit = self.portal_urban.codt_buildlicence.eventconfigs[
            "depot-de-la-demande-codt"
        ]
        event_config_intention = self.portal_urban.codt_buildlicence.eventconfigs[
            "intention-de-depot-de-plans-modifies"
        ]

        # receipt date + ultimatum date
        self.licence_1 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 1",
        )
        self.licence_1.setProcedureChoice("simple")

        event = self.licence_1.createUrbanEvent(event_config_deposit)
        event.setEventDate(datetime(2024, 4, 10))

        event_config_intention = self.portal_urban.codt_buildlicence.eventconfigs[
            "intention-de-depot-de-plans-modifies"
        ]
        event = self.licence_1.createUrbanEvent(event_config_intention)
        event.setReceiptDate(datetime(2024, 4, 20))
        event.setUltimeDate(datetime(2024, 6, 23))

        self.licence_1.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_1, transition="iscomplete")
        api.content.transition(self.licence_1, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_1))

        # receipt date only
        self.licence_2 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 2",
        )
        self.licence_2.setProcedureChoice("simple")

        event = self.licence_2.createUrbanEvent(event_config_deposit)
        event.setEventDate(datetime(2024, 4, 10))
        api.content.transition(event, to_state="closed")
        event = self.licence_2.createUrbanEvent(event_config_intention)
        event.setReceiptDate(datetime(2024, 4, 20))

        self.licence_2.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_2, transition="iscomplete")
        api.content.transition(self.licence_2, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_2))

        # no date
        self.licence_3 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 3",
        )
        self.licence_3.setProcedureChoice("simple")
        event = self.licence_3.createUrbanEvent(event_config_deposit)
        event.setEventDate(datetime(2024, 4, 10))
        event_config_intention = self.portal_urban.codt_buildlicence.eventconfigs[
            "intention-de-depot-de-plans-modifies"
        ]
        event = self.licence_3.createUrbanEvent(event_config_intention)

        self.licence_3.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_3, transition="iscomplete")
        api.content.transition(self.licence_3, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_3))

        # no date and not suspended
        self.licence_4 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 4",
        )
        self.licence_4.setProcedureChoice("simple")
        event = self.licence_4.createUrbanEvent(event_config_deposit)
        event.setEventDate(datetime.now() - relativedelta(days=+10))
        event_config_intention = self.portal_urban.codt_buildlicence.eventconfigs[
            "intention-de-depot-de-plans-modifies"
        ]
        event = self.licence_4.createUrbanEvent(event_config_intention)
        event.setReceiptDate(datetime.now())

        self.licence_4.setHasModifiedBlueprints(True)
        notify(ObjectModifiedEvent(self.licence_4))

        # not suspended and deposit under 35 days
        self.licence_5 = api.content.create(
            type="CODT_BuildLicence",
            container=self.portal.urban.codt_buildlicences,
            title="Licence 5",
        )
        self.licence_5.setProcedureChoice("simple")
        event = self.licence_5.createUrbanEvent(event_config_deposit)
        event.setEventDate(datetime.now() - relativedelta(days=+35))
        event_config_intention = self.portal_urban.codt_buildlicence.eventconfigs[
            "intention-de-depot-de-plans-modifies"
        ]
        event = self.licence_5.createUrbanEvent(event_config_intention)
        event.setReceiptDate(datetime.now() - relativedelta(days=+35))

        self.licence_5.setHasModifiedBlueprints(True)
        notify(ObjectModifiedEvent(self.licence_5))

        logout()
        login(portal, "urbaneditor")

    def tearDown(self):
        login(self.portal, "urbanmanager")
        api.content.delete(self.licence_1)
        api.content.delete(self.licence_2)
        api.content.delete(self.licence_3)
        api.content.delete(self.licence_4)
        api.content.delete(self.licence_5)

    def test_start_date(self):
        # receipt date + ultimatum date
        self.assertTrue("TASK_reception" in self.licence_1)
        self.assertTrue("TASK_attente_plans_modifies" in self.licence_1.TASK_reception)
        task = self.licence_1.TASK_reception.TASK_attente_plans_modifies
        self.assertEqual(datetime(2024, 6, 23).date(), self._get_due_date(task))

        # receipt date only
        self.assertTrue("TASK_reception" in self.licence_2)
        self.assertTrue("TASK_attente_plans_modifies" in self.licence_2.TASK_reception)
        task = self.licence_2.TASK_reception.TASK_attente_plans_modifies
        self.assertEqual(datetime(2024, 10, 17).date(), self._get_due_date(task))

        # no date
        self.assertTrue("TASK_reception" in self.licence_3)
        self.assertTrue("TASK_attente_plans_modifies" in self.licence_3.TASK_reception)
        task = self.licence_3.TASK_reception.TASK_attente_plans_modifies
        self.assertEqual(datetime(9999, 1, 1).date(), self._get_due_date(task))

    def test_delay_amend_then_resume(self):
        """1 2 3 4 5"""
        login(self.portal, "urbanmanager")

        self._create_recepisse_plans_modificatifs(self.licence_1, datetime(2024, 5, 10))
        api.content.transition(self.licence_1, transition="resume")
        notify(ObjectModifiedEvent(self.licence_1))
        self.assertTrue("TASK_reception" in self.licence_1)
        self.assertTrue("TASK_check_completion-1" in self.licence_1.TASK_reception)
        task = self.licence_1.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

        self._create_recepisse_plans_modificatifs(self.licence_2, datetime(2024, 5, 10))
        api.content.transition(self.licence_2, transition="resume")
        notify(ObjectModifiedEvent(self.licence_2))
        self.assertTrue("TASK_reception" in self.licence_2)
        self.assertTrue("TASK_check_completion-1" in self.licence_2.TASK_reception)
        task = self.licence_2.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

        self._create_recepisse_plans_modificatifs(self.licence_3, datetime(2024, 5, 10))
        api.content.transition(self.licence_3, transition="resume")
        notify(ObjectModifiedEvent(self.licence_3))
        self.assertTrue("TASK_reception" in self.licence_3)
        self.assertTrue("TASK_check_completion-1" in self.licence_3.TASK_reception)
        task = self.licence_3.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

    def test_delay_resume_only(self):
        """tester 1 2 4 (check 5 = date 2 + 180j)"""
        login(self.portal, "urbanmanager")

        api.content.transition(self.licence_1, transition="resume")
        notify(ObjectModifiedEvent(self.licence_1))

        self.assertTrue("TASK_reception" in self.licence_1)
        self.assertTrue("TASK_check_completion-1" in self.licence_1.TASK_reception)
        task = self.licence_1.TASK_reception["TASK_check_completion-1"]

        self.assertEqual(datetime(2024, 7, 23).date(), self._get_due_date(task))

        api.content.transition(self.licence_2, transition="resume")
        notify(ObjectModifiedEvent(self.licence_2))
        self.assertTrue("TASK_check_completion-1" in self.licence_2.TASK_reception)
        task = self.licence_2.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 11, 16).date(), self._get_due_date(task))

        api.content.transition(self.licence_3, transition="resume")
        notify(ObjectModifiedEvent(self.licence_3))
        self.assertTrue("TASK_check_completion-1" in self.licence_3.TASK_reception)
        task = self.licence_3.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 5, 10).date(), self._get_due_date(task))

    def test_delay_resume_then_amend(self):
        """1 2 4 3 (check 5 = date dépot plans du 3 + 20/30j) 5"""
        login(self.portal, "urbanmanager")

        api.content.transition(self.licence_1, transition="resume")
        notify(ObjectModifiedEvent(self.licence_1))
        self._create_recepisse_plans_modificatifs(self.licence_1, datetime(2024, 5, 10))
        self.assertTrue("TASK_reception" in self.licence_1)
        self.assertTrue("TASK_check_completion-1" in self.licence_1.TASK_reception)
        task = self.licence_1.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

        api.content.transition(self.licence_2, transition="resume")
        notify(ObjectModifiedEvent(self.licence_2))
        self._create_recepisse_plans_modificatifs(self.licence_2, datetime(2024, 5, 10))
        self.assertTrue("TASK_reception" in self.licence_2)
        self.assertTrue("TASK_check_completion-1" in self.licence_2.TASK_reception)
        task = self.licence_2.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

        api.content.transition(self.licence_3, transition="resume")
        notify(ObjectModifiedEvent(self.licence_3))
        self._create_recepisse_plans_modificatifs(self.licence_3, datetime(2024, 5, 10))
        self.assertTrue("TASK_reception" in self.licence_3)
        self.assertTrue("TASK_check_completion-1" in self.licence_3.TASK_reception)
        task = self.licence_3.TASK_reception["TASK_check_completion-1"]
        self.assertEqual(datetime(2024, 6, 9).date(), self._get_due_date(task))

    def test_task_closed_on_suspend(self):
        """Ensure that task are correctly closed when we suspend the licence"""
        login(self.portal, "urbanmanager")

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_deposit",
        ]
        reception_task = self.licence_4.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "created"),
            ("TASK_deposit", "to_do"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        self.licence_4.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_4, transition="iscomplete")
        api.content.transition(self.licence_4, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_4))

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_send_acknoledgment",
            "TASK_deposit",
            "TASK_attente_plans_modifies",
        ]
        reception_task = self.licence_4.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "to_do"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        # Ensure that even after a modification, nothing changed
        notify(ObjectModifiedEvent(self.licence_4))
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

    def test_task_on_reopen(self):
        """Ensure that task are correctly recreated when we reopen the licence"""
        login(self.portal, "urbanmanager")

        self.licence_4.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_4, transition="iscomplete")
        api.content.transition(self.licence_4, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_4))

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_send_acknoledgment",
            "TASK_deposit",
            "TASK_attente_plans_modifies",
        ]
        reception_task = self.licence_4.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "to_do"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        api.content.transition(self.licence_4, transition="resume")
        notify(ObjectModifiedEvent(self.licence_4))

        expected_tasks_ids.append("TASK_check_completion-1")
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_check_completion-1", "created"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        api.content.transition(self.licence_4, transition="iscomplete")
        notify(ObjectModifiedEvent(self.licence_4))

        expected_tasks_ids.append("TASK_send_acknoledgment-1")
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_check_completion-1", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_send_acknoledgment-1", "created"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        # Ensure that even after a modification, nothing changed
        notify(ObjectModifiedEvent(self.licence_4))
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

    def test_choice_fd_task_closed_on_suspend(self):
        """Ensure that task related to fd choice are correctly closed
        when we suspend the licence"""
        login(self.portal, "urbanmanager")

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_deposit",
        ]
        reception_task = self.licence_5.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "created"),
            ("TASK_deposit", "to_do"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        self.licence_5.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_5, transition="iscomplete")
        api.content.transition(self.licence_5, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_5))

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_send_acknoledgment",
            "TASK_deposit",
            "TASK_attente_plans_modifies",
            "TASK_procedure_choice_fd",
            "TASK_procedure_choice_past_20days",
        ]
        reception_task = self.licence_5.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "to_do"),
            ("TASK_procedure_choice_fd", "closed"),
            ("TASK_procedure_choice_past_20days", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        # Ensure that even after a modification, nothing changed
        notify(ObjectModifiedEvent(self.licence_5))
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

    def test_choice_fd_task_on_reopen(self):
        """Ensure that task related to fd choice are correctly recreated
        when we reopen the licence"""
        login(self.portal, "urbanmanager")

        self.licence_5.setHasModifiedBlueprints(True)
        api.content.transition(self.licence_5, transition="iscomplete")
        api.content.transition(self.licence_5, transition="suspend")
        notify(ObjectModifiedEvent(self.licence_5))

        expected_tasks_ids = [
            "TASK_check_completion",
            "TASK_send_acknoledgment",
            "TASK_deposit",
            "TASK_attente_plans_modifies",
            "TASK_procedure_choice_fd",
            "TASK_procedure_choice_past_20days",
        ]
        reception_task = self.licence_5.TASK_reception
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "to_do"),
            ("TASK_procedure_choice_fd", "closed"),
            ("TASK_procedure_choice_past_20days", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        api.content.transition(self.licence_5, transition="resume")
        notify(ObjectModifiedEvent(self.licence_5))

        expected_tasks_ids.append("TASK_check_completion-1")
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )

        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_check_completion-1", "created"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "closed"),
            ("TASK_procedure_choice_fd", "closed"),
            ("TASK_procedure_choice_past_20days", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        api.content.transition(self.licence_5, transition="iscomplete")
        notify(ObjectModifiedEvent(self.licence_5))

        expected_tasks_ids.extend(
            [
                "TASK_send_acknoledgment-1",
                "TASK_procedure_choice_fd-1",
                "TASK_procedure_choice_past_20days-1",
            ]
        )
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        expected_states = [
            ("TASK_check_completion", "closed"),
            ("TASK_check_completion-1", "closed"),
            ("TASK_send_acknoledgment", "closed"),
            ("TASK_send_acknoledgment-1", "closed"),
            ("TASK_deposit", "closed"),
            ("TASK_attente_plans_modifies", "closed"),
            ("TASK_procedure_choice_fd", "closed"),
            ("TASK_procedure_choice_fd-1", "created"),
            ("TASK_procedure_choice_past_20days", "closed"),
            ("TASK_procedure_choice_past_20days-1", "closed"),
        ]
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )

        # Ensure that even after a modification, nothing changed
        notify(ObjectModifiedEvent(self.licence_5))
        self.assertListEqual(
            sorted(expected_tasks_ids),
            sorted(reception_task.objectIds()),
        )
        self.assertListEqual(
            sorted(expected_states),
            sorted(
                [
                    (i, api.content.get_state(reception_task[i]))
                    for i in expected_tasks_ids
                ]
            ),
        )
