# -*- coding: utf-8 -*-

from Products.urban.notice.address import NoticeAddress
from Products.urban.notice.base import NoticeElement
from Products.urban.notice.document import NoticeDocument
from Products.urban.notice.parcel import NoticeParcel
from Products.urban.notice.party import NoticeParty
from Products.urban.notice.sender import NoticeSender
from datetime import datetime
from lxml import etree
from plone import api


class NoticeNotification(NoticeElement):
    """Class that represent a notification from Notice Webservice"""

    _notice_keys = (
        "event_config",
        "event_configs",
        "licence",
        "notice_type",
        "send_date",
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
                        penv_classe = None
                        for document in self.documents:
                            if (
                                document.document_mimetype == "application/xml"
                                and document.document_type_code == "PJ_FORMULAIRE"
                            ):
                                tree = etree.parse(document.file)
                                classe_elements = tree.xpath("/dataStore/item/classe")
                                if len(classe_elements) == 1:
                                    penv_classe = classe_elements[0].text
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

    def event_config(self, interface_identifier):
        """
        Return the event config for a given marker interface identifier.
        """
        for brain in api.content.find(
            context=self.event_configs, portal_type="EventConfig", review_state="enabled"
        ):
            config = brain.getObject()
            config_event_types = config.eventType or []
            if interface_identifier in config_event_types:
                return config
        raise ValueError(
            "No enabled EventConfig found for marker {} of licence type {}".format(
                interface_identifier,
                self.type,
            )
        )

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
