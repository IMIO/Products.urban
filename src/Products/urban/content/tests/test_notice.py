# -*- coding: utf-8 -*-

from Products.urban.testing import URBAN_TESTS_LICENCES_FUNCTIONAL
from plone.app.testing import login
from zope.globalrequest import getRequest
from zope.globalrequest import setRequest

import unittest


class TestEventNotice(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES_FUNCTIONAL

    def setUp(self):
        portal = self.layer['portal']
        self.portal = portal
        self.buildlicence = portal.urban.envclasstwos.objectValues('EnvClassTwo')[0]
        self.portal_urban = portal.portal_urban
        login(portal, 'urbaneditor')
        if not getRequest():
            setRequest(self.portal.REQUEST)

    def test_create_dpa(self):
        msg = "résultat favorable"
        created_event = self.buildlicence.createUrbanEvent(
            'envoi-demande-FT',
            commentForDPA=msg,
        )
        self.assertEqual(created_event.getCommentForDPA, msg)
