# -*- coding: utf-8 -*-
from datetime import date
from DateTime import DateTime

from Products.urban import testing
from Products.urban.services.notice import WebserviceNotice
from Products.urban.services.tests.data import load_notif_content
from Products.urban.services.tests.data import load_notif_json
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

    def test_incomplete_notification(self):
        result = self._create_licence()
        self.assertEqual("OK", result)
        licence_folder = self.portal.urban.envclasstwos
        licence = licence_folder.values()[-1]
        licence.reference = "PE2/2025/5"
        licence.reindexObject()
        self.assertEqual(licence.reference, "PE2/2025/5")
        #verify workflow state is different from incmplete
        #wf = api.portal.get_tool("portal_workflow")
        #current_state = wf.getInfoFor(licence, "review_state")
        #self.assertEqual(api.content.get_state(licence), "deposit")
        self.assertNotEqual(api.content.get_state(licence), "incomplete")
        #mock notification
        # Mocknotification INCOMPLETE
        with mock.patch(
            "Products.urban.services.notice.WebserviceNotice._get_notification",
            return_value=MockedRequest(load_notif_json("INCOMPLETE", "1407578-INCOMPLETE-NOTIFICATION.json")),
        ):
            # create incomplete event dossier-incomplet
            incomplete_event = self._create_licence_event(licence, "dossier-incomplet")
            incomplete_event.setEventDate(DateTime(2025, 7, 11))
            
            # close the event
            api.content.transition(incomplete_event, "close")

            #change licence state to incomplete
            api.content.transition(licence, "isincomplete")

        
        #event_state = wf.getInfoFor(incomplete_event, "review_state")
        self.assertEqual(api.content.get_state(incomplete_event), "closed")

        # verify licence state is now incomplete
        #new_state = wf.getInfoFor(licence, "review_state")
        self.assertEqual(api.content.get_state(licence), "incomplete")
        
        
        #assert folder incomplete absent
        self.assertIsNone(licence.getLastMissingPart())
        self._create_dossier_complet()

        # 5.3 assert dossier complet présent
        incomplete_folder = licence.getLastMissingPart()
        self.assertIsNotNone(incomplete_folder)
    
        # 5.4 assert dossier complet date, état complet
        self.assertEqual(incomplete_folder.getEventDate().Date(), "2025/07/11")
        self.assertEqual(api.content.get_state(incomplete_folder), "closed")
       