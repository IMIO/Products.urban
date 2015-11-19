
from Products.Five import BrowserView

from Products.urban.browser.table.urbantable import ParcelsTable
from Products.urban.interfaces import IDivision
from Products.urban.interfaces import IGenericLicence
from Products.urban.interfaces import IUrbanCertificateBase

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
        if not self.searchHasCriteria(self.request):
            #we still not launched the search, everything is ok ;-)
            if 'division' in request or 'location' in request or 'prcOwner' in request:
                plone_utils = api.portal.get_tool('plone_utils')
                plone_utils.addPortalMessage(translate('warning_enter_search_criteria'), type="warning")

    def __call__(self):
        if 'add_parcel' in self.request.form:
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
        from Products.urban.services import cadastre  # keep the import here as long connections settings are on portal_urban
        if not cadastre.check_connection():
            return None

        all_divisions = [('', translate('all_divisions', 'urban', context=self.request))]
        for division in cadastre.get_all_divisions():
            all_divisions.append(division)

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

    def getDivisions(self):
        """
          Returns the existing divisions
          If we had a problem getting the divisions, we return nothing so the
          search form is not displayed
        """
        return self.divisions

    def searchHasCriteria(self, request):
        """
        """
        division = request.get('division', '')
        section = request.get('section', '')
        radical = request.get('radical', '')
        bis = request.get('bis', '')
        exposant = request.get('exposant', '')
        puissance = request.get('puissance', '')
        location = request.get('location', '')
        prcOwner = request.get('prcOwner', '')
        #the division is not enough
        if (not division or (not section and not radical and not bis and not exposant and not puissance and not location and not prcOwner)) and not location and not prcOwner:
            return False
        else:
            return True

    def findParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, location=None, prc_owner=None, prc_history=None, browseoldparcels=False):
        """
           Return the concerned parcels
        """
        if not self.searchHasCriteria(self.context.REQUEST):
            return []
        if prc_history:
            return []
        parcels = self.portal_urban.queryParcels(division, section, radical, bis, exposant, puissance, location, prc_owner)
        result = [prc.getParcelAsDictionary() for prc in parcels]
        already_found = set([str(prc) for prc in parcels])
        if browseoldparcels and not prc_history and not prc_owner:
            old_parcels = self.portal_urban.queryParcels(division, section, radical, bis, exposant, puissance, browseold=browseoldparcels)
            for parcel in old_parcels:
                if str(parcel) not in already_found:
                    dict_prc = parcel.getParcelAsDictionary()
                    dict_prc['old'] = True
                    result.append(dict_prc)
        return result

    def findOldParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, old=False):
        """
        Return the concerned parcels
        """
        parcel = self.portal_urban.queryParcels(division, section, radical, bis, exposant, puissance, historic=True, browseold=True, fuzzy=False)[0]
        return parcel.getHistoricForDisplay()

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
