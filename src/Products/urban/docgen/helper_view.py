# -*- coding: utf-8 -*-

from collective.documentgenerator.helper.archetypes import ATDisplayProxyObject
from collective.documentgenerator.helper.archetypes import ATDocumentGenerationHelperView
from datetime import date as _date
from dateutil.relativedelta import relativedelta
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.CMFCore.utils import getToolByName
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import getCurrentFolderManager
from zope.i18n import translate
from plone import api


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

    def display_date(self, field_name, long_format=False, custom_format=None):
        date = self.get_value(field_name)
        if custom_format:
            formatted_date = date.strftime(custom_format)
        else:
            formatted_date = self.format_date(date, long_format=long_format)
        return formatted_date

    def format_date(self, date=_date.today(), translatemonth=True, long_format=False):
        """
          Format the date for printing in pod templates
        """
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
        parcel_view = parcels and parcels[0].restrictedTraverse('document_generation_helper_view')
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
        context = self.real_context
        proprietaries = [pro for pro in context.objectValues('Applicant') if pro.portal_type == 'Proprietary']
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

    def get_related_licences_of_parcel(self):
        """
          Returns the licences related to a parcel
        """
        context = self.real_context.aq_parent
        parcels = context.getParcels()
        relatedLicences = []
        for parcel in parcels:
            parcelRecordsView = context.restrictedTraverse('parcelrecordsview')
            parcelRecordsView.parcel_id = parcel.id
            relatedLicences += parcelRecordsView.getRelatedLicencesOfParcel()
        return relatedLicences

    def get_related_licences_titles_of_parcel(self):
        """
          Returns the titles of licences related to a parcel
        """
        context = self.real_context
        parcels = context.getParcels()
        relatedLicencesTitles = []
        for parcel in parcels:
            parcelRecordsView = context.restrictedTraverse('parcelrecordsview')
            parcelRecordsView.parcel_id = parcel.id
            relatedLicences = parcelRecordsView.getRelatedLicencesOfParcel()
            for relatedLicence in relatedLicences:
                relatedLicencesTitles.append(relatedLicence['title'].decode('utf8'))
        return relatedLicencesTitles

    def get_specific_features_text(self):
        """
        # Particularité(s) du bien
        """
        context = self.real_context.aq_parent
        specificFeatures = context.getSpecificFeatures()
        specific_features_text = []
        tool = getToolByName(self, 'portal_urban')
        for specificFeature in specificFeatures:
            if specificFeature['check']:
                if specificFeature['text']:
                    specific_feature_text = tool.renderText(text=specificFeature['text'], context=context)
                    specific_features_text.append(specific_feature_text)
            else:
                if specificFeature['defaultText']:
                    specific_feature_text = tool.renderText(text=specificFeature['defaultText'], context=context)
                    specific_features_text.append(specific_feature_text)
        return specific_features_text

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

    def getEvent(self, title=''):
        """
          Return a specific title's UrbanEvent
        """
        i = 0
        found = False
        events = self.context.getAllEvents()
        event = None
        while i < len(events) and not found:
            if events[i].Title() == title:
                found = True
                event = events[i]
            i = i + 1
        return event

    def getExpirationDate(self, date=_date.today(), year=5):
        expirationDate = _date(date.year(), date.month(), date.day())
        return self.format_date(expirationDate + relativedelta(years=year))


class UrbanDocGenerationLicenceHelperView(UrbanDocGenerationHelperView):
    def get_parcellings(self):
        """
        # Lotissement
        """
        context = self.real_context
        parcellings = context.getParcellings()
        return parcellings.Title()

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


class UrbanDocGenerationEventHelperView(UrbanDocGenerationHelperView):
    """
    """


class UrbanDocGenerationFacetedHelperView(ATDocumentGenerationHelperView):
    def get_work_location_dict(self, index, folder):
        """
        # Adresse(s) des travaux
        return a dictionary containing specific work locations informations
        """
        view = folder.restrictedTraverse('document_generation_helper_view')
        work_location_dict = view.get_work_location_dict(index)
        return work_location_dict

    def get_related_licences_of_parcel(self, folder):
        """
          Returns the licences related to a parcel
        """
        view = folder.restrictedTraverse('document_generation_helper_view')
        relatedLicences = view.get_related_licences_of_parcel()
        return relatedLicences

    def get_related_licences_titles_of_parcel(self, folder):
        """
          Returns the licences related to a parcel
        """
        view = folder.restrictedTraverse('document_generation_helper_view')
        relatedLicences = view.get_related_licences_titles_of_parcel()
        return relatedLicences

    def getEvent(self, folder, title=''):
        view = folder.restrictedTraverse('document_generation_helper_view')
        event = view.getEvent(title)
        return event

    def format_date(self, folder, date=_date.today(), translatemonth=True, long_format=False):
        view = folder.restrictedTraverse('document_generation_helper_view')
        formated_date = view.format_date(date, translatemonth, long_format)
        return formated_date

class LicenceDisplayProxyObject(ATDisplayProxyObject):
    """
    """
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
        context = self.context
        view = context.restrictedTraverse('document_generation_helper_view')
        work_location_dict = view.get_work_location_dict(index)
        return work_location_dict

    def get_work_location_signaletic(self, workLocation):
        """
        # Adresse(s) des travaux
        return a street name and number from a specific workLocation
        """
        catalog = api.portal.get_tool("uid_catalog")
        street = catalog(UID=workLocation['street'])[0].getObject()
        return "{} {}".format(workLocation['number'], street.Title())

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

# Contact(s)
#------------------------------------------------------------------------------
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
        personTitle_dict['multiplicity'] = personTitleTerm.listMultiplicity().getValue(personTitleTerm.getMultiplicity())
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
        contact_dict['fax'] = contact.getFax()
        contact_dict['registrationNumber'] = contact.getRegistrationNumber()
        contact_dict['nationalRegister'] = contact.getNationalRegister()
        return contact_dict

    def _get_contact(
            self,
            contact,
            resident = {
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée ',
                'Féminin-Pluriel':' domiciliées '
                },
            reversed_name = False,
            withaddress = True
            ):
        """
        """
        contact = self._get_contact_dict(contact)
        gender_multiplicity = contact['gender'] + '-' + contact['multiplicity']
        gender_multiplicity = gender_multiplicity.encode('utf8')
        contact_names = \
                contact['personTitle'] + ' ' +\
                contact['name2'] + ' ' +\
                contact['name1']
        reversed_contact_names = \
                contact['personTitle'] + ' ' +\
                contact['name1'] + ' ' +\
                contact['name2']
        contact_address = \
                resident[gender_multiplicity] +\
                contact['street'] + ' ' +\
                contact['number'] + ' ' +\
                contact['zipcode'] + ' ' +\
                contact['city']
        contact = contact_names
        if reversed_name:
            contact = reversed_contact_names
        if withaddress:
            contact += contact_address
        return contact


# Architecte(s)
#------------------------------------------------------------------------------
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
            resident = {
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée ',
                'Féminin-Pluriel':' domiciliées '
                },
            reversed_name = False,
            withaddress = True
            ):
        result = self._get_contact(architect, resident, reversed_name, withaddress)
        return result

    def get_architects(
            self,
            resident = {
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée ',
                'Féminin-Pluriel':' domiciliées '
                },
            reversed_name = False,
            withaddress = True,
            separator = ', '
            ):
        context = self.context
        architects = context.getArchitects()
        result = self._get_architect(architects[0], resident, reversed_name, withaddress)
        for architect in architects[1:]:
            result += separator + self._get_architect(architect, resident, reversed_name, withaddress)
        return result


# Agent(s) traitant(s)
#------------------------------------------------------------------------------
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
            resident = {
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée ',
                'Féminin-Pluriel':' domiciliées '
                },
            reversed_name = False,
            withaddress = False
            ):
        result = self._get_contact(foldermanager, resident, reversed_name, withaddress)
        return result

    def get_foldermanagers(
            self,
            resident = {
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée ',
                'Féminin-Pluriel':' domiciliées '
                },
            reversed_name = False,
            withaddress = False,
            separator = ', '
            ):
        context = self.context
        foldermanagers = context.getFoldermanagers()
        result = self._get_foldermanager(foldermanagers[0], resident, reversed_name, withaddress)
        for foldermanager in foldermanagers[1:]:
            result += separator + self._get_foldermanager(foldermanager, resident, reversed_name, withaddress)
        return result

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

# Demandeur(s)
#------------------------------------------------------------------------------
    def get_applicants_names_and_address(
            self,
            applicant_separator=', ',
            representedBy_separator=' et ',
            resident={
                'Masculin-Singulier':' domicilié ',
                'Masculin-Pluriel':' domiciliés ',
                'Féminin-Singulier':' domiciliée',
                'Féminin-Pluriel':' domiciliées'
            },
            represented={
                'Masculin-Singulier':' représenté par ',
                'Masculin-Pluriel':' représentés par ',
                'Féminin-Singulier':' représentée par',
                'Féminin-Pluriel':' représentées par'
            },
            reversed_name=True,
        ):
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

    def _get_applicant_names_and_address(self, applicant, resident, represented, reversed_name, representedBy_separator):
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
                applicants_names += separator + self._get_contact(applicant, reversed_name=reversed_name,
                        withaddress=False)
        return applicants_names

class EventDisplayProxyObject(ATDisplayProxyObject):
    """
    """
