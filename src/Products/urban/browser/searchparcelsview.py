
from Products.Five import BrowserView

from Products.urban.browser.table.urbantable import ParcelsTable
from Products.urban.interfaces import IDivision
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanCertificateBase
from Products.urban import services
from Products.urban.services.cadastral import IGNORE

from plone import api

from zope.i18n import translate

import Levenshtein
import re


class SearchParcelsView(BrowserView):
    """
      This manage the search parcels view
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

        self.portal_urban = api.portal.get_tool('portal_urban')
        #this way, get_all_divisions display a portal message if needed
        self.divisions = self._init_divisions()
        #if the search was launched with no criteria, add a message
        if not self.has_enough_criterions(self.request):
            plone_utils = api.portal.get_tool('plone_utils')
            plone_utils.addPortalMessage(translate('warning_enter_search_criteria'), type="warning")

    def __call__(self):
        if 'add_parcel.x' in self.request.form:
            parcel_data = {
                'division': self.request.get('division', None),
                'section': self.request.get('section', None),
                'radical': self.request.get('radical', None),
                'bis': self.request.get('bis', None),
                'exposant': self.request.get('exposant', None),
                'puissance': self.request.get('puissance', None),
                'partie': self.request.get('partie', None),
                'outdated': self.request.get('old', False),
            }
            if 'proprietary' in self.request.form:
                proprietary_data = {
                    'proprietary': self.request.get('proprietary', None),
                    'proprietary_city': self.request.get('proprietary_city', None),
                    'proprietary_address': self.request.get('proprietary_street', None),
                }
                parcel_data['location'] = self.request.get('location')
                self.createParcelAndProprietary(parcel_data, proprietary_data)
            else:
                self.createParcel(parcel_data)

            return self.request.response.redirect(self.context.absolute_url())

        return self.index()

    def _init_divisions(self):
        if not services.cadastre.check_connection():
            return None

        all_divisions = [('', translate('all_divisions', 'urban', context=self.request))]
        cadastre = services.cadastre.new_session()
        for division in cadastre.get_all_divisions():
            all_divisions.append(division)
        cadastre.close()

        return all_divisions

    def contextIsLicence(self):
        return IGenericLicence.providedBy(self.context)

    def renderParcelsListing(self):
        parcels = self.context.getParcels()
        if not parcels:
            return ''
        parcellisting = ParcelsTable(parcels, self.request)
        parcellisting.update()
        return parcellisting.render()

    def extract_search_criterions(self, request):
        arguments = self.extract_parcel_reference_criterions(request)
        if not request.get('browse_old_parcels', False):
            arguments['location'] = request.get('location', '') or IGNORE
            arguments['parcel_owner'] = request.get('parcel_owner', '') or IGNORE

        return arguments

    def extract_parcel_reference_criterions(self, request):
        refs = ['division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        arguments = {}
        for ref in refs:
            ref_value = request.get(ref, '')
            if ref_value:
                arguments[ref] = ref_value

        return arguments

    def extract_search_options(self, request):
        arguments = {
            'parcel_history': request.get('parcel_history', False),
            'browse_old_parcels': request.get('browse_old_parcels', False),
        }
        return arguments

    def has_enough_criterions(self, request):
        """
        """
        criterions = self.extract_search_criterions(request)

        division = criterions.pop('division', None)
        location = criterions.pop('location', None)
        parcel_owner = criterions.pop('parcel_owner', None)
        criterions_values = criterions.values()
        misc_criterions = any(criterions_values)
        enough_misc_criterions = len([val for val in criterions_values if val]) > 1

        text_search = location or parcel_owner
        enough = (division and misc_criterions) or enough_misc_criterions or text_search
        return enough

    def search_parcels(self):
        """
        Return parcels macthing search criterions.
        """
        search_args = self.extract_search_criterions(self.request)
        options = self.extract_search_options(self.request)

        if not self.has_enough_criterions(self.request):
            return []
        if options.get('parcel_history'):
            return []

        cadastre = services.cadastre.new_session()
        query_result = cadastre.query_parcels(**search_args)
        cadastre.close()

        if options.get('browse_old_parcels'):
            old_parcels = self.search_old_parcels(parcels_to_ignore=query_result)
            query_result.extend(old_parcels)

        return query_result

    def search_old_parcels(self, parcels_to_ignore=[]):
        """
        Return old parcels macthing search criterions 'search_args'.
        """
        to_ignore = set([str(prc) for prc in parcels_to_ignore])
        search_args = self.extract_search_criterions(self.request)

        cadastre = services.cadastre.new_session()
        query_result = cadastre.query_old_parcels(**search_args)
        cadastre.close()

        search_result = []
        for parcel in query_result:
            if str(parcel) not in to_ignore:
                setattr(parcel, 'old', True)
                search_result.append(parcel)

        return search_result


    def search_parcels_custom(self, old=False, **search_args):
        """
        Return parcels matching method parameters.
        """
        search_result = []
        search_args = dict((k, v) for k, v in search_args.iteritems() if v)
        cadastre = services.cadastre.new_session()
        try:
            if old:
                query_result_old = cadastre.query_old_parcels(**search_args)
                for parcel in query_result_old:
                    setattr(parcel, 'old', True)
                    search_result.append(parcel)
            else:
                search_result = cadastre.query_parcels(**search_args)
        finally:
            cadastre.close()
            
        return search_result


    def search_historic_of_parcel(self):
        """
        Return the concerned parcels
        """
        search_args = self.extract_parcel_reference_criterions(self.request)
        cadastre = services.cadastre.new_session()
        historic = cadastre.query_parcel_historic(**search_args)
        cadastre.close()
        return historic

    def createParcelAndProprietary(self, parcel_data, proprietary_data):
        parcel_address = parcel_data.pop('location')
        self.createApplicantFromParcel(parcel_address=parcel_address, **proprietary_data)
        self.createParcel(parcel_data)

    def createParcel(self, parcel_data):
        portal_urban = api.portal.get_tool('portal_urban')
        portal_urban.createPortionOut(container=self.context, **parcel_data)

    def createApplicantFromParcel(self, proprietary, proprietary_city, proprietary_address, parcel_address):
        """
           Create the PortionOut with given parameters...
        """
        contact_type = 'Applicant'
        if IUrbanCertificateBase.providedBy(self.context) or IDivision.providedBy(self.context):
            contact_type = 'Proprietary'

        container = self.context
        same_address = self._areSameAdresses(proprietary_address, parcel_address)
        city = proprietary_city.split()
        zipcode = city[0]
        city = ' '.join(city[1:])
        person_street, person_number = self._extractStreetAndNumber(proprietary_address)

        contacts = proprietary.split('&')
        for contact in contacts:
            names = contact.split(',')
            contact_info = {
                'isSameAddressAsWorks': same_address,
                'name1': names[0],
                'zipcode': zipcode,
                'city': city,
                'street': person_street,
                'number': person_number,
            }
            if len(names) > 1:
                contact_info['name2'] = names[1].split()[0].capitalize()
            container.invokeFactory(contact_type, id=container.generateUniqueId(contact_type), **contact_info)

        container.updateTitle()

    def _extractStreetAndNumber(self, address):
        address_words = address.split()
        number = address_words[-1]
        if re.match('\d', number) and number.lower() != '1er':
            street = ' '.join(address_words[0:-1])
            return (street, number)
        else:
            return (address, '')

    def _areSameAdresses(self, address_a, address_b):
        """
         Addresses are the same if fuzzy match on street name and EXACT match on number
        """
        street_a, number_a = self._extractStreetAndNumber(address_a)
        street_b, number_b = self._extractStreetAndNumber(address_b)

        same_street = Levenshtein.ratio(street_a, street_b) > 0.8
        same_number = self._haveSameNumbers(number_a, number_b)

        return same_street and same_number

    def _haveSameNumbers(self, num_a, num_b):
        match_expr = '\d+'
        numbers_a = re.findall(match_expr, num_a)
        numbers_b = re.findall(match_expr, num_b)
        common_numbers = list(set(numbers_a).intersection(set(numbers_b)))
        return common_numbers
