# -*- coding: utf-8 -*-

from Products.urban.services.base import WebService
from Products.urban.notice import NoticeNotification
from plone import api

import requests


class WebserviceNotice(WebService):
    """Webservice to interract with Notice"""

    def __init__(self, user="", password=""):
        self.user = user
        self.password = password

    @property
    def url(self):
        url = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.url"
        )
        if url.endswith("/"):
            return url[:-1]
        return url

    @property
    def instance_code(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id"
        )

    @property
    def _auth(self):
        if self.user and self.password:
            return (self.user, self.password)

    def _get(self, endpoint, **parameters):
        return requests.get(
            "{0}/{1}".format(self.url, endpoint),
            auth=self._auth,
            headers={"Accept": "application/json"},
            params=parameters,
        )

    def _post(self, endpoint, data):
        return requests.post(
            "{0}/{1}".format(self.url, endpoint),
            auth=self._auth,
            data=data,
            headers={"Accept": "application/json", "content-type": "application/json"},
        )

    def _get_notifications(self, status="EN_ATTENTE_REPONSE"):
        """Get notifications for the current instance response from REST API"""
        return self._get(
            "instances/{instance_code}/notifications".format(
                instance_code=self.instance_code
            ),
            status=status,
        )

    def get_notifications(self, status="EN_ATTENTE_REPONSE"):
        """Get notifications for the current instance"""
        response = self._get_notifications(status=status)
        if response.status_code != 200:
            raise ValueError("Unexpected response '{}'".format(response.status_code))
        result = response.json()
        if result["status"]["value"] != "PROCESSED":
            raise ValueError("Error in response '{}'".format(result["status"]["value"]))
        return result["notices"]["notice"]

    def _get_notification(self, notification_id):
        """Get a notification informations response from REST API"""
        return self._get(
            "notifications/{notification_id}".format(notification_id=notification_id)
        )

    def get_notification(self, notification_id):
        """Get a notification informations"""
        response = self._get_notification(notification_id)
        if response.status_code != 200:
            raise ValueError("Unexpected response '{}'".format(response.status_code))
        result = response.json()
        if result["status"]["value"] != "PROCESSED":
            raise ValueError("Error in response '{}'".format(result["status"]["value"]))
        return NoticeNotification(self, result["notice"])

    def _get_notification_document(self, notification_id, document_id):
        """Get a document for a notification response from REST API"""
        return self._get(
            "notifications/{notification_id}/documents/{document_id}".format(
                notification_id=notification_id, document_id=document_id
            )
        )

    def get_notification_document(self, notification_id, document_id):
        """Get a document for a notification"""
        response = self._get_notification_document(notification_id, document_id)
        if response.status_code != 200:
            raise ValueError("Unexpected response '{}'".format(response.status_code))
        result = response.json()
        if result["status"]["value"] != "PROCESSED":
            raise ValueError("Error in response '{}'".format(result["status"]["value"]))
        return result["document"]

    def _post_notification_response(self, notification_id, data):
        """Post a response for a notification using REST API"""
        return self._post(
            "notifications/{notification_id}/responses".format(
                notification_id=notification_id
            ),
            json=data,
        )

    def post_notification_response(self, notification_id, data):
        """Post a response for a notification"""
        response = self._post_notification_response(notification_id, data)
        if response.status_code != 200:
            raise ValueError("Unexpected response '{}'".format(response.status_code))
        result = response.json()
        if result["status"]["value"] != "PROCESSED":
            raise ValueError("Error in response '{}'".format(result["status"]["value"]))
        return result