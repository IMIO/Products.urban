# -*- coding: utf-8 -*-
from Products.urban import testing

import unittest


class TestBuildLicence(unittest.TestCase):

    layer = testing.URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.portal_urban = portal.portal_urban

    def testGetNotariesEmail(self):
        notaries = self.portal.urban.notaries
        view = notaries.restrictedTraverse('getemails')
        expected_email = 'NotaryName1 NotarySurname1 <maitre.duchnoque@notaire.be>; André Sanfrapper <maitre.andre@notaire.be>'
        generated_email = view.getEmails()
        self.assertEqual(expected_email, generated_email)

    def testGetArchitectsEmail(self):
        architects = self.portal.urban.architects
        view = architects.restrictedTraverse('getemails')
        expected_email = 'Archi1Name Archi1FirstName <Archi1Email>; Archi2Name Archi2FirstName <Archi2Email>; Archi3Name Archi3FirstName <Archi3Email>'
        generated_email = view.getEmails()
        self.assertEqual(expected_email, generated_email)

    def testGetGeometriciansEmail(self):
        geometricians = self.portal.urban.geometricians
        view = geometricians.restrictedTraverse('getemails')
        expected_email = 'GeometricianName1 GeometricianSurname1 <geo.trouvetout@geometre.be>'
        generated_email = view.getEmails()
        self.assertEqual(expected_email, generated_email)
