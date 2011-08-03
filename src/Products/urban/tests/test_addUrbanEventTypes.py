# -*- coding: utf-8 -*-
import unittest
from time import sleep
from zope.component import createObject
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


class TestUrbanEventTypes(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban        
        urban = portal.urban
        login(portal, 'urbaneditor')
        
    def testAddUrbanEventTypes(self):
        """ 1) ajout template
            2) update template test by test(avec modif)
            3) update template test by test(sans modif ne rien faire)
            4) update template test by mons
            5) update template mons by test(ne rien faire)
            6) update template mons by mons(avec modif)
            7) update template alors que la template déjà modifié dans plone(ne rien faire)
         """