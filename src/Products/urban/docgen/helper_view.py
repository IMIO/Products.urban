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
        return self.getEvent(title) != None

    def format_date(self, date=_date.today(), translatemonth=True, long_format=False):
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

    def get_applicant_dict(self, index):
        applicants = self.get_applicants()
        applicant_dict = {}
        if index < len(applicants):
            applicant_dict = {
                    'personTitle': '',
                    'name1': '',
                    'name2': '',
                    'society': '',
                    'street': '',
                    'number': '',
                    'zipcode': '',
                    'city': '',
                    'country': '',
                    'email': '',
                    'phone': '',
                    'registrationNumber': '',
                    'nationalRegister': '',
            }
            applicant = self.get_applicants()[index]
            applicant_dict['personTitle'] = applicant.getPersonTitle()
            applicant_dict['name1'] = applicant.getName1()
            applicant_dict['name2'] = applicant.getName2()
            applicant_dict['society'] = applicant.getSociety()
            applicant_dict['street'] = applicant.getStreet()
            applicant_dict['number'] = applicant.getNumber()
            applicant_dict['zipcode'] = applicant.getZipcode()
            applicant_dict['city'] = applicant.getCity()
            applicant_dict['country'] = applicant.getCountry()
            applicant_dict['email'] = applicant.getEmail()
            applicant_dict['phone'] = applicant.getPhone()
            applicant_dict['registrationNumber'] = applicant.getRegistrationNumber()
            applicant_dict['nationalRegister'] = applicant.getNationalRegister()
        return applicant_dict

    def get_applicant_names(self, applicant, reversed_name=True):
        applicant_names = applicant['personTitle'] + ' ' + applicant['name2'] + ' ' + applicant['name1']
        if reversed_name:
            applicant_names = applicant['personTitle'] + ' ' + applicant['name1'] + ' ' + applicant['name2']
        return applicant_names

    def get_applicant_names_and_adress(self, applicant, reversed_name=True, resident=' domicilié '):
        applicant_names_and_adress = \
                applicant['personTitle'] + ' ' +\
                applicant['name2'] + ' ' +\
                applicant['name1'] + resident +\
                applicant['street'] + ' ' +\
                applicant['number'] + ' ' +\
                applicant['zipcode'] + ' ' +\
                applicant['city']
        if reversed_name:
            applicant_names_and_adress = \
                    applicant['personTitle'] + ' ' +\
                    applicant['name1'] + ' ' +\
                    applicant['name2'] + resident +\
                    applicant['street'] + ' ' +\
                    applicant['number'] + ' ' +\
                    applicant['zipcode'] + ' ' +\
                    applicant['city']
        return applicant_names_and_adress

    def get_applicants(self):
        """
           Return the list of applicants for the Licence
        """
        licence = self.real_context
        applicants = [app for app in licence.objectValues('Applicant') if app.portal_type == 'Applicant']
        return applicants

    def get_applicants_list_dict(self):
        applicants = self.get_applicants()
        applicants_list_dict = []
        for i in range(len(applicants)):
            applicants_list_dict.append(self.get_applicant_dict(i))
        return applicants_list_dict

    def get_applicants_names(self, separator=', ', reversed_name=True):
        applicants = self.get_applicants_list_dict()
        applicants_names = ""
        if applicants:
            applicants_names = self.get_applicant_names(applicants[0], reversed_name)
            for applicant in applicants[1:]:
                applicants_names += separator + self.get_applicant_names(applicant, reversed_name)
        return applicants_names

    def get_applicants_names_and_adress(self, separator=', ', reversed_name=True, resident=' domicilié '):
        applicants = self.get_applicants_list_dict()
        applicants_names_and_adress = ""
        if applicants:
            applicants_names_and_adress = self.get_applicant_names_and_adress(
                    applicants[0],
                    reversed_name,
                    resident
            )
            for applicant in applicants[1:]:
                applicants_names_and_adress += separator + self.get_applicant_names_and_adress(
                        applicant,
                        reversed_name,
                        resident
                )
        return applicants_names_and_adress

    def get_checked_specific_features_id_list(self):
        """
        # Particularité(s) du bien
        """
        licence = self.real_context
        specificFeatures = licence.getSpecificFeatures()
        specific_features_id_list = []
        for specificFeature in specificFeatures:
            if specificFeature['check']:
                specific_features_id_list.append(specificFeature['id'])
        return specific_features_id_list

        proprietaries = [pro for pro in self.objectValues('Applicant') if pro.portal_type == 'Proprietary']
        return proprietaries

    def get_division(self):
        parcels = self.context.getParcels()
        parcel_view = parcels and parcels[0].restrictedTraverse('document_generation_helper_view')
        raw_div = parcel_view.context.division
        division = raw_div and raw_div[raw_div.find('(') + 1:-1] or 'DIVISION INCONNUE'
        return division

    def get_parcellings_dict(self):
        """
        # Lotissement
        """
        licence = self.real_context
        parcellings = licence.getParcellings()
        parcellings_dict = {
                'label': '',
                'subdividerName': '',
                'authorizationDate': '',
                'approvalDate': '',
                'DGO4Reference': '',
                'numberOfParcels': '',
                'changesDescription': ''
        }
        if parcellings:
            parcellings_dict['label'] = parcellings.getLabel()
            parcellings_dict['subdividerName'] = parcellings.getSubdividerName()
            parcellings_dict['authorizationDate'] = parcellings.getAuthorizationDate()
            parcellings_dict['approvalDate'] = parcellings.getApprovalDate()
            parcellings_dict['DGO4Reference'] = parcellings.getDGO4Reference()
            parcellings_dict['numberOfParcels'] = parcellings.getNumberOfParcels()
            parcellings_dict['changesDescription'] = parcellings.getChangesDescription()
        return parcellings_dict

    def get_pca_dict(self):
        """
        # Plan Communal d'Aménagement
        """
        licence = self.real_context
        pca = licence.getField('pca').get(licence)
        urbanConfig = licence.getLicenceConfig()
        pca_config = urbanConfig.pcas
        pcaTerm = getattr(pca_config, pca, '')
        pca_dict = {
                'title': '',
                'label': '',
                'number': '',
                'decreeDate': '',
                'decreeType': '',
                'changes': '',
                'comment': ''
        }
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
            #add a separator between every parcel
            #either a '\n'
            if not isFirst and linebyline:
                toreturn += '\n'
            #or an "and "
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
                toreturn += '/%s' % portionOutObj.getBis()
            toreturn += portionOutObj.getExposant()
            toreturn += portionOutObj.getPuissance()
            isFirst = False
        return toreturn

    def get_proprietaries(self):
        """
           Return the list of proprietaries for the Licence
        """
        licence = self.real_context
        proprietaries = [pro for pro in licence.objectValues('Applicant') if pro.portal_type == 'Proprietary']
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

    def get_proprietaries_names_and_adress(self, separator=', ', reversed_name=True, resident=' domicilié '):
        proprietaries = self.get_proprietaries_list_dict()
        proprietaries_names_and_adress = ""
        if proprietaries:
            proprietaries_names_and_adress = self.get_proprietary_names_and_adress(
                    proprietaries[0],
                    reversed_name,
                    resident
            )
            for proprietary in proprietaries[1:]:
                proprietaries_names_and_adress += separator + self.get_proprietary_names_and_adress(
                        proprietary,
                        reversed_name,
                        resident
                )
        return proprietaries_names_and_adress

    def get_proprietary_dict(self, index):
        proprietaries = self.get_proprietaries()
        proprietary_dict = {}
        if index < len(proprietaries):
            proprietary_dict = {
                    'personTitle': '',
                    'name1': '',
                    'name2': '',
                    'society': '',
                    'street': '',
                    'number': '',
                    'zipcode': '',
                    'city': '',
                    'country': '',
                    'email': '',
                    'phone': '',
                    'registrationNumber': '',
                    'nationalRegister': '',
            }
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

    def get_proprietary_names_and_adress(self, proprietary, reversed_name=True, resident=' domicilié '):
        proprietary_names_and_adress = \
                proprietary['personTitle'] + ' ' +\
                proprietary['name2'] + ' ' +\
                proprietary['name1'] + resident +\
                proprietary['street'] + ' ' +\
                proprietary['number'] + ' ' +\
                proprietary['zipcode'] + ' ' +\
                proprietary['city']
        if reversed_name:
            proprietary_names_and_adress = \
                    proprietary['personTitle'] + ' ' +\
                    proprietary['name1'] + ' ' +\
                    proprietary['name2'] + resident +\
                    proprietary['street'] + ' ' +\
                    proprietary['number'] + ' ' +\
                    proprietary['zipcode'] + ' ' +\
                    proprietary['city']
        return proprietary_names_and_adress

    def get_related_licences_of_parcel(self):
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

    def get_street_dict(self, uid):
        street_dict = {
                'bestAddressKey': '',
                'streetCode': '',
                'streetName': '',
                'startDate': '',
                'endDate': '',
                'regionalRoad': '',
        }
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=uid)[0].getObject()
        street_dict['bestAddressKey'] = street.getBestAddressKey()
        street_dict['streetCode'] = street.getStreetCode()
        street_dict['streetName'] = street.getStreetName()
        street_dict['startDate'] = street.getStartDate()
        street_dict['endDate'] = street.getEndDate()
        street_dict['regionalRoad'] = street.getRegionalRoad()
        return street_dict

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

    def get_work_location_dict(self, index):
        """
        return a dictionary containing all work locations informations
        """
        licence = self.real_context
        workLocation = licence.getWorkLocations()[index]
        street_dict = self.get_street_dict(workLocation['street'])
        work_location_dict = street_dict.update({'number': workLocation['number']})
        return work_location_dict

    def get_work_location_signaletic(self, workLocation):
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=workLocation['street'])[0].getObject()
        return street.getStreetName() + ' ' +  workLocation['number']

    def get_work_locations_list_dict(self):
        licence = self.real_context
        workLocations = licence.getWorkLocations()
        work_locations_list_dict = []
        for i in range(len(workLocations)):
            work_locations_list_dict.append(self.get_work_location_dict(i))
        return work_locations_list_dict

    def get_work_locations_signaletic(self, separator=', '):
        licence = self.real_context
        workLocations = licence.getWorkLocations()
        workLocation_signaletic = self.get_work_location_signaletic(workLocations[0])
        for workLocation in workLocations[1:]:
            workLocation_signaletic += separator + self.get_work_location_signaletic(workLocation)
        return workLocation_signaletic

    def getEvent(self, title=''):
        """
          Return a specific title's UrbanEvent
        """
        i = 0
        found = False
        opinionRequestsUrbanEvents = self.context.getUrbanEventOpinionRequests()
        inquiryUrbanEvents = self.context.getUrbanEventInquiries()
        urbanEvents = self.context.getUrbanEvents()
        events = opinionRequestsUrbanEvents + inquiryUrbanEvents + urbanEvents
        event = None
        while i < len(events) and not found:
            if events[i].Title() == title:
                found = True
                event = events[i]
            i = i + 1
        return event

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

