# -*- coding: utf-8 -*-
from xml.etree import ElementTree

from ftw.testbrowser import browsing
from ftw.testbrowser.pages import statusmessages
from imio.urban.core.testing import FunctionalTestCase
from plone import api

from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL


def preconditions(browser, actor):
    """Login as actor."""
    browser.login(username=actor['username'], password=actor['password']).open()


def step_1(browser, context):
    """The actor opens edit form."""
    browser.open(context.absolute_url() + '/edit')


def step_3a(browser):
    """The actor cancels the form."""
    form = browser.forms['form']
    form.find_button_by_label('Annuler').click()


class TestLicenceCreation(FunctionalTestCase):
    """Use case tests.
    Name: Create licence
    Actor(s): urban admin
    Goal: allows actors to create an an xml export to Ecompte
    Author: Julien Jaumotte
    Created: 08/02/2021
    Updated: 08/02/2021
    Preconditions: The actor must be authenticated in a given specific context :
    - a pst admin in the context of a pst project space in state (internally_published)
    """

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        import ipdb; ipdb.set_trace() # TODO REMOVE BREAKPOINT
        # Actors
        self.urban_admin = {'username': 'urbanmanager', 'password': 'urbanmanager'}
        self.urban_editor = {'username': 'urbaneditor', 'password': 'urbaneditor'}
        # Contexts
        self.portal = self.layer['portal']
        self.urban = self.portal['urban']
        # scenarios
        self.scenarios = [
            'main_scenario',
        ]

    @browsing
    def test_scenarios_as_admin_in_pst_project_space_internally_published(self, browser):
        state = api.content.get_state(obj=self.urban)
        self.assertEqual(state, 'internally_published')
        self.call_scenarios(browser, self.urban_admin, self.urban)

    def call_scenarios(self, browser, actor, context):
        for scenario in self.scenarios:
            self.__getattribute__(scenario)(browser, actor, context)

    def main_scenario(self, browser, actor, context):
        preconditions(browser, actor)  # Login as actor
        self.start_up(browser, context)  # Open context
        step_1(browser, context)  # The actor opens edit form
        self.step_2(browser)  # The system displays pst project space edit form
        self.step_3(browser)  # The actor update organization type field and save
        self.step_4(browser, context)  # The system save changes with "Modify changes" info success

    def alternative_scenario_3a(self, browser, actor, context):
        """The actor cancel the form."""
        preconditions(browser, actor)
        self.start_up(browser, context)
        step_1(browser, context)
        self.step_2(browser)
        step_3a(browser)  # The actor cancels the form
        self.step_4a(browser, context)  # The system back to the previous page with "Modification canceled" Info

    def start_up(self, browser, context):
        """Open context."""
        browser.open(context)
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(context.Title().decode('utf8'), heading.text)

    def step_2(self, browser):
        """The system displays pst project space edit form."""
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(u'Editer Espace de projets PST', heading.text)

    def step_3(self, browser):
        """The actor update organization type field and save."""
        form = browser.forms['form']
        fields = form.values
        fields[self.organization_type_form_widget_name] = u"cpas"
        form.find_button_by_label('Sauvegarder').click()

    def step_4(self, browser, context):
        """The system save changes with "Modify changes" info success."""
        heading = browser.css('.documentFirstHeading').first
        # TODO: PRJ-481
        # self.assertEqual(context.Title().decode('utf8'), heading.text)
        # statusmessages.assert_message(u'Modifications sauvegardées')

    def step_4a(self, browser, context):
        """The system back to the previous page with 'Modification canceled' Info."""
        heading = browser.css('.documentFirstHeading').first
        self.assertEqual(context.Title().decode('utf8'), heading.text)
        statusmessages.assert_message(u'Modification annulée')
