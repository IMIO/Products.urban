# -*- coding: utf-8 -*-

from Products.Archetypes.event import ObjectInitializedEvent
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.services import notice
from Products.urban.browser.cron.transitions import EVENT_TYPE_TO_TRANSITION
from datetime import datetime
from DateTime import DateTime
from plone import api
from zope.event import notify
from zope.i18n import translate

import logging
import transaction

logger = logging.getLogger("urban: Notice Cron")


class ImportFromNoticeView(BrowserView):
    """Get new notification from Notice API"""

    def __call__(self):

        # initialization

        self.notice_service = notice.WebserviceNotice()
        self.retry_failed_notifications = self.request.form.get("retry") == "1"
        self.last_import_date = (
            api.portal.get_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.last_import_date",
                default=datetime(2000, 1, 1),
            )
            or datetime(2000, 1, 1)
        )
        self.failed_notifications = (
            api.portal.get_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
            default=[],
            )
            or []
        )
        self.already_handled_notifications = []

        # retry failed notifications, if requested

        if self.retry_failed_notifications and self.failed_notifications:
            logger.info(
                u"Retrying %d failed notifications",
                len(self.failed_notifications)
            )
            remaining_failed = []

            for failed_notice_id in self.failed_notifications:
                if failed_notice_id in self.already_handled_notifications:
                    continue
                self.already_handled_notifications.append(failed_notice_id)
                try:
                    self._handle_notification(failed_notice_id)
                    logger.info(u"Retried notification %s succeeded", failed_notice_id)
                except Exception as exc:
                    logger.exception(
                        u"Retried notification %s failed again: %s",
                        failed_notice_id,
                        exc,
                    )
                    remaining_failed.append(failed_notice_id)

            api.portal.set_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
                remaining_failed,
            )
            self.failed_notifications = remaining_failed

        # try fresh notifications

        latest_successful_date = self.last_import_date
        fresh_notifications = self._get_notice_notifications()
        for notification in fresh_notifications:

            notice_id = notification["noticeId"]
            notif_last_status_date = datetime.strptime(
                notification["status"]["date"][0:26],
                "%Y-%m-%dT%H:%M:%S.%f",
            )

            if notice_id in self.already_handled_notifications:
                continue
            self.already_handled_notifications.append(notice_id)

            try:
                self._handle_notification(notice_id)
                if notif_last_status_date > latest_successful_date:
                    latest_successful_date = notif_last_status_date
                logger.info(u"Notification %s succeeded", notice_id)
            except Exception as exc:
                logger.exception(
                    u"Error while processing notification %s: %s",
                    notice_id,
                    exc,
                )
                self.failed_notifications.append(notice_id)

        # save progress markers

        if latest_successful_date > self.last_import_date:
            api.portal.set_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.last_import_date",
                latest_successful_date,
            )
            logger.info(
                u"Updated last_import_date to %s", latest_successful_date.isoformat()
            )

        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
            self.failed_notifications,
        )
        if self.failed_notifications:
            logger.warning(
                u"%d notification(s) recorded as failed", len(self.failed_notifications)
            )

        return "OK"

    def _get_notice_notifications(self):
        notifications = []
        try:
            notifications = self.notice_service.get_notifications()
        except Exception as exc:
            logger.exception(
                u"Failed getting the list of recent notifications: %s",
                exc,
            )
        return notifications

    def _add_error(self, licence, msg, serialized_data):
        """Add an error"""
        error = _(
            u"<p>${msg} for informations: ${data}</p>",
            mapping={
                "msg": msg,
                "data": u", ".join(
                    [u"{0}: {1}".format(k, v) for k, v in serialized_data.items()]
                ),
            },
        )
        licence.description.raw += translate(error, context=self.request)
        licence._p_changed = 1

    def _handle_notification(self, notice_id):
        detailed_notification = self.notice_service.get_notification(
            notice_id,
        )
        if detailed_notification.notice_type == "TRANSFERT_DOSSIER":
            self._transfert_dossier(detailed_notification)
        if detailed_notification.notice_type == "NOTIF_COMPLETUDE1_INCOMPLET_COMMUNE":
            self.process_incomplete_folder_notification(detailed_notification)

    def _transfert_dossier(self, detailed_notification):
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
        event_config_deposit = detailed_notification.event_config(
            "Products.urban.interfaces.IDepositEvent"
        )
        event = licence.createUrbanEvent(event_config_deposit)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        api.content.transition(event, "close")

        transaction.commit()  # Useful in case of an error
    
    def update_license(self, license, detailed_notification, event_type=None):
        if not event_type:
            return
        event_configs = detailed_notification.event_configs
        # Normalizing event_type to list
        if isinstance(event_type, (list, tuple)):
            event_types = event_type
        else:
            event_types = [event_type]   
        configs = []
        for etype in event_types:                                         
            event_config = event_configs.get(etype)
            if  event_config:
                configs.append((etype,event_config))
        if not configs:
            return
        with api.env.adopt_roles(["Manager"]):
            for etype, event_config in configs:
                event = license.createUrbanEvent(event_config)
                event_date = DateTime(str(detailed_notification.send_date))
                event.setEventDate(event_date)
                api.content.transition(event, "close")
                transition = EVENT_TYPE_TO_TRANSITION.get(etype)
                if transition:
                    api.content.transition(license, transition)

    def process_incomplete_folder_notification(self, detailed_notification):
        license = detailed_notification.licence
        self.update_license(license, detailed_notification, event_type="dossier-incomplet")
        transaction.commit() 
    