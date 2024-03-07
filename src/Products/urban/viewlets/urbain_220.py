# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.urban.config import NIS
from Products.urban.interfaces import IToUrbain220Street
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from StringIO import StringIO

from eea.facetednavigation.interfaces import IFacetedNavigable

from collective.eeafaceted.dashboard.utils import getDashboardQueryResult
from collective.eeafaceted.dashboard.utils import getCriterionByIndex

from plone import api
from plone.app.layout.viewlets import ViewletBase

from zope.component import getAdapter
from zope.interface import implements
from zope.i18n import translate
from Products.urban import UrbanMessage as _

import json
import unidecode


class Urbain220Viewlet(ViewletBase):
    """For displaying on dashboards."""

    render = ViewPageTemplateFile("./templates/urbain_220.pt")

    def available(self):
        """
        This viewlet is only visible on buildlicences faceted view if we queried by date.
        """
        allowed_contexts = [
            "urban",
            "article127s",
            "buildlicences",
            "declarations",
            "integratedlicences",
            "uniquelicences",
            "preliminarynotices",
            "codt_article127s",
            "codt_buildlicences",
            "codt_integratedlicences",
            "codt_uniquelicences",
        ]
        allowed = self.context.id in allowed_contexts
        faceted_context = bool(IFacetedNavigable.providedBy(self.context))
        return faceted_context and allowed and self.get_date_range()

    def get_date_range(self):
        """
        Return the faceted query date range.
        """
        criterion = getCriterionByIndex(self.context, u"getDecisionDate")
        if not criterion:
            return
        decisiondate_id = "{}[]".format(criterion.getId())
        date_range = self.request.get(decisiondate_id, None)
        return date_range

    def get_links_info(self):
        base_url = self.context.absolute_url()
        output_format = "xml"
        url = "{base_url}/generate_urbain_220xml?output_format={output_format}".format(
            base_url=base_url, output_format=output_format
        )
        link = {
            "link": url,
            "title": "Liste 220",
            "output_format": output_format,
            "template_uid": "",
        }
        return [link]


class LicenceToUrbain220Street(object):
    """ """

    implements(IToUrbain220Street)

    def __init__(self, licence):
        catalog = api.portal.get_tool("portal_catalog")
        addresses = licence.getWorkLocations()
        first_address = addresses and addresses[0]
        street_brain = catalog(UID=first_address["street"])
        self.first_street = street_brain and street_brain[0].getObject()
        self.street_number = first_address["number"]

    @property
    def street_name(self):
        return self.first_street and self.first_street.getStreetName()

    @property
    def street_code(self):
        return self.first_street.getStreetCode()


class UrbainXMLExport(BrowserView):
    def __call__(self):
        datefrom, dateto = self.get_date_range()
        brains = getDashboardQueryResult(self.context)
        return self.generateUrbainXML(brains, datefrom, dateto)

    def get_date_range(self):
        faceted_query = self.request.get("facetedQuery", None)
        if faceted_query:
            query = json.JSONDecoder().decode(faceted_query)
            criterion = getCriterionByIndex(self.context, u"getDecisionDate")
            decisiondate_id = criterion.getId()
            date_range = query.get(decisiondate_id)
            date_range = [DateTime(date) for date in date_range]
            return date_range

    def _set_header_response(self):
        """
        Tell the browser that the resulting page contains ODT.
        """
        portal_urban = api.portal.get_tool("portal_urban")
        townshipname = portal_urban.getCityName()
        from_date, to_date = self.get_date_range()
        response = self.request.RESPONSE
        response.setHeader("Content-type", "text/xml")
        response.setHeader(
            "Content-disposition",
            u'attachment;filename="urbain_{name}_{from_date}-{to_date}.xml"'.format(
                name=unidecode.unidecode(townshipname.decode("utf-8")),
                from_date=from_date.strftime("%d_%m_%Y"),
                to_date=to_date.strftime("%d_%m_%Y"),
            ),
        )

    def generateUrbainXML(self, licence_brains, datefrom, dateto):
        def reverseDate(date):
            split = date.split("/")
            for i in range(len(split)):
                if len(split[i]) == 1:
                    split[i] = "0%s" % split[i]
            split.reverse()
            return "/".join(split)

        def check(self, condition, error_message, mapping):
            if not condition:
                tr_error_message = translate(
                    error_message,
                    domain=u"urban",
                    mapping=mapping,
                    context=self.context.REQUEST,
                )
                error.append(tr_error_message)
            return condition

        xml = []
        error = []
        html_list = []
        xml.append('<?xml version="1.0" encoding="iso-8859-1"?>')
        xml.append("<dataroot>")
        xml.append("  <E_220_herkomst>")
        xml.append("    <E_220_NIS_Gem>%s</E_220_NIS_Gem>" % NIS)
        xml.append(
            "    <E_220_Periode_van>%s</E_220_Periode_van>"
            % datefrom.strftime("%Y%m%d")
        )
        xml.append(
            "    <E_220_Periode_tot>%s</E_220_Periode_tot>" % dateto.strftime("%Y%m%d")
        )
        xml.append("    <E_220_ICT>COM</E_220_ICT>")
        xml.append("  </E_220_herkomst>")
        html_list.append("<HTML><TABLE>")
        for licence_brain in licence_brains:
            licence = licence_brain.getObject()
            try:
                licence.title.encode("iso-8859-1")
            except UnicodeEncodeError:
                check(
                    self,
                    False,
                    u"title_encoding_error_label",
                    {"reference": str(licence.getReference())},
                )
                continue
            applicantObj = (
                licence.getApplicants() and licence.getApplicants()[0] or None
            )
            architects = (
                licence.getField("architects") and licence.getArchitects() or []
            )
            if api.content.get_state(licence) in ["accepted", "authorized"]:
                html_list.append(
                    "<TR><TD>%s  %s</TD><TD>%s</TD></TR>"
                    % (
                        str(licence.getReference()),
                        licence.title.encode("iso-8859-1"),
                        str(licence_brain.getDecisionDate),
                    )
                )
                xml.append("  <Item220>")
                xml.append(
                    "      <E_220_Ref_Toel>%s</E_220_Ref_Toel>"
                    % str(licence.getReference())
                )
                parcels = licence.getParcels()
                if check(
                    self,
                    parcels,
                    u"no_parcels_found_on_licence",
                    {"reference": str(licence.getReference())},
                ):
                    xml.append(
                        "      <Doc_Afd>%s</Doc_Afd>" % parcels[0].getDivisionCode()
                    )

                if check(
                    self,
                    licence.getWorkLocations(),
                    u"no_address_found_on_licence",
                    {"reference": str(licence.getReference())},
                ):
                    street_info = getAdapter(licence, IToUrbain220Street)
                    number = street_info.street_number
                    street_name = street_info.street_name
                    street_code = street_info.street_code
                    if check(
                        self,
                        street_code,
                        u"no_street_with_code_found_on_licence",
                        {"reference": str(licence.getReference())},
                    ):
                        xml.append(
                            "      <E_220_straatcode>%s</E_220_straatcode>"
                            % str(street_code)
                        )
                        if check(
                            self,
                            street_name,
                            u"no_street_name_found_on_licence",
                            {"reference": str(licence.getReference())},
                        ):
                            xml.append(
                                "      <E_220_straatnaam>%s</E_220_straatnaam>"
                                % str(street_name)
                                .decode("iso-8859-1")
                                .encode("iso-8859-1")
                            )
                    if number:
                        xml.append(
                            "      <E_220_huisnr>%s</E_220_huisnr>" % str(number)
                        )
                worktype = licence.getWorkType() and licence.getWorkType()[0] or ""
                work_types = UrbanVocabulary("folderbuildworktypes").getAllVocTerms(
                    licence
                )
                worktype_map = {}
                for k, v in work_types.iteritems():
                    worktype_map[k] = v.getExtraValue()
                xml_worktype = ""
                if check(
                    self,
                    worktype in worktype_map.keys(),
                    u"unknown_worktype_on_licence",
                    {"worktype": worktype, "reference": str(licence.getReference())},
                ):
                    xml_worktype = worktype_map[worktype]
                xml.append("      <E_220_Typ>%s</E_220_Typ>" % xml_worktype)
                xml.append(
                    "      <E_220_Werk>%s</E_220_Werk>"
                    % licence.licenceSubject.encode("iso-8859-1")
                )
                strDecisionDate = str(licence_brain.getDecisionDate)
                xml.append(
                    "      <E_220_Datum_Verg>%s%s%s</E_220_Datum_Verg>"
                    % (
                        strDecisionDate[0:4],
                        strDecisionDate[5:7],
                        strDecisionDate[8:10],
                    )
                )
                authority = "COM"
                if licence.portal_type in ["Article127", "CODT_Article127"]:
                    authority = "REGION"
                else:
                    if hasattr(licence, "getAuthority"):
                        auth_map = {"college": "COM", "ft": "REGION", "fd_ft": "REGION"}
                        authority = auth_map[licence.getAuthority()]
                    elif licence.getLastRecourse():
                        authority = "MINISTRE"
                xml.append("      <E_220_Instan>%s</E_220_Instan>" % authority)
                if check(
                    self,
                    applicantObj,
                    u"no_applicant_found_on_licence",
                    {"reference": str(licence.getReference())},
                ):
                    firstname = (
                        applicantObj.portal_type == "Corporation"
                        and applicantObj.getDenomination()
                        or applicantObj.getName1()
                    )
                    lastname = (
                        applicantObj.portal_type == "Corporation"
                        and applicantObj.getLegalForm()
                        or applicantObj.getName2()
                    )
                    xml.append("      <PERSOON>")
                    xml.append(
                        "        <naam>%s %s</naam>"
                        % (
                            firstname.decode("iso-8859-1").encode("iso-8859-1"),
                            lastname.decode("iso-8859-1").encode("iso-8859-1"),
                        )
                    )
                    xml.append(
                        "        <straatnaam>%s</straatnaam>"
                        % applicantObj.getStreet()
                        .decode("iso-8859-1")
                        .encode("iso-8859-1")
                    )
                    xml.append("        <huisnr>%s</huisnr>" % applicantObj.getNumber())
                    xml.append(
                        "        <postcode>%s</postcode>" % applicantObj.getZipcode()
                    )
                    xml.append(
                        "        <gemeente>%s</gemeente>"
                        % applicantObj.getCity()
                        .decode("iso-8859-1")
                        .encode("iso-8859-1")
                    )
                    xml.append("        <hoedanig>DEMANDEUR</hoedanig>")
                    xml.append("      </PERSOON>")
                    if architects:
                        architectObj = architects[0]
                        list_architects_terms = [
                            "NON REQUIS",
                            "lui-meme",
                            "Eux-memes",
                            "elle-meme",
                            "lui-meme",
                            "lui-même",
                            "lui-meme ",
                            "Lui-meme",
                            "A COMPLETER ",
                        ]
                        if architectObj.getName1() in list_architects_terms:
                            xml.append("      <PERSOON>")
                            xml.append(
                                "        <naam>%s %s</naam>"
                                % (
                                    firstname.decode("iso-8859-1").encode("iso-8859-1"),
                                    lastname.decode("iso-8859-1").encode("iso-8859-1"),
                                )
                            )
                            xml.append(
                                "        <straatnaam>%s</straatnaam>"
                                % applicantObj.getStreet()
                                .decode("iso-8859-1")
                                .encode("iso-8859-1")
                            )
                            xml.append(
                                "        <huisnr>%s</huisnr>" % applicantObj.getNumber()
                            )
                            xml.append(
                                "        <postcode>%s</postcode>"
                                % applicantObj.getZipcode()
                            )
                            xml.append(
                                "        <gemeente>%s</gemeente>"
                                % applicantObj.getCity()
                                .decode("iso-8859-1")
                                .encode("iso-8859-1")
                            )
                            xml.append("        <hoedanig>ARCHITECTE</hoedanig>")
                            xml.append("      </PERSOON>")
                        else:
                            xml.append("      <PERSOON>")
                            xml.append(
                                "        <naam>%s %s</naam>"
                                % (
                                    architectObj.getName1()
                                    .decode("iso-8859-1")
                                    .encode("iso-8859-1"),
                                    architectObj.getName2()
                                    .decode("iso-8859-1")
                                    .encode("iso-8859-1"),
                                )
                            )
                            xml.append(
                                "        <straatnaam>%s</straatnaam>"
                                % architectObj.getStreet()
                                .decode("iso-8859-1")
                                .encode("iso-8859-1")
                            )
                            xml.append(
                                "        <huisnr>%s</huisnr>" % architectObj.getNumber()
                            )
                            xml.append(
                                "        <postcode>%s</postcode>"
                                % architectObj.getZipcode()
                            )
                            xml.append(
                                "        <gemeente>%s</gemeente>"
                                % architectObj.getCity()
                                .decode("iso-8859-1")
                                .encode("iso-8859-1")
                            )
                            xml.append("        <hoedanig>ARCHITECTE</hoedanig>")
                            xml.append("      </PERSOON>")
                for prc in parcels:
                    xml.append("      <PERCELEN>")
                    try:
                        strRadical = "%04d" % float(prc.getRadical())
                    except:
                        strRadical = "0000"
                    try:
                        strPuissance = "%03d" % float(prc.getPuissance())
                    except:
                        strPuissance = "000"
                    try:
                        strBis = "%02d" % float(prc.getBis())
                    except:
                        strBis = "00"
                    xml.append(
                        "        <E_220_percid>%s_%s_%s_%s_%s_%s</E_220_percid>"
                        % (
                            prc.getDivisionCode(),
                            prc.getSection(),
                            strRadical,
                            prc.getExposant(),
                            strPuissance,
                            strBis,
                        )
                    )
                    xml.append(
                        "        <kadgemnr>%s</kadgemnr>" % prc.getDivisionCode()
                    )
                    xml.append("        <sectie>%s</sectie>" % prc.getSection())
                    xml.append("        <grondnr>%s</grondnr>" % prc.getRadical())
                    if prc.getExposant() != "":
                        xml.append(
                            "        <exponent>%s</exponent>" % prc.getExposant()
                        )
                    if prc.getPuissance() != "":
                        xml.append("        <macht>%s</macht>" % prc.getPuissance())
                    if prc.getBis() != "":
                        xml.append("        <bisnr>%s</bisnr>" % prc.getBis())
                    xml.append("      </PERCELEN>")
                xml.append("  </Item220>")
        html_list.append("</TABLE></HTML>")
        xml.append("</dataroot>")
        if error != []:
            return "Error in these licences: \n%s" % "\n".join(error)
        else:
            site = api.portal.get()
            response = site.REQUEST.RESPONSE
            response.setHeader("Content-type", "text/plain;;charset=iso-8859-1")
            output = StringIO()
            chain = []
            for line in xml:
                chain.append(
                    unicode(str(line).replace("&", "&amp;"), "iso-8859-1").encode(
                        "iso-8859-1"
                    )
                )
            output.write("\n".join(chain))
            self._set_header_response()
            return output.getvalue()
