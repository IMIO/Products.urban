# -*- coding: utf-8 -*-

from Products.urban.notice.address import NoticeAddress
from Products.urban.notice.base import NoticeElement
from Products.urban.notice.document import NoticeDocument
from Products.urban.notice.parcel import NoticeParcel
from Products.urban.notice.party import NoticeParty
from Products.urban.notice.sender import NoticeSender
from Products.urban.utils import get_rubric_obj
from datetime import datetime
from lxml import etree
from plone import api


class NoticeNotification(NoticeElement):
    """Class that represent a notification from Notice Webservice"""

    _notice_keys = (
        "notice_type",
        "sender",
        "status",
        "notice_type",
        "notification_subtype",
        "notification_type",
    )
    _excluded_keys = (
        "addresses",
        "container",
        "documents",
        "parcels",
        "parties",
    )

    def __init__(self, service, json):
        self.service = service
        self.json = json

    @property
    def noticeId(self):
        """Return notice unique identifier"""
        return self._get_data("noticeIdentifier", "noticeId")

    @property
    def _last_status(self):
        """
        Return the last status
        beware: random order !
        """
        sorted_status = sorted(self._get_data("status", "status"), key=lambda x: x["date"])
        return sorted_status[-1]

    @property
    def status(self):
        """Return the last notice notification status e.g. 'EN_ATTENTE_REPONSE'"""
        return self._last_status["code"]["code"]

    @property
    def status_date(self):
        """Return the last notice notification date"""
        raw_date = self._last_status["date"]
        return datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f").date()

    @property
    def notice_type(self):
        """Return notice notification type e.g. 'TRANSFERT_DOSSIER'"""
        return self._get_data("BO", "codeTypeNoticeBO")

    @property
    def notification_type(self):
        """Return notification type e.g. 'PEPU'"""
        return self._get_data("BO", "typeBO", "code")

    @property
    def notification_subtype(self):
        """Return notification subtype e.g. 'PE'"""
        return self._get_data("BO", "typeBOSubtype", "code")

    @property
    def type(self):
        """Return the portal type corresponding to notice subtype"""

        if not hasattr(self, "_licence_type"):
            self._licence_type = None

            if self.notice_type == "TRANSFERT_DOSSIER":
                if self.notification_type == "PE_PU":
                    if self.notification_subtype == "PU":
                        self._licence_type = "UniqueLicence"
                    elif self.notification_subtype == "PE":
                        # PE class is not yet available in TRANSFERT_DOSSIER
                        # => extract it from XML document
                        classe_elements = self._pj_formulaire_xml_tree.xpath(
                            "/dataStore/item/classe"
                        )
                        penv_classe = (
                            classe_elements[0].text if len(classe_elements) == 1 else None
                        )
                        self._licence_type = {
                            "1": "EnvClassOne",
                            "2": "EnvClassTwo",
                            "3": "EnvClassThree",
                        }.get(penv_classe, None)
            else:
                existing_licence = self.licence
                if existing_licence:
                    self._licence_type = existing_licence.portal_type

        return self._licence_type

    @property
    def id(self):
        """Return a generated id"""
        return api.portal.get().generateUniqueId(self.type)

    @property
    def reference(self):
        """Return the URBAN reference, if present"""
        specific = {
            "TRANSFERT_DOSSIER": "ns3:TwiceDefaultRequest",
            "DEMANDE_EP": "ns3:PublicSurveyRequest",
            "NOTIF_COMPLETUDE1_INCOMPLET_COMMUNE":"ns3:TwiceDefaultRequest",
        }
        return self._get_data("specific", specific.get(self.notice_type), "ns3:municipalityReference")

    @property
    def _pj_formulaire_xml_tree(self):
        """Return XML tree with all data entered by residents in Mon Espace"""
        for document in self.documents:
            if (
                document.document_mimetype == "application/xml"
                and document.document_type_code == "PJ_FORMULAIRE"
            ):
                return etree.parse(document.file)
        raise ValueError("No PJ_FORMULAIRE XML document found")

    @property
    def rubrics(self):
        """Return the rubrics as a list of UIDs, if present"""
        found_uids = []
        missing_rubrics = []

        if self.notice_type == "TRANSFERT_DOSSIER":
            rubrique_elements = self._pj_formulaire_xml_tree.xpath(
                "/dataStore/projet/rubriques/item"
            )
            for rubrique in rubrique_elements:
                classe = rubrique.xpath("classe/text()")[0]
                number = rubrique.xpath("numRubrique")[0].text
                rubric_obj = get_rubric_obj(classe, number)
                if rubric_obj:
                    found_uids.append(rubric_obj.UID())
                else:
                    missing_rubrics.append("classe {}, {}".format(classe, number))

        if missing_rubrics:
            raise ValueError(
                "cannot find these rubrics: {}".format(" | ".join(missing_rubrics))
            )
        return found_uids

    @property
    def send_date(self):
        """Return the send date"""
        raw_date = self._get_data("sendDate")
        return datetime.strptime(raw_date[:19], "%Y-%m-%dT%H:%M:%S").date()

    @property
    def container(self):
        urban_folder = api.portal.get()["urban"]
        return getattr(urban_folder, "{0}s".format(self.type.lower()))

    @property
    def licence(self):
        """Return the licence, if there is already one"""
        if not self.reference:
            return
        catalog = api.portal.get_tool("portal_catalog")
        brains = catalog.unrestrictedSearchResults(getReference=self.reference)
        if len(brains) != 1:
            return
        licence = brains[0].getObject()
        return licence

    @property
    def event_configs(self):
        portal_urban_folder = api.portal.get().urban.portal_urban
        licence_type_folder = getattr(portal_urban_folder, "{0}".format(self.type.lower()))
        return getattr(licence_type_folder, "eventconfigs")

    @property
    def licenceSubject(self):
        """Return subject of the folder"""
        return self._get_data("subjectNotice")

    @property
    def sender(self):
        """Return sender"""
        return NoticeSender(self.service, self.json["sender"])

    @property
    def parcels(self):
        """Return parcels"""
        return [NoticeParcel(self.service, p) for p in self.json["parcels"]["parcel"]]

    @property
    def parties(self):
        """Return parties"""
        return [
            NoticeParty(self.service, p)
            for p in self._get_data("parties", "part") or []
        ]

    @property
    def addresses(self):
        """Return work locations"""
        return [
            NoticeAddress(self.service, a) for a in self.json["addresses"]["address"]
        ]

    @property
    def documents(self):
        """Return documents"""
        return [
            NoticeDocument(self.service, d, self.noticeId)
            for d in self.json["documents"]["document"]
        ]

    @property
    def workLocations(self):
        """Initialize workLocations"""
        return []
