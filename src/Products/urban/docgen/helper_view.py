# -*- coding: utf-8 -*-

from collective.documentgenerator.helper.archetypes import ATDocumentGenerationHelperView
from datetime import date as _date
from Products.CMFPlone.i18nl10n import ulocalized_time
from zope.i18n import translate
from plone import api
from Products.urban.services import cadastre


class UrbanDocGenerationHelperView(ATDocumentGenerationHelperView):
    """
    Urban implementation of document generation helper methods.
    """

    def get_division(self):
        parcels = self.context.getParcels()
        parcel_view = parcels and parcels[0].restrictedTraverse('document_generation_helper_view')
        raw_div = parcel_view.context.division
        division = raw_div and raw_div[raw_div.find('(') + 1:-1] or 'DIVISION INCONNUE'
        return division

    def get_work_location(self, index):
        """
        return a dictionary containing all work locations informations
        """
        work_location = {
                'bestAddressKey': '',
                'streetCode': '',
                'streetName': '',
                'startDate': '',
                'endDate': '',
                'regionalRoad': '',
                'number': '',
        }
        workLocation = self.context.getWorkLocations()[index]
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=workLocation['street'])[0].getObject()
        work_location['bestAddressKey'] = street.getBestAddressKey()
        work_location['streetCode'] = street.getStreetCode()
        work_location['streetName'] = street.getStreetName()
        work_location['startDate'] = street.getStartDate()
        work_location['endDate'] = street.getEndDate()
        work_location['regionalRoad'] = street.getRegionalRoad()
        work_location['number'] =  workLocation['number']
        return work_location

    def formatDate(self, date=_date.today(), translatemonth=True, long_format=False):
        """
          Format the date for printing in pod templates
        """
        if date:
            if not translatemonth:
                return ulocalized_time(date, long_format=long_format, context=self, request=self.request).encode('utf8')
            else:
                #we need to translate the month and maybe the day (1er)
                year, month, day, hour = str(date.strftime('%Y/%m/%d/%Hh%M')).split('/')
                #special case when the day need to be translated
                #for example in french '1' becomes '1er' but in english, '1' becomes '1st'
                #if no translation is available, then we use the default where me remove foregoing '0'
                #'09' becomes '9', ...
                daymsgid = "date_day_%s" % day
                translatedDay = translate(daymsgid, 'urban', context=self.request, default=day.lstrip('0')).encode('utf8')
                #translate the month
                #msgids already exist in the 'plonelocales' domain
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

    def query_parcels_in_radius(self, radius='50'):
        """
        """
        parcels = self.context.getOfficialParcels()
        session = cadastre.new_session()
        return session.query_parcels_in_radius(parcels, radius)

    def query_parcels_locations_in_radius(self, radius='50'):
        """
        """
        parcels = self.context.getOfficialParcels()
        session = cadastre.new_session()
        parcels = session.query_parcels_in_radius(parcels, radius)
        locations = [parcel.location for parcel in parcels]
        locations.sort()
        return locations

    def getRelatedLicencesOfParcel(self):
        """
          Returns the licences related to a parcel
        """
        licence = self.real_context.aq_parent
        parcels = licence.getParcels()
        relatedLicences = []
        for parcel in parcels:
            parcelRecordsView = licence.restrictedTraverse('parcelhistoricrecordsview')
            parcelRecordsView.parcel_id = parcel.id
            #relatedLicences += parcelRecordsView.getRelatedLicencesOfParcel()
            relatedLicences += parcelRecordsView.get_related_licences_of_parcel()
        return relatedLicences

    def contains_road_equipment(self, road_equipment):
        roadEquipments = self.context.getRoadEquipments()
        answer = False
        for roadEquipment in roadEquipments:
            if roadEquipment['road_equipment'] == road_equipment:
                answer = True
        return answer
