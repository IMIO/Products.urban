# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES

from plone import api
from plone.app.testing import login
from plone.testing.z2 import Browser

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestSearchView(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.urban = portal.urban
        self.searchview = portal.restrictedTraverse('urbansearchview')
        self.buildlicence = self.urban.buildlicences.objectValues()[-1]
        self.division = self.urban.divisions.objectValues()[-1]
        self.miscdemand = self.urban.miscdemands.objectValues()[-1]

        login(portal, 'urbanmanager')
        self.browser = Browser(self.portal)
        self.browserLogin('urbanmanager')
        self.browser.handleErrors = False

    def browserLogin(self, user):
        self.browser.open(self.portal.absolute_url() + "/login_form")
        self.browser.getControl(name='__ac_name').value = user
        self.browser.getControl(name='__ac_password').value = user
        self.browser.getControl(name='submit').click()

    def test_search_view_display(self):
        """
         Test search  view is not broken for whatsoever reason
        """
        search_url = '{base_url}/urbansearchview'.format(base_url=self.urban.absolute_url())
        self.browser.open(search_url)

    def test_search_view_result_display(self):
        """ Just push the search button and see if it display results correctly """
        search_url = '{base_url}/urbansearchview'.format(base_url=self.urban.absolute_url())
        self.browser.open(search_url)

        search_form = self.browser.getForm('search')
        search_form.submit()

        self.assertTrue('contenttype-buildlicence state-in_progress' in self.browser.contents)
        self.assertTrue('contenttype-division state-in_progress' in self.browser.contents)
        self.assertTrue('contenttype-notaryletter state-in_progress' in self.browser.contents)
        self.assertTrue('contenttype-parceloutlicence state-in_progress' in self.browser.contents)

    def test_reindex_applicantInfos_when_applicant_is_modified(self):
        """ """

        catalog = api.portal.get_tool('portal_catalog')

        applicant = self.buildlicence.getApplicants()[0]

        firstname = 'Grégoire'
        lastname = 'Rasoir'

        applicant.setName1(firstname)
        applicant.setName2(lastname)

        search_result = catalog(
            portal_type='BuildLicence',
            applicantInfosIndex=[firstname, lastname]
        )
        self.assertTrue(not search_result)

        event = ObjectModifiedEvent(applicant)
        notify(event)

        search_result = catalog(
            portal_type='BuildLicence',
            applicantInfosIndex=[firstname, lastname]
        )
        found_licence = search_result[0].getObject()
        self.assertTrue(found_licence == self.buildlicence)

    def test_searchByName(self):
        """ """

        licence_types = ['BuildLicence', 'Division', 'MiscDemand']
        contact_types = ['Applicant', 'Notary', 'Architect', 'Geometrician']

        firstname = 'Lazarus'
        lastname = 'McDeathSinger'

        search_result = self.searchview.searchByName(licence_types, firstname, contact_types)

        # so far we should not find anything..
        self.assertTrue(not search_result)

        # change names of different contacts on different licences
        architect = self.buildlicence.getArchitects()[0]
        architect.setName1(firstname)
        architect.setName2(lastname)
        architect.reindexObject()

        notary = self.division.getNotaryContact()[0]
        notary.setName1(firstname)
        notary.setName2(lastname)
        notary.reindexObject()

        applicant = self.miscdemand.getApplicants()[0]
        applicant.setName1(firstname)
        applicant.setName2(lastname)
        applicant.reindexObject()
        event = ObjectModifiedEvent(applicant)
        notify(event)

        search_result = self.searchview.searchByName(licence_types, firstname, contact_types)
        search_result = [brain.getObject() for brain in search_result]

        self.assertTrue(len(search_result) == 3)
        self.assertTrue(self.buildlicence in search_result)
        self.assertTrue(self.division in search_result)
        self.assertTrue(self.miscdemand in search_result)

    def test_searchByName_contacttype_filter(self):
        """ """

        licence_types = ['BuildLicence', 'Division', 'MiscDemand']

        # we only search for Applicant and Architect contacts
        contact_types = ['Applicant', 'Architect']

        firstname = 'Lazarus'
        lastname = 'McDeathSinger'

        search_result = self.searchview.searchByName(licence_types, firstname, contact_types)

        # so far we should not find anything..
        self.assertTrue(not search_result)

        # change names of different contacts on different licences
        architect = self.buildlicence.getArchitects()[0]
        architect.setName1(firstname)
        architect.setName2(lastname)
        architect.reindexObject()

        notary = self.division.getNotaryContact()[0]
        notary.setName1(firstname)
        notary.setName2(lastname)
        notary.reindexObject()

        applicant = self.miscdemand.getApplicants()[0]
        applicant.setName1(firstname)
        applicant.setName2(lastname)
        applicant.reindexObject()
        event = ObjectModifiedEvent(applicant)
        notify(event)

        search_result = self.searchview.searchByName(licence_types, firstname, contact_types)
        search_result = [brain.getObject() for brain in search_result]

        # we should find the buildlicence (Architect contact)  and the
        # miscdemand (Applicant contact)
        self.assertTrue(len(search_result) == 2)
        self.assertTrue(self.buildlicence in search_result)
        self.assertTrue(self.miscdemand in search_result)
        # .. but not the division (Notary contact)
        self.assertTrue(self.division not in search_result)

    def test_searchByFolderReference(self):
        """ """

        licence_types = ['BuildLicence', 'Division', 'MiscDemand']

        reference = 'trololo lvl 77'

        search_result = self.searchview.searchByFolderReference(licence_types, reference)

        # so far we should not find anything..
        self.assertTrue(not search_result)

        self.buildlicence.setReference(reference)
        self.buildlicence.reindexObject()
        self.division.setReference(reference)
        self.division.reindexObject()

        search_result = self.searchview.searchByFolderReference(licence_types, reference)
        search_result = [brain.getObject() for brain in search_result]

        self.assertTrue(len(search_result) == 2)
        self.assertTrue(self.buildlicence in search_result)
        self.assertTrue(self.division in search_result)
        # we did not change the miscdemand
        self.assertTrue(self.miscdemand not in search_result)

    def test_searchByStreet(self):
        """ """

        licence_types = ['BuildLicence', 'Division', 'MiscDemand']

        portal_urban = api.portal.get_tool('portal_urban')
        streets_folder = portal_urban.streets.city1
        street_id = streets_folder.invokeFactory('Street', id="yolo_street", streetName='YOLO SWAG Street')
        street = getattr(streets_folder, street_id)

        search_result = self.searchview.searchByStreet(licence_types, street.Title())

        # so far we should not find anything..
        self.assertTrue(not search_result)

        new_location = ({'street': street.UID(), 'number': '42'},)
        self.buildlicence.setWorkLocations(new_location)
        self.buildlicence.reindexObject()
        self.division.setWorkLocations(new_location)
        self.division.reindexObject()

        search_result = self.searchview.searchByStreet(licence_types, street.Title())
        search_result = [brain.getObject() for brain in search_result]

        self.assertTrue(len(search_result) == 2)
        self.assertTrue(self.buildlicence in search_result)
        self.assertTrue(self.division in search_result)
        # we did not change the miscdemand street adress
        self.assertTrue(self.miscdemand not in search_result)
