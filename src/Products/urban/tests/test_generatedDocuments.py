# -*- coding: utf-8 -*-
import unittest
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL
from Products.urban.scripts.odtsearch import searchInTextElements
import zipfile
import xml.dom.minidom

class TestDocuments(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal_urban = portal.portal_urban
        urban = portal.urban
        login(portal, 'urbaneditor')

    def testAppyErrorsInDocuments(self):

        site = self.layer['portal']
        available_licence_types = {
            'BuildLicence':{
            },
            'Declaration':{
            },
            'Division':{
            },
            'UrbanCertificateOne':{
            },
            'UrbanCertificateTwo':{
            },
            'NotaryLetter':{
            },
            'MiscDemand':{
            },
        }
        log = []
        #parcourir tous les dossiers de permis
        for licence_type in available_licence_types.keys():
            #trouver chaque permis d'exemple
            licence_folder = getattr(site.urban, "%ss" % licence_type.lower())
            test_licence = licence_folder.listFolderContents()[0]
            #parcourir chaque event
            for event in test_licence.listFolderContents({'portal_type':'UrbanEvent'}):
                #parcourir chaque doc généré de chaque event
                for document in event.listFolderContents({'portal_type':'UrbanDoc'}):
                    odt_file = document.getFile().blob.open()
                    raw_xml = zipfile.ZipFile(odt_file, 'r').open('content.xml')
                    xml_tree = xml.dom.minidom.parseString(raw_xml.read())
                    #on ouvre le document et cherche pour des annotations contenant les messages d'erreurs
                    annotations = [node.getElementsByTagName('text:p') for node in xml_tree.getElementsByTagName('office:annotation')]
                    if annotations:
                        #stocker les logs d'erreurs trouvées
                        result = searchInTextElements(annotations, document.getFilename(), 'commentaire', ["^(Error|Action).*$"], verbosity=-1)
                        log.append([result, test_licence.Title(), event.Title(), document.Title()])
        #afficher toutes les erreurs trouvées (type de procédure->event->nom du doc->erreurs)
        if log:
            print '\n'
            for line in log:
                print "%i error(s) in %s => event: %s => document: %s" % (len(line[0]), line[1], line[2], line[3])
        self.assertEquals(len(log), 0)

