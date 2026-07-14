# -*- coding: utf-8 -*-

import logging
import requests

from Products.urban import UrbanMessage as _
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanEvent
from Products.urban.notice import NoticeNotification
from Products.urban.notice.exceptions import MalformedFieldException
from Products.urban.notice.exceptions import MissingFieldException
from Products.urban.notice.exceptions import MissingNotificationException
from Products.urban.notice.exceptions import NoticeResponseException
from Products.urban.notice.exceptions import UnprocessableEntityException
from Products.urban.notice.exceptions import WrongStatusException
from Products.urban.services.base import WebService
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.services import Service
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


logger = logging.getLogger("urban: Notice Service")


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Notice(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {"notice": {"@id": "{}/@notice".format(self.context.absolute_url())}}
        if not expand:
            return result

        data = {}

        if IGenericLicence.providedBy(self.context):
            notice_ids = getattr(self.context, "notice_ids", {})
            data["notice_ids"] = notice_ids

        if IUrbanEvent.providedBy(self.context):
            annotations = IAnnotations(self.context)
            for key in (
                "notice_notification",
                "notice_transmit_dates",
                "notice_reception_date",
            ):
                data[key] = annotations.get(key, None)

        return json_compatible({"notice": data})


class NoticeGet(Service):
    def reply(self):
        notice = Notice(self.context, self.request)
        return notice(expand=True)["notice"]


class WebserviceNotice(WebService):
    """Webservice to interract with Notice"""

    def __init__(self, user="", password=""):
        self.user = user
        self.password = password

    @property
    def url(self):
        url = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.url",
            default=None
        )
        if not url:
            return
        if url.endswith("/"):
            return url[:-1]
        return url

    @property
    def instance_code(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id"
        )

    @property
    def sent_on_behalf_of(self):
        return api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.sent_on_behalf_of_municipality_id"
        )
    
    @property
    def is_setup(self):
        return self.url and self.instance_code and self.sent_on_behalf_of

    @property
    def _auth(self):
        if self.user and self.password:
            return (self.user, self.password)

    def _get(self, endpoint, **parameters):
        return requests.get(
            "{0}/{1}".format(self.url, endpoint),
            auth=self._auth,
            headers={
                "Accept": "application/json",
                "X-Sent-On-Behalf-Of": self.sent_on_behalf_of,
            },
            params=parameters,
        )

    def _post(self, endpoint, data):
        return requests.post(
            "{0}/{1}".format(self.url, endpoint),
            auth=self._auth,
            json=data,
            headers={
                "Accept": "application/json",
                "content-type": "application/json",
                "X-Sent-On-Behalf-Of": self.sent_on_behalf_of,
            },
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
            raise ValueError(
                "Unexpected response {}: '{}'".format(response.status_code, response.content)
            )
        result = response.json()
        if result["status"] != "PROCESSED":
            raise ValueError("Error in response '{}'".format(result["status"]["value"]))
        notices_obj = result.get("notices") or {}
        notices_list = notices_obj.get("notice") or []
        return notices_list

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
        if result["status"] != "PROCESSED":
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
        return response.content

    def _post_notification_response(self, notification_id, data):
        """Post a response for a notification using REST API"""
        return self._post(
            "notifications/{notification_id}/responses".format(
                notification_id=notification_id
            ),
            data=data,
        )

    def _post_notification_document(self, notification_id, data):
        """Post a document for a notification using REST API"""
        return self._post(
            "notifications/{notification_id}/documents".format(
                notification_id=notification_id
            ),
            data=data,
        )

    def _handle_error(self, response):
        """
        This method should raise an Exception in any case.

        :type response: requests.Response
        """

        try:
            body = response.json()
        except Exception as e:
            custom_exc = NoticeResponseException(original_exception=e)
            logger.exception(
                u"Couldn't decode JSON from NOTICE WS response\n%s",
                custom_exc,
            )
            raise custom_exc
        if response.status_code == 422:  # FastAPI can't parse the data
            custom_exc = UnprocessableEntityException(response.url, body.get("detail"))
            logger.exception(u"%s", custom_exc)
            raise custom_exc
        if body.get("status") == u"ERROR" and u"error" in body:  # error coming from SOAP WS
            customer_ticket = body.get("customerTicket", "")
            error = body["error"]
            information = error.get("information") or {}

            if (
                error["code"]["code"] in (u"00006", u"00007")
                and error["category"] == u"600"
            ):
                custom_exc = WrongStatusException(
                    str(information), customer_ticket=customer_ticket
                )
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            elif (
                error["code"]["code"] in (u"00004", u"00005")
                and error["category"] == u"600"
            ):
                custom_exc = MissingNotificationException(
                    str(information), customer_ticket=customer_ticket
                )
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            elif error["code"]["code"] == u"00003" and error["category"] == u"600":
                custom_exc = MalformedFieldException(
                    str(information), customer_ticket=customer_ticket
                )
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            elif error["code"]["code"] == u"00002" and error["category"] == u"600":
                custom_exc = MissingFieldException(
                    str(information), customer_ticket=customer_ticket
                )
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            elif error["code"]["code"] == u"00001" and error["category"] == u"100":
                custom_exc = MissingNotificationException(
                    str(information), customer_ticket=customer_ticket
                )
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            elif error["code"]["code"] == u"00001" and error["category"] == u"600":
                custom_exc = NoticeResponseException(customer_ticket=customer_ticket)
                logger.exception(u"%s", custom_exc)
                raise custom_exc
            else:
                custom_exc = NoticeResponseException(customer_ticket=customer_ticket)
                logger.exception(
                    u"Unknown error coming from NOTICE WS\ncategory %s, code %s\n%s",
                    error["code"]["code"],
                    error["category"],
                    custom_exc,
                )
                raise custom_exc

        custom_exc = NoticeResponseException()
        logger.exception(
            u"Unhandled error when sending response to NOTICE WS\n%s",
            custom_exc,
        )
        raise custom_exc

    def post_notification_response(self, notification_id, data):
        """Post a response for a notification"""
        response = self._post_notification_response(notification_id, data)
        if response.status_code != 200:
            self._handle_error(response)
        result = response.json()
        if result["status"] != "PROCESSED":
            custom_exc = NoticeResponseException()
            logger.exception(
                u"Sent response couldn't be processed by NOTICE WS\n%s",
                custom_exc,
            )
            raise custom_exc
        return {"error": False, "body": result}

    def post_notification_document(self, notification_id, data):
        """Post a document for a notification"""
        response = self._post_notification_document(notification_id, data)
        if response.status_code != 204:
            self._handle_error(response)
        return "OK"
