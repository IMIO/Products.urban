# -*- coding: utf-8 -*-

from Products.urban import testing
from Products.urban.services.notice import WebserviceNotice
from plone import api

import unittest


class TestNoticeService(unittest.TestCase):
    layer = testing.URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.service = WebserviceNotice()
        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id",
            u"0206.524.876"
        )

    def test_get_notifications(self):
        response = self.service._get_notifications()
        self.assertEqual(200, response.status_code)
        notifications = response.json()
        self.assertEqual("PROCESSED", notifications["status"]["value"])
        self.assertTrue("notices" in notifications)

    def test_get_notification(self):
        response = self.service._get_notification(933311)
        self.assertEqual(200, response.status_code)
        notification = response.json()
        self.assertEqual("PROCESSED", notification["status"]["value"])
        self.assertTrue("notice" in notification)
        self.assertTrue("specific" in notification["notice"])

    def test_get_notification_document(self):
        response = self.service._get_notification_document(
            933311, "cc8d5a94-c7e5-4d06-b908-521deecb74cf"
        )
        self.assertEqual(200, response.status_code)
        document = response.json()
        self.assertEqual("PROCESSED", document["status"]["value"])
        self.assertTrue("document" in document)
        self.assertTrue("content" in document["document"])
        self.assertTrue("documentData" in document["document"])
        self.assertTrue("mimeType" in document["document"]["documentData"])
        self.assertTrue("filename" in document["document"]["documentData"])
