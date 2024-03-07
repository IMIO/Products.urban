# -*- coding: utf-8 -*-

from DateTime import DateTime

from html import escape

from plone import api

from z3c.table.column import Column, GetAttrColumn, LinkColumn
from z3c.table.interfaces import IColumnHeader

from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from Products.urban.setuphandlers import _ as _t
from Products.urban.browser.table.interfaces import (
    ITitleColumn,
    IActionsColumn,
    ILocalityColumn,
    IStreetColumn,
    IUrbanColumn,
    ITitleCell,
)


class UrbanColumn(Column):
    """base class for a column that expect a ItemForUrbanTable item"""

    implements(IUrbanColumn)

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)


class EventDateColumn(UrbanColumn):
    """
    Implement a column showing the urban event main date
    """

    header = "label_colname_eventDate"
    weight = 20

    def renderCell(self, urbanlist_item):
        event = urbanlist_item.getObject()
        date = event.getKeyDate()

        if date and date.year() < 1900:
            return "{}/{}/{}".format(date.day(), date.month(), date.year())
        date = date and date.strftime("%d/%m/%Y") or "no date defined"

        return date

    def getSortKey(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        return obj.getKeyDate()


class RelatedLicencesColumn(Column):
    """
    Implement a column that provides a link to all the licences related to any parcel of the item
    """

    header = "parcelLinkedLicences"
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)

    def renderCell(self, parcel):
        url = parcel.aq_parent.absolute_url()
        id = parcel.getId()
        img = '<img  src="linkedfolders.png" class="urban-linkedfolders-icon"/>'
        link = '<a class="link-overlay" href="%s/@@parcelrecordsview?id=%s">%s</a>' % (
            url,
            id,
            img,
        )
        cell = '<span id="urban-parcel-related-licences">%s</span>' % link
        return cell


class TitleColumn(UrbanColumn):
    """ """

    implements(ITitleColumn)

    header = "label_colname_Title"
    weight = 1

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        header = queryMultiAdapter(
            (self.context, self.request, self.table, self), IColumnHeader
        )
        if header:
            header.update()
            return header.render()
        return translate(self.header, "urban", context=self.request)

    def renderTitleLink(self, urbanlist_item):
        portal_type = urbanlist_item.getPortalType().lower()
        state = urbanlist_item.getState()
        css_class = "contenttype-%s state-%s" % (portal_type, state)
        url = urbanlist_item.getURL()
        title = escape(urbanlist_item.Title())

        title_words = title.split()
        for split in range(len(title_words) / 15):
            title_words.insert(15 * (split + 1), "<br />")
        title = " ".join(title_words)

        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title

    def renderCell(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        adapter = queryMultiAdapter(
            (self.context, self, urbanlist_item, obj), ITitleCell
        )
        if adapter:
            title = adapter.render()
        else:
            title = self.renderTitleLink(urbanlist_item)
        return title.decode("utf-8")

    def getSortKey(self, urbanlist_item):
        return urbanlist_item.Title()


class TitleColumnHeader:
    """return the right label to display in Title Column header"""

    implements(IColumnHeader)

    def __init__(self, context, request, table, column):
        self.request = request
        self.label = ""

    def update(self):
        """to implement"""

    def render(self):
        return translate(self.label, "urban", context=self.request)


class ApplicantTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_applicant_data"


class ProprietaryTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_proprietary_data"


class TenantTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_tenant_data"


class PlaintiffTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_plaintiff_data"


class NotaryTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_notary_data"


class ArchitectTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_architect_data"


class GeometricianTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_geometrician_data"


class ClaimantTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_claimant_data"


class RecipientCadastreTitleColumnHeader(TitleColumnHeader):
    def update(self):
        self.label = "label_colname_name"


class TitleDisplay(object):
    """Base class for Title cell adapter"""

    implements(ITitleCell)

    def __init__(self, context, column, urbanlist_item, obj):
        self.context = context
        self.column = column
        self.urbanlist_item = urbanlist_item
        self.obj = obj

    def render(self):
        """to implement"""


class ContacTitleDisplay(TitleDisplay):
    """Adapts a contact to a TitleCell"""

    def render(self):
        contact = self.obj
        title = self.column.renderTitleLink(self.urbanlist_item)

        address = ""
        street = escape(contact.getStreet())
        number = escape(contact.getNumber())
        if street or number:
            address = "<br /><span>%s %s</span>" % (street, number)

        zipcode = escape(str(contact.getZipcode()))
        city = escape(contact.getCity())
        if zipcode or city:
            address = "%s<br /><span>%s %s</span>" % (address, zipcode, city)

        phone = contact.getPhone()
        gsm = contact.getGsm()

        tel = gsm if gsm else phone
        tel = escape(tel)
        if tel:
            address = "%s<br /><span>%s</span>" % (address, tel)

        title = "%s%s" % (title, address)
        return title


class ParcelTitleDisplay(TitleDisplay):
    """Adapts a parcel to a TitleCell"""

    def render(self):
        parcel = self.obj
        link = '<a class="link-overlay" href="{url}/@@parcelview">{title}</a>'.format(
            url=parcel.absolute_url(), title=escape(parcel.Title())
        )
        cell = '<span id="urban-parcel-display">{}</span>'.format(link)
        return cell


class EventTitleDisplay(TitleDisplay):
    """Adapts an event to a TitleCell"""

    def render(self):
        event = self.obj
        title = self.column.renderTitleLink(self.urbanlist_item)

        suffix = self.urbanlist_item.canBeEdited() and "/external_edit" or ""

        documents = []
        for doc in event.getDocuments():
            doc_title = escape(doc.Title())
            doc_link = "%s%s" % (doc.absolute_url(), suffix)
            doc_link = (
                '<br /><a href="%s" class="discreet" style="margin-left:20px">%s</a>'
                % (doc_link, doc_title)
            )
            documents.append(doc_link)
        documents = "".join(documents)

        suffix = ""
        annexes = []
        for annex in event.getAttachments():
            annex_title = escape(annex.Title())
            annex_link = "%s%s" % (annex.absolute_url(), suffix)
            annex_link = (
                '<br /><a href="%s" class="discreet" style="margin-left:20px">%s</a>'
                % (annex_link, annex_title)
            )
            annexes.append(annex_link)
        annexes = "".join(annexes)

        return "%s%s%s" % (title, documents, annexes)


class DocumentTitleDisplay(TitleDisplay):
    """Adapts an event to a TitleCell"""

    def render(self):
        doc = self.obj
        title = escape(doc.Title())
        suffix = self.urbanlist_item.canBeEdited() and "/external_edit" or ""
        url = "%s%s" % (doc.absolute_url(), suffix)
        css_class = "contenttype-%s" % doc.portal_type.lower()
        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title


class RecipientCadastreTitleDisplay(TitleDisplay):
    """Adapts an event to a TitleCell"""

    def render(self):
        recipient = self.obj
        urbanlist_item = self.urbanlist_item

        portal_type = recipient.portal_type.lower()
        state = urbanlist_item.getState()
        css_class = "contenttype-%s state-%s" % (portal_type, state)
        title = escape(recipient.Title())
        title = '<span class="%s">%s</span>' % (css_class, title)
        parcels_info = '<span class="discreet">%s %s</span>' % (
            recipient.getCapakey(),
            recipient.getParcel_nature(),
        )
        parcels_info_street = '<span class="discreet">%s %s</span>' % (
            recipient.getParcel_street(),
            recipient.getParcel_police_number(),
        )
        title = "%s<br />%s<br />%s" % (title, parcels_info, parcels_info_street)
        return title


class CreationDateColumn(Column):

    header = u"label_colname_created"
    weight = 10

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)


class ObjectCreationDateColumn(CreationDateColumn):
    """ """

    def renderCell(self, obj):
        return obj.creation_date.strftime("%d/%m/%Y")

    def getSortKey(self, obj):
        return obj.creation_date


class BrainCreationDateColumn(CreationDateColumn):
    """ """

    def renderCell(self, brain):
        date = DateTime(brain.CreationDate)
        return date.strftime("%d/%m/%Y")

    def getSortKey(self, brain):
        return brain.CreationDate


class CreatorColumn(Column):
    """ """

    header = u"label_colname_Creator"
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)


class ObjectCreatorColumn(CreatorColumn):
    """ """

    def renderCell(self, urbanlist_item):
        return "".join(sorted(urbanlist_item.getObject().listCreators()))

    def getSortKey(self, urbanlist_item):
        return urbanlist_item.getObject().listCreators()


class BrainCreatorColumn(CreatorColumn):
    """ """

    def renderCell(self, obj):
        return "".join(sorted(obj.listCreators))

    def getSortKey(self, urbanlist_item):
        return urbanlist_item.getObject.listCreators()


class ParentLocationColumn(UrbanColumn):
    """ """

    header = u"label_colname_ParentLocation"
    weight = 25

    def renderCell(self, obj):
        obj = obj.getObject()
        parent = obj.aq_parent
        link = '<a href="{url}">{title}</a>'.format(
            url=parent.absolute_url(),
            title=parent.Title(),
        )
        return link.decode("utf-8")


class FoldermanagerColumn(Column):
    """ """

    header = u"label_colname_foldermanager"
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)

    def renderCell(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        foldermanagers = obj.getFoldermanagers()
        foldermanager_names = u", ".join(
            [fm.getSignaletic(short=True) for fm in foldermanagers]
        )
        return foldermanager_names


class ActionsColumn(UrbanColumn):
    """ """

    implements(IActionsColumn)

    weight = 100
    cssClasses = {"th": "actionsheader"}
    header = "actions"

    def renderCell(self, urbanlist_item):
        path = urbanlist_item.getPath()
        portal = api.portal.get()
        if urbanlist_item.id not in self.context.objectIds():
            return ""
        return portal.unrestrictedTraverse("{}/actions_panel".format(path))(
            showActions=True
        )


class ReorderActionsColumn(UrbanColumn):
    """ """

    implements(IActionsColumn)

    weight = 100
    cssClasses = {"th": "actionsheader"}
    header = "reorder_actions"

    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)

    def renderCell(self, urbanlist_item):
        path = urbanlist_item.getPath()
        portal = api.portal.get()
        if urbanlist_item.id not in self.context.objectIds():
            return ""
        return portal.unrestrictedTraverse("{}/reorder_actions_panel".format(path))(
            showActions=True
        )


class LocalityColumn(GetAttrColumn):
    """ """

    implements(ILocalityColumn)

    attrName = "adr1"
    header = "label_colname_adr1"
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)


class StreetColumn(Column):
    """ """

    implements(IStreetColumn)

    attrName = "street"
    header = "label_colname_street"
    weight = 30

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)

    def renderCell(self, recipient):

        street = "<span>%s</span>" % recipient.getStreet()
        secondary_street = '<span class="discreet">%s</span>' % recipient.getAdr2()
        street = "%s<br />%s" % (street, secondary_street)

        return street.decode("utf-8")


class InternalServiceColumn(Column):
    """ """

    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, "urban", context=self.request)


class InternalServiceId(UrbanColumn):
    """ """

    header = "label_service_id"
    weight = 10

    def renderCell(self, record):
        return record["id"]


class InternalServiceName(UrbanColumn):
    """ """

    header = "label_service_name"
    weight = 20

    def renderCell(self, record):
        return record["full_name"]


class InternalServiceGroups(UrbanColumn):
    """ """

    header = "label_service_groups"
    weight = 30

    def renderCell(self, record):
        portal = api.portal.get()

        group_ids = [record["validator_group_id"], record["editor_group_id"]]
        groups = dict([(id_, api.group.get(id_)) for id_ in group_ids])
        cell = ""

        for group_id, group in groups.iteritems():
            if group:
                cell = '{cell}<div><a href="{url}/@@usergroup-groupmembership?groupname={group_id}">{name}</a></div>'.format(
                    cell=cell,
                    name=group.getProperty("title"),
                    url=portal.absolute_url(),
                    group_id=group_id,
                )
            else:
                cell = '{cell}<div class="late-event-delay">{group_id}: GROUPE MANQUANT !</div>'.format(
                    cell=cell,
                    group_id=group_id,
                )

        return cell.decode("utf-8")


class InternalServiceTaskConfigs(UrbanColumn):
    """ """

    header = "label_service_taskconfigs"
    weight = 40

    def renderCell(self, record):
        portal_urban = api.portal.get_tool("portal_urban")
        schedule_folder = portal_urban.opinions_schedule

        task_ids = [record["task_answer_id"], record["task_validate_id"]]
        task_configs = dict(
            [(id_, getattr(schedule_folder, id_, None)) for id_ in task_ids]
        )
        cell = ""

        for task_config_id, task_config in task_configs.iteritems():
            if task_config:
                cell = '{cell}<div><a href="{url}/">{name}</a>{active}</div>'.format(
                    cell=cell,
                    name=task_config.Title(),
                    url=task_config.absolute_url(),
                    active=not task_config.enabled
                    and ':&nbsp;<span class="late-event-delay">DÉSACTIVÉ !</span>'
                    or "",
                )
            else:
                cell = '{cell}<div class="late-event-delay">{task_config_id}: TACHE MANQUANTE !</div>'.format(
                    cell=cell,
                    task_config_id=task_config_id,
                )

        return cell.decode("utf-8")


class GenerationColumn(LinkColumn):
    header = ""
    weight = 7
    iconName = "++resource++Products.urban/mailing.gif"

    def getLinkURL(self, item):
        """Setup link url."""
        url = item.getURL()
        doc_url = url.rsplit("/", 1)[0]
        doc_path = item.absolute_url_path() or ""
        if doc_path.startswith("/"):
            doc_path = doc_path[1:]
        # must use new view with title given and reference to mailing template
        return (
            "%s/@@mailing-loop-persistent-document-generation?document_url_path=%s"
            % (doc_url, doc_path)
        )

    def getLinkContent(self, item):
        return u"""<img title="%s" src="%s" />""" % (
            _t(u"Mailing"),
            "%s/%s" % (self.table.portal_url, self.iconName),
        )

    def has_mailing(self, item):
        obj = item.getObject()
        annot = IAnnotations(obj)
        if "documentgenerator" in annot and annot["documentgenerator"]["need_mailing"]:
            return True
        return False

    def renderCell(self, item):
        if not self.has_mailing(item):
            return ""
        return '<a href="%s"%s%s%s>%s</a>' % (
            escape(self.getLinkURL(item)),
            self.getLinkTarget(item),
            self.getLinkCSS(item),
            self.getLinkTitle(item),
            self.getLinkContent(item),
        )


class InspectionReportVisitDate(UrbanColumn):

    header = "urban_label_reportVisitDate"
    weight = 7

    def getSortKey(self, item):
        return item.getReportDate()

    def renderCell(self, report):
        raw_date = report.getEventDate()
        date = raw_date and raw_date.strftime("%d/%m/%Y") or "no date defined"
        return date


class InspectionReportDate(UrbanColumn):

    header = "urban_label_reportDate"
    weight = 8

    def getSortKey(self, item):
        return item.getReportDate()

    def renderCell(self, report):
        raw_date = report.getReportDate()
        date = raw_date and raw_date.strftime("%d/%m/%Y") or "no date defined"
        return date


class InspectionReportText(UrbanColumn):

    header = "urban_label_report"
    weight = 9

    def renderCell(self, report):
        cell = report.getReport().decode("utf-8")
        return cell


class InspectionReportFollowUp(UrbanColumn):

    header = "urban_label_followup_proposition"
    weight = 10

    def renderCell(self, report):
        voc = report.listFollowupPropositions().items()
        selected = report.getFollowup_proposition()
        cell = u", ".join([v for k, v in voc if k in selected and k != "other"])
        if "other" in selected:
            url = (
                report.absolute_url()
                + "/@@longtextview?field=other_followup_proposition"
            )
            link = '<a class="link-overlay" href="{}">autre</a>'.format(url)
            cell = u'<span>{}, </span><span id="inspection_other_followup">{}</span>'.format(
                cell, link
            )
        return cell


class InspectionFolderManager(UrbanColumn):

    header = "urban_label_folderManager"
    weight = 9

    def renderCell(self, report):
        folder_manager_id = ""
        if "inspectionreport_event_workflow" in report.value.workflow_history:
            wf_histories = report.value.workflow_history[
                "inspectionreport_event_workflow"
            ]
            for wf_history in wf_histories:
                if wf_history.get("action", "") == "propose_report":
                    folder_manager_id = wf_history.get("actor", "")
        if not folder_manager_id:
            folder_manager_id = str(report.getOwner())
        members = api.portal.get_tool("portal_membership")
        folder_manager_name = (
            members.getMemberInfo(folder_manager_id)["fullname"] or folder_manager_id
        )
        cell = folder_manager_name.decode("utf-8")
        return cell
