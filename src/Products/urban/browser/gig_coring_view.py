# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from Products.urban.services import gig
from datetime import datetime
from datetime import timedelta
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import urllib
import os
import hashlib


def generate_tokens(context):
    """Return the valid tokens to validate the response
    This token is based on the context, a secret and the current date"""
    secret = os.getenv("GIG_SECRET", "GIG_SECRET")
    now = datetime.now()
    tokens = []
    for i in range(-1, 1):
        date = now + timedelta(days=i)
        token = hashlib.md5(
            "{0}{1}{2}".format(
                context.UID(),
                secret,
                date.strftime("%Y-%m-%d"),
            ),
        ).hexdigest()
        tokens.append(token)
    return tokens


class GigCoringView(BrowserView):
    """
    view to send parcels id and connect to gig interface
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def open_gig_and_load_parcels(self):
        licence = self.context
        capakeys = [
            urllib.quote(parcel.capakey, safe="") for parcel in licence.getParcels()
        ]
        gig_url = "{}?matrices={}&post_carottage={}/gig_coring_response/{}".format(
            gig.url,
            ",".join(capakeys),
            urllib.quote(licence.absolute_url(), safe=""),
            generate_tokens(self.context)[-1],
        )
        return self.request.RESPONSE.redirect(gig_url)


@implementer(IPublishTraverse)
class GigCoringResponse(BrowserView):
    """
    Store coring result on coringResult field of the licence.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.params = []

    def publishTraverse(self, request, token):
        self.params.append(token)
        return self

    @property
    def _token(self):
        if len(self.params) != 1:
            raise Exception(
                "Must supply exactly one parameter (dotted name of"
                "the record to be retrieved)"
            )

        return self.params[0]

    def _validate_token(self):
        valid_tokens = generate_tokens(self.context)
        return self._token in valid_tokens

    def __call__(self, **kwargs):
        if self._validate_token() is False:
            self.request.RESPONSE.setStatus(
                401,
                reason="You are not allowed to perform this action",
                lock=True,
            )
            return

        self.request.RESPONSE.setHeader(
            "Access-Control-Allow-Origin", self.request.get("HTTP_ORIGIN")
        )
        self.request.RESPONSE.setHeader(
            "Access-Control-Allow-Headers", "content-type,x-requested-with"
        )
        self.request.RESPONSE.setHeader("Access-Control-Allow-Methods", "POST, PATCH")
        if self.request.get("REQUEST_METHOD") == "OPTIONS":
            self.request.RESPONSE.setStatus(204, reason="No Content", lock=True)
        else:
            self.context.setCoringResult(self.request["BODY"])
            self.request.RESPONSE.setStatus(204, reason="No Content", lock=True)
