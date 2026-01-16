# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.services import notice
from datetime import datetime
from plone import api
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent

import logging
import transaction

logger = logging.getLogger("urban: Notice Cron")


class ImportFromNoticeView(BrowserView):
    """Get new notification from Notice API"""

    def __call__(self):

        self._initialize()
        self._retry_failed_notifications()
        self._process_fresh_notifications()
        self._save_progress()
        return "OK"

    def _initialize(self):
        """Initialize service and configuration values."""

        self.notice_service = notice.WebserviceNotice()
        self.retry_failed_notifications = self.request.form.get("retry") == "1"
        self.last_import_date = (
            api.portal.get_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.last_import_date",
                default=datetime(2000, 1, 1),
            )
            or datetime(2000, 1, 1)
        )
        self.latest_successful_date = self.last_import_date
        self.failed_notifications = (
            api.portal.get_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
                default=[],
            )
            or []
        )
        self.already_handled_notifications = []

    def _retry_failed_notifications(self):
        """Retry processing of previously failed notifications, if requested."""
        if not self.retry_failed_notifications or not self.failed_notifications:
            return

        logger.info(u"Retrying %d failed notifications", len(self.failed_notifications))
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

    def _process_fresh_notifications(self):
        """Process new notifications from the Notice API."""

        fresh_notifications = self._get_notice_notifications()
        for notification in fresh_notifications:

            notice_id = notification["noticeId"]
            notif_last_status_date = datetime.strptime(
                notification["status"]["date"][0:26],
                "%Y-%m-%dT%H:%M:%S.%f",
            )
            if notif_last_status_date <= self.last_import_date:
                continue

            if notice_id in self.failed_notifications:
                continue

            if notice_id in self.already_handled_notifications:
                continue
            self.already_handled_notifications.append(notice_id)

            try:
                self._handle_notification(notice_id)
                if notif_last_status_date > self.latest_successful_date:
                    self.latest_successful_date = notif_last_status_date
                logger.info(u"Notification %s succeeded", notice_id)
            except Exception as exc:
                logger.exception(
                    u"Error while processing notification %s: %s",
                    notice_id,
                    exc,
                )
                self.failed_notifications.append(notice_id)

    def _save_progress(self):
        """Save the progress markers and failed notifications."""

        if self.latest_successful_date > self.last_import_date:
            api.portal.set_registry_record(
                "Products.urban.browser.notice_settings.INoticeSettings.last_import_date",
                self.latest_successful_date,
            )
            logger.info(
                u"Updated last_import_date to %s",
                self.latest_successful_date.isoformat(),
            )

        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.failed_notifications",
            self.failed_notifications,
        )
        if self.failed_notifications:
            logger.warning(
                u"%d notification(s) recorded as failed", len(self.failed_notifications)
            )

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

    def _demande_ep(self, detailed_notification):
        licence = detailed_notification.licence
        if not licence:
            return  # TODO: possible case ?

        event_config_complete = detailed_notification.event_config(
            "Products.urban.interfaces.IAcknowledgmentEvent"
        )
        event = licence.createUrbanEvent(event_config_complete)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")

        api.content.transition(licence, "iscomplete")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        licence.set_notice_id("DEMANDE_EP", detailed_notification.noticeId)

        transaction.commit()

    def _rapport_synthese(self, detailed_notification):
        licence = detailed_notification.licence
        if not licence:
            return


        event_config = detailed_notification.event_config(
            "Products.urban.interfaces.IDecisionProjectFromSPWEvent"
        )
        event = licence.createUrbanEvent(event_config)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        licence.set_notice_id("NOTIFICATION_RS", detailed_notification.noticeId)

        transaction.commit()

    def _decision_spw(self, detailed_notification):
        licence = detailed_notification.licence
        if not licence:
            return

        event_config = detailed_notification.event_config(
            "Products.urban.interfaces.IWalloonRegionDecisionEvent"
        )
        event = licence.createUrbanEvent(event_config)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)

        # set decision (octroi / refus)
        mapping_decision_terms = {"OCTROI": "favorable", "REFUS": "defavorable"}
        urban_decision_term = mapping_decision_terms.get(
            detailed_notification.decision_code
        )
        if urban_decision_term:
            event.setDecision(urban_decision_term)
        else:
            event.setDescription(
                u"Décision: {}".format(detailed_notification.decision_code)
            )

        api.content.transition(event, "close")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        licence.set_notice_id("NOTIFICATION_DECISION", detailed_notification.noticeId)

        transaction.commit()

    def _handle_notification(self, notice_id):
        detailed_notification = self.notice_service.get_notification(
            notice_id,
        )

        if detailed_notification.notice_type == "TRANSFERT_DOSSIER":
            self._transfert_dossier(detailed_notification)
        elif detailed_notification.notice_type in (
                "NOTIF_COMPLETUDE1_INCOMPLET_COMMUNE",
                "NOTIF_COMPLETUDE1_NON_RECEVABLE_COMMUNE",
        ):
            self.process_incomplete_folder_notification(detailed_notification)
        elif detailed_notification.notice_type in (
            "NOTIF_COMPLETUDE1_IRRECEVABLE_COMMUNE",
            "NOTIF_COMPLETUDE2_IRRECEVABLE_COMMUNE",
            "NOTIF_COMPLETUDE2_NON_RECEVABLE_COMMUNE",
        ):
            self.process_inadmissible_folder_notification(detailed_notification)
        elif detailed_notification.notice_type in (
            "DEMANDE_EP",
            "DEMANDE_EP_DOSSIER_PRECEDENT",
            "DEMANDE_EP_EXTRA",
        ):
            self._demande_ep(detailed_notification)
        elif detailed_notification.notice_type == "NOTIFICATION_PROROGATION_COMMUNE":
            self.process_extension_of_deadline_notification(detailed_notification)
        elif detailed_notification.notice_type in (
                "NOTIFICATION_RS_COMMUNE",
                "NOTIFICATION_RS_COMMUNE_RETARD",
                "NOTIFICATION_RS_COMMUNE_RETARD_SFD",
                "NOTIFICATION_PAS_ENVOI_RS",
                "NOTIFICATION_PAS_ENVOI_RS_SFD",
        ):
            self._rapport_synthese(detailed_notification)
        elif detailed_notification.notice_type == "NOTIFICATION_DECISION_COMMUNE":
            self._decision_spw(detailed_notification)
        else:
            raise NotImplementedError(
                "No implementation found for notification type: %s"
                % detailed_notification.notice_type
            )

    def _transfert_dossier(self, detailed_notification):
        container = detailed_notification.container
        licence = api.content.create(
            container=container, **detailed_notification.serialize()
        )
        licence.set_notice_id("TRANSFERT_DOSSIER", detailed_notification.noticeId)
        licence.setFoldermanagers(
            detailed_notification.foldermanagers
        )  # Must be set manually, serialized value is ignored at creation
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
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")
        # Reindex licence
        licence.reindexObject()

        transaction.commit()  # Useful in case of an error

    def process_incomplete_folder_notification(self, detailed_notification):
        licence = detailed_notification.licence

        event_config_incomplete = detailed_notification.event_config(
            "Products.urban.interfaces.IMissingPartEvent"
        )
        event = licence.createUrbanEvent(event_config_incomplete)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")

        if api.content.get_state(licence) == "deposit":
            api.content.transition(licence, "isincomplete")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        transaction.commit()

    def process_inadmissible_folder_notification(self, detailed_notification):
        licence = detailed_notification.licence

        event_config_refused_incompleteness = detailed_notification.event_config(
            "Products.urban.interfaces.IRefusedIncompletenessEvent"
        )
        event = licence.createUrbanEvent(event_config_refused_incompleteness)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")

        api.content.transition(licence, "isinacceptable")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        transaction.commit()

    def process_extension_of_deadline_notification(self, detailed_notification):
        licence = detailed_notification.licence

        # set prorogation field (if it's activated)
        if licence.attributeIsUsed("prorogation"):
            licence.getField("prorogation").set(licence, True)
            notify(ObjectModifiedEvent(licence))
            licence.reindexObject()

        event_config_prorogation = detailed_notification.event_config(
            "Products.urban.interfaces.IProrogationEvent"
        )
        event = licence.createUrbanEvent(event_config_prorogation)
        event_date = DateTime(str(detailed_notification.send_date))
        event.setEventDate(event_date)
        event.store_reception_date(detailed_notification.reception_date)
        api.content.transition(event, "close")

        for document in detailed_notification.documents:
            api.content.create(container=event, **document.serialize())

        transaction.commit()
