# -*- coding: utf-8 -*-
from Acquisition import aq_base
from datetime import date
from DateTime import DateTime

from Products.urban import testing
from Products.urban.services.notice import WebserviceNotice
from Products.urban.services.tests.data import load_notif_content
from Products.urban.services.tests.data import load_notif_json
from Products.urban.interfaces import IRefusedIncompletenessEvent
        
from zope.annotation.interfaces import IAnnotations
from plone import api

import mock
import unittest


class MockedRequest(object):
    def __init__(self, response_data, status_code=200):
        self._response_data = response_data
        self.status_code = status_code

    def json(self):
        return self._response_data

    @property
    def content(self):
        return self._response_data


class TestNoticeCronPE2(unittest.TestCase):
    layer = testing.URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer["portal"]
        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.municipality_id",
            u"0206.524.876",
        )
        api.portal.set_registry_record(
            "Products.urban.browser.notice_settings.INoticeSettings.sent_on_behalf_of_municipality_id",
            u"0216697802",
        )


    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=load_notif_json("TRANSFERT_DOSSIER", "1357456_notifications.json"),
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(load_notif_json("TRANSFERT_DOSSIER", "1357456-NOUVEAU_DOSSIER-EN_ATTENTE_REPONSE.json")),
    )
    @mock.patch(
        "Products.urban.notice.address.NoticeAddress._find_address",
        return_value=[{"text": "street, 1 (1400 - Nivelles)", "id": "1234"}],
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification_document",
        return_value=MockedRequest(load_notif_content("TRANSFERT_DOSSIER", "document.pdf")),
    )
    def _create_licence(self, address_patch, doc_patch, notif_patch, notifs_patch):
        address_patch, doc_patch, notif_patch, notifs_patch  # noqa

        with api.env.adopt_roles(["Manager"]):
            import_view = self.portal.restrictedTraverse("@@import-from-notice")
            return import_view()


    def _create_licence_event(self, licence, event_type):
        event_configs = self.portal.portal_urban.envclasstwo.eventconfigs
        event_config = event_configs[event_type]
        with api.env.adopt_roles(["Manager"]):
            event = licence.createUrbanEvent(event_config)
        return event


    def test_transmit(self):
        # 1) create licence
        result = self._create_licence()
        self.assertEqual("OK", result)
        licence_folder = self.portal.urban.envclasstwos
        licence = licence_folder.values()[-1]
        self.assertEqual(licence.reference, "PE2/2025/2")

        # 2) create deposit
        deposit_event = self._create_licence_event(licence, "depot-de-la-demande")
        deposit_event.setEventDate(DateTime(2025, 6, 19))

        # 3) create UrbanEventNotice (must have ITransmitToSPWEvent)
        transmit_event = self._create_licence_event(licence, "envoi-demande-FT")
        transmit_event.setEventDate(DateTime(2025, 6, 19))
        dates = self._get_notice_transmit_dates(transmit_event)
        self.assertIsNone(dates.get("transfer_folder_to_dpa"))

        # 4) mock NoticeOutgoingNotification / transmit
        with mock.patch(
                "Products.urban.services.notice.WebserviceNotice._post_notification_response",
                return_value=MockedRequest(load_notif_json("TRANSFERT_DOSSIER", "1357456-NOUVEAU_DOSSIER-transmit_response.json"))
        ) as mock_post_notification_response:
            transmit_response = transmit_event.transfer_folder_to_dpa()
        self.assertFalse(transmit_response["error"])
        self.assertEqual(transmit_response["body"]["status"], "PROCESSED")

        dates = self._get_notice_transmit_dates(transmit_event)
        self.assertEqual(dates.get("transfer_folder_to_dpa").date(), date(2025, 6, 19))

        # 5) mock get notif, verify updates are applied
        with mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification",
            return_value=MockedRequest(
                load_notif_json("TRANSFERT_DOSSIER", "1357456-NOUVEAU_DOSSIER-TERMINE.json")
            )
        ) as mock_get_notification:
            service = WebserviceNotice()
            updated_notification = service.get_notification(1357456)
        self.assertEqual(updated_notification.status, "TERMINE")
        self.assertEqual(updated_notification.status_date, date(2025, 6, 19))
        self.assertEqual(updated_notification.reference, "PE2/2025/2")

        # 6) make another test for double transmit, make sure it handles error case

        # reset transmit date (store fake one), assert it's reset
        transmit_event.store_transmit_date("transfer_folder_to_dpa", date(2000, 1, 1))
        dates = self._get_notice_transmit_dates(transmit_event)
        self.assertEqual(dates.get("transfer_folder_to_dpa"), date(2000, 1, 1))

        with mock.patch(
            "Products.urban.services.notice.WebserviceNotice._post_notification_response",
            return_value=MockedRequest(
                load_notif_json("TRANSFERT_DOSSIER", "1357456-NOUVEAU_DOSSIER-transmit_bis_response.json"), status_code=400
            ),
        ) as mock_post_notification_response, mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification",
            return_value=MockedRequest(load_notif_json("TRANSFERT_DOSSIER", "1357456-NOUVEAU_DOSSIER-TERMINE.json")),
        ) as mock_get_notification:
            transmit_response = transmit_event.transfer_folder_to_dpa()

        # assert good transmit date is back
        dates = self._get_notice_transmit_dates(transmit_event)
        self.assertEqual(dates.get("transfer_folder_to_dpa"), date(2025, 6, 19))
    def _get_notice_transmit_dates(self, event):
        annotations = IAnnotations(event)
        dates = annotations.get("notice_transmit_dates", {})
        return dates

    def tearDown(self):
        with api.env.adopt_roles(["Manager"]):
            licence_folder = self.portal.urban.envclasstwos
            licence = licence_folder.values()[-1]
            api.content.delete(obj=licence)


    """@mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=load_notif_json("DEMANDE_EP", "1342038_notifications.json"),
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(load_notif_json("DEMANDE_EP", "1342038-DEMANDE_EP-EN_ATTENTE_REPONSE.json")),
    )
    def _create_dossier_complet(self, notif_patch, notifs_patch):
        notif_patch, notifs_patch  # noqa

        with api.env.adopt_roles(["Manager"]):
            import_view = self.portal.restrictedTraverse("@@import-from-notice")
            return import_view()"""
    
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=load_notif_json("INCOMPLETE", "1407578-NOTIFICATIONS.json"),
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(load_notif_json("INCOMPLETE", "1407578-INCOMPLETE-NOTIFICATION.json")),
    )
    def _create_incomplete_folder(self, notif_patch, notifs_patch):
        notif_patch, notifs_patch  
        self.notif_patch = notif_patch
        
        with api.env.adopt_roles(["Manager"]):
            import_view = self.portal.restrictedTraverse("@@import-from-notice")
            import_view()
    
    def test_incomplete_notification(self):
        # 1) create licence
        with mock.patch(
            "Products.urban.services.notice.WebserviceNotice.get_notifications",
            return_value=load_notif_json("INCOMPLETE", "959254_notifications.json"),
        ) as mock_get_notifications, mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification",
            return_value=MockedRequest(
                load_notif_json(
                    "INCOMPLETE", "959254-TRANSFERT-DOSSIER-EN_ATTENTE_REPONSE.json"
                )
            ),
        ) as mock_get_notification, mock.patch(
            "Products.urban.notice.address.NoticeAddress._find_address",
            return_value=[{"text": "street, 1 (1400 - Nivelles)", "id": "1234"}],
        ) as mock_address, mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification_document",
            return_value=MockedRequest(load_notif_content("TRANSFERT_DOSSIER", "document.pdf")),
        ) as mock_get_document:
            with api.env.adopt_roles(["Manager"]):
                import_view = self.portal.restrictedTraverse("@@import-from-notice")
                import_view()

        licence_folder = self.portal.urban.envclasstwos
        licence = licence_folder.values()[-1]
        licence.reference = "PE2/2025/5"  # force reference, already sent to NOTICE
        licence.reindexObject()
        self.assertIsNone(licence.getLastMissingPart())
        self._create_incomplete_folder()
        # 5.3 assert folder incomplet présent
        incomplete_folder = licence.getLastMissingPart()
        self.assertIsNotNone(incomplete_folder)
        # 5.4 assert folder is closed
        self.assertEqual(incomplete_folder.getEventDate().Date(), "2025/07/11")
        self.assertEqual(api.content.get_state(incomplete_folder), "closed")

    def _create_not_admissible_folder(self, suffix, notif_id):
        folder_name = "NOT_ADMISSIBLE{0}".format(suffix)
        notif_file = "{0}_notifications.json".format(notif_id)

        if notif_id is None:
            raise ValueError("Vous devez passer un notif_id pour ce test")
        single_notif_file = "{0}-NOT-ADMISSIBLE-NOTIFICATION.json".format(notif_id)
        # Load JSON
        data = load_notif_json(folder_name, notif_file)

        # Mock
        with mock.patch(
            "Products.urban.services.notice.WebserviceNotice.get_notifications",
            return_value=data,
        ), mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification",
            return_value=MockedRequest(load_notif_json(folder_name, single_notif_file)),
        ):
            with api.env.adopt_roles(["Manager"]):
                import_view = self.portal.restrictedTraverse("@@import-from-notice")
                import_view()
    
    def test_not_admissible_notification_second_tour(self):
        licence_folder = self.portal.urban.envclasstwos
        licence = licence_folder.values()[-1]
        licence.reference = "PE2/2025/4"
        licence.reindexObject()

        # Création folder 2ème tour
        self._create_not_admissible_folder("2","1443529")

        not_admissible_folder = licence.getLastRefusedNotification()
        self.assertIsNotNone(not_admissible_folder)
        self.assertEqual(not_admissible_folder.getEventDate().Date(), "2025/09/19")
        self.assertEqual(api.content.get_state(not_admissible_folder), "closed")
    
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=load_notif_json("INADMISSIBLE", "1443524-NOTIFICATIONS.json"),
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(
            load_notif_json("INADMISSIBLE", "1443524-INADMISSIBLE-NOTIFICATION.json")
        ),
    )
    def _create_inadmissible_folder(self, notif_patch, notifs_patch):
        notif_patch, notifs_patch
        self.notif_patch = notif_patch

    
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice.get_notifications",
        return_value=load_notif_json("INADMISSIBLE", "1443524-NOTIFICATIONS.json"),
    )
    @mock.patch(
        "Products.urban.services.notice.WebserviceNotice._get_notification",
        return_value=MockedRequest(
            load_notif_json("INADMISSIBLE", "1443524-INADMISSIBLE-NOTIFICATION.json")
        ),
    )
    def _create_inadmissible_folder(self, notif_patch, notifs_patch):
        notif_patch, notifs_patch
        self.notif_patch = notif_patch

        with api.env.adopt_roles(["Manager"]):
            import_view = self.portal.restrictedTraverse("@@import-from-notice")
            import_view()

    def test_inadmissible_notification_second_tour(self):
        # create licence
        licence_folder = self.portal.urban.envclasstwos
        licence = licence_folder.values()[-1]
        licence.reference = "PUN/2025/08261437"
        licence.reindexObject()
        self._create_inadmissible_folder()
        # assert folder inadmissible present
        inadmissible_folder = licence.getLastRefusedNotification()
        self.assertIsNotNone(inadmissible_folder)
        # assert folder is closed
        self.assertEqual(inadmissible_folder.getEventDate().Date(), "2025/09/16")
        self.assertEqual(api.content.get_state(inadmissible_folder), "closed")
