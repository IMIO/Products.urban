# -*- coding: utf-8 -*-

from Acquisition import aq_base

from zope.lifecycleevent import ObjectCreatedEvent
from Products.CMFCore.utils import getToolByName
from Products.urban.testing import URBAN_TESTS_PROFILE_FUNCTIONAL, URBAN_TESTS_LICENCES

from plone.app.testing import login
from plone import api

from zope import event

import unittest


class TestOpinionRequest(unittest.TestCase):

    layer = URBAN_TESTS_PROFILE_FUNCTIONAL

    def setUp(self):
        portal = self.layer["portal"]
        self.portal_urban = portal.portal_urban

    def testCreateOpinionRequestEventType(self):
        tool = self.portal_urban
        urbaneventtypes_folder = tool.buildlicence.urbaneventtypes
        with api.env.adopt_roles(["Manager"]):
            term_id = urbaneventtypes_folder.invokeFactory(
                "OpinionRequestEventType",
                id="voodoo",
                title="Vood00",
                description="gni",
            )
        term = getattr(
            urbaneventtypes_folder, term_id, "NOT FOUND RHAAAAAAAAAAAAAAAAAAAAAA!!!!"
        )
        self.failUnless(term in urbaneventtypes_folder.objectValues())


class TestOpinionRequestOnLicence(unittest.TestCase):

    layer = URBAN_TESTS_LICENCES

    def setUp(self):
        portal = self.layer["portal"]
        self.licence = portal.urban.buildlicences.objectValues("BuildLicence")[0]
        login(portal, "urbanmanager")

    def testNewOpinioneventtypeAppearsInFieldVocabulary(self):
        # when adding a new OpinionRequestEventType, its extraValue shouldbe
        # used as the display value in the vocabulary of solicitOpinions field
        # of buildlicences
        tool = getToolByName(self.licence, "portal_urban")
        urbaneventtypes_folder = tool.buildlicence.urbaneventtypes

        with api.env.adopt_roles(["Manager"]):
            term_id = urbaneventtypes_folder.invokeFactory(
                "OpinionRequestEventType",
                id="voodoo",
                title="Demande d'avis (Vood00)",
                extraValue="Vood00",
            )
            voc_cache = tool.restrictedTraverse("urban_vocabulary_cache")
            voc_cache.update_procedure_all_vocabulary_cache(tool.buildlicence)
        term = getattr(tool.buildlicence.urbaneventtypes, term_id)
        expected_voc_term = (term_id, term.getExtraValue())

        solicitOpinions_field = self.licence.getField("solicitOpinionsTo")
        field_voc = solicitOpinions_field.vocabulary.getDisplayList(self.licence)

        self.failUnless(expected_voc_term in field_voc.items())

    def testInquiryWithOpinionRequestIsLinkedToItsUrbanEventOpinionRequest(self):
        # if there is an inquiry with an opinion request and that its corresponding UrbanEventOpinionRequest
        # is added, a link should be created between this inquiry and this UrbanEventOpinionRequest

        licence = self.licence
        UrbanEventOpinionRequest = None
        for content in licence.objectValues():
            if content.portal_type == "UrbanEventOpinionRequest":
                UrbanEventOpinionRequest = content
                aq_base(UrbanEventOpinionRequest)._at_creation_flag = True
                break
        event.notify(ObjectCreatedEvent(UrbanEventOpinionRequest))
        self.failUnless(
            licence.getLinkedUrbanEventOpinionRequest("belgacom")
            == UrbanEventOpinionRequest
        )
