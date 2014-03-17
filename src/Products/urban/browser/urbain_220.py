# -*- coding: utf-8 -*-

from DateTime import DateTime
from StringIO import StringIO

from Products.Five import BrowserView

from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from plone import api


class UrbainXMLExport(BrowserView):

    def __call__(self):
        datefrom = self.request.form['datefrom']
        dateto = self.request.form['dateto']
        list_only = self.request.form.get('list_only', False)
        return self.generateUrbainXML(datefrom, dateto, list_only)

    def generateUrbainXML(self, datefrom, dateto, list_only):

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

        datefrom = reverseDate(datefrom)
        dateto = reverseDate(dateto)
        portal_urban = api.portal.get_tool('portal_urban')
        catalog = api.portal.get_tool('portal_catalog')
        pw = api.portal.get_tool('portal_workflow')
        results = catalog.searchResults(
            getDecisionDate={'query': (DateTime(datefrom), DateTime(dateto)), 'range': 'minmax'},
            object_provides='Products.urban.interfaces.ITheLicenceEvent',
            portal_type='UrbanEvent'
        )
        results = [brain.getObject() for brain in results if brain.getObject().aq_parent.portal_type in ['BuildLicence', ]]
        xml = []
        error = []
        html_list = []
        xml.append('<?xml version="1.0" encoding="iso-8859-1"?>')
        xml.append('<dataroot>')
        xml.append('  <E_220_herkomst>')
        xml.append('    <E_220_NIS_Gem>%s</E_220_NIS_Gem>' % portal_urban.getNISNum())
        xml.append('    <E_220_Periode_van>%s</E_220_Periode_van>' % datefrom.replace("/", ""))
        xml.append('    <E_220_Periode_tot>%s</E_220_Periode_tot>' % dateto.replace("/", ""))
        xml.append('    <E_220_ICT>COM</E_220_ICT>')
        xml.append('  </E_220_herkomst>')
        html_list.append('<HTML><TABLE>')
        for eventObj in results:
            licenceObj = eventObj.getParentNode()
            applicantObj = licenceObj.getApplicants() and licenceObj.getApplicants()[0] or None
            architects = licenceObj.getField('architects') and licenceObj.getArchitects() or []
            if pw.getInfoFor(licenceObj, 'review_state') == 'accepted':
                html_list.append(
                    '<TR><TD>%s  %s</TD><TD>%s</TD></TR>'
                    % (str(licenceObj.getReference()), licenceObj.title.encode('iso-8859-1'),
                    str(eventObj.getDecisionDate()))
                )
                xml.append('  <Item220>')
                xml.append('      <E_220_Ref_Toel>%s</E_220_Ref_Toel>' % str(licenceObj.getReference()))
                parcels = licenceObj.getParcels()
                if check(parcels, 'no parcels found on licence %s' % str(licenceObj.getReference())):
                    xml.append('      <Doc_Afd>%s</Doc_Afd>' % parcels[0].getDivisionCode())
                street = number = None
                if licenceObj.getWorkLocations():
                    number = licenceObj.getWorkLocations()[0]['number']
                    street = catalog.searchResults(UID=licenceObj.getWorkLocations()[0]['street'])
                if check(street, 'no street found on licence %s' % str(licenceObj.getReference())):
                    street = street[0].getObject()
                    xml.append('      <E_220_straatcode>%s</E_220_straatcode>' % str(street.getStreetCode()))
                    xml.append('      <E_220_straatnaam>%s</E_220_straatnaam>' % str(street.getStreetName()).decode('iso-8859-1').encode('iso-8859-1'))
                if number:
                    xml.append('      <E_220_huisnr>%s</E_220_huisnr>' % number)
                worktype = licenceObj.getWorkType() and licenceObj.getWorkType()[0] or ''
                work_types = UrbanVocabulary('folderbuildworktypes').getAllVocTerms(licenceObj)
                worktype_map = {}
                for k, v in work_types.iteritems():
                    worktype_map[k] = v.getExtraValue()
                xml_worktype = ''
                if check(worktype in worktype_map.keys(), 'unknown worktype %s on licence %s' % (worktype, str(licenceObj.getReference()))):
                    xml_worktype = worktype_map[worktype]
                xml.append('      <E_220_Typ>%s</E_220_Typ>' % xml_worktype)
                xml.append('      <E_220_Werk>%s</E_220_Werk>' % licenceObj.licenceSubject.encode('iso-8859-1'))
                strDecisionDate = str(eventObj.getDecisionDate())
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
        if list_only:
            output = StringIO()
            output.write(unicode('\n'.join(html_list).replace("&", "&amp;"), 'iso-8859-1').encode('iso-8859-1'))
            return output.getvalue()
        else:
            if error != []:
                return 'Error in these licences: \n%s' % '\n'.join(error)
            else:
                output = StringIO()
                output.write(unicode('\n'.join(xml).replace("&", "&amp;"), 'iso-8859-1').encode('iso-8859-1'))
                return output.getvalue()
