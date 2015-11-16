# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from StringIO import StringIO

from eea.facetednavigation.interfaces import IFacetedNavigable

from imio.dashboard.utils import getDashboardQueryResult
from imio.dashboard.utils import getCriterionByIndex

from plone import api
from plone.app.layout.viewlets import ViewletBase

import json


class Urbain220Viewlet(ViewletBase):
    """For displaying on dashboards."""

    render = ViewPageTemplateFile('./templates/urbain_220.pt')

    def available(self):
        """
        This viewlet is only visible on buildlicences faceted view if we queried by date.
        """
        buildlicences = self.context.id == 'buildlicences'
        faceted_context = bool(IFacetedNavigable.providedBy(self.context))
        return faceted_context and buildlicences and self.get_date_range()

    def get_date_range(self):
        """
        Return the faceted query date range.
        """
        criterion = getCriterionByIndex(self.context, u'getDecisionDate')
        decisiondate_id = '{}[]'.format(criterion.getId())
        date_range = self.request.get(decisiondate_id, None)
        return date_range

    def get_links_info(self):
        base_url = self.context.absolute_url()
        output_format = 'xml'
        url = '{base_url}/generate_urbain_220xml?output_format={output_format}'.format(
            base_url=base_url,
            output_format=output_format
        )
        link = {'link': url, 'title': 'Liste 220', 'output_format': output_format, 'template_uid': ''}
        return [link]


class UrbainXMLExport(BrowserView):

    def __call__(self):
        dateto, datefrom = self.get_date_range()
        brains = getDashboardQueryResult(self.context)
        return self.generateUrbainXML(brains, datefrom, dateto)

    def get_date_range(self):
        faceted_query = self.request.get('facetedQuery', None)
        if faceted_query:
            query = json.JSONDecoder().decode(faceted_query)
            criterion = getCriterionByIndex(self.context, u'getDecisionDate')
            decisiondate_id = criterion.getId()
            date_range = query.get(decisiondate_id)
            date_range = [DateTime(date) for date in date_range]
            return date_range

    def _set_header_response(self):
        """
        Tell the browser that the resulting page contains ODT.
        """
        from_date, to_date = self.get_date_range()
        response = self.request.RESPONSE
        response.setHeader('Content-type', 'text/xml')
        response.setHeader(
            'Content-disposition',
            u'attachment;filename="urbain_export-{from_date}-{to_date}.xml"'.format(
                from_date=from_date.strftime('%d_%m_%Y'),
                to_date=to_date.strftime('%d_%m_%Y')
            )
        )

    def generateUrbainXML(self, licence_brains, datefrom, dateto):

        def reverseDate(date):
            split = date.split('/')
            for i in range(len(split)):
                if len(split[i]) == 1:
                    split[i] = '0%s' % split[i]
            split.reverse()
            return '/'.join(split)

        def check(condition, error_message):
            if not condition:
                error.append(error_message)
            return condition

        portal_urban = api.portal.get_tool('portal_urban')
        catalog = api.portal.get_tool('portal_catalog')

        xml = []
        error = []
        html_list = []
        xml.append('<?xml version="1.0" encoding="iso-8859-1"?>')
        xml.append('<dataroot>')
        xml.append('  <E_220_herkomst>')
        xml.append('    <E_220_NIS_Gem>%s</E_220_NIS_Gem>' % portal_urban.getNISNum())
        xml.append('    <E_220_Periode_van>%s</E_220_Periode_van>' % datefrom.strftime('%d%m%Y'))
        xml.append('    <E_220_Periode_tot>%s</E_220_Periode_tot>' % dateto.strftime('%d%m%Y'))
        xml.append('    <E_220_ICT>COM</E_220_ICT>')
        xml.append('  </E_220_herkomst>')
        html_list.append('<HTML><TABLE>')
        for licence_brain in licence_brains:
            licence = licence_brain.getObject()
            decision_event = licence.getLastTheLicence()
            applicantObj = licence.getApplicants() and licence.getApplicants()[0] or None
            architects = licence.getField('architects') and licence.getArchitects() or []
            if api.content.get_state(licence) == 'accepted':
                html_list.append(
                    '<TR><TD>%s  %s</TD><TD>%s</TD></TR>'
                    % (str(licence.getReference()), licence.title.encode('iso-8859-1'),
                    str(decision_event.getDecisionDate()))
                )
                xml.append('  <Item220>')
                xml.append('      <E_220_Ref_Toel>%s</E_220_Ref_Toel>' % str(licence.getReference()))
                parcels = licence.getParcels()
                if check(parcels, 'no parcels found on licence %s' % str(licence.getReference())):
                    xml.append('      <Doc_Afd>%s</Doc_Afd>' % parcels[0].getDivisionCode())
                street = number = None
                if licence.getWorkLocations():
                    number = licence.getWorkLocations()[0]['number']
                    street = catalog.searchResults(UID=licence.getWorkLocations()[0]['street'])
                if check(street, 'no street found on licence %s' % str(licence.getReference())):
                    street = street[0].getObject()
                    xml.append('      <E_220_straatcode>%s</E_220_straatcode>' % str(street.getStreetCode()))
                    xml.append('      <E_220_straatnaam>%s</E_220_straatnaam>' % str(street.getStreetName()).decode('iso-8859-1').encode('iso-8859-1'))
                if number:
                    xml.append('      <E_220_huisnr>%s</E_220_huisnr>' % number)
                worktype = licence.getWorkType() and licence.getWorkType()[0] or ''
                work_types = UrbanVocabulary('folderbuildworktypes').getAllVocTerms(licence)
                worktype_map = {}
                for k, v in work_types.iteritems():
                    worktype_map[k] = v.getExtraValue()
                xml_worktype = ''
                if check(worktype in worktype_map.keys(), 'unknown worktype %s on licence %s' % (worktype, str(licence.getReference()))):
                    xml_worktype = worktype_map[worktype]
                xml.append('      <E_220_Typ>%s</E_220_Typ>' % xml_worktype)
                xml.append('      <E_220_Werk>%s</E_220_Werk>' % licence.licenceSubject.encode('iso-8859-1'))
                strDecisionDate = str(decision_event.getDecisionDate())
                xml.append('      <E_220_Datum_Verg>%s%s%s</E_220_Datum_Verg>' % (strDecisionDate[0: 4], strDecisionDate[5: 7], strDecisionDate[8: 10]))
                xml.append('      <E_220_Instan>COM</E_220_Instan>')
                xml.append('      <PERSOON>')
                xml.append('        <naam>%s %s</naam>' % (applicantObj.getName1().decode('iso-8859-1').encode('iso-8859-1'), applicantObj.getName2().decode('iso-8859-1').encode('iso-8859-1')))
                xml.append('        <straatnaam>%s</straatnaam>' % applicantObj.getStreet().decode('iso-8859-1').encode('iso-8859-1'))
                xml.append('        <huisnr>%s</huisnr>' % applicantObj.getNumber())
                xml.append('        <postcode>%s</postcode>' % applicantObj.getZipcode())
                xml.append('        <gemeente>%s</gemeente>' % applicantObj.getCity().decode('iso-8859-1').encode('iso-8859-1'))
                xml.append('        <hoedanig>DEMANDEUR</hoedanig>')
                xml.append('      </PERSOON>')
                if architects:
                    architectObj = architects[0]
                    list_architects_terms = ["NON REQUIS", "lui-meme", "Eux-memes", "elle-meme", "lui-meme", "lui-même", "lui-meme ", "Lui-meme", "A COMPLETER "]
                    if architectObj.getName1() in list_architects_terms:
                        xml.append('      <PERSOON>')
                        xml.append('        <naam>%s %s</naam>'
                                   % (applicantObj.getName1().encode('iso-8859-1'), applicantObj.name2.encode('iso-8859-1')))
                        xml.append('        <straatnaam>%s</straatnaam>' % applicantObj.getStreet().encode('iso-8859-1'))
                        xml.append('        <huisnr>%s</huisnr>' % applicantObj.getNumber())
                        xml.append('        <postcode>%s</postcode>' % applicantObj.getZipcode())
                        xml.append('        <gemeente>%s</gemeente>' % applicantObj.getCity().encode('iso-8859-1'))
                        xml.append('        <hoedanig>ARCHITECTE</hoedanig>')
                        xml.append('      </PERSOON>')
                    else:
                        xml.append('      <PERSOON>')
                        xml.append('        <naam>%s %s</naam>'
                                   % (architectObj.getName1().decode('iso-8859-1').encode('iso-8859-1'), architectObj.getName2().decode('iso-8859-1').encode('iso-8859-1')))
                        xml.append('        <straatnaam>%s</straatnaam>' % architectObj.getStreet().decode('iso-8859-1').encode('iso-8859-1'))
                        xml.append('        <huisnr>%s</huisnr>' % architectObj.getNumber())
                        xml.append('        <postcode>%s</postcode>' % architectObj.getZipcode())
                        xml.append('        <gemeente>%s</gemeente>' % architectObj.getCity().decode('iso-8859-1').encode('iso-8859-1'))
                        xml.append('        <hoedanig>ARCHITECTE</hoedanig>')
                        xml.append('      </PERSOON>')
                for prc in parcels:
                    xml.append('      <PERCELEN>')
                    try:
                        strRadical = '%04d' % float(prc.getRadical())
                    except:
                        strRadical = '0000'
                    try:
                        strPuissance = '%03d' % float(prc.getPuissance())
                    except:
                        strPuissance = '000'
                    try:
                        strBis = '%02d' % float(prc.getBis())
                    except:
                        strBis = '00'
                    xml.append('        <E_220_percid>%s_%s_%s_%s_%s_%s</E_220_percid>'
                               % (prc.getDivisionCode(), prc.getSection(), strRadical, prc.getExposant(), strPuissance, strBis))
                    xml.append('        <kadgemnr>%s</kadgemnr>' % prc.getDivisionCode())
                    xml.append('        <sectie>%s</sectie>' % prc.getSection())
                    xml.append('        <grondnr>%s</grondnr>' % prc.getRadical())
                    if prc.getExposant() != '':
                        xml.append('        <exponent>%s</exponent>' % prc.getExposant())
                    if prc.getPuissance() != '':
                        xml.append('        <macht>%s</macht>' % prc.getPuissance())
                    if prc.getBis() != '':
                        xml.append('        <bisnr>%s</bisnr>' % prc.getBis())
                    xml.append('      </PERCELEN>')
                xml.append('  </Item220>')
        html_list.append('</TABLE></HTML>')
        xml.append('</dataroot>')
        if error != []:
            return 'Error in these licences: \n%s' % '\n'.join(error)
        else:
            output = StringIO()
            output.write(unicode('\n'.join(xml).replace("&", "&amp;"), 'iso-8859-1').encode('iso-8859-1'))
            self._set_header_response()
            return output.getvalue()
