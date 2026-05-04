# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Archetypes.event import ObjectInitializedEvent
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.contentrules.notice import NoticeImportFailedEvent
from Products.urban.contentrules.notice import NoticeImportSucceededEvent
from Products.urban.interfaces import IBaseBuildLicence
from Products.urban.services import notice
from StringIO import StringIO
from datetime import datetime
from plone import api
from plone.api.exc import InvalidParameterError
from plone.stringinterp.interfaces import IContextWrapper
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
            savepoint = transaction.savepoint()
            try:
                self._handle_notification(failed_notice_id)
                logger.info(u"Retried notification %s succeeded", failed_notice_id)
            except Exception as exc:
                savepoint.rollback()
                logger.exception(
                    u"Retried notification %s failed again: %r",
                    failed_notice_id,
                    exc,
                )
                self._notify_import_error(failed_notice_id, "failed retry")
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

            savepoint = transaction.savepoint()
            try:
                self._handle_notification(notice_id)
                if notif_last_status_date > self.latest_successful_date:
                    self.latest_successful_date = notif_last_status_date
                logger.info(u"Notification %s succeeded", notice_id)
            except Exception as exc:
                savepoint.rollback()
                logger.exception(
                    u"Error while processing notification %s: %s",
                    notice_id,
                    exc,
                )
                self._notify_import_error(notice_id, "failed import")
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
            self._notify_import_error("webservice", "can't get notifications")
        return notifications

    def _notify_import_error(self, notice_id="", notice_type=""):
        try:
            args = {
                "notice_id": notice_id,
                "notice_type": notice_type,
            }
            urban_folder = api.portal.get().urban
            event_wrapper = IContextWrapper(urban_folder)(**args)
            notify(NoticeImportFailedEvent(event_wrapper))
        except Exception:
            logger.exception(
                u"Failed to emit NoticeImportFailedEvent for notice_id=%s",
                notice_id,
            )

    def _handle_notification(self, notice_id):
        handler = None
        detailed_notification = self.notice_service.get_notification(
            notice_id,
        )

        # TWICE

        if detailed_notification.notice_type == "TRANSFERT_DOSSIER":
            handler = NewLicenceHandler
        elif detailed_notification.notice_type in (
                "NOTIF_COMPLETUDE1_INCOMPLET_COMMUNE",
                "NOTIF_COMPLETUDE1_NON_RECEVABLE_COMMUNE",
        ):
            handler = IncompleteHandler
        elif detailed_notification.notice_type in (
            "NOTIF_COMPLETUDE1_IRRECEVABLE_COMMUNE",
            "NOTIF_COMPLETUDE2_IRRECEVABLE_COMMUNE",
            "NOTIF_COMPLETUDE2_NON_RECEVABLE_COMMUNE",
        ):
            handler = InadmissibleHandler
        elif detailed_notification.notice_type in (
            "DEMANDE_EP",
            "DEMANDE_EP_DOSSIER_PRECEDENT",
        ):
            handler = PublicSurveyHandler
        elif detailed_notification.notice_type == "DEMANDE_EP_EXTRA":
            handler = BorderingPublicSurveyHandler
        elif detailed_notification.notice_type == "NOTIFICATION_PROROGATION_COMMUNE":
            handler = DeadlineExtensionHandler
        elif detailed_notification.notice_type in (
            "NOTIFICATION_RS_COMMUNE",
            "NOTIFICATION_RS_COMMUNE_RETARD",
            "NOTIFICATION_RS_COMMUNE_RETARD_SFD",
            "NOTIFICATION_PAS_ENVOI_RS",
            "NOTIFICATION_PAS_ENVOI_RS_SFD",
        ):
            handler = SummaryReportHandler
        elif detailed_notification.notice_type in (
            "NOTIFICATION_DECISION_COMMUNE",
            "NOTIFICATION_DEC_RS_COMMUNE",
            "NOTIFICATION_DECRS_REFUS_TACITE_COMMUNE",
        ):
            handler = DecisionSPWHandler

        # GESPER

        elif detailed_notification.notice_type in (
            "DEMANDE_AVIS_OBLIGATOIRE_PLAN_INITIAL_1_ERE_INSTANCE",
            # "DEMANDE_AVIS_OBLIGATOIRE_PLAN_INITIAL_2_EME_INSTANCE",
            # "DEMANDE_AVIS_OBLIGATOIRE_PLAN_MODIFIE_2_EME_INSTANCE",
            "DEMANDE_AVIS_FACULTATIF_PLAN_INITIAL_1_ERE_INSTANCE",
            # "DEMANDE_AVIS_FACULTATIF_PLAN_INITIAL_2_EME_INSTANCE",
            # "DEMANDE_AVIS_FACULTATIF_PLAN_MODIFIE_2_EME_INSTANCE",
        ):
            handler = GesperPublicSurveyHandler
        elif detailed_notification.notice_type in (
            "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_1_ERE_INSTANCE",
            # "DEMANDE_ENQUETE_PUBLIQUE_PLAN_INITIAL_2_EME_INSTANCE",
            # "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_2_EME_INSTANCE",
        ):
            handler = GesperPublicSurveyHandler
        elif detailed_notification.notice_type in (
            "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_1_ERE_INSTANCE",
            # "DEMANDE_ANNONCE_PROJET_PLAN_INITIAL_2_EME_INSTANCE",
            # "DEMANDE_ANNONCE_PROJET_PLAN_MODIFIE_2_EME_INSTANCE",
        ):
            handler = GesperPublicSurveyHandler
        elif detailed_notification.notice_type in (
            "DEMANDE_AVIS_OBLIGATOIRE_PLAN_MODIFIE_1_ERE_INSTANCE",
            "DEMANDE_AVIS_FACULTATIF_PLAN_MODIFIE_1_ERE_INSTANCE",
            "DEMANDE_ENQUETE_PUBLIQUE_PLAN_MODIFIE_1_ERE_INSTANCE",
            "DEMANDE_ANNONCE PROJET_PLAN_MODIFIE_1_ERE_INSTANCE",
        ):
            handler = GesperAmendedPlansSPWHandler
        elif detailed_notification.notice_type in (
            "DECISION_GESPER_1_ERE_INSTANCE",
            # "DECISION_GESPER_2_EME_INSTANCE",
        ):
            handler = GesperDecisionSPWHandler
        else:
            raise NotImplementedError(
                "No implementation found for notification type: %s"
                % detailed_notification.notice_type
            )

        if handler:
            handler(detailed_notification, self.request).process()


class IncomingNoticeHandler(object):
    event_config_marker = None
    create_licence_if_missing = False

    def __init__(self, notification, request):
        self.notification = notification
        self.request = request
        self.licence = notification.licence
        self.event = None

    def process(self):
        if self.licence:
            self.update_licence()
        elif self.create_licence_if_missing:
            self.create_licence()
        else:
            raise ValueError(
                "No licence found with reference number {} / reference FT {} / reference DGATLP".format(
                    self.notification.reference,
                    self.notification.referenceFT,
                    self.notification.referenceDGATLP,
                )
            )
        self.create_incoming_event()
        self.import_documents()
        self.do_licence_transition()
        self.notify_successful_import()

    def create_licence(self):
        self.licence = api.content.create(
            container=self.notification.container, **self.notification.serialize()
        )
        if IBaseBuildLicence.providedBy(self.licence):
            self.licence.setUsage("not_applicable")
        self.licence.setFoldermanagers(
            self.notification.foldermanagers
        )  # Must be set manually, serialized value is ignored at creation

        self.import_parties()
        self.import_parcels()
        self.import_addresses()

        self.licence._p_changed = 1
        notify(ObjectInitializedEvent(self.licence))
        self.licence.reindexObject()

    def import_parties(self):
        for party in self.notification.parties:
            api.content.create(container=self.licence, **party.serialize())

    def import_parcels(self):
        for parcel in self.notification.parcels:
            if not parcel.parcel:
                data = {
                    translate(_("CaPaKey"), context=self.request): parcel.capakey,
                    translate(_("urban_label_division"), context=self.request): parcel.division,
                    translate(_("urban_label_section"), context=self.request): parcel.section,
                    translate(_("urban_label_radical"), context=self.request): parcel.radical,
                    translate(_("urban_label_bis"), context=self.request): parcel.bis,
                    translate(_("urban_label_exposant"), context=self.request): parcel.exposant,
                    translate(_("urban_label_puissance"), context=self.request): parcel.puissance,
                }
                self._add_error(_("Can not find a parcel"), data)
                continue
            api.content.create(container=self.licence, **parcel.serialize())

    def import_addresses(self):
        for address in self.notification.addresses:
            data = {
                translate(_("urban_label_street"), context=self.request): address.notice_street,
                translate(_("urban_label_locality"), context=self.request): address.locality,
                translate(
                    _("municipality"), context=self.request
                ): address.municipality,
                translate(_("urban_label_zipCode"), context=self.request): address.postCode,
                translate(_("urban_label_number"), context=self.request): address.number,
            }
            if not address.address:
                self._add_error(_("Can not find an address"), data)
                continue
            if len(address.address) > 1:
                self._add_error(_("Multiple results for an address"), data)
                continue
            self.licence.workLocations += (address.serialize(),)
            self.licence._p_changed = 1

    def create_incoming_event(self):
        event_config = self.notification.event_config(self.event_config_marker)
        self.event = self.licence.createUrbanEvent(event_config)
        self.fill_incoming_event()
        api.content.transition(self.event, "close")

    def fill_incoming_event(self):
        usable_date = None
        if self.notification.send_date:
            usable_date = self.notification.send_date
        elif self.notification.status_date:
            usable_date = self.notification.status_date

        if usable_date:
            event_date = DateTime(str(usable_date))
            self.event.setEventDate(event_date)

        self.event.store_incoming_notice(
            self.notification.noticeId,
            self.notification.notice_type,
            self.notification.reception_date,
        )

    def import_documents(self):
        for document in self.notification.documents:
            at_file = api.content.create(container=self.event, **document.serialize())
            data_wrapper = StringIO(document.document)
            data_wrapper.filename = document.filename
            at_file.setFile(data_wrapper)
            at_file.setContentType(document.document_mimetype)

    @property
    def desired_licence_state(self):
        """Leave empty if the licence state is already appropriate"""
        return ""

    def do_licence_transition(self):
        if self.desired_licence_state:
            try:
                api.content.transition(
                    self.licence,
                    to_state=self.desired_licence_state,
                    comment=self._notification_transition_comment,
                )
            except InvalidParameterError:
                logger.warning(
                    "While handling notification %s, couldn't transition licence %s to state %s",
                    self.notification.noticeId,
                    self.licence.absolute_url_path(),
                    self.desired_licence_state,
                )

    def update_licence(self):
        self.set_reference_ft()
        self.set_reference_dgatlp()

    def set_reference_ft(self):
        try:
            licence_ref = self.licence.getReferenceFT()
        except AttributeError:
            return

        notification_ref = self.notification.referenceFT
        if notification_ref and licence_ref != notification_ref:
            self.licence.setReferenceFT(notification_ref)
            self.licence.reindexObject(idxs=["referenceFT"])

    def set_reference_dgatlp(self):
        try:
            licence_ref = self.licence.getReferenceDGATLP()
        except AttributeError:
            return

        notification_ref = self.notification.referenceDGATLP
        if notification_ref and licence_ref != notification_ref:
            self.licence.setReferenceDGATLP(notification_ref)
            self.licence.reindexObject(idxs=["referenceDGATLP"])

    def _add_error(self, msg, serialized_data):
        error = _(
            u"<p>${msg} for informations: ${data}</p>",
            mapping={
                "msg": msg,
                "data": u", ".join(
                    [u"{0}: {1}".format(k, v) for k, v in serialized_data.items()]
                ),
            },
        )
        description_field = self.licence.getField("description")
        old_description = description_field.getRaw(self.licence)
        new_description = old_description + translate(error, context=self.request).encode("utf8")
        description_field.set(self.licence, new_description)
        self.licence._p_changed = 1

    @property
    def _notification_transition_comment(self):
        msg = _(
            u"NOTICe notification n° ${noticeId}",
            mapping={
                "noticeId": self.notification.noticeId,
            },
        )
        return translate(msg, context=self.request)

    def notify_successful_import(self):
        notice_id = ""
        try:
            notice_id = self.notification.noticeId
            notice_type = self.notification.notice_type
            args = {
                "notice_id": notice_id,
                "notice_type": notice_type,
            }
            event_wrapper = IContextWrapper(self.event)(**args)
            notify(NoticeImportSucceededEvent(event_wrapper))
        except Exception:
            logger.exception(
                u"Failed to emit NoticeImportSucceededEvent for notice_id=%s",
                notice_id,
            )


class NewLicenceHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IDepositEvent"
    create_licence_if_missing = True


class InadmissibleHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IRefusedIncompletenessEvent"

    @property
    def desired_licence_state(self):
        return "inacceptable"


class IncompleteHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IMissingPartEvent"
    licence_transition = "isincomplete"

    @property
    def desired_licence_state(self):
        return "incomplete"


class PublicSurveyHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IAcknowledgmentEvent"

    @property
    def desired_licence_state(self):
        return "complete"


class BorderingPublicSurveyHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IAcknowledgmentEvent"
    create_licence_if_missing = True

    def import_parties(self):
        super(BorderingPublicSurveyHandler, self).import_parties()

        business_name = self.notification.business_reference_denomination
        if business_name:
            api.content.create(
                container=self.licence,
                type="Corporation",
                title=business_name,
                denomination=business_name,
            )

    def import_addresses(self):
        addresses = self.notification.addresses
        if addresses:
            first_address = addresses[0]
            self.licence.setZipcode(first_address.postCode)
            self.licence.setCity(first_address.municipality)
            self.licence.setWorkLocations(
                [
                    {"number": address.number, "street": address.notice_street}
                    for address in addresses
                ]
            )
            self.licence._p_changed = 1

    def import_parcels(self):
        self.licence.setManualParcels(
            [
                {"ref": "", "capakey": parcel.capakey}
                for parcel in self.notification.parcels
            ]
        )

    @property
    def desired_licence_state(self):
        return "complete"


class DeadlineExtensionHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IProrogationEvent"

    def update_licence(self):
        super(DeadlineExtensionHandler, self).update_licence()

        # set prorogation field (if it's activated)
        if self.licence.attributeIsUsed("prorogation"):
            self.licence.getField("prorogation").set(self.licence, True)
            notify(ObjectModifiedEvent(self.licence))
            self.licence.reindexObject()


class SummaryReportHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IDecisionProjectFromSPWEvent"


class DecisionSPWHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IWalloonRegionDecisionEvent"

    def fill_incoming_event(self):
        super(DecisionSPWHandler, self).fill_incoming_event()

        if self.notification.decision_code:
            # set decision (octroi / refus)
            mapping_decision_terms = {
                "OCTROI": "favorable",
                "REFUS": "defavorable",
            }
            urban_decision_term = mapping_decision_terms.get(
                self.notification.decision_code
            )
            if urban_decision_term:
                self.event.setDecision(urban_decision_term)
            else:
                self.event.setDescription(
                    u"Décision: {}".format(self.notification.decision_code)
                )

    @property
    def desired_licence_state(self):
        decision_code = self.notification.decision_code
        if decision_code:
            mapping_decision_states = {
                "OCTROI": "accepted",
                "REFUS": "refused",
            }
            return mapping_decision_states.get(decision_code, "")
        else:
            return ""


class GesperPublicSurveyHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IAcknowledgmentEvent"
    create_licence_if_missing = True

    @property
    def desired_licence_state(self):
        return "complete"


class GesperDecisionSPWHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IWalloonRegionDecisionEvent"
    create_licence_if_missing = True

    def fill_incoming_event(self):
        super(GesperDecisionSPWHandler, self).fill_incoming_event()

        decision_code = self.notification.decision_code
        if decision_code:
            mapping_decision_terms = {
                "UFD2_DEMAT_DECISION_FD": "favorable",
                "UFD2_DECISION_FD_OCTROI": "favorable",
                "UFD2_DECISION_FD_REFUSEE": "defavorable",
            }
            urban_decision_term = mapping_decision_terms.get(
                decision_code
            )
            if urban_decision_term:
                self.event.setDecision(urban_decision_term)
            else:
                self.event.setDescription(
                    u"Décision: {}".format(decision_code)
                )

    @property
    def desired_licence_state(self):
        decision_code = self.notification.decision_code
        if decision_code:
            mapping_decision_states = {
                "UFD2_DEMAT_DECISION_FD": "accepted",
                "UFD2_DECISION_FD_OCTROI": "accepted",
                "UFD2_DECISION_FD_REFUSEE": "refused",
            }
            return mapping_decision_states.get(decision_code, "")
        else:
            return ""


class GesperAmendedPlansSPWHandler(IncomingNoticeHandler):
    event_config_marker = "Products.urban.interfaces.IAmendedPlansAcknowledgmentEvent"
    create_licence_if_missing = True

    @property
    def desired_licence_state(self):
        return "complete"
