# -*- coding: utf-8 -*-

from ftw.testbrowser import browsing

from Products.urban.testing import URBAN_TESTS_FUNCTIONAL
from imio.urban.core.testing import FunctionalTestCase
from plone import api


def preconditions(browser, actor):
    """Login as actor."""
    browser.login(username=actor['username'], password=actor['password']).open()


class TestLicenceCreation(FunctionalTestCase):
    """Use case tests.
    Name: Create licence
    Actor(s): Site admin, Urban manager
    Goal: allows actors to create an an xml export to Ecompte
    Author: Julien Jaumotte, Franck Ngaha
    Created: 08/02/2021
    Updated: 09/02/2021
    Preconditions: The actor must be authenticated in a given specific context :
    - a site admin in the context of an urban folder in private following state (private)
    - an urban manager in the context of an urban folder in private following state (private)
    """

    layer = URBAN_TESTS_FUNCTIONAL

    def setUp(self):
        # Actors
        self.siteadmin = {'username': 'siteadmin', 'password': 'siteadmin'}
        self.urbanmanager = {'username': 'urbanmanager', 'password': 'urbanmanager'}
        # Contexts
        self.portal = self.layer['portal']
        self.urban_folder = self.portal['urban']
        # scenarios
        self.scenarios = [
            'main_scenario',
        ]

    @browsing
    def test_scenarios_as_urban_manager_in_portal_private(self, browser):
        state = api.content.get_state(obj=self.urban_folder)
        self.assertEqual(state, 'private')
        self.call_scenarios(browser, self.urban_manager, self.urban_folder)

    def call_scenarios(self, browser, actor, context):
        for scenario in self.scenarios:
            self.__getattribute__(scenario)(browser, actor, context)

    def main_scenario(self, browser, actor, context):
        import ipdb; ipdb.set_trace()
        preconditions(browser, actor)  # Login as actor
        self.start_up(browser, context)  # Open context

    def start_up(self, browser, context):
        """Open context."""
        browser.open(context)
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(context.Title().decode('utf8'), heading.text)
