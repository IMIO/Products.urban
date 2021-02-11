# -*- coding: utf-8 -*-

from ftw.testbrowser import browsing

from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from imio.urban.core.testing import FunctionalTestCase
from plone import api


def preconditions(browser, actor):
    """Login as actor."""
    browser.login(username=actor['username'], password=actor['password']).open()


def step_1(browser, context):
    """The actor adds build licence."""
    browser.open(
        context.absolute_url() +
        '/codt_buildlicences/collection_codt_buildlicence/codt_buildlicences/createObject?type_name=CODT_BuildLicence'
    )


class TestLicenceCreation(FunctionalTestCase):
    """Use case tests.
    Name: Create licence
    Actor(s): Admin, Urban manager
    Goal: allows actors to create an an xml export to Ecompte
    Author: Julien Jaumotte, Franck Ngaha
    Created: 08/02/2021
    Updated: 09/02/2021
    Preconditions: The actor must be authenticated in a given specific context :
    - an admin in the context of an urban folder in private following state (private)
    - an urban manager in the context of an urban folder in private following state (private)
    """

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        # Actors
        self.urbanadmin = {'username': 'urbanadmin', 'password': 'urbanadmin'}
        self.urbanmanager = {'username': 'urbanmanager', 'password': 'urbanmanager'}
        # Contexts
        self.portal = self.layer['portal']
        self.app_folder = self.portal['urban']
        # scenarios
        self.scenarios = [
            'main_scenario',
        ]

    @browsing
    def test_scenarios_as_urbanadmin_in_portal_private(self, browser):
        state = api.content.get_state(obj=self.app_folder)
        self.assertEqual(state, 'private')
        self.call_scenarios(browser, self.urbanadmin, self.app_folder)

    @browsing
    def test_scenarios_as_urbanmanager_in_portal_private(self, browser):
        state = api.content.get_state(obj=self.app_folder)
        self.assertEqual(state, 'private')
        self.call_scenarios(browser, self.urbanmanager, self.app_folder)

    def call_scenarios(self, browser, actor, context):
        for scenario in self.scenarios:
            self.__getattribute__(scenario)(browser, actor, context)

    def main_scenario(self, browser, actor, context):
        preconditions(browser, actor)  # Login as actor
        self.start_up(browser, context)  # Open context
        step_1(browser, context)  # The actor adds build licence
        self.step_2(browser, context)  # The system calculates default values and displays the form

    def start_up(self, browser, context):
        """Open context."""
        browser.open(context)
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(context.Title().decode('utf8'), heading.text)

    def step_2(self, browser, context):
        """The system calculates default values and displays the form."""
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(u"Ajouter Permis d'urbanisme (CODT)", heading.text)

