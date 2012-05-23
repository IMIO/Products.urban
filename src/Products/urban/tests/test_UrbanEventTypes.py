# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope import event
from zope.component.interface import interfaceToName
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.urban.interfaces import IAcknowledgmentEvent
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFPlone.utils import safe_hasattr
from Products.urban.utils import getMd5Signature

class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbaneditor')

    def testLastKeyEventPropertyDefaultCase(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #by defaut, no key event should be enabled, and the index in the catalog should be empty
        self.assertEqual(urban_event_type_a.getIsKeyEvent(), False)
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def testSetLastKeyEventPropertyWithEventAlreadyExisting(self):
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #set 'rapport-du-college' as a key event, buildlicence index should be updated, cu2 index should not change as
        #the urbanEventType belongs to buildlicence cfg and not cu2 cfg
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        cu2_brain = catalog(portal_type='UrbanCertificateTwo')[0]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_a.Title())
        self.assertEqual(cu2_brain.last_key_event, None)
   
    def testSetLastKeyEventPropertyWithNoExistingEventCreated(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the 
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an 
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type_b = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'service-pop-opinion-request', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #set 'service-pop-opinion-request' as a key event, buildlicence last_key_event index should not change 
        #as the corresponding urbanEvent has never been created in this buildlicence
        urban_event_type_b.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_b))
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event, None)

    def testOrderInKeyEventsWhenActivatingLastKeyEventProperty(self):
        """
        When the field LastKeyEvent is activated in an urbanEvenType UET of the cfg, all the licences of the 
        given cfg type should have the index 'lastKeyEvent' updated to the value UET if they owns an 
        urbanEvent UET and if that urbanEvent is the last keyEvent created in the licence.
        """
        portal = self.layer['portal']
        catalog = getToolByName(portal, 'portal_catalog')
        urban_event_type_a = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'rapport-du-college', None)
        urban_event_type_c = getattr(self.portal_urban.buildlicence.urbaneventtypes, 'depot-de-la-demande', None)
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        #set 'rapport-du-college' as a key event, buildlicence index should be updated
        urban_event_type_a.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        #set 'depot-de-la-demande' as key event, buildlicence last_key_event index should not change as 
        #'rapport-du-college' is still the most recent keyEvent created
        urban_event_type_c.setIsKeyEvent(True)
        event.notify(ObjectEditedEvent(urban_event_type_c))
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_a.Title())
        #set 'rapport-du-college' back as a normal urbanEvenType, buildlicence last_key_event index should be
        #updated as 'depot-de-la-demande' becomes now the most recent key urban event created
        urban_event_type_a.setIsKeyEvent(False)
        event.notify(ObjectEditedEvent(urban_event_type_a))
        buildlicence_brain = catalog(portal_type='BuildLicence')[0]
        self.assertEqual(buildlicence_brain.last_key_event.split(',  ')[1], urban_event_type_c.Title())

    def testUrbanTemplateIsUnderActivationWF(self):
        portal = self.layer['portal']
        wf_tool = getToolByName(portal, 'portal_workflow')
        #Check that templates .odt files in urbanEventTypes are under activation wf policy
        urban_event_type = getattr(self.portal_urban.buildlicence.urbaneventtypes,'accuse-de-reception',None)
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
        all_templates = [obj for obj in urban_event_type.objectValues() if obj.portal_type == 'File']
        urban_event = catalog(object_provides=interfaceToName(portal, IAcknowledgmentEvent))[0].getObject()
        #by default all the templates should be enabled
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())
        #disable the first template, the available doc list should contain one element less
        wf_tool.doActionFor(all_templates[0], 'disable')
        self.assertEqual(len(all_templates)-1, len(urban_event.getTemplates()))
        for i in range(len(all_templates)-1):
            self.assertEqual(all_templates[i+1].Title(), urban_event.getTemplates()[i].Title())
        #re-enable the first template, the available doc list should contain one element more
        wf_tool.doActionFor(all_templates[0], 'enable')
        self.assertEqual(len(all_templates), len(urban_event.getTemplates()))
        for i in range(len(all_templates)):
            self.assertEqual(all_templates[i].Title(), urban_event.getTemplates()[i].Title())


    def testUrbanTemplatesUpdate(self):
        """
            Testing updating templates, depending on:
            - profile
            - md5Loaded
            - md5Modified
        """
        # check if template is well already installed
        my_accuse_folder = getattr(self.portal_urban.buildlicence.urbaneventtypes,'accuse-de-reception',None)
        self.assertNotEqual(my_accuse_folder,None)  
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertNotEqual(my_file_odt,None)
        my_update_file_datetime = my_file_odt.modified()

        # update template test by profil test (same template, identical md5loaded) : do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')   
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)

        # update template test by profil test (md5Loaded changed) : replace
        my_file_odt.manage_changeProperties({"md5Loaded":'reloadtemplate'})
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')   
        self.assertNotEqual(my_file_odt.modified(),my_update_file_datetime)

        # update template test by profil testCommune1 : replace template
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1','urban-Commune1UpdateTemplates')    
        self.assertNotEqual(my_file_odt.modified(),my_update_file_datetime)
        my_update_file_datetime = my_file_odt.modified() #warning, date have changed        

        # update template testCommune1 by profil test: do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates') 
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)         

        # update template testCommune1 by profil testCommune2: do nothing
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune2','urban-Commune2UpdateTemplates')
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)        

        # modify the value of property profilename (testCommune1) by (tests) and launch test profile : replace template
        my_file_odt.manage_changeProperties({"profileName":'tests'})
        my_update_file_datetime = my_file_odt.modified() #warning, date have changed by manage_changeProperties
        sleep(1)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')
        self.assertNotEqual(my_file_odt.modified(),my_update_file_datetime)

        # modify the value of property md5Modified and update template test by profil testCommune1 : replace template 
        #   because the template profile is 'test' so we override it
        my_file_odt.manage_changeProperties({"md5Modified":'aaaaaaa'})
        my_update_file_datetime = my_file_odt.modified() #warning, date have changed by manage_changeProperties
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1','urban-Commune1UpdateTemplates')   
        self.assertNotEqual(my_file_odt.modified(),my_update_file_datetime)

        # change the value of property md5Modified, set the value of property profileName to testCommune1 and update template test 
        #   by profil testCommune1 : do nothing because template has been customised
        my_file_odt.manage_changeProperties({"md5Loaded":'reloadtemplate'})
        my_file_odt.manage_changeProperties({"md5Modified":'aaaaaaa'})
        my_update_file_datetime = my_file_odt.modified() #warning, date have changed by manage_changeProperties
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1','urban-Commune1UpdateTemplates')   
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)

    def testUrbanTemplatesUpdateForced(self):
        """
            Testing updating templates when force
        """
        # check if template is well already installed
        my_accuse_folder = getattr(self.portal_urban.buildlicence.urbaneventtypes,'accuse-de-reception',None)
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertNotEqual(my_file_odt,None)
        my_update_file_datetime = my_file_odt.modified()
        my_header_odt = getattr(self.portal_urban.globaltemplates,'header.odt',None)
        self.assertNotEqual(my_header_odt, None)
        my_update_header_datetime = my_header_odt.modified()
        portal = self.layer['portal']

        # Without forcing: no change
        # First loaded template is the same
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)
        # Second loaded template isn't the same and template is modified
        my_file_odt.manage_changeProperties({"md5Loaded":'reloadtemplate', "md5Modified":'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded":'reloadtemplate', "md5Modified":'modified'})
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)

        # Forcing replacement when loaded template is the same as on the file system
        my_file_odt.manage_changeProperties({"md5Loaded":getMd5Signature(my_file_odt.data), "md5Modified":getMd5Signature(my_file_odt.data)})
        my_header_odt.manage_changeProperties({"md5Loaded":getMd5Signature(my_header_odt.data), "md5Modified":getMd5Signature(my_header_odt.data)})
        portal.REQUEST.form['reload_globals'] = 1
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')
        self.assertNotEquals(my_header_odt.modified(), my_update_header_datetime)
        self.assertEqual(my_file_odt.modified(),my_update_file_datetime)
        portal.REQUEST.form.pop('reload_globals')

        # Forcing replacement when template has been modified
        portal.REQUEST.form['replace_mod_events'] = 1
        my_file_odt.manage_changeProperties({"md5Loaded":'reloadtemplate', "md5Modified":'modified'})
        my_header_odt.manage_changeProperties({"md5Loaded":'reloadtemplate', "md5Modified":'modified'})
        my_update_file_datetime = my_file_odt.modified()
        my_update_header_datetime = my_header_odt.modified()
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-updateAllUrbanTemplates')
        self.assertEqual(my_header_odt.modified(), my_update_header_datetime)
        self.assertNotEquals(my_file_odt.modified(),my_update_file_datetime)
        portal.REQUEST.form.pop('replace_mod_events')
