
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
import ast


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
        # this way, get_all_divisions display a portal message if needed
        self.divisions = self._init_divisions()
        # if the search was launched with no criteria, add a message
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
            if 'owners' in self.request.form:
                owners = ast.literal_eval(self.request.get('owners', None))
                parcel_data['location'] = self.request.get('location').decode('utf8')
                self.createParcelAndProprietary(parcel_data, owners)
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

        if not self.has_enough_criterions(self.request):
            return []

        cadastre = services.cadastre.new_session()
        query_result = cadastre.query_parcels(**search_args)
        cadastre.close()

        if self.request.get('browse_old_parcels', False):
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

    def createParcelAndProprietary(self, parcel_data, owners):
        parcel_address = parcel_data.pop('location')
        self.createApplicantFromParcel(owners, parcel_address)
        self.createParcel(parcel_data)

    def createParcel(self, parcel_data):
        portal_urban = api.portal.get_tool('portal_urban')
        portal_urban.createPortionOut(container=self.context, **parcel_data)

    def createApplicantFromParcel(self, owners, parcel_address):
        """
           Create the PortionOut with given parameters...
        """
        contact_type = 'Applicant'
        if IUrbanCertificateBase.providedBy(self.context) or IDivision.providedBy(self.context):
            contact_type = 'Proprietary'

        container = self.context
        for owner in owners:
            contact_info = {
                    'isSameAddressAsWorks': self._areSameAdresses(owners[owner]['street'], parcel_address),
                    'name1': owners[owner]['name'],
                    'name2': owners[owner]['firstname'],
                    'zipcode': owners[owner]['zipcode'],
                    'city': owners[owner]['city'],
                    'street': owners[owner]['street'],
                    'number': owners[owner]['number'],
            }
            container.invokeFactory(contact_type, id=container.generateUniqueId(contact_type), **contact_info)
        container.updateTitle()

    def _extractStreetAndNumber(self, address):
        streetAndNumber = (address, '')
        address_words = address.split()
        if address_words:
            number = address_words[-1]
            if re.match('\d', number) and number.lower() != '1er':
                street = ' '.join(address_words[0:-1])
                streetAndNumber = (street, number)
        return streetAndNumber

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
