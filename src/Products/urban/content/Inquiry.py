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

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = "plaintext"

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

optional_fields = [
    "derogationDetails",
    "investigationDetails",
    "investigationReasons",
    "investigationArticlesText",
    "investigationArticles",
    "demandDisplay",
    "derogation",
    "derogationDetails",
    "roadModificationSubject",
]
##/code-section module-header

schema = Schema(
    (
        StringField(
            name="investigation_radius",
            widget=SelectionWidget(
                label=_("urban_label_investigation_radius", default="Investigation_radius"),
            ),
            vocabulary=UrbanVocabulary("investigations_radius", inUrbanConfig=False),
            default_method="getDefaultValue",
            schemata="urban_inquiry"
        ),
        LinesField(
            name="derogation",
            widget=MultiSelect2Widget(
                format="checkbox",
                label=_("urban_label_derogation", default="Derogation"),
            ),
            multiValued=1,
            vocabulary=UrbanVocabulary("derogations"),
            default_method="getDefaultValue",
            schemata="urban_inquiry",
        ),
        TextField(
            name="derogationDetails",
            allowable_content_types=("text/plain",),
            widget=TextAreaWidget(
                label=_("urban_label_derogationDetails", default="Derogationdetails"),
            ),
            default_output_type="text/plain",
            default_content_type="text/plain",
            default_method="getDefaultText",
            schemata="urban_inquiry",
        ),
        LinesField(
            name="investigationArticles",
            widget=MultiSelect2Widget(
                size=10,
                label=_(
                    "urban_label_investigationArticles", default="Investigationarticles"
                ),
            ),
            multiValued=True,
            vocabulary=UrbanVocabulary("investigationarticles"),
            default_method="getDefaultValue",
            schemata="urban_inquiry",
        ),
        TextField(
            name="investigationArticlesText",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_investigationArticlesText",
                    default="Investigationarticlestext",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            schemata="urban_inquiry",
        ),
        DateTimeField(
            name="demandDisplay",
            widget=DateTimeField._properties["widget"](
                show_hm=False,
                format="%d/%m/%Y",
                starting_year=1930,
                ending_year=WIDGET_DATE_END_YEAR,
                label=_("urban_label_demandDisplay", default="Demanddisplay"),
            ),
            schemata="urban_inquiry",
        ),
        TextField(
            name="investigationDetails",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_investigationDetails", default="Investigationdetails"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            schemata="urban_inquiry",
        ),
        TextField(
            name="investigationReasons",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_investigationReasons", default="Investigationreasons"
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            schemata="urban_inquiry",
        ),
        TextField(
            name="roadModificationSubject",
            allowable_content_types=("text/html",),
            widget=RichWidget(
                label=_(
                    "urban_label_roadModificationSubject",
                    default="Roadmodificationsubject",
                ),
            ),
            default_content_type="text/html",
            default_method="getDefaultText",
            default_output_type="text/x-html-safe",
            schemata="urban_inquiry",
        ),
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
    ),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

Inquiry_schema = BaseSchema.copy() + schema.copy()

##code-section after-schema #fill in your manual code here
Inquiry_schema["title"].widget.visible = False
# implicitly rmove the not used description field because it is defined with default
# values that are wrong for BuildLicence that heritates from self and GenericLicence
# GenericLicence redefines 'description' and self too...  See ticket #3502
del Inquiry_schema["description"]
##/code-section after-schema


class Inquiry(BaseContent, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.IInquiry)

    meta_type = "Inquiry"
    _at_rename_after_creation = True

    schema = Inquiry_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

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

    security.declarePublic("getDefaultText")

    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = getToolByName(self, "portal_urban")
        return urban_tool.getTextDefaultValue(field.getName(), context, html=html)

    security.declarePrivate("manage_beforeDelete")

    def manage_beforeDelete(self, item, container):
        """
        We can not remove an Inquiry if a linked UrbanEventInquiry exists
        """
        linkedUrbanEventInquiry = self.getLinkedUrbanEventInquiry()
        if linkedUrbanEventInquiry:
            raise BeforeDeleteException, "cannot_remove_inquiry_linkedurbaneventinquiry"
        BaseContent.manage_beforeDelete(self, item, container)

    security.declarePublic("getLinkedUrbanEventInquiry")

    def getLinkedUrbanEventInquiry(self):
        """
        Return the linked UrbanEventInquiry object if exists
        """
        brefs = self.getBRefs("linkedInquiry")
        if brefs:
            # linkedInquiry may come from a UrbanEventInquiry or an UrbanEventOpinionRequest
            for bref in brefs:
                if bref and bref.portal_type == "UrbanEventInquiry":
                    return bref
        else:
            return None

    security.declarePublic("getCustomInvestigationArticles")

    def getCustomInvestigationArticles(self):
        items = []
        for article in self.getInvestigationArticles():
            if self.displayValue(
                UrbanVocabulary("investigationarticles").getDisplayList(self), article
            ):
                items.append(
                    self.displayValue(
                        UrbanVocabulary("investigationarticles").getDisplayList(self),
                        article,
                    )
                )
        return items

    security.declarePublic("getLinkedUrbanEventOpinionRequest")

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

    def _getSelfPosition(self):
        """
        Return the position of the self between every Inquiry objects
        """
        container = self
        if not interfaces.IGenericLicence.providedBy(self):
            container = self.aq_parent
        inquiries = [container]
        for obj in container.objectValues():
            if interfaces.IInquiry.providedBy(obj):
                inquiries.append(obj)
        i = 0
        for inquiry in inquiries:
            if inquiry.UID() == self.UID():
                break
            i = i + 1
        return i

    security.declarePublic("generateInquiryTitle")

    def generateInquiryTitle(self):
        """
        Generates a title for the inquiry
        """
        # we need to generate the title as the number of the inquiry is into it
        position = self._getSelfPosition()
        return translate(
            "inquiry_title_and_number",
            "urban",
            mapping={"number": position + 1},
            context=self.REQUEST,
        )

    security.declarePublic("getInquiries")

    def getInquiries(self):
        """
        Returns the existing inquiries
        """
        return self._get_inquiry_objs(all_=False)

    security.declarePublic("getAllInquiries")

    def getAllInquiries(self):
        """
        Returns the existing inquiries
        """
        return self._get_inquiry_objs(all_=True)

    def _get_inquiry_objs(self, all_=False, portal_type="Inquiry"):
        """
        Returns the existing inquiries or announcements
        """
        all_inquiries = []
        other_inquiries = self.objectValues(portal_type)
        if all_ or other_inquiries:
            all_inquiries.append(self)
        all_inquiries.extend(list(other_inquiries))
        return all_inquiries

    security.declarePublic("getUrbanEventInquiries")

    def getUrbanEventInquiries(self):
        """
        Returns the existing UrbanEventInquiries
        """
        return self.listFolderContents({"portal_type": "UrbanEventInquiry"})

    def getLastInquiry(self, use_catalog=True):
        return self.getLastEvent(interfaces.IInquiryEvent)

    def getLastOpinionRequest(self):
        return self.getLastEvent(interfaces.IOpinionRequestEvent)

    def getAllTechnicalServiceOpinionRequests(self):
        return self.getAllEvents(interfaces.ITechnicalServiceOpinionRequestEvent)

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
        inquiries = [inq for inq in self.getInquiries() if inq != self]
        for inquiry in inquiries:
            if (
                organisation in inquiry.getSolicitOpinionsTo()
                or organisation in inquiry.getSolicitOpinionsToOptional()
            ):
                limit += 1
        limit = limit - len(self.getOpinionRequests(organisation))
        return limit > 0

    security.declarePublic("mayAddInquiryEvent")

    def mayAddInquiryEvent(self):
        """
        This is used as TALExpression for the UrbanEventInquiry
        We may add an inquiry if we defined one on the licence
        We may add another if another is defined on the licence and so on
        """
        # first of all, we can add an InquiryEvent if an inquiry is defined on the licence at least
        inquiries = self.getAllInquiries()
        urbanEventInquiries = self.getUrbanEventInquiries()
        # if we have only the inquiry defined on the licence and no start date is defined
        # it means that no inquiryEvent can be added because no inquiry is defined...
        # or if every UrbanEventInquiry have already been added
        if len(urbanEventInquiries) >= len(inquiries):
            return False
        return True

    def getAllTechnicalServiceOpinionRequestsNoDup(self):
        allOpinions = self.getAllTechnicalServiceOpinionRequests()
        allOpinionsNoDup = {}
        for opinion in allOpinions:
            actor = opinion.getUrbaneventtypes().getId()
            allOpinionsNoDup[actor] = opinion
        return allOpinionsNoDup.values()

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

    def getAllInquiryEvents(self):
        return self.getAllEvents(interfaces.IInquiryEvent)

    def getAllClaimsTexts(self):
        claimsTexts = []
        for inquiry in self.getAllInquiryEvents():
            text = inquiry.getClaimsText()
            if text is not "":
                claimsTexts.append(text)
        return claimsTexts

    security.declarePublic("getFolderMakersCSV")

    def getFolderMakersCSV(self):
        """
        Returns a formatted version of the folder maker address to be used in POD templates
        """
        urban_tool = getToolByName(self, "portal_urban")
        foldermakers_config = urban_tool.getLicenceConfig(self).eventconfigs
        foldermakers = [
            fm
            for fm in foldermakers_config.objectValues("OpinionEventConfig")
            if fm.id in self.getSolicitOpinionsTo()
        ]
        toreturn = "[CSV]Nom|Description|AdresseLigne1|AdresseLigne2"
        for foldermaker in foldermakers:
            toreturn = toreturn + "%" + foldermaker.getAddressCSV()
        toreturn = toreturn + "[/CSV]"
        return toreturn

    def get_suspension_delay(self):
        inquiry_event = self.getLinkedUrbanEventInquiry()
        if not inquiry_event:
            return 0

        start_date = inquiry_event.getInvestigationStart()
        if not start_date:
            return 0

        end_date = inquiry_event.getInvestigationEnd()
        if not end_date:
            return 0

        portal_urban = api.portal.get_tool("portal_urban")
        licence = IGenericLicence.providedBy(self) and self or self.aq_parent
        suspension_periods = portal_urban.get_offday_periods("inquiry_suspension")
        suspension_delay = 0

        for suspension_period in suspension_periods:
            suspension_start = DateTime(str(suspension_period["start_date"]))
            suspension_end = DateTime(str(suspension_period["end_date"]))
            if start_date < suspension_start and end_date >= suspension_start:
                suspension_delay = suspension_end - suspension_start
                return int(suspension_delay)
            elif start_date >= suspension_start and start_date < suspension_end + 1:
                suspension_delay = suspension_end - start_date + 1
                return suspension_delay

        return suspension_delay

    security.declarePublic("getAllInquiriesAndAnnouncements")

    def getAllInquiriesAndAnnouncements(self):
        """
        Returns the existing inquiries
        """
        inqs = [inq for inq in self._get_inquiry_objs(all_=True)]
        return inqs


    def get_impact_study_radius(self, has_impact_study):
        """ """
        if has_impact_study:
            return "200m"
        return "50m"


registerType(Inquiry, PROJECTNAME)
# end of class Inquiry

##code-section module-footer #fill in your manual code here
##/code-section module-footer
