# -*- coding: utf-8 -*-
from DateTime import DateTime
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL
from datetime import datetime
from plone import api
from plone.app.testing import login
from zope.event import notify
from zope.i18n import translate
from zope.lifecycleevent import ObjectModifiedEvent

import unittest2 as unittest


class TestUrbanVocabularyTerm(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    # self.portal_urban.urbancertificateone.basement.values()[0].__dict__

    def setUp(self):
        portal = self.layer["portal"]
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        self.urbancertificateones = urban.urbancertificateones
        default_user = self.layer.default_user
        login(portal, default_user)
        event_config = self.portal_urban.urbancertificateone.eventconfigs["depot-de-la-demande"]

        self.certificate = api.content.create(
            type="UrbanCertificateOne",
            container=self.urbancertificateones,
            id="licence1",
        )
        self.certificate.creation_date = DateTime(2024, 3, 30)
        event = self.certificate.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 3, 31))

        self.certificate_2 = api.content.create(
            type="UrbanCertificateOne",
            container=self.urbancertificateones,
            id="licence2",
        )
        self.certificate_2.creation_date = DateTime(2024, 4, 1)
        event = self.certificate_2.createUrbanEvent(event_config)
        event.setEventDate(datetime(2024, 4, 1))

        # set language to 'fr' as we do some translations above
        ltool = portal.portal_languages
        defaultLanguage = "fr"
        supportedLanguages = ["en", "fr"]
        ltool.manage_setLanguageSettings(
            defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False
        )
        # this needs to be done in tests for the language to be taken into account...
        ltool.setLanguageBindings()

        # Set validity dates
        self._zip_3 = self.portal_urban.urbancertificateone.zip.values()[2]
        self._zip_3.setEndValidity(DateTime(2024, 3, 31))
        self._zip_4 = self.portal_urban.urbancertificateone.zip.values()[3]
        self._zip_4.setStartValidity(DateTime(2024, 4, 1))
        notify(ObjectModifiedEvent(self._zip_4))

    def tearDown(self):
        api.content.delete(self.certificate)
        api.content.delete(self.certificate_2)
        self._zip_3.setEndValidity(None)
        self._zip_4.setEndValidity(None)
        notify(ObjectModifiedEvent(self._zip_4))

    def testGetRenderedDescription(self):
        """
        Test that rendered description works
        """
        # take an existing UrbanVocabularyTerm
        # Description in setuphandlers is :
        # <p>est situé en [[object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>
        expected = "<p>est situé en zone d'habitat au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        # use the new UrbanVocabularyTerm
        self.certificate.setFolderZone(("zh",))
        uvt = getattr(
            self.portal_urban.urbancertificateone.specificfeatures, "situe-en-zone"
        )
        # the expression is valid, it should render as expected...
        self.assertEqual(uvt.getRenderedDescription(self.certificate), expected)

        # now change the description and remove a leading '['
        newDescription = "<p>est situé en [object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype="text/html")
        expected = "<p>est situé en [object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        # nothing rendered, the result is equal to the new description as no expression is detected...
        self.assertEqual(uvt.getRenderedDescription(self.certificate), newDescription)
        self.assertEqual(uvt.getRenderedDescription(self.certificate), expected)

        # now correctly define a wrong expression ;-)
        newDescription = "<p>est situé en [[object.getTralala()]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype="text/html")
        expected = u"<p>est situé en %s au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>" % translate(
            "error_in_expr_contact_admin",
            domain="urban",
            mapping={"expr": "[[object.getTralala()]]"},
            context=self.certificate.REQUEST,
        )
        # a error message is rendered...
        self.assertEqual(
            uvt.getRenderedDescription(self.certificate), expected.encode("utf-8")
        )

        # we can also specify that we want the expressions to be replaced by a "null" value, aka "..."
        newDescription = "<p>est situé en [[object.getTralala()]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype="text/html")
        expected = "<p>est situé en ... au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        # expressions are replaced by the null value, aka "..."
        self.assertEqual(
            uvt.getRenderedDescription(self.certificate, renderToNull=True), expected
        )

    def test_get_raw_voc_creation(self):
        """Ensure that values are correctly returned based on creation date"""
        vocabulary = UrbanVocabulary("zip")
        terms = vocabulary.get_raw_voc(
            self.urbancertificateones,
            licence_type="UrbanCertificateOne",
        )
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-4"], [t["id"] for t in terms])

    def test_get_raw_voc_deposit(self):
        """Ensure that values are correctly returned based on deposit date"""
        vocabulary = UrbanVocabulary("zip")

        terms = vocabulary.get_raw_voc(self.certificate)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-3"], [t["id"] for t in terms])

        terms = vocabulary.get_raw_voc(self.certificate_2)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-4"], [t["id"] for t in terms])

    def test_getDisplayListForTemplate_deposit(self):
        """Ensure that values are correctly returned based on deposit date"""
        # XXX Not working ATM but maybe this function need to be removed
        vocabulary = UrbanVocabulary("zip")
        display_list = vocabulary.getDisplayListForTemplate(self.certificate)
        self.assertEqual(3, len(display_list))
        self.assertEqual(["type-1", "type-2", "type-3"], display_list.keys())

        display_list = vocabulary.getDisplayListForTemplate(self.certificate_2)
        self.assertEqual(3, len(display_list))
        self.assertEqual(["type-1", "type-2", "type-4"], display_list.keys())

    def test_getAllVocTerms_deposit(self):
        """Ensure that values are correctly returned based on deposit date"""
        vocabulary = UrbanVocabulary("zip")
        terms = vocabulary.getAllVocTerms(self.certificate)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-3"], sorted(terms.keys()))

        terms = vocabulary.getAllVocTerms(self.certificate_2)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-4"], sorted(terms.keys()))

    def test_listAllVocTerms_deposit(self):
        """Ensure that values are correctly returned based on deposit date"""
        vocabulary = UrbanVocabulary("zip")
        terms = vocabulary.listAllVocTerms(self.certificate)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-3"], [t.id for t in terms])

        terms = vocabulary.listAllVocTerms(self.certificate_2)
        self.assertEqual(3, len(terms))
        self.assertEqual(["type-1", "type-2", "type-4"], [t.id for t in terms])