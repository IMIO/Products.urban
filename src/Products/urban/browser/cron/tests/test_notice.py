# -*- coding: utf-8 -*-

from Products.urban import testing
from Products.urban.services.tests.data import notice_data
from plone import api

import mock
import unittest


class MockedRequest(object):
    def __init__(self, json, status_code=200):
        self._json = json
        self.status_code = status_code

    def json(self):
        return self._json


class TestNoticeCron(unittest.TestCase):
    layer = testing.URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer["portal"]
        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id",
            u"0206.524.876",
        )

    def tearDown(self):
        pass

    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=notice_data["notifications_without_rubrics"],
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(notice_data["notification_without_rubrics"]),
    )
    @mock.patch(
        "Products.urban.notice.address.NoticeAddress._find_address",
        return_value=[{"text": "street, 1 (1400 - Nivelles)", "id": "1234"}]
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification_document",
        return_value=MockedRequest(notice_data["document_data"]),
    )
    def test_import_notification_success(self, address_patch, doc_patch, notif_patch, notifs_patch):
        address_patch, doc_patch, notif_patch, notifs_patch  # noqa
        licence_folder = self.portal.urban.envclasstwos
        self.assertEqual(1, len(licence_folder))
        with api.env.adopt_roles(["Manager"]):
            import_view = self.portal.restrictedTraverse("@@import-from-notice")
            result = import_view()
        self.assertEqual("OK", result)
        self.assertEqual(2, len(licence_folder))
        licence = licence_folder.values()[-1]
        self.assertTrue(licence.reference.startswith(u"PE2"))
        self.assertEqual("933311", licence.noticeId)
        self.assertEqual(
            u"PE2/2023/1 - Renouvellement du permis d'exploiter la station d'épuration de Fouches. - Société coopérative IDELUX Eau",
            licence.title,
        )
        self.assertEqual(
             ({'number': '', 'street': '1234'},),
             licence.workLocations,
        )
        # We have 4 subelements, 1 applicant, 1 parcel and 2 documents
        self.assertEqual(4, len(licence))
        self.assertListEqual(
            [
                "idelux-eau",
                "62006A0122_00B002",
                "10010658_demande-complete-et-recevable",
                "10010658_demande-complete-et-recevable-1"
            ],
            licence.keys(),
        )