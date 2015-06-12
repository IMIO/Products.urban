# -*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_TESTS_LICENCES
from Products.urban.scripts.odtsearch import searchInTextElements
import cgi
import zipfile
import xml.dom.minidom
import psycopg2


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

        portal_urban = portal.portal_urban

        #set the connection to the test cadatsral DB
        portal_urban.setSqlHost('localhost')
        portal_urban.setSqlName('urb_fleron')
        portal_urban.setSqlUser('urb_fleron')
        portal_urban.setSqlPassword('urb_fleron')
        self.portal_urban = portal_urban

        # set the test parcel division
        parcel = self.buildlicence.getParcels()[0]
        self.division = str(portal_urban.findDivisions(all=False)[0]['da'])
        parcel.setDivision(self.division)
        self.parcel = parcel

        login(portal, 'urbaneditor')

    def testDBConnection(self):
        """
         We should at least have a connection to a test DB in order
         to run the remaining tests correctly
        """
        connection = self.portal_urban.getDBConnection()
        self.failUnless(type(connection) == psycopg2._psycopg.connection)

    def testNoDivisionRenaming(self):
        licence = self.buildlicence
        division = self.division
        portal_urban = self.portal_urban

        expected_division_name = [line['name'] for line in portal_urban.getDivisionsRenaming() if line['division'] == division]
        expected_division_name = expected_division_name[0]

        self.failUnless(expected_division_name in licence.getPortionOutsText())

    def testDivisionRenaming(self):
        licence = self.buildlicence
        division = self.division
        portal_urban = self.portal_urban

        alternative_name = 'bla'
        # so far we did not configure anything
        self.failIf(alternative_name in licence.getPortionOutsText())

        # configure an alternative name for the division
        new_config = list(portal_urban.getDivisionsRenaming())
        for line in new_config:
            if line['division'] == division:
                line['alternative_name'] = alternative_name
                break
        portal_urban.setDivisionsRenaming(new_config)

        self.failUnless(alternative_name in licence.getPortionOutsText())


class TestInvertNamesOfMailAddress(unittest.TestCase):
    """
     Names inversion in contact signaletic should occurs only if the option is set and only
     when we call the signaletic line by line (case where its used in the mail address)
    """

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.buildlicences.objectValues()[0]
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
            # for a 'classic' signaletic, name order should not change
            expected_name = '%s %s' % (contact.getName1(), contact.getName2())
            self.failUnless(expected_name in contact.getSignaletic())

            # but names should be inverted for the linebyline signaletic used in mailing address
            expected_name = '%s %s' % (contact.getName2(), contact.getName1())
            expected_name = cgi.escape(expected_name)
            self.failUnless(expected_name in contact.getSignaletic(linebyline=True))


class TestDocuments(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')

    def testAppyErrorsInDocuments(self):

        site = self.layer['portal']
        available_licence_types = [
            'BuildLicence',
            'Declaration',
            'Division',
            'UrbanCertificateOne',
            'UrbanCertificateTwo',
            'NotaryLetter',
            'MiscDemand',
        ]
        log = []
        #parcourir tous les dossiers de permis
        for licence_type in available_licence_types:
            #trouver chaque permis d'exemple
            licence_folder = getattr(site.urban, "%ss" % licence_type.lower())
            test_licence = licence_folder.listFolderContents()[0]
            #parcourir chaque event
            for event in test_licence.listFolderContents({'portal_type': 'UrbanEvent'}):
                #parcourir chaque doc généré de chaque event
                for document in event.listFolderContents({'portal_type': 'UrbanDoc'}):
                    odt_file = document.getFile().blob.open()
                    raw_xml = zipfile.ZipFile(odt_file, 'r').open('content.xml')
                    xml_tree = xml.dom.minidom.parseString(raw_xml.read())
                    #on ouvre le document et cherche pour des annotations contenant les messages d'erreurs
                    annotations = [node.getElementsByTagName('text:p') for node in xml_tree.getElementsByTagName('office:annotation')]
                    if annotations:
                        #stocker les logs d'erreurs trouvées
                        result = searchInTextElements(annotations, document.getFilename(), 'commentaire', ["^(Error|Action).*$"])
                        log.append([result, test_licence.Title(), event.Title(), document.Title()])
        #afficher toutes les erreurs trouvées (type de procédure->event->nom du doc->erreurs)
        if log:
            print '\n'
            for line in log:
                print "%i error(s) in %s => event: %s => document: %s" % (len(line[0]), line[1], line[2], line[3])
        self.assertEquals(len(log), 0)
