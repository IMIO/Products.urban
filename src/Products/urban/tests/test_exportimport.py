#  -*- coding: utf-8 -*-
import unittest2 as unittest
from Products.CMFPlone.utils import base_hasattr
from Products.urban.Extensions.imports import createStreet
from Products.urban.testing import URBAN_TESTS_CONFIG
from plone import api


class TestStreetImports(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.utool = portal.portal_urban
        self.wtool = portal.portal_workflow
        self.streets = self.utool.streets

    def testCreateStreet(self):
        ex_streets = {}
        # createStreet(self, city, zipcode, streetcode, streetname, bestAddresskey, startdate, enddate, regionalroad, ex_streets)

        # create a first street, historical one
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '0', "Rue de l'Estampage", 7090730, "2010/09/07", "2011/08/04", '', ex_streets)
        # checking once the city folder creation
        self.failUnless(base_hasattr(self.streets, 'awans'))
        awans = getattr(self.streets, 'awans')
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-lestampage'))
        rue1 = getattr(awans, 'rue-de-lestampage')
        # checking state
        self.assertEquals(self.wtool.getInfoFor(rue1, 'review_state'), 'disabled')
        # create a second street, new version of the recent one
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '1091', "Rue de l'Estampage", 7090730, "2011/08/04", None, '', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-lestampage1'))
        rue2 = getattr(awans, 'rue-de-lestampage1')
        self.assertEquals(self.wtool.getInfoFor(rue2, 'review_state'), 'enabled')
        self.assertEquals(self.wtool.getInfoFor(rue1, 'review_state'), 'disabled')

        # create the same first street => nothing must be done
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '0', "Rue de l'Estampage", 7090730, "2010/09/07", "2011/08/04", '', ex_streets)
        # checking creation
        self.failIf(base_hasattr(awans, 'rue-de-lestampage2'))
        self.assertEquals(len(awans.objectIds()), 2)
        # create the same second street => nothing must be done
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '1091', "Rue de l'Estampage", 7090730, "2011/08/04", None, '', ex_streets)
        # checking creation
        self.failIf(base_hasattr(awans, 'rue-de-lestampage2'))
        self.assertEquals(len(awans.objectIds()), 2)

        # create a new street, the actual first and after the historical
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '1032', "Rue de la Chaudronnerie", 7090729, "2011/08/04", None, '', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-la-chaudronnerie'))
        rue3 = getattr(awans, 'rue-de-la-chaudronnerie')
        self.assertEquals(self.wtool.getInfoFor(rue3, 'review_state'), 'enabled')
        # create a new street, historical
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '0', "Rue de la Chaudronnerie", 7090729, "2010/09/07", "2011/08/04", '', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-la-chaudronnerie1'))
        rue4 = getattr(awans, 'rue-de-la-chaudronnerie1')
        self.assertEquals(self.wtool.getInfoFor(rue4, 'review_state'), 'disabled')
        self.assertEquals(self.wtool.getInfoFor(rue3, 'review_state'), 'enabled')

        # create a new street, regional road first and after without
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '1025', "Rue de Bruxelles", 7020318, "2010/09/07", None, 'N3', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-bruxelles'))
        rue5 = getattr(awans, 'rue-de-bruxelles')
        self.assertEquals(self.wtool.getInfoFor(rue5, 'review_state'), 'enabled')
        # create a new street, same street name but without regional road
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '1025', "Rue de Bruxelles", 7020319, "2010/09/07", None, '', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-bruxelles1'))
        rue6 = getattr(awans, 'rue-de-bruxelles1')
        self.assertEquals(self.wtool.getInfoFor(rue6, 'review_state'), 'enabled')
        self.assertEquals(self.wtool.getInfoFor(rue5, 'review_state'), 'disabled')  # previous street has been disabled

        # create a new street, without regional road first and after with one
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '5000', "Rue de Namur", 7020320, "2010/09/07", None, '', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-namur'))
        rue7 = getattr(awans, 'rue-de-namur')
        self.assertEquals(self.wtool.getInfoFor(rue7, 'review_state'), 'enabled')
        # create a new street, same street name but with regional road
        with api.env.adopt_roles(['Manager']):
            createStreet('Awans', 4340, '5000', "Rue de Namur", 7020321, "2010/09/07", None, 'N4', ex_streets)
        # checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-namur1'))
        rue8 = getattr(awans, 'rue-de-namur1')
        self.assertEquals(self.wtool.getInfoFor(rue8, 'review_state'), 'disabled')
        self.assertEquals(self.wtool.getInfoFor(rue7, 'review_state'), 'enabled')  # previous street is unchanged
