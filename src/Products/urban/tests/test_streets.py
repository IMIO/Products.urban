# -*- coding: utf-8 -*-


from OFS.ObjectManager import BeforeDeleteException
from Products.urban.testing import URBAN_TESTS_CONFIG
from Products.urban.tests.helpers import BrowserTestCase

from plone.app.testing import login




class TestUrbanStreets(BrowserTestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        site = self.layer['portal']
        self.site = site
        self.buildlicence = site.urban.buildlicences.objectValues()[-1]
        self.city = site.urban.portal_urban.streets.objectValues()[-1]
        portal = self.layer['portal']
        login(portal, 'urbanmanager')

    def test_streets_delete(self):
            # create a street
            self.city.invokeFactory('Street', id="streetId1", streetCode="666", streetName="Rue de la gare",
                                                bestAddressKey="123456")
            wl = self.buildlicence.getWorkLocations()
            wll = list(wl)
            wll.append({'street': self.city.streetId1.UID(), 'number': '123'})
            # link licence to this first street
            self.buildlicence.setWorkLocations(tuple(wll))

            # street must not be deleted if linked to a licence
            self.assertRaises(BeforeDeleteException, self.city.manage_delObjects, [self.city.streetId1.id])

            # create a street and don't link it to a licence
            self.city.invokeFactory('Street', id="streetId2", streetCode="777", streetName="Rue de la suppression",
                                                bestAddressKey="654321")
            # delete this former street must not raise a BeforeDeleteException
            self.city.manage_delObjects([self.city.streetId2.id])
            print('end')
