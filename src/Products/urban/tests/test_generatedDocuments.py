# -*- coding: utf-8 -*-

from plone.app.testing import login
from Products.urban.profiles.testsWithLicences.licences_data import licences_data
from Products.urban.testing import URBAN_TESTS_LICENCES
from Products.urban.scripts.odtsearch import searchInTextElements

import cgi
import unittest
import xml.dom.minidom
import zipfile


class TestDivisionsRenaming(unittest.TestCase):
    """
     Names inversion in contact signaletic should occurs only if the option is set and only
     when we call the signaletic line by line (case where its used in the mail address)
    """

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues()[-1]
        self.helper_view = self.buildlicence.unrestrictedTraverse('document_generation_helper_view')
        self.document_proxy_licence = self.helper_view.context
        self.portal_urban = portal.portal_urban

        # set dummy divisions
        divisions = ['MyDivision', 'SecondDivision']
        rows = []
        for division in divisions:
            row = {
                'division': division.lower(),
                'name': division,
                'alternative_name': division
            }
            rows.append(row)
        self.portal_urban.setDivisionsRenaming(rows)

        # set the test parcel division
        parcel = self.buildlicence.getParcels()[0]
        self.division = 'mydivision'
        parcel.division = self.division
        self.parcel = parcel

        login(portal, 'urbaneditor')

    def testNoDivisionRenaming(self):
        division = self.division
        portal_urban = self.portal_urban

        expected_division_name = [line['name'] for line in portal_urban.getDivisionsRenaming() if line['division'] == division]
        expected_division_name = expected_division_name[0]

        self.failUnless(expected_division_name in self.document_proxy_licence.getPortionOutsText())

    def testDivisionRenaming(self):
        division = self.division
        portal_urban = self.portal_urban

        alternative_name = 'bla'
        # so far we did not configure anything
        self.failIf(alternative_name in self.document_proxy_licence.getPortionOutsText())

        # configure an alternative name for the division
        new_config = list(portal_urban.getDivisionsRenaming())
        for line in new_config:
            if line['division'] == division:
                line['alternative_name'] = alternative_name
                break
        portal_urban.setDivisionsRenaming(new_config)
        self.failUnless(alternative_name in self.document_proxy_licence.getPortionOutsText())


class TestInvertNamesOfMailAddress(unittest.TestCase):
    """
     Names inversion in contact signaletic should occurs only if the option is set and only
     when we call the signaletic line by line (case where its used in the mail address)
    """

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues('BuildLicence')[0]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testNameNotInvertedForAddressMailing(self):
        contacts = self.buildlicence.getApplicants()
        for contact in contacts:
            # by default, should be name1 followed by name 2 in all cases
            expected_name = '%s %s' % (contact.getName1(), contact.getName2())
            self.failUnless(expected_name in contact.getSignaletic())
            expected_name = cgi.escape(expected_name)
            self.failUnless(expected_name in contact.getSignaletic(linebyline=True))

    def testNameInvertedForAddressMailing(self):

        # we set the name inversion to True
        self.portal_urban.setInvertAddressNames(True)

        contacts = self.buildlicence.getApplicants()
        for contact in contacts:
            # names should be inverted for the linebyline signaletic used in mailing address
            expected_name = '%s %s' % (contact.getName2(), contact.getName1())
            expected_name = cgi.escape(expected_name)
            self.failUnless(expected_name in contact.getSignaletic(linebyline=True))


class TestDocuments(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testAppyErrorsInDocuments(self):

        site = self.layer['portal']
        available_licence_types = licences_data.keys()
        log = []
        # parcourir tous les dossiers de permis
        for licence_type in available_licence_types:
            # trouver chaque permis d'exemple
            licence_folder = getattr(site.urban, "%ss" % licence_type.lower())
            test_licence = licence_folder.listFolderContents()[0]
            # parcourir chaque event
            for event in test_licence.listFolderContents({'portal_type': 'UrbanEvent'}):
                # parcourir chaque doc généré de chaque event
                for document in event.listFolderContents({'portal_type': 'UrbanDoc'}):
                    odt_file = document.getFile().blob.open()
                    raw_xml = zipfile.ZipFile(odt_file, 'r').open('content.xml')
                    xml_tree = xml.dom.minidom.parseString(raw_xml.read())
                    # on ouvre le document et cherche pour des annotations contenant les messages d'erreurs
                    annotations = [node.getElementsByTagName('text:p') for node in xml_tree.getElementsByTagName('office:annotation')]
                    if annotations:
                        # stocker les logs d'erreurs trouvées
                        result = searchInTextElements(annotations, document.getFilename(), 'commentaire', ["^(Error|Action).*$"])
                        log.append([result, test_licence.Title(), event.Title(), document.Title()])
        # afficher toutes les erreurs trouvées (type de procédure->event->nom du doc->erreurs)
        if log:
            print '\n'
            for line in log:
                print "%i error(s) in %s => event: %s => document: %s" % (len(line[0]), line[1], line[2], line[3])
        self.assertEquals(len(log), 0)


class TestPortionOutTextFormat(unittest.TestCase):
    """
     Names inversion in contact signaletic should occurs only if the option is set and only
     when we call the signaletic line by line (case where its used in the mail address)
    """

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.buildlicence = portal.urban.buildlicences.objectValues()[-1]
        self.helper_view = self.buildlicence.unrestrictedTraverse('document_generation_helper_view')
        self.document_proxy_licence = self.helper_view.context
        login(portal, 'urbaneditor')

    def testPortionOutsTextOutputFormat(self):
        # test getPortionOutsText helper view method output format
        # simple parcel
        self.buildlicence.invokeFactory(
            'Parcel',
            'test_parcel',
            division='62006',
            section='A',
            radical='86',
            exposant='C'
        )
        # parcel = self.document_proxy_licence.getParcels()[-1]
        self.failUnless(self.document_proxy_licence.getPortionOutsText().encode('utf-8').endswith("86 C"))
        # parcel with bis
        self.buildlicence.invokeFactory(
            'Parcel',
            'test_parcel2',
            division='62006',
            section='A',
            radical='87',
            bis='2',
            exposant='D'
        )
        self.failUnless(self.document_proxy_licence.getPortionOutsText().encode('utf-8').endswith("86 C,  87/2 D"))
        # parcel with bis and puissance
        self.buildlicence.invokeFactory(
            'Parcel',
            'test_parcel3',
            division='62006',
            section='A',
            radical='88',
            bis='3',
            exposant='E',
            puissance='4'
        )
        self.failUnless(self.document_proxy_licence.getPortionOutsText().encode('utf-8').endswith("86 C,  87/2 D,  88/3 E 4"))
        # parcel with puissance only
        self.buildlicence.invokeFactory(
            'Parcel',
            'test_parcel4',
            division='62006',
            section='A',
            radical='89',
            exposant='F',
            puissance='5'
        )
        self.failUnless(self.document_proxy_licence.getPortionOutsText().encode('utf-8').endswith("86 C,  87/2 D,  88/3 E 4,  89 F 5"))


class TestGetParcels(unittest.TestCase):
    """
     Test get_parcels output text
    """

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        login(portal, 'urbaneditor')
        portal.urban.buildlicences.invokeFactory('BuildLicence', 'buildlicence1')
        self.buildlicence = portal.urban.buildlicences.objectValues()[-1]
        self.helper_view = self.buildlicence.unrestrictedTraverse('document_generation_helper_view')

    def testGetParcelsEmptyBisPuissanceValues(self):
        # test get_parcels output text with no bis & puissance
        self.buildlicence.invokeFactory(
            'Parcel',
            'test_parcel5',
            division='62006',
            section='A',
            radical='86',
            exposant='C'
        )
        self.assertTrue(self.helper_view.get_parcels().endswith(u"section A n\xb0 86C"))
