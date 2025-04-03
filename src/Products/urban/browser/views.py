# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from Products.Five import BrowserView
from Acquisition import aq_inner, aq_base
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.urban import config
from Products.urban.cartography import config as carto_config
from Products.urban import services
from Products.urban.utils import getMd5Signature
from urlparse import urlparse

from plone import api

import logging
import urllib
import urllib2
import xml.etree.ElementTree as ET
import socket

logger = logging.getLogger("urban: Views")

namespaces = {"ctx": "http://www.opengis.net/context"}

ET.register_namespace("", "http://www.opengis.net/context")
ET.register_namespace("ol", "http://openlayers.org/context")


class WMC(BrowserView):
    def minx(self):
        return self.xmin

    def miny(self):
        return self.ymin

    def maxx(self):
        return self.xmax

    def maxy(self):
        return self.ymax

    def parseWMC(self, mapUrl):
        url = mapUrl
        conn = urllib2.urlopen(url, timeout=6)
        swmc = ET.fromstring(conn.read())

        bbox = swmc.find(".//ctx:BoundingBox", namespaces)
        bbox.set("SRS", "EPSG:31370")
        bbox.set("minx", str(self.xmin))
        bbox.set("miny", str(self.ymin))
        bbox.set("maxx", str(self.xmax))
        bbox.set("maxy", str(self.ymax))

        for srs in swmc.findall(".//ctx:SRS", namespaces):
            srs.text = "EPSG:31370"

        for layer in swmc.findall(".//ctx:Layer", namespaces):
            ext = ET.Element("Extension")
            isBase = ET.SubElement(ext, "{http://openlayers.org/context}isBaseLayer")
            isBase.text = "false"
            transparent = ET.SubElement(
                ext, "{http://openlayers.org/context}transparent"
            )
            transparent.text = "true"
            layer.append(ext)

        return ET.tostring(swmc)

    def getLayers(self):
        tool = api.portal.get_tool("portal_urban")
        defaulturl = carto_config.geoserver.get("wms_url")
        """
        Samples:
        layers = [
                {'url' : defaulturl, 'srs':'EPSG:31370', 'title':'N° de parcelle', 'name' : '', ':canu', 'format':'image/png', 'style':'ParcelsNum', 'hidden': 0},
                ]
        """
        layers = []
        for additional_layer in tool.additional_layers.objectValues():
            if additional_layer.getWMSUrl() == "":
                url = defaulturl
            else:
                url = additional_layer.getWMSUrl()
            hidden = 1
            if additional_layer.getVisibility():
                hidden = 0
            layers.append(
                {
                    "url": url,
                    "srs": additional_layer.getSRS(),
                    "title": additional_layer.Title,
                    "name": additional_layer.getLayers(),
                    "format": additional_layer.getLayerFormat(),
                    "style": additional_layer.getStyles(),
                    "hidden": hidden,
                    "transparency": additional_layer.getTransparency()
                    and "true"
                    or "false",
                    "queryable": additional_layer.getQueryable() and "1" or "0",
                }
            )
        return layers

    def wmc(self):
        """
        Initialize the map on element
        if no context get the map coordinates from config
        """
        urbantool = api.portal.get_tool("portal_urban")
        context = aq_inner(self.context)
        if not hasattr(aq_base(context), "getParcels"):
            try:
                extent = [
                    coord.strip()
                    for coord in config.URBANMAP_CFG.urbanmap.get(
                        "map_coordinates", ""
                    ).split(",")
                ]
                self.xmin = extent[0]
                self.ymin = extent[1]
                self.xmax = extent[2]
                self.ymax = extent[3]
            except:
                pass
        else:
            parcels = self.context.getParcels()
            if parcels:
                cadastre = services.cadastre.new_session()
                result = cadastre.query_parcels_coordinates(parcels)
                cadastre.close()
                try:
                    self.xmin = result[0]
                    self.ymin = result[1]
                    self.xmax = result[2]
                    self.ymax = result[3]
                except:
                    pass

        geonodeMapUrl = urbantool.getMapUrl()
        if geonodeMapUrl:
            return self.parseWMC(geonodeMapUrl)

        else:
            self.tmpl = ViewPageTemplateFile("wmc.pt")
            return self.tmpl(self)


class ProxyController(BrowserView):
    # todo check and put correct autorize domain
    allowed_domains = [
        "localhost:8081",
        "localhost:8082",
        "localhost:8083",
        "localhost:8084",
        "localhost:8085",
        "localhost:8086",
        "geoservices.wallonie.be",
        "ccff02.minfin.fgov.be",
        "sig.spge.be",
    ]
    # todo check and put correct unautorize ip
    blocked_networks = [
        "127.",  # 127.0.0.0/8 (localhost)
        "10.",  # 10.0.0.0/8 (private network)
        "192.168.",  # 192.168.0.0/16 (private network)
        "169.254.",  # 169.254.0.0/16 (link-local)
        "172.16.",
        "172.17.",
        "172.18.",
        "172.19.",
        "172.20.",
        "172.21.",
        "172.22.",
        "172.23.",
        "172.24.",
        "172.25.",
        "172.26.",
        "172.27.",
        "172.28.",
        "172.29.",
        "172.30.",
        "172.31.",
    ]

    def is_internal_address(self, host):
        """Check if the hostname resolves to an internal/private IP."""
        try:
            ip = socket.gethostbyname(host)
            return any(ip.startswith(prefix) for prefix in self.blocked_networks)
        except Exception:
            return False  # If we can't resolve the host, assume it's not internal

    def getProxy(self):
        try:
            url = self.request.get("url")
            if not url:
                return self.request.response.setStatus(400, "Bad Request: Missing URL")

            parsed_url = urlparse(url)
            # Ensure the domain is in the allowed list
            if parsed_url.netloc not in self.allowed_domains:
                logger.error("Blocked access to disallowed domain: %s" % url)
                raise Unauthorized("Access denied")

            # Prevent internal/private network access
            if self.is_internal_address(parsed_url.hostname):
                logger.error("Blocked access to internal IP: %s" % url)
                raise Unauthorized("Access denied")

            params = self.request.form.copy()
            params.pop("url")

            self.request.response.setHeader("content-type", "text/json")

            if params:
                url = "{}?{}".format(url, urllib.urlencode(params))

            conn = urllib2.urlopen(url, timeout=6)
            data = conn.read()
            conn.close()
            return data

        except Unauthorized as e:
            return self.request.response.setStatus(403, "Forbidden: %s" % str(e))

        except Exception as msg:
            logger.error("Cannot open url '%s': %s" % (url, msg))
            return self.request.response.setStatus(500, "Internal Server Error")


class testmap(ProxyController):
    pass


class TemplatesSummary(BrowserView):
    """
    Get all templates information to give a summary
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.tool = api.portal.get_tool("portal_urban")
        self.tot_count = 0
        self.mod_count = 0
        self.editicon = "edit.png"
        self.editlink = "edit"

    def getUrbanTemplate(self, folder):
        return folder.listFolderContents(
            contentFilter={"portal_type": ["UrbanTemplate"]}
        )

    def getGlobalTemplates(self):
        templates = ["globaltemplates"]
        for templ in self.getUrbanTemplate(self.tool.globaltemplates):
            templates.append({"o": templ, "s": self.isModified(templ)})
            self.tot_count += 1
        if len(templates) > 1 and templates[1]["o"].externalEditorEnabled():
            self.editicon = "extedit_icon.png"
            self.editlink = "external_edit"
        return templates

    def getEventsTemplates(self):
        # return something like [[urban_type1, [uet1, {doc1}, {doc2}, ...], [uet2, {doc3}, ...], ...], [urban_type2, [], ...], ...]
        templates = []
        for urban_type in config.URBAN_TYPES:
            templ_by_type = [urban_type]
            licenceConfigId = urban_type.lower()
            if not safe_hasattr(self.tool, licenceConfigId):
                continue
            configFolder = getattr(self.tool, licenceConfigId)
            if not safe_hasattr(configFolder, "eventconfigs"):
                continue
            for obj in configFolder.getEventConfigs():
                templ_by_event = [obj.Title()]
                for templ in self.getUrbanTemplate(obj):
                    self.tot_count += 1
                    templ_by_event.append({"o": templ, "s": self.isModified(templ)})
                templ_by_type.append(templ_by_event)
            templates.append(templ_by_type)
        return templates

    def isModified(self, template):
        if not template.hasProperty("md5Modified"):
            return "question-mark.png"
        if template.md5Modified != getMd5Signature(template.odt_file.data):
            # template manually changed
            self.mod_count += 1
            return "warning.png"
        return None
