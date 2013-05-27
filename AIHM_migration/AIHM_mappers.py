# -*- coding: utf-8 -*-

from Products.urban.Extensions.access_migration.mapper import *
from Products.urban.Extensions.access_migration.factory import *
from Products.urban.Extensions.AIHM_migration.AIHM_misc import *
from DateTime import DateTime
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
import re

#
# LICENCE
#

# factory


class LicenceFactory(BaseFactory):
    def getCreationPlace(self, **kwargs):
        path = '%s/urban/%ss' % (self.site.absolute_url_path(), kwargs['portal_type'].lower())
        return self.site.restrictedTraverse(path)

# mappers


class IdMapper(Mapper):
    def mapId(self, line, **kwargs):
        return normalizeString(self.getData('CLEF'))


class PortalTypeMapper(Mapper):
    def mapPortal_type(self, line, **kwargs):
        type_value = self.getData('TYPE')
        return TYPE_map[type_value]['portal_type']

    def mapFoldercategory(self, line, **kwargs):
        type_value = self.getData('TYPE')
        return TYPE_map[type_value]['foldercategory']


class WorklocationMapper(Mapper):
    def mapWorklocations(self, line, **kwargs):
        num = self.getData('NumPolParcelle')
        noisy_words = set(('d', 'du', 'de', 'des', 'le', 'la', 'les', 'à', ',', 'rues'))
        street = self.getData('AdresseDuBien')
        street = cleanAndSplitWord(street)
        street_keywords = [word for word in street if word not in noisy_words and len(word) > 1]
        street_keywords.extend(cleanAndSplitWord(self.getData('AncCommune')))
        try:
            brains = self.catalog(portal_type='Street', Title=street_keywords)
        except:
            import ipdb; ipdb.set_trace()
        if len(brains) == 1:
            return ({'street': brains[0].UID, 'number': num},)
        if street:
            self.logError('Couldnt find street or found too much streets', {'street': street_keywords, 'search result': len(brains)})
        return {}


class PcaMapper(Mapper):
    def mapIsinpca(self, line, **kwargs):
        return bool(self.getData('DatePPA'))

    def mapPca(self, line, **kwargs):
        if not self.mapIsinpca(line, **kwargs):
            return []
        pca_date = normalizeDate(self.getData('DatePPA'))
        pcas = self.catalog(Title=pca_date)
        if len(pcas) != 1:
            self.logError('Couldnt find pca or found too much pca', {'date': pca_date})
            return []
        return pcas[0].id


class ParcellingsMapper(Mapper):
    def mapIsinsubdivision(self, line, **kwargs):
        return any([self.getData('NumLot'), self.getData('DateLot'), self.getData('DateLotUrbanisme')])

    def mapParcellings(self, line, **kwargs):
        if not self.mapIsinsubdivision(line, **kwargs):
            return []
        auth_date = normalizeDate(self.getData('DateLot'))
        approval_date = normalizeDate(self.getData('DateLotUrbanisme'))
        city = self.getData('AncCommune').split('-')
        keywords = [approval_date] + city
        parcellings = self.catalog(Title=keywords)
        if len(parcellings) == 1:
            return parcellings[0].getObject().UID()
        keywords = [auth_date] + city
        parcellings = self.catalog(Title=keywords)
        if len(parcellings) == 1:
            return parcellings[0].getObject().UID()
        self.logError('Couldnt find parcelling or found too much parcelling', {'approval date': approval_date, 'auth_date': auth_date, 'city': city})
        return []


class ParcellingRemarksMapper(Mapper):
    def mapLocationtechnicalremarks(self, line, **kwargs):
        return '<p>%s</p>' % self.getData('PPAObservations')


class ObservationsMapper(Mapper):
    def mapDescription(self, line, **kwargs):
        return '<p>%s</p>' % self.getData('Observations')


class ReferenceMapper(PostCreationMapper):
    def mapReference(self, line, plone_object, **kwargs):
        date = self.getData('DateRecDem') and self.getData('DateRecDem') or None
        return self.site.portal_urban.generateReference(plone_object, **{'date': DateTime(date)})


class ArchitectMapper(PostCreationMapper):
    def mapArchitects(self, line, plone_object, **kwargs):
        archi_name = self.getData('NomArchitecte')
        fullname = cleanAndSplitWord(archi_name)
        if not fullname:
            return []
        noisy_words = ['monsieur', 'madame', 'architecte', '&', ',', '.']
        name_keywords = [word.lower() for word in fullname if word.lower() not in noisy_words]
        architects = self.catalog(portal_type='Architect', Title=name_keywords)
        if len(architects) == 1:
            return architects[0].getObject()
        self.logError('No architects found or too much architects found', {'name': name_keywords, 'search_result': len(architects)})
        return []


class GeometricianMapper(PostCreationMapper):
    def mapGeometricians(self, line, plone_object, **kwargs):
        title_words = [word for word in self.getData('Titre').lower().split()]
        for word in title_words:
            if word not in ['géometre', 'géomètre']:
                return
        name = self.getData('Nom')
        name = cleanAndSplitWord(name)
        firstname = self.getData('Prenom')
        firstname = cleanAndSplitWord(firstname)
        names = name + firstname
        geometrician = self.catalog(portal_type='Geometrician', Title=names)
        if not geometrician:
            geometrician = self.catalog(portal_type='Geometrician', Title=name)
        if len(geometrician) == 1:
            return geometrician[0].getObject()
        self.logError('no geometricians found or too much geometricians found',
                      {'title': self.getData('Titre'), 'name': name, 'firstname': firstname, 'search_result': len(geometrician)})
        return []


class NotaryMapper(PostCreationMapper):
    def mapNotarycontact(self, line, plone_object, **kwargs):
        title = self.getData('Titre').lower()
        if title not in Titre_map or Titre_map[title] not in ['master', 'masters']:
            return
        name = self.getData('Nom')
        firstname = self.getData('Prenom')
        notary = self.catalog(portal_type='Notary', Title=[name, firstname])
        if not notary:
            notary = self.catalog(portal_type='Notary', Title=name)
        if len(notary) == 1:
            return notary[0].getObject()
        self.logError('no notaries found or too much notaries found',
                      {'title': self.getData('Titre'), 'name': name, 'firstname': firstname, 'search_result': len(notary)})
        return []


class CompletionStateMapper(PostCreationMapper):
    def map(self, line, plone_object, **kwargs):
        self.line = line
        state = ''
        if bool(int(self.getData('DossierIncomplet'))):
            state = 'incomplete'
        elif self.getData('Refus') == 'O':
            state = 'accepted'
        elif self.getData('Refus') == 'N':
            state = 'refused'
        elif plone_object.portal_type in ['MiscDemand']:
            state = 'accepted'
        else:
            return
        workflow_tool = getToolByName(plone_object, 'portal_workflow')
        workflow_def = workflow_tool.getWorkflowsFor(plone_object)[0]
        workflow_id = workflow_def.getId()
        workflow_state = workflow_tool.getStatusOf(workflow_id, plone_object)
        workflow_state['review_state'] = state
        workflow_tool.setStatusOf(workflow_id, plone_object, workflow_state.copy())

#
# CONTACT
#

# factory


class ContactFactory(BaseFactory):
    def create(self, place, **kwargs):
        if self.getPortalType(place) == 'Applicant' or kwargs['personTitle'] not in ['master', 'masters']:
            return super(ContactFactory, self).create(place, **kwargs)
        else:
            #notaries are bound  with a reference
            return []

    def getPortalType(self, place, **kwargs):
        if place.portal_type in ['UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter']:
            return 'Proprietary'
        return 'Applicant'

# mappers


class ContactIdMapper(Mapper):
    def mapId(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        name = '%s %s' % (self.getData('%sNom' % m), self.getData('%sPrenom' % m))
        return normalizeString(self.site.portal_urban.generateUniqueId(name))


class ContactTitleMapper(Mapper):
    def mapPersontitle(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        titre = self.getData('%sTitre' % m).lower()
        if titre in Titre_map.keys():
            return Titre_map[titre]
        return 'notitle'


class ContactNameMapper(Mapper):
    def mapName1(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sNom' % m)


class ContactFirstnameMapper(Mapper):
    def mapName2(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sPrenom' % m)


class ContactSreetMapper(Mapper):
    def mapStreet(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sAdresse' % m)


class ContactNumberMapper(Mapper):
    def mapNumber(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        number = self.getData('%sNumPolice' % m)
        box = self.getData('%sBtePost' % m)
        return "%s%s" % (number, box and '/%s' % box or '')


class ContactZipcodeMapper(Mapper):
    def mapZipcode(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sCP' % m)


class ContactCityMapper(Mapper):
    def mapCity(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sLocalite' % m)


class ContactCountryMapper(Mapper):
    def mapCountry(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        try:
            return country_map[self.getData('%sPays' % m).lower()]
        except:
            self.logError('Unknown country', {'country': self.getData('Pays')})


class ContactPhoneMapper(Mapper):
    def mapPhone(self, line, **kwargs):
        m = self.getData('MandantNom') and 'Mandant' or ''
        return self.getData('%sTelephone' % m)


class ContactRepresentedByMapper(Mapper):
    def mapRepresentedby(self, line, container, **kwargs):
        if not self.getData('MandantNom'):
            return ''
        if container.portal_type == 'BuildLicence':
            return container.getArchitects() and container.getArchitects()[0].UID() or ''
        elif container.portal_type in ['UrbanCertificateOne', 'UrbanCertificateTwo']:
            return container.getNotaryContact() and container.getNotaryContact()[0].UID() or ''

#
# PARCEL
#

#factory


class ParcelFactory(MultiObjectsFactory):
    def create(self, place=None, **kwargs):
        found_parcels = {}
        not_found_parcels = {}
        searchview = self.site.restrictedTraverse('searchparcels')
        for index, args in kwargs.iteritems():
            #need to trick the search browser view about the args in its request
            for k, v in args.iteritems():
                searchview.context.REQUEST[k] = v
            #check if we can find a parcel in the db cadastre with these infos
            found = searchview.findParcel(**args)
            if not found:
                found = searchview.findParcel(browseoldparcels=True, **args)
            if len(found) == 1:
                args['divisionCode'] = args['division']
                args['division'] = args['division']
                found_parcels[index] = args
            else:
                not_found_parcels[index] = args
                self.logError('Too much parcels found or not enough parcels found', {'args': args, 'search result': len(found)})
        return super(ParcelFactory, self).create(place=place, **found_parcels)

# mappers


class ParcelDataMapper(SecondaryTableMapper):
    pass


class RadicalMapper(Mapper):
    def mapRadical(self, line, **kwargs):
        radical = self.getData('RADICAL')
        if not radical:
            return radical
        return str(int(float(radical)))


class ExposantMapper(Mapper):
    def mapExposant(self, line, **kwargs):
        raw_val = self.getData('EXPOSANT')
        result = re.search('[a-z]', raw_val, re.I)
        exposant = result and result.group().capitalize() or ''
        return exposant

    def mapPuissance(self, line, **kwargs):
        raw_val = self.getData('EXPOSANT')
        result = re.search('\d+', raw_val)
        puissance = result and result.group() or ''
        return puissance


class BisMapper(Mapper):
    def mapBis(self, line, **kwargs):
        bis = self.getData('BIS')
        if not bis:
            return bis
        return str(int(float(bis)))


#
# UrbanEvent deposit
#

# factory
class UrbanEventFactory(BaseFactory):
    def getPortalType(self, **kwargs):
        return 'UrbanEvent'

    def create(self, place, **kwargs):
        if not kwargs['eventtype']:
            return []
        urban_tool = getToolByName(place, 'portal_urban')
        edit_url = urban_tool.createUrbanEvent(place.UID(), kwargs['eventtype'])
        return [getattr(place, edit_url.split('/')[-2])]

#mappers


class DepositEventTypeMapper(Mapper):
    def mapEventtype(self, line, **kwargs):
        licence = kwargs['container']
        urban_tool = getToolByName(licence, 'portal_urban')
        eventtype_id = eventtype_id_map[licence.portal_type]['deposit_event']
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, eventtype_id).UID()


class DepositDateMapper(PostCreationMapper):
    def mapEventdate(self, line, plone_object, **kwargs):
        date = self.getData('DateRecDem')
        date = date and DateTime(date) or None
        if not date:
            self.logError('No deposit date found')
        return date

#
# UrbanEvent complete folder
#

#mappers


class CompleteFolderEventTypeMapper(Mapper):
    def mapEventtype(self, line, **kwargs):
        licence = kwargs['container']
        urban_tool = getToolByName(licence, 'portal_urban')
        eventtype_id = eventtype_id_map[licence.portal_type]['folder_complete']
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, eventtype_id).UID()


class CompleteFolderDateMapper(PostCreationMapper):
    def mapEventdate(self, line, plone_object, **kwargs):
        date = self.getData('AvisDossierComplet')
        date = date and DateTime(date) or None
        if not date:
            self.logError("No 'folder complete' date found")
        return date

#
# UrbanEvent decision
#

#mappers


class DecisionEventTypeMapper(Mapper):
    def mapEventtype(self, line, **kwargs):
        if self.getData('Refus') == 'A':
            return ''
        licence = kwargs['container']
        urban_tool = getToolByName(licence, 'portal_urban')
        eventtype_id = eventtype_id_map[licence.portal_type]['decision_event']
        config = urban_tool.getUrbanConfig(licence)
        return getattr(config.urbaneventtypes, eventtype_id).UID()


class DecisionDateMapper(PostCreationMapper):
    def mapDecisiondate(self, line, plone_object, **kwargs):
        date = self.getData('DateDecisionCollege')
        date = date and DateTime(date) or None
        if not date:
            self.logError('No decision date found')
        return date


class NotificationDateMapper(PostCreationMapper):
    def mapEventdate(self, line, plone_object, **kwargs):
        date = self.getData('DateNotif')
        date = date and DateTime(date) or None
        if not date:
            self.logError('No notification date found')
        return date


class DecisionMapper(PostCreationMapper):
    def mapDecision(self, line, plone_object, **kwargs):
        decision = self.getData('Refus')
        if decision == 'O':
            return 'favorable'
        elif decision == 'N':
            return 'defavorable'
        #error
        return
