# -*- coding: utf-8 -*-
from Products.urban import testing
from Products.urban.browser.cron import notice

import mock
import unittest


class TestDecisionRegistreCommuneDispatch(unittest.TestCase):

    def test_dispatch_to_modification_registry_decision_handler(self):
        self.assertEqual(
            notice.ModificationRegistryDecisionHandler.event_config_marker,
            "Products.urban.interfaces.IModificationRegistryDecisionEvent",
        )
        request = mock.Mock()
        notification = mock.Mock(notice_type="DECISION_REGISTRE_COMMUNE")
        view = notice.ImportFromNoticeView(mock.Mock(), request)
        view.notice_service = mock.Mock()
        view.notice_service.get_notification.return_value = notification
        with mock.patch.object(notice, "ModificationRegistryDecisionHandler") as handler:
            view._handle_notification("1231756")
        handler.assert_called_once_with(notification, request)
        handler.return_value.process.assert_called_once_with()


class TestDecisionRegistreCommuneMarker(unittest.TestCase):
    layer = testing.URBAN_TESTS_LICENCES_FUNCTIONAL

    def test_marker_is_an_event_type(self):
        from Products.urban.interfaces import IModificationRegistryDecisionEvent
        from Products.urban.interfaces import IEventTypeType

        self.assertTrue(IEventTypeType.providedBy(IModificationRegistryDecisionEvent))
