# -*- coding: utf-8 -*-
import unittest
from zope import event
from plone import api
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.Archetypes.event import ObjectEditedEvent


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer["portal"]
        login(portal, "urbaneditor")
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        self.catalog = api.portal.get_tool("portal_catalog")
        buildlicence_brains = self.catalog(
            portal_type="BuildLicence", Title="Exemple Permis Urbanisme"
        )
        self.buildlicence = buildlicence_brains[0].getObject()

    def testLastKeyEventPropertyDefaultCase(self):
        catalog = self.catalog
        urban_event_type_a = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "rapport-du-college", None
        )
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # by defaut, key events are enabled, and the index in the catalog should not be empty
        self.assertEqual(urban_event_type_a.getIsKeyEvent(), True)
        self.failUnless(buildlicence_brain.last_key_event is not None)

    def testSetLastKeyEventPropertyWithEventAlreadyExisting(self):
        catalog = self.catalog
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            uet.setIsKeyEvent(True)
            event.notify(ObjectEditedEvent(uet))
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_a = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "rapport-du-college", None
        )
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'rapport-du-college' as a key event, buildlicence index should be updated
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(
            buildlicence_brain.last_key_event.split(",  ")[1],
            urban_event_type_a.Title(),
        )

    def testSetLastKeyEventPropertyWithNoExistingEventCreated(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        catalog = self.catalog
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            uet.setIsKeyEvent(True)
            event.notify(ObjectEditedEvent(uet))
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_b = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "sncb", None
        )
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'belgacom' as a key event, buildlicence last_key_event index should not change
        # as the corresponding urbanEvent has never been created in this buildlicence
        urban_event_type_b.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_b))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def testOrderInKeyEventsWhenActivatingLastKeyEventProperty(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        catalog = self.catalog
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            # reset urban event types twice to make sure to trigger the reindex
            uet.setIsKeyEvent(True)
            event.notify(ObjectEditedEvent(uet))
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_a = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "rapport-du-college", None
        )
        urban_event_type_c = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "depot-de-la-demande", None
        )
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        # set 'rapport-du-college' as a key event, buildlicence index should be updated
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        # set 'depot-de-la-demande' as key event, buildlicence last_key_event index should not change as
        # 'rapport-du-college' is still the most recent keyEvent created
        urban_event_type_c.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_c))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(
            buildlicence_brain.last_key_event.split(",  ")[1],
            urban_event_type_a.Title(),
        )
        # set 'rapport-du-college' back as a normal urbanEvenType, buildlicence last_key_event index should be
        #  updated as 'depot-de-la-demande' becomes now the most recent key urban event created
        urban_event_type_a.setIsKeyEvent(False)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(UID=self.buildlicence.UID())[-1]
        self.assertEqual(
            buildlicence_brain.last_key_event.split(",  ")[1],
            urban_event_type_c.Title(),
        )

    def testUrbanTemplateIsUnderActivationWF(self):
        wf_tool = api.portal.get_tool("portal_workflow")
        # Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(
            self.portal_urban.buildlicence.urbaneventtypes, "accuse-de-reception", None
        )
        template = getattr(urban_event_type, "urb-accuse.odt", None)
        state = wf_tool.getInfoFor(template, "review_state")
        self.assertEqual(state, "enabled")

    def testGeneratedDocumentIsNotUnderActivationWF(self):
        wf_tool = api.portal.get_tool("portal_workflow")

        # Check that generated .odt files in urbanEvents are NOT under any wf policy
        urban_event = self.buildlicence.getLastAcknowledgment()
        document = getattr(urban_event, "urb-accuse.odt", None)
        exception_msg = ""
        try:
            wf_tool.getInfoFor(document, "review_state")
        except Exception, error:
            exception_msg = "%s" % error
        self.assertEqual(exception_msg, "No workflow provides '${name}' information.")
