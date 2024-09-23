# -*- coding: utf-8 -*-

from Acquisition import aq_inner

from Products.Five import BrowserView

from Products.urban import utils
from Products.urban.browser.table.urbantable import ApplicantTable
from Products.urban.browser.table.urbantable import ApplicantHistoryTable
from Products.urban.browser.table.urbantable import LicenceAttachmentsTable
from Products.urban.browser.table.urbantable import EventsTable
from Products.urban.browser.table.urbantable import NestedAttachmentsTable
from Products.urban.browser.table.urbantable import ParcelsTable
from Products.urban.browser.table.urbantable import ProprietaryTable
from Products.urban.browser.table.urbantable import ProprietaryHistoryTable
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanDoc
from Products.urban.interfaces import IUrbanEventAnnouncement
from Products.urban.interfaces import IUrbanEventInquiry
from Products.urban.interfaces import IUrbanWarningCondition

from plone import api
from plone.memoize import view
from zope.annotation import IAnnotations
from zope.i18n import translate
from zope.component import queryAdapter


class LicenceView(BrowserView):
    """
    Base class for licences browser views.
    """

    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)
        self.display_warnings()

    def display_warnings(self):
        """ """
        plone_utils = api.portal.get_tool("plone_utils")

        warned = set([])
        config = self.getLicenceConfig()
        for warning in config.getWarnings():
            name = warning["condition"]
            condition = queryAdapter(self.context, IUrbanWarningCondition, name)
            if condition.evaluate():
                level = warning["level"]
                plone_utils.addPortalMessage(
                    warning["message"].decode("utf-8"), type=level
                )
                warned.add(name)

        # only display global warnings if they are not overriden locally in the licence config
        urban_tool = api.portal.get_tool("portal_urban")
        for warning in urban_tool.getWarnings():
            name = warning["condition"]
            condition = queryAdapter(self.context, IUrbanWarningCondition, name)
            if name not in warned and condition.evaluate():
                level = warning["level"]
                plone_utils.addPortalMessage(
                    warning["message"].decode("utf-8"), type=level
                )

    @view.memoize
    def getMember(self):
        context = aq_inner(self.context)
        return context.restrictedTraverse("@@plone_portal_state/member")()

    def getLicenceMainTemplateMacro(self):
        """ """
        context = aq_inner(self.context)
        main_template_macro = context.unrestrictedTraverse("licencemainmacro/main")
        return main_template_macro

    def getAllowedEventConfigs(self):
        licence = aq_inner(self.context)
        licence_config = licence.getLicenceConfig()
        event_configs = [
            cfg
            for cfg in licence_config.getEnabledEventConfigs()
            if cfg.canBeCreatedInLicence(self.context)
        ]
        return event_configs

    def canAddUrbanEvent(self):
        licence = aq_inner(self.context)
        member = self.getMember()
        has_permission = member.has_permission("urban: Add UrbanEvent", licence)
        can_add = has_permission and self.getAllowedEventConfigs()
        return can_add

    def canAddAllAdvices(self):
        licence = aq_inner(self.context)
        member = self.getMember()

        all_advices = licence.getAllAdvices()
        has_permission = member.has_permission("urban: Add UrbanEvent", licence)
        return all_advices and has_permission

    def mayAddAttachment(self):
        context = aq_inner(self.context)
        member = api.portal.get_tool("portal_membership").getAuthenticatedMember()
        if member.has_permission("ATContentTypes: Add File", context):
            return True
        return False

    def isGigCoringActive(self):
        activation = api.portal.get_registry_record(
            "Products.urban.browser.gig_coring_settings.IGigCoringLink.gig_coring_activation"
        )
        return activation

    def getInquiryType(self):
        return "Inquiry"

    def getInquiryReclamationNumbers(self):

        inquiryReclamationNumbers = []
        context = aq_inner(self.context)
        totalOral = 0
        totalWrite = 0
        if context.getClaimants():
            for claimant in context.getClaimants():
                if claimant.getClaimType() == "oralClaim":
                    totalOral += 1
                elif claimant.getClaimType() == "writedClaim":
                    totalWrite += 1

        inquiryReclamationNumbers.append(totalOral)
        inquiryReclamationNumbers.append(totalWrite)
        return inquiryReclamationNumbers

    def renderAttachmentsListing(self):
        licence = aq_inner(self.context)
        attachments = licence.objectValues("ATBlob")
        if not attachments:
            return ""
        table = LicenceAttachmentsTable(self.context, self.request, values=attachments)
        return self.renderListing(table)

    def renderNestedAttachmentsListing(self):
        licence = aq_inner(self.context)
        path = "/".join(licence.getPhysicalPath())
        queryString = {
            "portal_type": "File",
            "path": {
                "query": path,
                "depth": 2,
            },
            "sort_on": "created",
        }
        catalog = api.portal.get_tool("portal_catalog")
        attachments = catalog(queryString)
        path_len = len(path.split("/"))
        nested_attachments = []
        for brain in attachments:
            attachment = brain.getObject()
            is_not_doc = not IUrbanDoc.providedBy(attachment)
            is_nested = len(brain.getPath().split("/")) > path_len + 1
            if is_nested and is_not_doc:
                nested_attachments.append(attachment)

        if not nested_attachments:
            return ""
        nested_attachments.sort(lambda a, b: cmp(a.Title(), b.Title()))
        table = NestedAttachmentsTable(
            self.context, self.request, values=nested_attachments
        )
        return self.renderListing(table)

    def getAdviceTitles(self):
        licence = aq_inner(self.context)
        all_advices = licence.getAllAdvices()
        advice_titles = [advice.Title() for advice in all_advices]
        advice_titles = ", ".join(advice_titles)
        return advice_titles

    def renderListing(self, table):
        table.update()
        return table.render()

    def renderApplicantListing(self):
        if not self.context.getApplicants():
            return ""
        contacttable = ApplicantTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderApplicantHistoryListing(self):
        if not self.context.get_applicants_history():
            return ""
        contacttable = ApplicantHistoryTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderProprietaryListing(self):
        if not self.context.getProprietaries():
            return ""
        contacttable = ProprietaryTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderProprietaryHistoryListing(self):
        if not self.context.get_proprietaries_history():
            return ""
        contacttable = ProprietaryHistoryTable(self.context, self.request)
        return self.renderListing(contacttable)

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ""
        parceltable = ParcelsTable(self.context, self.request, values=parcels)
        return self.renderListing(parceltable)

    def renderEventsListing(self):
        events = self.context.getAllEvents()
        if not events:
            return ""
        eventtable = EventsTable(self.context, self.request, values=events)
        return self.renderListing(eventtable)

    def getLicenceConfig(self):
        context = aq_inner(self.context)
        return context.getLicenceConfig()

    def getTabMacro(self, tab):
        context = aq_inner(self.context)
        macro_name = "{}_macro".format(tab)
        macros_view = self.getMacroViewName()
        macro = context.unrestrictedTraverse(
            "{view}/{macro}".format(view=macros_view, macro=macro_name)
        )
        return macro

    def getMacroViewName(self):
        return "licencetabs-macros"

    def getTabs(self):
        return self.getLicenceConfig().getActiveTabs()

    def getUseTabbing(self):
        return self.getLicenceConfig().getUseTabbingForDisplay()

    def getUsedAttributes(self):
        return self.getLicenceConfig().getUsedAttributes()

    def hasOutdatedParcels(self):
        context = aq_inner(self.context)
        if api.content.get_state(self.context) in ["accepted", "refused"]:
            return False
        return any(
            [
                not parcel.getIsOfficialParcel
                for parcel in context.listFolderContents(
                    contentFilter={"portal_type": "PortionOut"}
                )
            ]
        )

    def getKeyDates(self):
        context = aq_inner(self.context)
        urban_tool = api.portal.get_tool("portal_urban")
        with_empty_dates = urban_tool.getDisplayEmptyKeyDates()
        config = context.getLicenceConfig()
        ordered_dates = []

        # search in the config for all the Key eventconfigs and their key dates
        all_events = context.getAllEvents()
        for eventconfig in config.eventconfigs.objectValues():
            if eventconfig.getIsKeyEvent():
                linked_events = [
                    event
                    for event in all_events
                    if event.getUrbaneventtypes() == eventconfig
                ]
                keydates = [
                    (
                        date == "eventDate"
                        and eventconfig.getEventDateLabel()
                        or translate(
                            "urban_label_" + date,
                            "urban",
                            default=date,
                            context=self.request,
                        ),
                        date,
                    )
                    for date in eventconfig.getKeyDates()
                ]
                if linked_events:
                    for event in linked_events:
                        ordered_dates.append(
                            {
                                "label": event.Title(),
                                "dates": [
                                    {
                                        "date_label": date[0],
                                        "date": urban_tool.formatDate(
                                            getattr(event, date[1]),
                                            translatemonth=False,
                                        ),
                                        "url": event.absolute_url(),
                                    }
                                    for date in keydates
                                ],
                            }
                        )
                elif with_empty_dates:
                    ordered_dates.append(
                        {
                            "label": eventconfig.Title(),
                            "dates": [
                                {"date_label": date[0], "date": None, "url": None}
                                for date in keydates
                            ],
                        }
                    )

        return ordered_dates

    def getSchemataFields(self, schemata="", exclude=[], context=None):
        displayed_fields = self.getUsedAttributes()
        return utils.getSchemataFields(
            context or self.context, displayed_fields, schemata, exclude
        )

    def getDescriptionFields(self, exclude=[]):
        return self.getSchemataFields("urban_description", exclude)

    def getAnalysisFields(self, exclude=[]):
        return self.getSchemataFields("urban_analysis", exclude)

    def getEnvironmentFields(self, exclude=[]):
        return self.getSchemataFields("urban_environment", exclude)

    def getRoadFields(self, exclude=[]):
        return self.getSchemataFields("urban_road", exclude)

    def getLocationFields(self, exclude=[]):
        return self.getSchemataFields("urban_location", exclude)

    def getAdviceFields(self, exclude=[]):
        return self.getSchemataFields("urban_advices", exclude)

    def getInquiryFields(self, exclude=[]):
        return self.getSchemataFields("urban_inquiry", exclude)

    def getBoundInquiryFields(self, exclude=[], bound_context=None):
        return self.getSchemataFields("urban_inquiry", exclude, bound_context)

    def getDefaultFields(self, exclude=[], context=None):
        base_exclude = ["id", "title"]
        return self.getSchemataFields(
            "default", base_exclude + exclude, context=context
        )

    def getHabitationFields(self, exclude=[]):
        return self.getSchemataFields("urban_habitation", exclude)

    def getImpactStudyInfos(self):
        return {}

    def get_state(self):
        return api.content.get_state(self.context)

    def has_bound_inspections(self):
        annotations = IAnnotations(self.context)
        inspections = annotations.get("urban.bound_inspections", [])
        tickets = annotations.get("urban.bound_tickets", [])
        return inspections or tickets

    def get_bound_inspections(self):
        inspections_and_tickets = []
        annotations = IAnnotations(self.context)
        inspection_UIDs = list(annotations.get("urban.bound_inspections", []))
        ticket_UIDs = list(annotations.get("urban.bound_tickets", []))
        inspections_and_tickets_UIDs = inspection_UIDs + ticket_UIDs
        if inspections_and_tickets_UIDs:
            licence_folder = api.portal.get().urban
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(UID=inspections_and_tickets_UIDs)
            inspections_and_tickets = [
                {
                    "title": b.Title,
                    "url": "{}/{}s/{}".format(
                        licence_folder.absolute_url(), b.portal_type.lower(), b.id
                    ),
                    "state": b.review_state,
                }
                for b in brains
            ]
            return inspections_and_tickets

    def has_bound_roaddecrees(self):
        annotations = IAnnotations(self.context)
        roaddecrees = annotations.get("urban.bound_roaddecrees", [])
        return roaddecrees

    def get_bound_roaddecrees(self):
        roaddecrees = []
        annotations = IAnnotations(self.context)
        roaddecree_UIDs = list(annotations.get("urban.bound_roaddecrees", []))
        if roaddecree_UIDs:
            licence_folder = api.portal.get().urban
            catalog = api.portal.get_tool("portal_catalog")
            brains = catalog(UID=roaddecree_UIDs)
            roaddecrees = [
                {
                    "title": b.Title,
                    "url": "{}/{}s/{}".format(
                        licence_folder.absolute_url(), b.portal_type.lower(), b.id
                    ),
                    "state": b.review_state,
                }
                for b in brains
            ]
            return roaddecrees

    def getRoadDecreesInquiriesForDisplay(self):
        """
        Returns the bound road decrees inquiries to display on the buildlicence_view
        """
        roaddecrees = self.context.get_bound_roaddecrees()
        all_inquiries = []
        for roaddecree in roaddecrees:
            context = aq_inner(roaddecree)
            inquiries = [roaddecree, context.getAllInquiries()]
            all_inquiries.append(inquiries)
        return all_inquiries


class CODTLicenceView(LicenceView):
    """ """

    def getInquiryFields(self, exclude=[], context=None):
        return self.context.get_inquiry_fields_to_display(exclude=exclude)

    def getInquiryType(self):
        return "CODT_Inquiry"

    def getPatrimonyFields(self):
        return self.getSchemataFields(schemata="urban_patrimony")

    def getRankingOrdinanceTitle(self):
        code_dgo4 = "code dgo4"
        libelle = "libelle"
        historique_dossier = "historique_dossier"
        liendoc = "liendoc"
        return "{} - {} - {} - {}".format(
            code_dgo4, libelle, historique_dossier, liendoc
        )

    def getRankingOrdinanceLink(self):
        liendoc = "http://spw.wallonie.be/dgo4/index.php?thema=bc_pat&details=57081-CLT-0239-01"
        return liendoc


class UrbanCertificateBaseView(LicenceView):
    """
    This manage the view of UrbanCertificate and NotaryLetter Classes
    """

    def __init__(self, context, request):
        super(UrbanCertificateBaseView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getSpecificFeatures(self, subtype=""):
        context = aq_inner(self.context)
        accessor = getattr(context, "get%sSpecificFeatures" % subtype.capitalize())
        specific_features = accessor()
        return [
            spf.get("value", spf["text"])
            for spf in specific_features
            if "check" not in spf or spf["check"]
        ]


class CODTUrbanCertificateBaseView(UrbanCertificateBaseView):
    """
    This manage the view of CODT UrbanCertificate
    """

    def getInquiryFields(self, exclude=[], context=None):
        return self.context.get_inquiry_fields_to_display(exclude=exclude)

    def getInquiryType(self):
        return "CODT_Inquiry"


class EnvironmentLicenceView(LicenceView):
    """
    This manage helper methods for all environment licences views
    """

    def __init__(self, context, request):
        super(EnvironmentLicenceView, self).__init__(context, request)

    def getInquiriesForDisplay(self):
        """
        Returns the inquiries to display on the buildlicence_view
        This will move to the buildlicenceview when it will exist...
        """
        context = aq_inner(self.context)
        inquiries = context.getInquiries()
        if not inquiries:
            # we want to display at least the informations about the inquiry
            # defined on the licence even if no data have been entered
            inquiries.append(context)
        return inquiries

    def getRubrics(self):
        """
        display the rubrics number, their class and then the text
        """
        context = aq_inner(self.context)
        catalog = api.portal.get_tool("portal_catalog")
        rubric_uids = context.getField("rubrics").getRaw(context)
        rubric_brains = catalog(UID=rubric_uids)
        rubrics = [brain.getObject() for brain in rubric_brains]
        rubrics_display = [
            "<p>classe %s, %s</p>%s"
            % (rub.getExtraValue(), rub.getNumber(), rub.Description())
            for rub in rubrics
        ]
        return rubrics_display

    def _sortConditions(self, conditions):
        """
        sort exploitation conditions in this order: CI/CS, CI, CS
        """
        order = ["CI/CS", "CI", "CS", "CS-Eau", "Ville"]
        sorted_conditions = dict(
            [
                (
                    val,
                    [],
                )
                for val in order
            ]
        )
        for cond in conditions:
            val = cond.getExtraValue()
            sorted_conditions[val].append(
                {
                    "type": val,
                    "url": cond.absolute_url() + "/description/getRaw",
                    "title": cond.Title(),
                }
            )
        sort = []
        for val in order:
            sort.extend(sorted_conditions[val])
        return sort

    def getMinimumConditions(self):
        """
        sort the conditions from the field 'minimumLegalConditions'  by type (integral, sectorial, ...)
        """
        context = aq_inner(self.context)
        min_conditions = context.getMinimumLegalConditions()
        return self._sortConditions(min_conditions)


class ShowEditTabbing(BrowserView):
    """call this view to see if a licence should display the tabbing with edit icons"""

    def __call__(self):

        # this view is registered for any kind of content (because fuck you thats why)
        # we do the check if we are a licence or an events with tabs inside the call
        # allow custom tab for events because teh default tab do not allow
        # to redirect correctly.
        if IUrbanEventAnnouncement.providedBy(self.context):
            return True
        if IUrbanEventInquiry.providedBy(self.context):
            return True
        if not IGenericLicence.providedBy(self.context):
            return

        member = api.user.get_current()
        licence = self.context
        show_tabbing = member.has_permission("Modify portal content", licence)
        return show_tabbing
