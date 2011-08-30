# -*- coding: utf-8 -*-
#
# File: base.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.5
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from zope.component.interface import interfaceToName
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from zope.i18n import translate
from zope.interface import implements
import interfaces


class UrbanBase(object):
    """
      This class manage every methods chared cross different licences
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanBase)

    security.declarePublic('getApplicantsSignaletic')
    def getApplicantsSignaletic(self, withaddress=False):
        """
          Returns a string representing the signaletic of every applicants
        """
        applicants = self.getApplicants()
        signaletic = ''
        for applicant in applicants:
            #if the signaletic is not empty, we are adding several applicants
            if signaletic:
                signaletic += ' %s '% translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += applicant.getSignaletic(withaddress=withaddress)
        return signaletic

    security.declarePublic('getFolderManagersSignaletic')
    def getFolderManagersSignaletic(self, withGrade=False, withEmail=False, withTel=False):
        """
          Returns a string representing the signaletic of every folder managers
        """
        fms = self.getFoldermanagers()
        signaletic = ''
        for fm in fms:
            #if the signaletic is not empty, we are adding several folder managers
            if signaletic:
                signaletic += '<p><strong>%s</strong>' % fm.getSignaletic()
            else:
                signaletic = '<p><strong>%s</strong>' % fm.getSignaletic()
            if withGrade:
                signaletic += ' (%s)' % self.displayValue(fm.listGrades(), fm.getGrade()).encode('utf8')
            if withEmail:
                signaletic += '<br />%s' % fm.getEmail()
            if withTel:
                signaletic += '<br />%s' % fm.getPhone()
            signaletic += '</p>'
        return signaletic

    security.declarePublic('getReferenceForTemplate')
    def getReferenceForTemplate(self):
        """
          Calculate the reference to be displayed in the templates
        """
        return "Calculated/Reference/%s" % str(self.getReference())

    security.declarePublic('getNotariesSignaletic')
    def getNotariesSignaletic(self):
        """
          Returns a string reprensenting the signaletic of every notaries
        """
        notaries = self.getNotaryContact()
        signaletic = ''
        for notary in notaries:
            #if the signaletic is not empty, we are adding several notaries
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += notary.getSignaletic()
        return signaletic

    security.declarePublic('getArchitectsSignaletic')
    def getArchitectsSignaletic(self, withaddress=False):
        """
          Returns a string reprensenting the signaletic of every architects
        """
        architects = self.getArchitects()
        signaletic = ''
        for architect in architects:
            #if the signaletic is not empty, we are adding several architects
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += architect.getSignaletic(withaddress=withaddress)
        return signaletic

    security.declarePublic('submittedBy')
    def submittedBy(self):
        """
          Returns a formatted string with data about people that submitted
          3 cases :
          - the applicant submitted the request for himself
          - a notary submitted the request for the applicant
          - a notary submitted the request for himself
        """
        if self.getPortalTypeName() in ('UrbanCertificateOne', 'UrbanCertificateTwo', 'NotaryLetter'):
            who = self.getWhoSubmitted()
            if who == 'both':
                #a notary submitted the request for an applicant
                return translate('request_submitted_by_both', 'urban', context=self.REQUEST, mapping={'notary': self.getNotariesSignaletic(), 'applicant': self.getApplicantsSignaletic(), }).encode('utf8')
            elif who == 'applicant':
                #an applicant submitted the request for himself
                return translate('request_submitted_by_applicant', 'urban', context=self.REQUEST, mapping={'applicant': self.getApplicantsSignaletic(), }).encode('utf8')
            elif who == 'notary':
                #a notary submitted the request without an applicant (??? possible ???)
                return translate('request_submitted_by_notary', 'urban', context=self.REQUEST, mapping={'notary': self.getNotariesSignaletic(), }).encode('utf8')
            return ''
        elif self.getType() == 'ParceOutLicence':
            return 'test'

    security.declarePublic('getWorkLocationSignaletic')
    def getWorkLocationSignaletic(self):
        """
          Returns a string reprensenting the different worklocations
        """
        catalog = getToolByName(self, "uid_catalog")
        signaletic = ''
        for wl in self.getWorkLocations():
            #wl is a dict with street as the street obj uid and number as the number in the street
            street = catalog(UID = wl['street'])[0].getObject()
            city = street.getParentNode()
            if street.getPortalTypeName() == 'Locality':
                streetName = street.getLocalityName()
            else:
                streetName = street.getStreetName()
            number = wl['number']
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            #special case for locality where we clearly specify that this is a locality
            if street.portal_type == 'Locality':
                signaletic += '%s ' % translate('locality_for_worklocation', 'urban', context=self.REQUEST, default='locality').encode('utf8')
            if number:
                signaletic += "%s, %s - %d %s" % (number, streetName, city.getZipCode(), city.Title())
            else:
                signaletic += "%s - %d %s" % (streetName, city.getZipCode(), city.Title())
        return signaletic

    security.declarePublic('getLicenceTypeAcronym')
    def getLicenceTypeAcronym(self):
        """
          Returns a small string representing the licence type
        """
        licenceTypes = {
                        'BuildLicence': 'PU',
                        'ParcelOutLicence': 'PL',
                        'UrbanCertificateOne': 'CU1',
                        'UrbanCertificateTwo': 'CU2',
                        'EnvironmentalDeclaration': 'DeclEnv',
                        'Declaration': 'Decl',
                        'Division': 'Div',
                       }
        try:
            return licenceTypes[self.portal_type]
        except KeyError:
            #in some case (a portal_type not equals to the meta_type)
            #the portal_type is not set yet at factory time, try to find it
            portal_type = self.REQUEST['__factory__info__']['stack'][0]
            return licenceTypes[portal_type]

    security.declarePublic('getDepositDate')
    def getDepositDate(self):
        """
          Returns the date the folder was brought to the urbanism service
        """
        tool = getToolByName(self, 'portal_urban')
        #get the event called 'depot-de-la-demande' and returns the linked eventDate
        depositEvent = tool.getEventByEventTypeId(self, 'depot-de-la-demande')
        if depositEvent:
            tool = getToolByName(self, 'portal_urban')
            return tool.formatDate(depositEvent.getEventDate())
        return translate('warning_no_deposit_date', 'urban', context=self.REQUEST).encode('utf8')

    security.declarePublic('getMultipleApplicantsCSV')
    def getMultipleApplicantsCSV(self):
        """
          Returns a formatted version of the applicants to be used in POD templates
        """
        applicants = self.getApplicants()
        toreturn = '<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for applicant in applicants:
            toreturn = toreturn + '%' + applicant.getPersonTitleValue() + '|' + applicant.getName1() + \
                    '|' + applicant.getName2() + '|' + applicant.getNumber() + ', ' + \
                    applicant.getStreet() + '|' + applicant.getZipcode() + ' ' + applicant.getCity()
        toreturn = toreturn + '</CSV>'
        return toreturn
    getMultipleApplicants = getMultipleApplicantsCSV

    security.declarePublic('getMultipleArchitectsCSV')
    def getMultipleArchitectsCSV(self):
        """
          Returns a formatted version of the architects to be used in POD templates
        """
        architects = self.getArchitects()
        toreturn = '<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for architect in architects:
            toreturn = toreturn + '%' + architect.getPersonTitleValue() + '|' + architect.getName1() + '|' +\
                    architect.getName2() + '|' + architect.getNumber() + ', ' + architect.getStreet() + '|' + \
                    architect.getZipcode() + ' ' + architect.getCity()
        toreturn = toreturn + '</CSV>'
        return toreturn

    security.declarePublic('getMultipleNotariesCSV')
    def getMultipleNotariesCSV(self):
        """
          Returns a formatted version of the notaries to be used in POD templates
        """
        notaries = self.getNotaryContact()
        toreturn = '<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for notary in notaries:
            toreturn = toreturn + '%' + notary.getPersonTitleValue() + '|' + notary.getName1() + '|' +\
                    notary.getName2() + '|' + notary.getNumber() + ', ' + notary.getStreet() + '|' +\
                    notary.getZipcode() + ' ' + notary.getCity()
        toreturn = toreturn + '</CSV>'
        return toreturn

    security.declarePublic('getMultipleRealSubmittersCSV')
    def getMultipleRealSubmittersCSV(self):
        """
          Find who really submitted the request...
        """
        who = self.getWhoSubmitted()
        if who in ['notary', 'both']:
            return self.getMultipleNotariesCSV()
        elif who == 'applicant':
            return self.getMultipleApplicantsCSV()
        else:
            return ''

    security.declarePublic('getTerm')
    def getTerm(self, termFolder, termId):
        """
          Returns a term object for a given term folder
        """
        tool = getToolByName(self, 'portal_urban')
        urbanConfig = tool.getUrbanConfig(self)
        termFolderObj = getattr(urbanConfig, termFolder)
        return getattr(termFolderObj, termId)

    security.declarePublic('getPortionOutsText')
    def getPortionOutsText(self, linebyline=True):
        """
          Return a displayable version of the parcels
        """
        toreturn = ''
        isFirst = True
        for portionOutObj in self.getParcels():
            #add a separator between every parcel
            #either a '\n'
            if not isFirst and linebyline:
                toreturn += '\n'
            #or an "and "
            elif not isFirst:
                toreturn += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            toreturn += 'section %s' % portionOutObj.getSection()
            toreturn += ' %s' % portionOutObj.getRadical()
            if portionOutObj.getBis() != '':
                toreturn += '/%s' % portionOutObj.getBis()
            toreturn += portionOutObj.getExposant()
            toreturn += portionOutObj.getPuissance()
            isFirst = False
        return toreturn

    security.declarePublic('getListCapaKey')
    def getListCapaKey(self):
        """
           Return the list of capaKeys for each parcel(portionOut) for the Licence
        """
        listCapaKey = []
#        context=aq_inner(self.context)
        for parcel in  self.objectValues('PortionOut'):
            divisioncode = parcel.getDivisionCode()
            section = parcel.getSection()
            radical = parcel.getRadical()
            puissance = parcel.getPuissance()
            exposant = parcel.getExposant()
            bis = parcel.getBis()
            if not puissance:
                puissance = 0
            if not exposant:
                exposant = "_"
            if not bis:
                bis = 0
#            nis section (radical 0x) / (bis 0x) (exposant si blanc _)  (puissance 00x)
            try:
                capaKey = "%s%s%04d/%02d%s%03d" % (divisioncode, section, int(radical), int(bis), exposant, int(puissance))
            except ValueError:
                capaKey = ""
            listCapaKey.append(capaKey)
        return listCapaKey

    def _getAllEvents(self,  eventInterface=None):
        catalog = getToolByName(self, 'portal_catalog')
        currentPath = '/'.join(self.getPhysicalPath())
        query = {'path': {'query': currentPath,
                          'depth': 1},
                 'meta_type': ['UrbanEvent', 'UrbanEventInquiry'],
                 'sort_on': 'getObjPositionInParent'}
        if eventInterface is not None:
            interfaceName = interfaceToName(self, eventInterface)
            query['object_provides'] = interfaceName
        return [brain.getObject() for brain in catalog(**query)]

    def _getLastEvent(self, eventInterface=None):
        events = self._getAllEvents(eventInterface)
        if events:
            return events[-1]

    security.declarePublic('attributeIsUsed')    
    def attributeIsUsed(self, name):
        """
          Is the attribute named as param name used in this LicenceConfig ?
        """
        licenceConfig = getToolByName(self, 'portal_urban').getUrbanConfig(self, urbanConfigId=self.portal_type)
        return (name in licenceConfig.getUsedAttributes())

    security.declarePublic('getUrbanEvents')
    def getUrbanEvents(self):
        """
          Return every contained UrbanEvents (of any type)...
        """
        return self.listFolderContents({'portal_type': ('UrbanEventInquiry', 'UrbanEvent', ),})

