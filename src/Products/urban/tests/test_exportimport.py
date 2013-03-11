# -*- coding: utf-8 -*-
import unittest2 as unittest
from plone.app.testing import setRoles
from plone.app.testing.interfaces import TEST_USER_ID
from plone.app.testing import login
from Products.CMFPlone.utils import base_hasattr
from Products.CMFCore.utils import getToolByName
from Products.urban.Extensions.imports import createStreet
from Products.urban.testing import URBAN_TESTS_PROFILE_INTEGRATION, URBAN_IMPORTS

from StringIO import StringIO
import tarfile


class TestUrbanToolExportImport(unittest.TestCase):

    layer = URBAN_IMPORTS

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        tool = getToolByName(self.portal, 'portal_urban')
        tool_values = {
            'isDecentralized': False,
            'generateSingletonDocuments': True,
            'openOfficePort': 2002,
            'NISNum': '',
            'cityName': '',
            'sqlHost': '',
            'sqlName': '',
            'sqlUser': '',
            'sqlPassword': '',
            'webServerHost': '',
            'pylonsHost': '',
            'mapExtent': '',
            'unoEnabledPython': '',
            'editionOutputFormat': '',
        }
        #fill the tool attrributes with dummy values
        for field_name, value in tool_values.iteritems():
            field = tool.getField(field_name)
            mutator = field.getMutator(tool)
            if value is '':
                value = 'old %s' % field_name
            mutator(value)

        self.portal_urban = tool
        self.portal_setup = getToolByName(self.portal, 'portal_setup')

    def testExport(self):
        """
         Verify correctness of the generic setup export of urban tool attributes
        """
        export = self.portal_setup.runExportStep('urbantool')
        try:
            tar_file = tarfile.open(mode='r', fileobj=StringIO(export['tarball']))
            tar_file.extractall()
            xml = open('portal_urban.xml', 'r')
        except:
            self.fail()
        expected_xml = [
            '<?xml version="1.0"?>\n',
            '<object>\n',
            ' <isDecentralized value="False"/>\n',
            ' <generateSingletonDocuments value="True"/>\n',
            ' <openOfficePort value="2002"/>\n',
            ' <NISNum value="old NISNum"/>\n',
            ' <cityName value="old cityName"/>\n',
            ' <sqlHost value="old sqlHost"/>\n',
            ' <sqlName value="old sqlName"/>\n',
            ' <sqlUser value="old sqlUser"/>\n',
            ' <sqlPassword value="old sqlPassword"/>\n',
            ' <webServerHost value="old webServerHost"/>\n',
            ' <pylonsHost value="old pylonsHost"/>\n',
            ' <mapExtent value="old mapExtent"/>\n',
            ' <unoEnabledPython value="old unoEnabledPython"/>\n',
            ' <editionOutputFormat value="old editionOutputFormat"/>\n',
            '</object>\n'
        ]
        xml_lines = xml.readlines()
        self.failUnless(len(xml_lines) is len(expected_xml))
        self.failUnless(all([expected_xml[i] == line for i, line in enumerate(xml_lines)]))

    def testImports(self):
        """
         Verify correctness of the generic setup import of urban tool attributes
        """
        self.failUnless(self.portal_urban.getNISNum() == 'old NISNum')


class TestStreetImports(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_INTEGRATION

    def setUp(self):
        portal = self.layer['portal']
        self.utool = portal.portal_urban
        self.wtool = portal.portal_workflow
        self.streets = self.utool.streets
        login(portal, 'urbanmanager')

    def testCreateStreet(self):
        ex_streets = {}
        #createStreet(self, city, zipcode, streetcode, streetname, bestAddresskey, startdate, enddate, regionalroad, ex_streets)

        ##create a first street, historical one
        createStreet(self.utool, 'Awans', 4340, '0', "Rue de l'Estampage", 7090730, "2010/09/07", "2011/08/04", '', ex_streets)
        #checking once the city folder creation
        self.failUnless(base_hasattr(self.streets, 'awans'))
        awans = getattr(self.streets, 'awans')
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-lestampage'))
        rue1 = getattr(awans, 'rue-de-lestampage')
        #checking state
        self.assertEquals(self.wtool.getInfoFor(rue1, 'review_state'), 'disabled')
        ##create a second street, new version of the recent one
        createStreet(self.utool, 'Awans', 4340, '1091', "Rue de l'Estampage", 7090730, "2011/08/04", None, '', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-lestampage1'))
        rue2 = getattr(awans, 'rue-de-lestampage1')
        self.assertEquals(self.wtool.getInfoFor(rue2, 'review_state'), 'enabled')
        self.assertEquals(self.wtool.getInfoFor(rue1, 'review_state'), 'disabled')

        ##create the same first street => nothing must be done
        createStreet(self.utool, 'Awans', 4340, '0', "Rue de l'Estampage", 7090730, "2010/09/07", "2011/08/04", '', ex_streets)
        #checking creation
        self.failIf(base_hasattr(awans, 'rue-de-lestampage2'))
        self.assertEquals(len(awans.objectIds()), 2)
        ##create the same second street => nothing must be done
        createStreet(self.utool, 'Awans', 4340, '1091', "Rue de l'Estampage", 7090730, "2011/08/04", None, '', ex_streets)
        #checking creation
        self.failIf(base_hasattr(awans, 'rue-de-lestampage2'))
        self.assertEquals(len(awans.objectIds()), 2)

        ##create a new street, the actual first and after the historical
        createStreet(self.utool, 'Awans', 4340, '1032', "Rue de la Chaudronnerie", 7090729, "2011/08/04", None, '', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-la-chaudronnerie'))
        rue3 = getattr(awans, 'rue-de-la-chaudronnerie')
        self.assertEquals(self.wtool.getInfoFor(rue3, 'review_state'), 'enabled')
        ##create a new street, historical
        createStreet(self.utool, 'Awans', 4340, '0', "Rue de la Chaudronnerie", 7090729, "2010/09/07", "2011/08/04", '', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-la-chaudronnerie1'))
        rue4 = getattr(awans, 'rue-de-la-chaudronnerie1')
        self.assertEquals(self.wtool.getInfoFor(rue4, 'review_state'), 'disabled')
        self.assertEquals(self.wtool.getInfoFor(rue3, 'review_state'), 'enabled')

        ##create a new street, regional road first and after without
        createStreet(self.utool, 'Awans', 4340, '1025', "Rue de Bruxelles", 7020318, "2010/09/07", None, 'N3', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-bruxelles'))
        rue5 = getattr(awans, 'rue-de-bruxelles')
        self.assertEquals(self.wtool.getInfoFor(rue5, 'review_state'), 'enabled')
        ##create a new street, same street name but without regional road
        createStreet(self.utool, 'Awans', 4340, '1025', "Rue de Bruxelles", 7020319, "2010/09/07", None, '', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-bruxelles1'))
        rue6 = getattr(awans, 'rue-de-bruxelles1')
        self.assertEquals(self.wtool.getInfoFor(rue6, 'review_state'), 'enabled')
        self.assertEquals(self.wtool.getInfoFor(rue5, 'review_state'), 'disabled')  # previous street has been disabled

        ##create a new street, without regional road first and after with one
        createStreet(self.utool, 'Awans', 4340, '5000', "Rue de Namur", 7020320, "2010/09/07", None, '', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-namur'))
        rue7 = getattr(awans, 'rue-de-namur')
        self.assertEquals(self.wtool.getInfoFor(rue7, 'review_state'), 'enabled')
        ##create a new street, same street name but with regional road
        createStreet(self.utool, 'Awans', 4340, '5000', "Rue de Namur", 7020321, "2010/09/07", None, 'N4', ex_streets)
        #checking creation
        self.failUnless(base_hasattr(awans, 'rue-de-namur1'))
        rue8 = getattr(awans, 'rue-de-namur1')
        self.assertEquals(self.wtool.getInfoFor(rue8, 'review_state'), 'disabled')
        self.assertEquals(self.wtool.getInfoFor(rue7, 'review_state'), 'enabled')  # previous street is unchanged
