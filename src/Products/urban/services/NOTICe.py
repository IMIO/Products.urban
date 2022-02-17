# -*- coding: utf-8 -*-

import datetime
import uuid

from requests import Session
from zeep import Client, Transport
from zeep.wsse import utils
from zeep.wsse.signature import BinarySignature


class NOTICeService(object):

    def __init__(self,
                 proxy_server,
                 notification_wsdl,
                 echo_wsdl,
                 licence_context,
                 organisation_id,
                 key_file,
                 cert_file,
                 bced_commune
                 ):
        """
        """

        self.proxy_server = proxy_server
        self.notification_wsdl = notification_wsdl
        self.echo_wsdl = echo_wsdl
        self.licence_context = licence_context
        self.organisation_id = organisation_id
        self.key_file = key_file
        self.cert_file = cert_file
        self.BCED_commune = bced_commune

        self.session = Session()
        self.session.proxies["https"] = proxy_server
        self.transport = Transport(session=self.session)

        self.spw_signature = SPWSignature(
            key_file=self.key_file,
            certfile=self.cert_file,
            signature_method=None,
            digest_method=None,
        )

    def echo(self):
        """ """
        secured_client = Client(
            self.echo_wsdl,
            transport=self.transport,
            wsse=self.spw_signature,
        )
        request_uuid = str(uuid.uuid4())
        result = secured_client.service.checkAccessControl(
            requestIdentification={
                "ticket": request_uuid,
                "timestampSent": datetime.datetime.now(),
            },
            privacyLog={
                "context": self.licence_context,
                "treatmentManagerNumber": "71062731718",  # ou "civilServantIdentifier": "71062731718",
            },
            request="Bonjour tout le monde !!!",
        )
        return result

    @property
    def customer_informations(self):
        """
        """
        request_uuid = str(uuid.uuid4())
        customer_informations = {
            "ticket": request_uuid,
            "timestampSent": datetime.datetime.now(),
            "customerIdentification": {
                "organisationId": "IMIO",
            },
        }
        return customer_informations

    @property
    def privacy_log(self):
        privacy_log = {
            "context": self.licence_context,
            "treatmentManagerIdentifier": {"identityManager": "RN/RBis"},
            # il FAUT cette ligne mais la valeurs n'a pas d'importance
            "dossier": {"dossierId": {"source": "valeur sans importance"}},
        }
        return privacy_log

    def search_notifications(self, notif_type=[], status=''):
        """ """
        self.client = Client(self.notification_wsdl, transport=self.transport, wsse=self.spw_signature)

        result = self.client.service.searchNotification(
            customerInformations=self.customer_informations,
            privacyLog=self.privacy_log,
            request={
                "noticeInstanceId": self.BCED_commune,  # code BCED de la commune
                "status": 'EN_ATTENTE_REPONSE',
            },
        )
        return result

    def get_notification(self, notice_id):
        """ """
        self.client = Client(self.notification_wsdl, transport=self.transport, wsse=self.spw_signature)
        self.client.settings.strict = False

        result = self.client.service.getNotification(
            customerInformations=self.customer_informations,
            privacyLog=self.privacy_log,
            request={
                "noticeId": notice_id,  # id de la notification
            },
        )
        return result


class SPWSignature(BinarySignature):
    """
    Cette signature implémente la *Security Policy* du *SPW*.

    Elle consiste à rajouter dans le header un timestamp.
    Le payload ainsi que le timestamp doivent être signés.
    La requête et la réponse doivent être signées avec SHA256
    """

    def _create_timestamp_element(self):
        timestamp_element = utils.WSU.Timestamp()
        now_datetime = datetime.datetime.utcnow()
        expires_datetime = now_datetime + datetime.timedelta(minutes=10)
        elements = [
            utils.WSU.Created(now_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
            utils.WSU.Expires(expires_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")),
        ]
        timestamp_element.extend(elements)
        return timestamp_element

    def _add_timestamp_element(self, envelope):
        security = utils.get_security_header(envelope)
        security.append(self._create_timestamp_element())

    def apply(self, envelope, headers):
        self._add_timestamp_element(envelope)
        envelope, headers = super(SPWSignature, self).apply(envelope, headers)
        return envelope, headers

    def verify(self, envelope):  # remove verify
        return envelope
