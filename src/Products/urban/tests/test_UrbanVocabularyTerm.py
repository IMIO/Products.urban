# -*- coding: utf-8 -*-
import unittest2 as unittest
from zope.i18n import translate
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_CONFIG_FUNCTIONAL


class TestUrbanVocabularyTerm(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        self.urbancertificateones = urban.urbancertificateones
        LICENCE_ID = 'licence1'
        default_user = self.layer.default_user
        login(portal, default_user)
        self.urbancertificateones.invokeFactory('UrbanCertificateOne', LICENCE_ID)
        self.certificate = getattr(self.urbancertificateones, LICENCE_ID)
        #set language to 'fr' as we do some translations above
        ltool = portal.portal_languages
        defaultLanguage = 'fr'
        supportedLanguages = ['en', 'fr']
        ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages, setUseCombinedLanguageCodes=False)
        #this needs to be done in tests for the language to be taken into account...
        ltool.setLanguageBindings()

    def testGetRenderedDescription(self):
        """
          Test that rendered description works
        """
        #take an existing UrbanVocabularyTerm
        #Description in setuphandlers is :
        #<p>est situé en [[object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>
        expected = "<p>est situé en zone d'habitat au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        #use the new UrbanVocabularyTerm
        self.certificate.setFolderZone(('zh',))
        uvt = getattr(self.portal_urban.urbancertificateone.specificfeatures, 'situe-en-zone')
        #the expression is valid, it should render as expected...
        self.assertEqual(uvt.getRenderedDescription(self.certificate), expected)

        #now change the description and remove a leading '['
        newDescription = "<p>est situé en [object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype='text/html')
        expected = "<p>est situé en [object.getValueForTemplate('folderZone')]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        #nothing rendered, the result is equal to the new description as no expression is detected...
        self.assertEqual(uvt.getRenderedDescription(self.certificate), newDescription)
        self.assertEqual(uvt.getRenderedDescription(self.certificate), expected)

        #now correctly define a wrong expression ;-)
        newDescription = "<p>est situé en [[object.getTralala()]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype='text/html')
        expected = u"<p>est situé en %s au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>" \
                   % translate('error_in_expr_contact_admin', domain='urban', mapping={'expr': '[[object.getTralala()]]'}, context=self.certificate.REQUEST)
        #a error message is rendered...
        self.assertEqual(uvt.getRenderedDescription(self.certificate), expected.encode('utf-8'))

        #we can also specify that we want the expressions to be replaced by a "null" value, aka "..."
        newDescription = "<p>est situé en [[object.getTralala()]] au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        uvt.setDescription(newDescription, mimetype='text/html')
        expected = "<p>est situé en ... au plan de secteur de NAMUR adopté par Arrêté Ministériel du 14 mai 1986 et qui n'a pas cessé de produire ses effets pour le bien précité;</p>"
        #expressions are replaced by the null value, aka "..."
        self.assertEqual(uvt.getRenderedDescription(self.certificate, renderToNull=True), expected)
