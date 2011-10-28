# -*- coding: utf-8 -*-
import unittest
from time import sleep
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        self.portal_setup = portal.portal_setup
        login(portal, 'urbaneditor')
        
    def testAddUrbanEventTypes(self):
        """ 1) add template (by install of test profil)
            2) update template test by profil test(sans modif) : do nothing
            3) update template test by profil testCommune1 : replace template
            4) update template testCommune1 by profil test: do nothing
            5) update template testCommune1 by profil testCommune2: do nothing
            6) modify the value of property profilename (testCommune1) by (tests) and launch test profile : replace template
            7) modify the value of property md5Signature and update template test by profil testCommune1 : do nothing
        """
        # 1)
        my_accuse_folder = getattr(self.portal_urban.buildlicence.urbaneventtypes,'accuse-de-reception',None)
        self.assertNotEqual(my_accuse_folder,None)  
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertNotEqual(my_file_odt,None)
        my_update_file_datetime = my_file_odt.ModificationDate()
        # 2)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-addTestObjects')   
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertEqual(my_file_odt.ModificationDate(),my_update_file_datetime)
        # 3)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1','urban-Commune1UpdateTemplates')    
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertNotEqual(my_file_odt.ModificationDate(),my_update_file_datetime)
        my_update_file_datetime = my_file_odt.ModificationDate() #warning, date have changed        
        # 4)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-addTestObjects') 
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertEqual(my_file_odt.ModificationDate(),my_update_file_datetime)         
        # 5)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune2','urban-Commune2UpdateTemplates')
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertEqual(my_file_odt.ModificationDate(),my_update_file_datetime)        
        # 6)
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        my_file_odt.manage_changeProperties({"profileName":'tests'})
        my_file_odt.reindexObject()
        my_update_file_datetime = my_file_odt.ModificationDate() #warning, date have changed by manage_changeProperties
        sleep(1)
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:tests','urban-addTestObjects')  
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertNotEqual(my_file_odt.ModificationDate(),my_update_file_datetime)
        # 7) 
        my_file_odt.manage_changeProperties({"md5Signature":'aaaaaaa'})
        my_file_odt.reindexObject()
        my_update_file_datetime = my_file_odt.ModificationDate() #warning, date have changed by manage_changeProperties
        self.portal_setup.runImportStepFromProfile('profile-Products.urban:testCommune1','urban-Commune1UpdateTemplates')   
        my_file_odt = getattr(my_accuse_folder,'urb-accuse.odt',None)
        self.assertEqual(my_file_odt.ModificationDate(),my_update_file_datetime)
