# -*- coding: utf-8 -*-
#
# File: Inquiry.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

from Acquisition import aq_parent
from Acquisition import aq_inner
from AccessControl import ClassSecurityInfo
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban import UrbanMessage as _
from Products.urban.utils import WIDGET_DATE_END_YEAR
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from zope.i18n import translate
from OFS.ObjectManager import BeforeDeleteException
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IGenericLicence
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
from Products.urban.widget.select2widget import Select2Widget
from plone import api
from DateTime import DateTime

schema = Schema(
    (
        LinesField(
            name="solicitOpinionsTo",
            widget=Select2Widget(
                label=_("urban_label_solicitOpinionsTo", default="Solicit opinion to"),
                multiple=True,
            ),
            schemata="urban_advices",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "eventconfigs",
                vocType="OpinionEventConfig",
                value_to_use="abbreviation",
            ),
            default_method="getDefaultValue",
        ),
        LinesField(
            name="solicitOpinionsToOptional",
            widget=Select2Widget(
                label=_(
                    "urban_label_solicitOpinionsToOptional",
                    default="Solicitopinionstooptional",
                ),
                multiple=True,
            ),
            schemata="urban_advices",
            multiValued=1,
            vocabulary=UrbanVocabulary(
                "eventconfigs",
                vocType="OpinionEventConfig",
                value_to_use="abbreviation",
            ),
            default_method="getDefaultValue",
        ),
        IntegerField(
            name="opinion_round",
            widget=IntegerWidget(),
            schemata="urban_advices",
        ),
    ))

RequestForOpinion_schema = BaseSchema.copy() + schema.copy()

RequestForOpinion_schema["title"].widget.visible = False
RequestForOpinion_schema["opinion_round"].widget.visible = False

del RequestForOpinion_schema["description"]


class RequestForOpinion(BaseContent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IRequestForOpinion)

    meta_type = "RequestForOpinion"
    _at_rename_after_creation = True

    schema = RequestForOpinion_schema

    security.declarePublic("getDefaultValue")

    def getDefaultValue(self, context=None, field=None):
        if not context or not field:
            return [""]

        empty_value = getattr(field, "multivalued", "") and [] or ""
        if hasattr(field, "vocabulary") and isinstance(
            field.vocabulary, UrbanVocabulary
        ):
            return field.vocabulary.get_default_values(context)
        return empty_value
    
    def getRequestForOpinion(self):
        return self._get_request_for_opinion_objs()

    def getAllRequestForOpinion(self):
        return self._get_request_for_opinion_objs(all_=True)

    def getLastRequestForOpinion(self):
        return self._get_request_for_opinion_objs(all_=True)[-1]

    def getLinkedUrbanEventOpinionRequest(self, organisation):
        """
        Return the linked UrbanEventOpinionRequest objects if exist
        """
        brefs = self.getBRefs("linkedInquiry")
        if brefs:
            # linkedInquiry may come from a UrbanEventInquiry or an UrbanEventOpinionRequest
            for bref in brefs:
                if bref and bref.portal_type == "UrbanEventOpinionRequest":
                    if (
                        bref.getLinkedOrganisationTermId() == organisation
                        and bref.getLinkedInquiry() == self
                    ):
                        return bref
        return None

    def get_all_linked_urban_event_opinion_request(self):
        opinion_requests = [
            op
            for op in self.getAllEvents(interfaces.IOpinionRequestEvent)
            if op.portal_type == "UrbanEventOpinionRequest"
            and op.getLinkedInquiry() == self
        ]
        return opinion_requests

    def getSolicitOpinionValue(self, opinionId):
        """
        Return the corresponding opinion value from the given opinionId
        """
        vocabulary = self.getField("solicitOpinionsTo").vocabulary
        title = [
            v["title"] for v in vocabulary.get_raw_voc(self) if v["id"] == opinionId
        ]
        title = title and title[0] or ""
        return title

    def _get_request_for_opinion_objs(self, all_=False, portal_type="RequestForOpinion"):
        """
        Returns the existing request for opinion
        """
        all_request_for_opinion = []
        other_request_for_opinion = self.objectValues(portal_type)
        if all_ or other_request_for_opinion:
            all_request_for_opinion.append(self)
        all_request_for_opinion.extend(list(other_request_for_opinion))
        return all_request_for_opinion

    security.declarePublic("mayAddOpinionRequestEvent")

    def mayAddOpinionRequestEvent(self, organisation):
        """
        This is used as TALExpression for the UrbanEventOpinionRequest
        We may add an OpinionRequest if we asked one in an inquiry on the licence
        We may add another if another inquiry defined on the licence ask for it and so on
        """
        opinions = self.getSolicitOpinionsTo()
        opinions += self.getSolicitOpinionsToOptional()
        limit = organisation in opinions and 1 or 0
        requests_for_opinion = [req for req in self.getRequestForOpinion() if req != self]
        for request in requests_for_opinion:
            if (
                organisation in request.getSolicitOpinionsTo()
                or organisation in request.getSolicitOpinionsToOptional()
            ):
                limit += 1
        limit = limit - len(self.getOpinionRequests(organisation))
        return limit > 0
    
    def get_opinion_round_index_display(self):
        context = aq_inner(self)
        index = "(1er tour)"
        if context.portal_type == "RequestForOpinion":
            index = "({}e tour)".format(context.getOpinion_round())
        return str(index)

    security.declarePublic("generateInquiryTitle")

    def generateInquiryTitle(self):
        """
        Generates a title for the inquiry
        """
        # we need to generate the title as the number of the inquiry is into it
        round = self.get_opinion_round_index_display()
        return translate(
            "request_title_and_number",
            "urban",
            mapping={"round": round},
            context=self.REQUEST,
        )

    def get_title(self):
        title = self.title
        if interfaces.IGenericLicence.providedBy(self):
            title = translate(
                "request_title_and_number",
                "urban",
                mapping={"round": "(1er tour)"},
                context=self.REQUEST,
            )
        return title

    def getLastOpinionRequest(self):
        return self.getLastEvent(interfaces.IOpinionRequestEvent)

    security.declarePublic("getSolicitOpinionValue")

    def getSolicitOpinionValue(self, opinionId):
        """
        Return the corresponding opinion value from the given opinionId
        """
        vocabulary = self.getField("solicitOpinionsTo").vocabulary
        title = [
            v["title"] for v in vocabulary.get_raw_voc(self) if v["id"] == opinionId
        ]
        title = title and title[0] or ""
        return title

    security.declarePublic("getSolicitOpinionOptionalValue")

    def getSolicitOpinionOptionalValue(self, opinionId):
        """
        Return the corresponding opinion value from the given opinionId
        """
        vocabulary = self.getField("solicitOpinionsToOptional").vocabulary
        title = [
            v["title"] for v in vocabulary.get_raw_voc(self) if v["id"] == opinionId
        ]
        title = title and title[0] or ""
        return title

    def getAllOpinionRequests(self, organisation=""):
        if not organisation:
            return self.getAllEvents(interfaces.IOpinionRequestEvent)
        opinion_requests = [
            op
            for op in self.getAllEvents(interfaces.IOpinionRequestEvent)
            if organisation in op.id
        ]
        return opinion_requests

    def getAllLinkedOpinionRequests(self):
        opinion_requests = [
            op
            for op in self.getAllEvents(interfaces.IOpinionRequestEvent)
            if op.portal_type == "UrbanEventOpinionRequest"
            and op.getLinkedInquiry() == self
        ]
        return opinion_requests

    def getAllOpinionRequestsNoDup(self):
        allOpinions = self.getAllOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor] = opinion
        return allOpinionsNoDup.values()


registerType(RequestForOpinion, PROJECTNAME)
