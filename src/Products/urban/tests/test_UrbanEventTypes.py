# -*- coding: utf-8 -*-
import unittest
from zope import event
from zope.component.interface import interfaceToName
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectEditedEvent


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbaneditor')

    def testLastKeyEventPropertyDefaultCase(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        #by defaut, key events are enabled, and the index in the catalog should not be empty
        self.assertEqual(urban_event_type_a.getIsKeyEvent(), True)
        self.failUnless(buildlicence_brain.last_key_event is not None)

    def testSetLastKeyEventPropertyWithEventAlreadyExisting(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        #set 'rapport-du-college' as a key event, buildlicence index should be updated
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_a.Title())

    def testSetLastKeyEventPropertyWithNoExistingEventCreated(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_b = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'belgacom', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        #set 'belgacom' as a key event, buildlicence last_key_event index should not change
        #as the corresponding urbanEvent has never been created in this buildlicence
        urban_event_type_b.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_b))
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def testOrderInKeyEventsWhenActivatingLastKeyEventProperty(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        for uet in self.portal_urban.buildlicence.urbaneventtypes.objectValues():
            uet.setIsKeyEvent(False)
            event.notify(ObjectEditedEvent(uet))
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        urban_event_type_c = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'depot-de-la-demande', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        #set 'rapport-du-college' as a key event, buildlicence index should be updated
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        #set 'depot-de-la-demande' as key event, buildlicence last_key_event index should not change as
        #'rapport-du-college' is still the most recent keyEvent created
        urban_event_type_c.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_c))
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_a.Title())
        #set 'rapport-du-college' back as a normal urbanEvenType, buildlicence last_key_event index should be
        #updated as 'depot-de-la-demande' becomes now the most recent key urban event created
        urban_event_type_a.setIsKeyEvent(False)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(portal_type='BuildLicence')[-1]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_c.Title())

    def testUrbanTemplateIsUnderActivationWF(self):
        portal = self.layer['portal']
        wf_tool = getToolByName(portal, 'portal_workflow')
        #Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        template = getattr(urban_event_type, 'urb-accuse.odt', None)
        state = wf_tool.getInfoFor(template, 'review_state')
        self.assertEqual(state, 'enabled')

    def testGeneratedDocumentIsNotUnderActivationWF(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        wf_tool = getToolByName(portal, 'portal_workflow')
        #Check that generated .odt files in urbanEvents are NOT under any wf policy
        interfaceName = interfaceToName(portal, IAcknowledgmentEvent)
        urban_event = catalog(object_provides=interfaceName)[0].getObject()
        document = getattr(urban_event, 'urb-accuse.odt', None)
        exception_msg = ""
        try:
            wf_tool.getInfoFor(document, 'review_state')
        except Exception, error:
            exception_msg = "%s" % error
        self.assertEqual(exception_msg, "No workflow provides '${name}' information.")

    def testListAvailableUrbanTemplates(self):
        """
        When a template is disabled in the config, it should be removed from the list of documents to generate.
        When a template is (re)enabled, it should (re)appears in the list.
        """
        portal = self.layer['portal']
        wf_tool = getToolByName(portal, 'portal_workflow')
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'accuse-de-reception', None)
        all_templates = [obj for obj in urban_event_type.objectValues() if obj.portal_type == 'UrbanDoc']
        folder_path = "%s/urban/buildlicences" % '/'.join(portal.getPhysicalPath())
        urban_event = catalog(object_provides=interfaceToName(portal, IAcknowledgmentEvent), path={'query': folder_path, 'depth': 2})
        urban_event = urban_event[0].getObject()
        #by default all the templates should be enabled
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())
        #disable the first template, the available doc list should contain one element less
        wf_tool.doActionFor(all_templates[0], 'disable')
        self.assertEqual(len(all_templates) - 1, len(urban_event.getTemplates()))
        for i in range(len(all_templates) - 1):
            self.assertEqual(all_templates[i + 1].Title(), urban_event.getTemplates()[i].Title())
        #re-enable the first template, the available doc list should contain one element more
        wf_tool.doActionFor(all_templates[0], 'enable')
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())
