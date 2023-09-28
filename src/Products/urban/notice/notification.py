# -*- coding: utf-8 -*-

from Products.urban.notice.base import NoticeElement
from Products.urban.notice.address import NoticeAddress
from Products.urban.notice.document import NoticeDocument
from Products.urban.notice.parcel import NoticeParcel
from Products.urban.notice.party import NoticeParty
from Products.urban.notice.sender import NoticeSender
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
    def status(self):
        """Return notice notification status e.g. 'EN_ATTENTE_REPONSE'"""
        return self._get_data("status", "status", 0, "code", "code")

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
        return {
            "PE": "EnvClassTwo",
        }.get(self.notification_subtype)

    @property
    def id(self):
        """Return a generated id"""
        return api.portal.get().generateUniqueId(self.type)

    @property
    def container(self):
        urban_folder = api.portal.get()["urban"]
        return getattr(urban_folder, "{0}s".format(self.type.lower()))

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