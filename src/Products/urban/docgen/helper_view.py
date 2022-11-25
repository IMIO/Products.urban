# -*- coding: utf-8 -*-

from collective.documentgenerator.helper.archetypes import ATDisplayProxyObject
from collective.documentgenerator.helper.archetypes import ATDocumentGenerationHelperView
from collective.documentgenerator.helper.dexterity import DXDocumentGenerationHelperView

from datetime import date as _date, datetime
from dateutil.relativedelta import relativedelta

from plone.dexterity.interfaces import IDexterityContent

from Products.Archetypes.interfaces import IBaseObject
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.urban.interfaces import IUrbanEventInquiry, IEnvironmentBase, ITicket, IBaseBuildLicence, \
    IUrbanCertificateBase
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import getCurrentFolderManager
from Products.urban.utils import get_ws_meetingitem_infos
from Products.urban.services import cadastre

from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from DateTime import DateTime

import re


class BaseHelperView(object):
    """
    Urban implementation of document generation helper methods.
    """

    @property
    def portal_urban(self):
        urban_tool = api.portal.get_tool('portal_urban')
        return urban_tool

    def __str__(self):
        return self.context.__str__()

    def __unicode__(self):
        return self.context.__unicode__()

    def __getattr__(self, attr_name):
        """
        """
        attr = getattr(self.context, attr_name)
        if callable(attr) and not attr_name.startswith('_'):
            def proxy_method(*args, **kwargs):
                result = getattr(self.real_context, attr_name)(*args, **kwargs)
                if IBaseObject.providedBy(result) or IDexterityContent.providedBy(result):
                    result_helper = result.unrestrictedTraverse('document_generation_helper_view')
                    result_helper.appy_renderer = self.appy_renderer
                    return result_helper
                elif type(result) in [list, set]:
                    new_result = []
                    for element in result:
                        if IBaseObject.providedBy(element) or IDexterityContent.providedBy(element):
                            element_helper = element.unrestrictedTraverse('document_generation_helper_view')
                            new_result.append(element_helper)
                        else:
                            new_result.append(element)
                    return new_result
                return result
            return proxy_method
        return attr

    def xhtml(self, html_code, style='UrbanBody'):
        urban_tool = api.portal.get_tool('portal_urban')
        decorated_html = urban_tool.decorateHTML(style, html_code)
        xhtml = self.appy_renderer.renderXhtml(decorated_html)
        return xhtml

    def get_current_foldermanager(self):
        return getCurrentFolderManager()

    def contains_road_equipment(self, road_equipment):
        roadEquipments = self.context.getRoadEquipments()
        answer = False
        for roadEquipment in roadEquipments:
            if roadEquipment['road_equipment'] == road_equipment:
                answer = True
        return answer

    def containsEvent(self, title=''):
        """
          find a specific title's UrbanEvent
        """
        return self.getEvent(title) is not None

    def display_date(self, field_name, long_format=False, translatemonth=True, custom_format=None):
        date = self.get_value(field_name)
        if custom_format:
            formatted_date = date.strftime(custom_format)
        else:
            formatted_date = self.format_date(date, long_format=long_format, translatemonth=translatemonth)
        return formatted_date

    def today(self):
        """
        """
        return _date.today()

    def add_years(self, zope_DT, years):
        """
        """
        if isinstance(zope_DT, _date):
            zope_DT = DateTime(datetime(zope_DT.year, zope_DT.month, zope_DT.day))
        return DateTime(zope_DT.asdatetime() + relativedelta(years=years))

    @staticmethod
    def uncapitalize(string):
        """
        """
        if not string:
            return ''
        if type(string) is unicode:
            return u'{}{}'.format(string.strip()[0].lower(), string.strip()[1:])
        elif type(string) is str:
            return '{}{}'.format(string.strip()[0].lower(), string.strip()[1:])

    def format_date(self, date=None, translatemonth=True, long_format=False):
        """
          Format the date for printing in pod templates
        """
        if not date:
            date = _date.today()
        if date.year == 9999:
            return u"\u221E"
        if not translatemonth:
            u_date = ulocalized_time(str(date), long_format=long_format, context=self, request=self.request)
            u_date = u_date and u_date.encode('utf8') or ''
            return u_date
        else:
            # we need to translate the month and maybe the day (1er)
            if isinstance(date, DateTime):
                year, month, day, hour = str(date.asdatetime().strftime('%Y/%m/%d/%Hh%M')).split('/')
            else:
                year, month, day, hour = str(date.strftime('%Y/%m/%d/%Hh%M')).split('/')
            # special case when the day need to be translated
            # for example in french '1' becomes '1er' but in english, '1' becomes '1st'
            # if no translation is available, then we use the default where me remove foregoing '0'
            # '09' becomes '9', ...
            daymsgid = "date_day_%s" % day
            translatedDay = translate(daymsgid, 'urban', context=self.request, default=day.lstrip('0')).encode('utf8')
            # translate the month
            # msgids already exist in the 'plonelocales' domain
            monthMappings = {
                '01': 'jan',
                '02': 'feb',
                '03': 'mar',
                '04': 'apr',
                '05': 'may',
                '06': 'jun',
                '07': 'jul',
                '08': 'aug',
                '09': 'sep',
                '10': 'oct',
                '11': 'nov',
                '12': 'dec',
            }
            monthmsgid = "month_%s" % monthMappings[month]
            translatedMonth = translate(monthmsgid, 'plonelocales', context=self.request).encode('utf8').lower()
        if long_format:
            at_hour = translate('at_hour', 'urban', mapping={'hour': hour}, context=self.request).encode('utf-8')
            return "%s %s %s %s" % (translatedDay, translatedMonth, year, at_hour)
        else:
            return "%s %s %s" % (translatedDay, translatedMonth, year)
        return ''

    def listVocTerms(self, field):
        """
        Deprecated/backward compatibility only
        See voc_terms
        """
        context = self.real_context
        field = context.getField(field)
        keys = type(field.getRaw(context)) in (list, tuple) and field.getRaw(context) or [field.getRaw(context)]
        objs = [field.vocabulary.getAllVocTerms(context).get(key, None) for key in keys]
        return objs

    def all_voc_terms(self, field_name='', with_coring_values=False):
        context = self.real_context
        field = context.getField(field_name)
        voc_terms = []
        if field.vocabulary:
            voc_terms = field.vocabulary.getAllVocTerms(context).values()
        elif field.vocabulary_factory:
            voc_utility = getUtility(IVocabularyFactory, field.vocabulary_factory)
            if with_coring_values:
                simple_voc = voc_utility(context)
                return simple_voc.by_value.values()
            else:
                voc_terms = voc_utility._get_config_vocabulary_values(context)

        voc_terms_proxy = []
        for v in voc_terms:
            voc_terms_view = v.unrestrictedTraverse('@@document_generation_helper_view')
            voc_terms_view.appy_renderer = self.appy_renderer
            voc_terms_proxy.append(voc_terms_view.context)
        return voc_terms_proxy

    def voc_terms(self, field_name='', with_coring_values=False):
        context = self.real_context
        all_voc_terms = self.all_voc_terms(field_name, with_coring_values)
        selected_values = context.getField(field_name).get(context)
        voc_terms = [t for t in all_voc_terms if getattr(t, 'id', getattr(t, 'value', None)) in selected_values]
        return voc_terms

    def voc_terms_id(self, field_name='', with_coring_values=False):
        voc_terms = self.voc_terms(field_name, with_coring_values)
        voc_terms_id = [voc_term.id for voc_term in voc_terms]
        return voc_terms_id

    def voc_term(self, field_name='', with_coring_values=False):
        context = self.real_context
        all_voc_terms = self.all_voc_terms(field_name, with_coring_values)
        selected_value = context.getField(field_name).get(context)
        if type(selected_value) in [list, tuple]:
            selected_value = selected_value[0]
        for term in all_voc_terms:
            term_value = hasattr(term, 'id') and term.id or term.value
            if term_value == selected_value:
                return term
        return None


class UrbanDocGenerationHelperView(ATDocumentGenerationHelperView, BaseHelperView):
    """
    Urban implementation of document generation helper methods.
    """

    def __init__(self, context, request):
        super(UrbanDocGenerationHelperView, self).__init__(context, request)
        self.context.helper_view = self


class DXUrbanDocGenerationHelperView(DXDocumentGenerationHelperView, BaseHelperView):
    """
    Urban implementation of document generation helper methods.
    """

    def __init__(self, context, request):
        super(DXUrbanDocGenerationHelperView, self).__init__(context, request)
        self.context.helper_view = self


class UrbanDocGenerationLicenceHelperView(UrbanDocGenerationHelperView):
    """
    """

    def get_checked_specific_features_id_list(self):
        """
        # Particularité(s) du bien
        """
        context = self.real_context
        specificFeatures = context.getSpecificFeatures()
        specific_features_id_list = []
        for specificFeature in specificFeatures:
            if specificFeature['check']:
                specific_features_id_list.append(specificFeature['id'])
        return specific_features_id_list

        proprietaries = [pro for pro in self.objectValues('Applicant') if pro.portal_type == 'Proprietary']
        return proprietaries

    def get_division(self):
        parcels = self.context.getParcels()
        parcel_view = parcels and parcels[0].unrestrictedTraverse('document_generation_helper_view')
        raw_div = parcel_view.context.division
        division = raw_div and raw_div[raw_div.find('(') + 1:-1] or 'DIVISION INCONNUE'
        return division

    def get_pca_dict(self):
        """
        # Plan Communal d'Aménagement
        """
        context = self.real_context
        pca = context.getField('pca').get(context)
        urbanConfig = context.getLicenceConfig()
        pca_config = urbanConfig.pcas
        pca_dict = {}
        if type(pca) == str:
            pcaTerm = getattr(pca_config, pca, '')
            pca_dict['title'] = pcaTerm.getTitle()
            pca_dict['label'] = pcaTerm.getLabel()
            pca_dict['number'] = pcaTerm.getNumber()
            pca_dict['decreeDate'] = pcaTerm.getDecreeDate()
            pca_dict['decreeType'] = pcaTerm.getDecreeDate()
            pca_dict['changes'] = pcaTerm.getChanges()
            pca_dict['comment'] = pcaTerm.getComment()
        return pca_dict

    def get_portion_outs_text(self, linebyline=False):
        """
          Return a displayable version of the parcels
        """
        toreturn = ''
        isFirst = True
        first_div = None
        first_section = None
        for portionOutObj in self.context.getParcels():
            # add a separator between every parcel
            # either a '\n'
            if not isFirst and linebyline:
                toreturn += '\n'
            # or an "and "
            elif not isFirst:
                toreturn += ', '
            elif isFirst:
                first_div = portionOutObj.getDivisionAlternativeName()
                toreturn += '%s ' % portionOutObj.getDivisionAlternativeName()
                first_section = portionOutObj.getSection()
                toreturn += 'section %s' % portionOutObj.getSection()
                toreturn += ' n° '.decode('utf8')
            else:
                if first_div != portionOutObj.getDivisionAlternativeName():
                    toreturn += '%s ' % portionOutObj.getDivisionAlternativeName()
                if first_section != portionOutObj.getSection():
                    toreturn += 'section %s ' % portionOutObj.getSection()
            toreturn += ' %s' % portionOutObj.getRadical()
            if portionOutObj.getBis() not in ['', '0']:
                toreturn += '/%s' % portionOutObj.getBis()
            toreturn += portionOutObj.getExposant()
            if portionOutObj.getPuissance() not in ['', '0']:
                toreturn += portionOutObj.getPuissance()
            isFirst = False
        return toreturn

    def get_proprietaries(self):
        """
           Return the list of proprietaries for the Licence
        """
        context = self.real_context
        proprietaries = [pro for pro in context.objectValues() if pro.portal_type.startswith('Proprietary')]
        return proprietaries

    def get_proprietaries_list_dict(self):
        proprietaries = self.get_proprietaries()
        proprietaries_list_dict = []
        for i in range(len(proprietaries)):
            proprietaries_list_dict.append(self.get_proprietary_dict(i))
        return proprietaries_list_dict

    def get_proprietaries_names(self, separator=', ', reversed_name=True):
        proprietaries = self.get_proprietaries_list_dict()
        proprietaries_names = ""
        if proprietaries:
            proprietaries_names = self.get_proprietary_names(proprietaries[0], reversed_name)
            for proprietary in proprietaries[1:]:
                proprietaries_names += separator + self.get_proprietary_names(proprietary, reversed_name)
        return proprietaries_names

    def get_proprietaries_names_and_address(self, separator=', ', reversed_name=True, resident=' domicilié '):
        proprietaries = self.get_proprietaries_list_dict()
        proprietaries_names_and_address = ""
        if proprietaries:
            proprietaries_names_and_address = self.get_proprietary_names_and_address(
                proprietaries[0],
                reversed_name,
                resident
            )
            for proprietary in proprietaries[1:]:
                proprietaries_names_and_address += separator + self.get_proprietary_names_and_address(
                    proprietary,
                    reversed_name,
                    resident
                )
        return proprietaries_names_and_address

    def get_proprietary_dict(self, index):
        proprietaries = self.get_proprietaries()
        proprietary_dict = {}
        if index < len(proprietaries):
            proprietary_dict = {}
            proprietary = self.get_proprietaries()[index]
            proprietary_dict['personTitle'] = proprietary.getPersonTitle()
            proprietary_dict['name1'] = proprietary.getName1()
            proprietary_dict['name2'] = proprietary.getName2()
            proprietary_dict['society'] = proprietary.getSociety()
            proprietary_dict['street'] = proprietary.getStreet()
            proprietary_dict['number'] = proprietary.getNumber()
            proprietary_dict['zipcode'] = proprietary.getZipcode()
            proprietary_dict['city'] = proprietary.getCity()
            proprietary_dict['country'] = proprietary.getCountry()
            proprietary_dict['email'] = proprietary.getEmail()
            proprietary_dict['phone'] = proprietary.getPhone()
            proprietary_dict['registrationNumber'] = proprietary.getRegistrationNumber()
            proprietary_dict['nationalRegister'] = proprietary.getNationalRegister()
        return proprietary_dict

    def get_proprietary_names(self, proprietary, reversed_name=True):
        proprietary_names = proprietary['personTitle'] + ' ' + proprietary['name2'] + ' ' + proprietary['name1']
        if reversed_name:
            proprietary_names = proprietary['personTitle'] + ' ' + proprietary['name1'] + ' ' + proprietary['name2']
        return proprietary_names

    def get_proprietary_names_and_address(self, proprietary, reversed_name=True, resident=' domicilié '):
        proprietary_names_and_address = \
            proprietary['personTitle'] + ' ' +\
            proprietary['name2'] + ' ' +\
            proprietary['name1'] + resident +\
            proprietary['street'] + ' ' +\
            proprietary['number'] + ' ' +\
            proprietary['zipcode'] + ' ' +\
            proprietary['city']
        if reversed_name:
            proprietary_names_and_address = \
                proprietary['personTitle'] + ' ' +\
                proprietary['name1'] + ' ' +\
                proprietary['name2'] + resident +\
                proprietary['street'] + ' ' +\
                proprietary['number'] + ' ' +\
                proprietary['zipcode'] + ' ' +\
                proprietary['city']
        return proprietary_names_and_address

    def get_subdivisionDetails(self):
        context = self.real_context
        subdivisionDetails = context.getSubdivisionDetails()
        return subdivisionDetails.lstrip('<p>').rstrip('</p>')

    def _get_street_dict(self, uid):
        street_dict = {}
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=uid)[0].getObject()
        street_dict['bestAddressKey'] = street.getBestAddressKey()
        street_dict['streetCode'] = street.getStreetCode()
        street_dict['streetName'] = street.getStreetName()
        street_dict['startDate'] = street.getStartDate()
        street_dict['endDate'] = street.getEndDate()
        street_dict['regionalRoad'] = street.getRegionalRoad()
        return street_dict

    def get_work_location_dict(self, index):
        """
        # Adresse(s) des travaux
        return a dictionary containing specific work locations informations
        """
        context = self.real_context
        workLocation = context.getWorkLocations()[index]
        work_location_dict = self._get_street_dict(workLocation['street'])
        work_location_dict.update({'number': workLocation['number']})
        return work_location_dict

    def get_work_locations_list_dict(self):
        """
        # Adresse(s) des travaux
        return a list of work locations informations
        """
        context = self.context
        workLocations = context.getWorkLocations()
        work_locations_list_dict = []
        for i in range(len(workLocations)):
            work_locations_list_dict.append(self.get_work_location_dict(i))
        return work_locations_list_dict

    def get_work_locations_signaletic(self, separator=', '):
        """
        # Adresse(s) des travaux
        return all street name and number
        """
        context = self.context
        workLocations = context.getWorkLocations()
        workLocation_signaletic = self.get_work_location_signaletic(workLocations[0])
        for workLocation in workLocations[1:]:
            workLocation_signaletic += separator + self.get_work_location_signaletic(workLocation)
        return workLocation_signaletic

    def get_work_location_signaletic(self, workLocation):
        """
        # Adresse(s) des travaux
        return a street name and number from a specific workLocation
        """
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=workLocation['street'])[0].getObject()
        number = workLocation['number']
        zipCode = street.aq_parent.zipCode
        locality = street.aq_parent.Title()
        return "{} {}, {} {}".format(street.getStreetName(), number, zipCode, locality)

    def getPortionOutsText(self, linebyline=False):
        """
          Return a displayable version of the parcels
        """
        toreturn = ''
        isFirst = True
        first_div = None
        first_section = None
        for portionOutObj in self.context.getParcels():
            # add a separator between every parcel
            # either a '\n'
            if not isFirst and linebyline:
                toreturn += '\n'
            # or an "and "
            elif not isFirst:
                toreturn += ', '
            elif isFirst:
                first_div = portionOutObj.getDivisionAlternativeName()
                toreturn += '%s ' % portionOutObj.getDivisionAlternativeName()
                first_section = portionOutObj.getSection()
                toreturn += 'section %s' % portionOutObj.getSection()
                toreturn += ' n° '.decode('utf8')
            else:
                if first_div != portionOutObj.getDivisionAlternativeName():
                    toreturn += '%s ' % portionOutObj.getDivisionAlternativeName()
                if first_section != portionOutObj.getSection():
                    toreturn += 'section %s ' % portionOutObj.getSection()
            toreturn += ' %s' % portionOutObj.getRadical()
            if portionOutObj.getBis() != '':
                if portionOutObj.getBis() != '0':
                    toreturn += '/%s ' % portionOutObj.getBis()
                else:
                    toreturn += ' '
            toreturn += portionOutObj.getExposant()
            if portionOutObj.getPuissance() != '' and portionOutObj.getPuissance() != '0':
                toreturn += ' %s' % portionOutObj.getPuissance()
            isFirst = False
        return toreturn

    def get_last_opinions_round(self):
        opinions = self._get_last_opinions('solicitOpinionsTo')
        return opinions

    def get_last_optional_opinions_round(self):
        opinions = self._get_last_opinions('solicitOpinionsToOptional')
        return opinions

    def _get_last_opinions(self, field_name):
        licence = self.context
        inquiries = licence._get_inquiry_objs(all_=True)
        if inquiries:
            last_inquiry = inquiries[-1]
            opinions = licence.getValuesForTemplate(field_name, obj=last_inquiry)
            return opinions
        return []

    def get_related_licences(self, licence_types=[], decision_limit_date=None, licence_state=None, with_historic=False):
        related_licences = [licence.getObject() for licence in self.get_related_licences_of_parcel(licence_types, with_historic)]

        if decision_limit_date:
            related_licences_decision_limit_date = []
            if not isinstance(decision_limit_date, DateTime):
                decision_limit_date = DateTime(decision_limit_date)
            for licence in related_licences:
                delivered = ''
                if IBaseBuildLicence.providedBy(licence) or IUrbanCertificateBase.providedBy(licence):
                    delivered = licence.getLastTheLicence()
                elif IEnvironmentBase.providedBy(licence):
                    delivered = licence.getLastLicenceDelivery()
                elif ITicket.providedBy(licence):
                    delivered = licence.getLastTheTicket()
                if delivered and ((delivered.getDecisionDate() or delivered.getEventDate()) >= decision_limit_date):
                    related_licences_decision_limit_date.append(licence)
            related_licences = related_licences_decision_limit_date

        if licence_state:
            licences = []
            for licence in related_licences:
                licence_review_state = api.content.get_state(obj=licence)
                if licence_review_state == licence_state:
                    licences.append(licence)
            related_licences = licences

        return related_licences

    def get_related_licences_of_parcel(self, licence_types=[], with_historic=False):
        """
          Returns the licences related to a parcel
        """
        context = self.context
        parcels = context.getParcels()
        relatedLicences = []
        licence_uids = set([])
        for parcel in parcels:
            for brain in parcel.getRelatedLicences(licence_type=licence_types, with_historic=with_historic):
                if brain.UID not in licence_uids:
                    relatedLicences.append(brain)
                    licence_uids.add(brain.UID)
        return relatedLicences

    def get_related_licences_titles_of_parcel(self, licence_types=[]):
        """
          Returns the titles of licences related to a parcel
        """
        relatedLicencesTitles = []
        for relatedLicence in self.get_related_licences_of_parcel(licence_types):
            relatedLicencesTitles.append(relatedLicence.Title.decode('utf8'))
        return relatedLicencesTitles

    def get_delivered_related_licences(self, limit_date, licence_types=[]):
        licences = []
        for brain in self.get_related_licences_of_parcel(licence_types):
            licence = brain.getObject()
            delivered = licence.getLastTheLicence()
            if delivered and (delivered.getDecisionDate() or delivered.getEventDate()) > limit_date:
                if delivered.getDecision() == 'favorable':
                    licences.append(licence)
                elif api.content.get_state(licence) in ['accepted', 'ended']:
                    licences.append(licence)
            elif not delivered and api.content.get_state(licence) in ['accepted', 'ended']:
                licences.append(licence)
        return licences

    def get_related_Buildlicences(self):
        limit_date = DateTime('1977/01/01')
        return self.get_delivered_related_licences(
            limit_date,
            ['BuildLicence', 'CODT_BuildLicence']
        )

    def get_related_UrbanCertificateOne(self):
        # cu1 cannot be older than 2 years
        limit_date = self.getLastTheLicence().getEventDate() - 731
        return self.get_delivered_related_licences(
            limit_date,
            ['UrbanCertificateOne', 'CODT_UrbanCertificateOne'],
        )

    def get_related_Parceloutlicence(self):
        limit_date = DateTime('1977/01/01')
        return self.get_delivered_related_licences(
            limit_date,
            ['ParcelOutLicence', 'CODT_ParcelOutLicence'],
        )

    def get_related_UrbanCertificateTwo(self, date=None):
        # cu2 cannot be older than 2 years
        if self.getLastTheLicence():
            limit_date = self.getLastTheLicence().getEventDate() - 731
        elif date:
            limit_date = date - 731
        else:
            limit_date = self.getLastDeposit().getEventDate() - 731
        return self.get_delivered_related_licences(
            limit_date,
            ['UrbanCertificateTwo', 'CODT_UrbanCertificateTwo'],
        )

    def get_specific_features_text(self, where=[''], only_selected=False):
        """
        # Particularité(s) du bien
        """
        context = self.context
        specific_features_text = []
        tool = api.portal.get_tool('portal_urban')
        for location in where:
            specificfeature_accessor = "get%sSpecificFeatures" % location.capitalize()
            specificFeatures = getattr(context, specificfeature_accessor)()
            for specificFeature in specificFeatures:
                if specificFeature['check']:
                    if specificFeature['text']:
                        specific_feature_text = tool.renderText(text=specificFeature['text'], context=context)
                        specific_features_text.append(specific_feature_text)
                elif not only_selected:
                    if specificFeature['defaultText']:
                        specific_feature_text = tool.renderText(text=specificFeature['defaultText'], context=context)
                        specific_features_text.append(specific_feature_text)
        return specific_features_text

    def getEvent(self, title=''):
        """
          Return a specific title's UrbanEvent
        """
        events = self.getAllEvents()
        for event in events[::-1]:
            if event.Title() == title:
                return event

    def getExpirationDate(self, date=None, year=5):
        if not date:
            date = _date.today()
        expirationDate = _date(date.year(), date.month(), date.day())
        return self.format_date(expirationDate + relativedelta(years=year))

    def getLimitDate(self, firstDepositDate, delay=20):
        context = self.real_context
        if context.annoncedDelay:
            delay = self.voc_term('annoncedDelay').getDeadLineDelay()
        limitDate = firstDepositDate + int(delay)
        return self.format_date(limitDate)

    def get_parcels(self, with_commas=False, with_division=True):
        result = u""
        context = self.real_context
        parcels = context.getParcels()
        for i in range(len(parcels)):
            for j in range(len(parcels)):
                if parcels[i].Title() > parcels[j].Title():
                    parcels[i], parcels[j] = parcels[j], parcels[i]
        list_grouped_parcels = []
        grouped_parcels = []
        division = ''
        for parcel in parcels:
            if parcel.getDivisionAlternativeName() != division:
                division = parcel.getDivisionAlternativeName()
                grouped_parcels = []
                grouped_parcels.append(parcel)
                list_grouped_parcels.append(grouped_parcels)
            else:
                grouped_parcels.append(parcel)
        for elms in list_grouped_parcels:
            for i in range(len(elms)):
                for j in range(len(elms)):
                    if elms[i].getSection() > elms[j].getSection():
                        elms[i], elms[j] = elms[j], elms[i]
        for gp in enumerate(list_grouped_parcels):
            divisionAlternativeName = gp[1][0].getDivisionAlternativeName()
            section = gp[1][0].getSection().decode('utf8')
            if with_division:
                if with_commas:
                    result += u"{}, section {}, ".format(divisionAlternativeName, section)
                else:
                    result += u"{} section {} ".format(divisionAlternativeName, section)
            else:
                result += u"section {} ".format(section)
            for p in enumerate(gp[1]):
                if section != p[1].getSection():
                    section = p[1].getSection()
                    if with_commas:
                        result += u"section {}, ".format(section)
                    else:
                        result += u"section {} ".format(section)
                bis = p[1].getBis() if p[1].getBis() != '0' else ''
                puissance = p[1].getPuissance() if p[1].getPuissance() != '0' else ''
                result += u"n° {}{}{}{}".format(
                    p[1].getRadical(), bis, p[1].getExposant(), puissance
                )
                if p[0] + 1 != len(gp[1]):
                    result += u", "
            if gp[0] + 1 != len(list_grouped_parcels):
                result += u", "
        return result

    def query_parcels_in_radius(self, radius='50'):
        parcels = self.context.getOfficialParcels()
        session = cadastre.new_session()
        return session.query_parcels_in_radius(parcels, radius)

    def query_parcels_locations_in_radius(self, radius='50'):
        parcels = self.context.getOfficialParcels()
        session = cadastre.new_session()
        parcels = session.query_parcels_in_radius(parcels, radius)
        locations = [parcel.location for parcel in parcels]
        locations.sort()
        return locations

    def get_parcellings_dict(self):
        """
        # Lotissement
        """
        context = self.real_context
        parcellings = context.getParcellings()
        parcellings_dict = {}
        if parcellings:
            parcellings_dict['label'] = parcellings.getLabel()
            parcellings_dict['subdividerName'] = parcellings.getSubdividerName()
            parcellings_dict['authorizationDate'] = parcellings.getAuthorizationDate()
            parcellings_dict['approvalDate'] = parcellings.getApprovalDate()
            parcellings_dict['DGO4Reference'] = parcellings.getDGO4Reference()
            parcellings_dict['numberOfParcels'] = parcellings.getNumberOfParcels()
            parcellings_dict['changesDescription'] = parcellings.getChangesDescription()
        return parcellings_dict

    def _get_personTitle_dict(self, id):
        """
        # Titre
        """
        context = self.context
        urbanConfig = context.getLicenceConfig()
        personTitle_config = urbanConfig.persons_titles
        personTitle_dict = {}
        personTitleTerm = getattr(personTitle_config, id, '')
        personTitle_dict['title'] = personTitleTerm.Title()
        personTitle_dict['abbreviation'] = personTitleTerm.getAbbreviation()
        personTitle_dict['gender'] = personTitleTerm.listGender().getValue(personTitleTerm.getGender())
        personTitle_dict['multiplicity'] = personTitleTerm.listMultiplicity().getValue(
            personTitleTerm.getMultiplicity()
        )
        personTitle_dict['reverseTitle'] = personTitleTerm.getReverseTitle()
        return personTitle_dict

    def _get_contact_dict(self, contact):
        """
        """
        contact_dict = {}
        if contact.getPersonTitle():
            contact_dict['personTitle'] = self._get_personTitle_dict(contact.getPersonTitle())['title']
            contact_dict['abbreviation'] = self._get_personTitle_dict(contact.getPersonTitle())['abbreviation']
            contact_dict['gender'] = self._get_personTitle_dict(contact.getPersonTitle())['gender']
            contact_dict['multiplicity'] = self._get_personTitle_dict(contact.getPersonTitle())['multiplicity']
            contact_dict['reverseTitle'] = self._get_personTitle_dict(contact.getPersonTitle())['reverseTitle']
        contact_dict['name1'] = contact.getName1()
        contact_dict['name2'] = contact.getName2()
        contact_dict['society'] = contact.getSociety()
        contact_dict['street'] = contact.getStreet()
        contact_dict['number'] = contact.getNumber()
        contact_dict['zipcode'] = contact.getZipcode()
        contact_dict['city'] = contact.getCity()
        contact_dict['country'] = contact.getCountry()
        contact_dict['email'] = contact.getEmail()
        contact_dict['phone'] = contact.getPhone()
        contact_dict['gsm'] = contact.getGsm()
        contact_dict['fax'] = hasattr(contact, 'fax') and contact.getFax() or ''
        contact_dict['registrationNumber'] = contact.getRegistrationNumber()
        contact_dict['nationalRegister'] = contact.getNationalRegister()
        return contact_dict

    def _get_contact(
            self,
            contact,
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée ',
                'Féminin-Pluriel': ' domiciliées '
            },
            reversed_name=False,
            withaddress=True):
        """
        """
        contact = self._get_contact_dict(contact)
        contact_names = \
            contact.get('personTitle', '') + ' ' +\
            contact['name2'] + ' ' +\
            contact['name1']
        reversed_contact_names = \
            contact.get('personTitle', '') + ' ' +\
            contact['name1'] + ' ' +\
            contact['name2']
        if reversed_name:
            contact_names = reversed_contact_names
        if withaddress:
            gender_multiplicity = contact['gender'] + '-' + contact['multiplicity']
            gender_multiplicity = gender_multiplicity.encode('utf8')
            contact_address = \
                resident[gender_multiplicity] +\
                contact['street'] + ' ' +\
                contact['number'] + ' ' +\
                contact['zipcode'] + ' ' +\
                contact['city']
            contact_names += contact_address
        return contact_names

    def get_architect_dict(self, index):
        """
        """
        context = self.context
        architects = context.get_architects()
        result = {}
        if index < len(architects):
            architect = architects[index]
            result = self.get_contact_dict(architect)
        return result

    def _get_architect(
            self,
            architect,
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée ',
                'Féminin-Pluriel': ' domiciliées '
            },
            reversed_name=False,
            withaddress=True):
        result = self._get_contact(architect, resident, reversed_name, withaddress)
        return result

    def get_architects(
            self,
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée ',
                'Féminin-Pluriel': ' domiciliées '
            },
            reversed_name=False,
            withaddress=True,
            separator=', '):
        context = self.context
        architects = context.getArchitects()
        result = self._get_architect(architects[0], resident, reversed_name, withaddress)
        for architect in architects[1:]:
            result += separator + self._get_architect(architect, resident, reversed_name, withaddress)
        return result

    def get_current_foldermanager(self):
        return getCurrentFolderManager()

    def get_foldermanager_dict(self, index):
        """
        """
        context = self.context
        foldermanagers = context.getFoldermanagers()
        result = {}
        if index < len(foldermanagers):
            foldermanager = foldermanagers[index]
            result = self.get_contact_dict(foldermanager)
            result['initials'] = foldermanager.getInitials()
            result['grade'] = foldermanager.getGrade()
            result['ploneUserId'] = foldermanager.getPloneUserId()
            result['manageableLicences'] = foldermanager.getManageableLicences()
        return result

    def _get_foldermanager(
            self,
            foldermanager,
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée ',
                'Féminin-Pluriel': ' domiciliées '
            },
            reversed_name=False,
            withaddress=False):
        result = self._get_contact(foldermanager, resident, reversed_name, withaddress)
        return result

    def get_foldermanagers(
            self,
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée ',
                'Féminin-Pluriel': ' domiciliées '
            },
            reversed_name=False,
            withaddress=False,
            separator=', '):
        context = self.context
        foldermanagers = context.getFoldermanagers()
        result = self._get_foldermanager(foldermanagers[0], resident, reversed_name, withaddress)
        for foldermanager in foldermanagers[1:]:
            result += separator + self._get_foldermanager(foldermanager, resident, reversed_name, withaddress)
        return result

    def get_foldermanagers_by_grade(self, grade_id=''):
        foldermanagers = [fm for fm in self.context.getFoldermanagers() if fm.grade == grade_id]
        return foldermanagers

    def get_roadEquipments(self):
        context = self.context
        roadEquipments = context.getRoadEquipments()
        result = []
        folderroadequipments = UrbanVocabulary('folderroadequipments', inUrbanConfig=False)
        allVocTerms = folderroadequipments.getAllVocTerms(context)
        for roadEquipment in roadEquipments:
            road_equipment = allVocTerms[roadEquipment['road_equipment']]
            road_equipment_details = roadEquipment['road_equipment_details']
            result.append({'road_equipment': road_equipment.Title(), 'road_equipment_details': road_equipment_details})
        return result

    def get_parcellings(self):
        context = self.context
        parcellings = context.getParcellings()
        result = parcellings.Title()
        return result

    def get_applicants_names_and_address(
            self,
            applicant_separator=', ',
            representedBy_separator=' et ',
            resident={
                'Masculin-Singulier': ' domicilié ',
                'Masculin-Pluriel': ' domiciliés ',
                'Féminin-Singulier': ' domiciliée',
                'Féminin-Pluriel': ' domiciliées'
            },
            represented={
                'Masculin-Singulier': ' représenté par ',
                'Masculin-Pluriel': ' représentés par ',
                'Féminin-Singulier': ' représentée par',
                'Féminin-Pluriel': ' représentées par'
            },
            reversed_name=True):
        applicants = self.getApplicants()
        applicants_names_and_address = ""
        if applicants:
            applicants_names_and_address = self._get_applicant_names_and_address(
                applicants[0],
                resident,
                represented,
                reversed_name,
                representedBy_separator
            )
            for applicant in applicants[1:]:
                applicants_names_and_address += applicant_separator + self._get_applicant_names_and_address(
                    applicant,
                    resident,
                    represented,
                    reversed_name,
                    representedBy_separator
                )
        return applicants_names_and_address

    def _get_applicant_names_and_address(self, applicant, resident, represented,
                                         reversed_name, representedBy_separator):
        applicant_names_and_address = self._get_contact(applicant, resident, reversed_name)
        if applicant['representedBySociety']:
            gender_multiplicity = applicant['gender'] + '-' + applicant['multiplicity']
            applicant_names_and_address += represented[gender_multiplicity] +\
                self._get_representedBy_names_and_address(applicant, resident, reversed_name, representedBy_separator)
        return applicant_names_and_address

    def get_applicants_list_dict(self):
        context = self.context
        applicants = context.getApplicants()
        applicants_list_dict = []
        for i in range(len(applicants)):
            applicants_list_dict.append(self.get_applicant_dict(i))
        return applicants_list_dict

    def get_applicant_dict(self, index):
        context = self.context
        applicant = context.getApplicants()[index]
        applicant_dict = self._get_contact_dict(applicant)
        applicant_dict['representedBySociety'] = applicant.getRepresentedBySociety()
        applicant_dict['isSameAddressAsWorks'] = applicant.getIsSameAddressAsWorks()
        applicant_dict['representedBy'] = applicant.getRepresentedBy()
        return applicant_dict

    def _get_representedBy_names_and_address(self, applicant, resident, reversed_name, representedBy_separator):
        representedBy_list = self._get_representedBy_list(applicant)
        representedBy_names_and_address = ""
        if representedBy_list:
            representedBy_names_and_address = self._get_contact(
                representedBy_list[0],
                resident,
                reversed_name
            )
            for representedBy in representedBy_list[1:]:
                representedBy_names_and_address += representedBy_separator + self._get_contact(
                    representedBy,
                    resident,
                    reversed_name
                )
        return representedBy_names_and_address

    def _get_representedBy_list(self, applicant):
        representedBy_UIDs = applicant['representedBy']
        representedBy_list = []
        for representedBy_UID in representedBy_UIDs:
            catalog = self.portal.portal_catalog
            brains = catalog.searchResults(UID=representedBy_UID)
            representedBy = brains[0].getObject()
            contact_dict = self._get_contact_dict(representedBy)
            representedBy_list.append(contact_dict)
        return representedBy_list

    def get_applicants_names(self, separator=', ', reversed_name=True):
        context = self.context
        applicants = context.getApplicants()
        applicants_names = ""
        if applicants:
            applicants_names = self._get_contact(applicants[0], reversed_name=reversed_name, withaddress=False)
            for applicant in applicants[1:]:
                applicants_names += separator + self._get_contact(
                    applicant, reversed_name=reversed_name, withaddress=False
                )
        return applicants_names

    def _get_date(self, event, date_name='eventDate', translatemonth=True, long_format=False):
        if not event:
            return

        date_field = event.getField(date_name)
        raw_date = date_field.get(event)
        if not raw_date:
            return

        formatted_date = self.helper_view.format_date(raw_date, translatemonth, long_format)
        return formatted_date

    def get_notification_date(self, date_name='eventDate', translatemonth=True, long_format=False):
        event = self.context.getLastTheLicence()
        date = self._get_date(event, date_name, translatemonth, long_format)
        return date

    def get_solicitOpinions_descriptions(self):
        context = self.context
        opinions = context.getUrbanEventOpinionRequests()
        descriptions = []
        for opinion in opinions:
            descriptions.append(opinion.getLinkedOrganisationTerm().Description())
        return descriptions


class UrbanDocGenerationEventHelperView(UrbanDocGenerationHelperView):
    """
    """
    def mailing_list(self, gen_context=None):
        mailing_list = []
        use_proxy = True
        if gen_context and 'publipostage' in gen_context:
            if gen_context['publipostage'] == 'demandeurs':
                mailing_list = self.real_context.getParentNode().getApplicants()
            elif gen_context['publipostage'] == 'architectes':
                mailing_list = self.context.getArchitects()
            elif gen_context['publipostage'] == 'geometres':
                mailing_list = self.context.getGeometricians()
            elif gen_context['publipostage'] == 'notaires':
                mailing_list = self.context.getNotaryContact()
            elif gen_context['publipostage'] == 'plaignants':
                mailing_list = self.real_context.getParentNode().getPlaintiffs()
            elif gen_context['publipostage'] == 'locataires':
                mailing_list = self.real_context.getParentNode().getTenants()
            elif gen_context['publipostage'] == 'reclamants':
                mailing_list = self.context.getClaimants()
            elif gen_context['publipostage'] == 'derniers_reclamants':
                mailing_list = self.context.getLinkedUrbanEventInquiry().getClaimants()
            elif gen_context['publipostage'] == 'proprietaires':
                mailing_list = self.real_context.getParentNode().getProprietaries()
            elif gen_context['publipostage'] == 'proprietaires_voisinage_enquete':
                if IUrbanEventInquiry.providedBy(self.real_context):
                    inquiry_event = self.real_context
                else:
                    # for docs outside inquiry events
                    inquiry_event = self.real_context.getParentNode().getLastInquiry()
                mailing_list = inquiry_event.getRecipients(onlyActive=True)
            elif gen_context['publipostage'] == 'organismes':
                mailing_list = self.getFolderMakersMailing()
                use_proxy = False
        if use_proxy:
            mailing_list = [obj.unrestrictedTraverse('@@document_generation_helper_view').context for obj in mailing_list]
        return mailing_list

    def getFolderMakersMailing(self):
        """  """
        mailing_list = []
        foldermakers = self.getFolderMakers()
        for foldermaker in foldermakers:
            html_description = foldermaker['OpinionEventConfig'].Description()
            transformed_description = self.portal.portal_transforms.convert(
                'html_to_web_intelligent_plain_text', html_description).getData().strip('\n ')
            mailing = {
                'OpinionEventConfig': foldermaker['OpinionEventConfig'],
                'UrbanEventOpinionRequest': foldermaker['UrbanEventOpinionRequest'],
                'description': transformed_description
            }
            mailing_list.append(mailing)
        return mailing_list

    def getFolderMakers(self):
        """  """
        urban_tool = api.portal.get_tool('portal_urban')
        foldermakers_config = urban_tool.getLicenceConfig(self.context).eventconfigs
        all_opinion_request_events = self.context.getAllOpinionRequests()
        foldermakers = []
        opinion_cfgs = [fm for fm in foldermakers_config.objectValues() if fm.portal_type == 'OpinionEventConfig']
        for opinionRequestEventType in opinion_cfgs:
            foldermaker = {}
            if opinionRequestEventType.id in self.getSolicitOpinions():
                foldermaker['OpinionEventConfig'] = opinionRequestEventType
                for urbanEventOpinionRequest in all_opinion_request_events:
                    if urbanEventOpinionRequest.getUrbaneventtypes() == opinionRequestEventType:
                        foldermaker['UrbanEventOpinionRequest'] = urbanEventOpinionRequest
                        foldermakers.append(foldermaker)
                        break
        return foldermakers

    def getSolicitOpinions(self):
        """  """
        return self.context.getSolicitOpinionsTo() + self.context.getSolicitOpinionsToOptional()

    def _get_wspm_field(self, field_name):
        field = 'NO FIELD {} FOUND'.format(field_name)
        linked_pm_items = get_ws_meetingitem_infos(self.real_context, extra_attributes=True)
        if linked_pm_items:
            linked_item = linked_pm_items[0]
            if field_name in linked_item:
                field = linked_item[field_name]
            elif field_name in linked_item.extraInfos:
                field = linked_item.extraInfos[field_name]
        return field

    def _get_wspm_text_field(self, field_name):
        text = self._get_wspm_field(field_name)
        corrected_text = re.sub('\n\s*\n', '\n<p>&nbsp;</p>\n', text)
        return corrected_text

    def get_wspm_decision_date(self, translatemonth=True, long_format=False):
        field_name = 'meeting_date'
        decision_date = 'NO FIELD {} FOUND'.format(field_name)
        raw_date = self._get_wspm_field(field_name)
        if raw_date != decision_date:
            decision_date = self.helper_view.format_date(
                date=raw_date,
                translatemonth=translatemonth,
                long_format=long_format
            )
        return decision_date

    def get_wspm_description_text(self):
        field_name = 'description'
        description_text = self._get_wspm_text_field(field_name)
        return description_text

    def get_wspm_decision_text(self):
        field_name = 'decision'
        decision_text = self._get_wspm_text_field(field_name)
        return decision_text

    def get_wspm_motivation_text(self):
        field_name = 'motivation'
        motivation_text = self._get_wspm_text_field(field_name)
        return motivation_text

    def get_wspm_meeting_state(self):
        field_name = 'review_state'
        state = self._get_wspm_text_field(field_name)
        return state


class UrbanDocGenerationFacetedHelperView(ATDocumentGenerationHelperView):
    def get_work_location_dict(self, index, folder):
        """
        # Adresse(s) des travaux
        return a dictionary containing specific work locations informations
        """
        view = folder.unrestrictedTraverse('document_generation_helper_view')
        work_location_dict = view.get_work_location_dict(index)
        return work_location_dict

    def get_related_licences_of_parcel(self, folder):
        """
          Returns the licences related to a parcel
        """
        view = folder.unrestrictedTraverse('document_generation_helper_view')
        relatedLicences = view.get_related_licences_of_parcel()
        return relatedLicences

    def get_related_licences_titles_of_parcel(self, folder):
        """
          Returns the licences related to a parcel
        """
        view = folder.unrestrictedTraverse('document_generation_helper_view')
        relatedLicences = view.get_related_licences_titles_of_parcel()
        return relatedLicences

    def getEvent(self, folder, title=''):
        view = folder.unrestrictedTraverse('document_generation_helper_view')
        event = view.getEvent(title)
        return event

    def format_date(self, folder, date=None, translatemonth=True, long_format=False):
        if not date:
            date = _date.today()
        view = folder.unrestrictedTraverse('document_generation_helper_view')
        formated_date = view.format_date(date, translatemonth, long_format)
        return formated_date


class UrbanBaseProxyObject(ATDisplayProxyObject):
    """
    """

    helper_view = None
