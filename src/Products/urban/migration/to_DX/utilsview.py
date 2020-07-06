# -*- coding: utf-8 -*-

import logging

from datetime import datetime
from plone import api

from Products.Five import BrowserView

logger = logging.getLogger("urban: migrations utils")


class PortalTypesInfosView(BrowserView):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        catalog = api.portal.get_tool("portal_catalog")
        if "type" in self.request.form:
            type = self.request.form["type"]
        else:
            type = "log"
        portal_type = self.request.form["portal_type"]
        if type and portal_type:
            portal_types = [
                brain.getObject() for brain in catalog(portal_type=portal_type)
            ]

            if portal_types:
                if type == "log":
                    for portal_type in portal_types:
                        logger.info(portal_type.absolute_url())
                    logger.info("Portal type found : {}".format(len(portal_types)))
                if type == "csv":
                    with open(
                        "{}_{}.csv".format(
                            datetime.today().strftime("%Y_%m_%d_%H_%M_%S"), portal_type
                        ),
                        "a",
                    ) as file:
                        for portal_type in portal_types:
                            file.write(portal_type.absolute_url() + "\n")
            else:
                logger.info("Portal type not found in linked catalog")
