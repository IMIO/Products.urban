# -*- coding: utf-8 -*-

from Products.Archetypes.event import ObjectInitializedEvent
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.services import notice
from datetime import datetime
from plone import api
from zope.event import notify
from zope.i18n import translate

import transaction


class ImportFromNoticeView(BrowserView):
    """Get new notification from Notice API"""

    def __call__(self):
        self.notice_service = notice.WebserviceNotice()
        self.max_date = api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.last_import_date",
            default=datetime(2000, 1, 1),
        ) or datetime(2000, 1, 1)
        self.notification_dates = []
        notifications = self._get_notice_notifications()
        for notification in notifications:
            self._create_content(notification)
        return "OK"

    def _get_notice_notifications(self):
        return self.notice_service.get_notifications()

    def _add_error(self, licence, msg, serialized_data):
        """Add an error"""
        error = _(
            "<p>${msg} for informations: ${data}</p>",
            mapping={
                "msg": msg,
                "data": ", ".join(
                    ["{0}: {1}".format(k, v) for k, v in serialized_data.items()]
                ),
            },
        )
        licence.description.raw += translate(error, context=self.request)
        licence._p_changed = 1

    def _create_content(self, notification):
        notification_date = datetime.strptime(
            notification["status"]["date"][0:26],
            "%Y-%m-%dT%H:%M:%S.%f",
        )
        if notification_date > self.max_date:
            self.notification_dates.append(notification_date)
        else:
            return
        if notification["labelType"] != "Nouveau dossier à destination de la commune":
            return
        detailed_notification = self.notice_service.get_notification(
            notification["noticeId"]
        )
        container = detailed_notification.container
        licence = api.content.create(
            container=container, **detailed_notification.serialize()
        )
        licence.noticeId = detailed_notification.noticeId
        licence._p_changed = 1
        for party in detailed_notification.parties:
            api.content.create(container=licence, **party.serialize())
        for parcel in detailed_notification.parcels:
            if not parcel.parcel:
                self._add_error(licence, _("Can not find a parcel"), parcel.serialize())
                continue
            api.content.create(container=licence, **parcel.serialize())
        for address in detailed_notification.addresses:
            data = {
                translate(_("street"), context=self.request): address.notice_street,
                translate(_("locality"), context=self.request): address.locality,
                translate(
                    _("municipality"), context=self.request
                ): address.municipality,
                translate(_("zipcode"), context=self.request): address.postCode,
            }
            if not address.address:
                self._add_error(licence, _("Can not find an address"), data)
                continue
            if len(address.address) > 1:
                self._add_error(licence, _("Multiple results for an address"), data)
                continue
            licence.workLocations += (address.serialize(),)
            licence._p_changed = 1
        for document in detailed_notification.documents:
            api.content.create(container=licence, **document.serialize())
        # Set title and update reference number
        notify(ObjectInitializedEvent(licence))
        # Change workflow and add deposit event
        transaction.commit()  # Usefull in case of an error
