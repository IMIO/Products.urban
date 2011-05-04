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

from AccessControl import ClassSecurityInfo
from Products.urban.config import *
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate as _

class UrbanBase:
    """
      This class manage every methods chared cross different licences
    """
    security = ClassSecurityInfo()

    security.declarePublic('getApplicantsSignaletic')
    def getApplicantsSignaletic(self, withaddress=False):
        """
          Returns a string reprensenting the signaletic of every applicants
        """
        applicants = self.getApplicants()
        signaletic = ''
        for applicant in applicants:
            #if the signaletic is not empty, we are adding several applicants
            if signaletic:
                try:
                    signaletic = signaletic + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
                except UnicodeDecodeError:
                    signaletic = unicode(signaletic, 'utf-8') + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
            try:
                signaletic = signaletic + applicant.getSignaletic(withaddress=withaddress)
            except UnicodeDecodeError:
                signaletic = signaletic + unicode(applicant.getSignaletic(withaddress=withaddress), 'utf-8')
        return signaletic

    security.declarePublic('getFolderManagersSignaletic')
    def getFolderManagersSignaletic(self, withgrade=True):
        """
          Returns a string reprensenting the signaletic of every folder managers
        """
        fms = self.getFoldermanagers()
        signaletic = ''
        for fm in fms:
            #if the signaletic is not empty, we are adding several folder managers
            if signaletic:
                signaletic = signaletic + '<p>' + fm.getSignaletic()
            else:
                signaletic = '<p>' + fm.getSignaletic()
            if withgrade:
                signaletic = signaletic + ' (' + self.displayValue(fm.listGrades(), fm.getGrade()) + ')'
            signaletic = signaletic + '</p>'
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
                signaletic = unicode(signaletic, 'utf-8') + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
            signaletic = signaletic + notary.getSignaletic()
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
                try:
                    signaletic = signaletic + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
                except UnicodeDecodeError:
                    signaletic = unicode(signaletic, 'utf-8') + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
                signaletic = unicode(signaletic, 'utf-8') + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
            try:
                signaletic = signaletic + architect.getSignaletic(withaddress=withaddress)
            except UnicodeDecodeError:
                signaletic = signaletic + unicode(architect.getSignaletic(withaddress=withaddress), 'utf-8')
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
        applicants = self.getApplicants()
        if self.getPortalTypeName() in ('UrbanCertificateOne','UrbanCertificateTwo','NotaryLetter'):
            who = self.getWhoSubmitted()
            if who == 'both':
                #a notary submitted the request for an applicant
                return _('request_submitted_by_both', 'urban', context=self.REQUEST, mapping={'notary': self.getNotariesSignaletic(), 'applicant': self.getApplicantsSignaletic(), })
            elif who == 'applicant':
                #an applicant submitted the request for himself
                return _('request_submitted_by_applicant', 'urban', context=self.REQUEST, mapping={'applicant': self.getApplicantsSignaletic(), })
            elif who == 'notary':
                #a notary submitted the request without an applicant (??? possible ???)
                return _('request_submitted_by_notary', 'urban', context=self.REQUEST, mapping={'notary': self.getNotariesSignaletic(), })
            return ''
        elif self.getType() == 'ParceOutLicence':
            return 'test'

    security.declarePublic('getWorkLocationSignaletic')
    def getWorkLocationSignaletic(self):
        """
          Returns a string reprensenting the different worklocations
        """
        signaletic = ''
        for wl in self.getWorkLocations():
            if signaletic:
                signaletic = unicode(signaletic, 'utf-8') + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
            signaletic = signaletic + wl.getSignaletic()
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

    security.declarePublic('getDefaultFolderManagers')
    def getDefaultFolderManagers(self):
        """
          Returns the default folderManagers for a licence
          This is the default_method for 'foldermanagers' field of different licences
        """
        pass

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
        return _('warning_no_deposit_date', 'urban', context=self.REQUEST)

    security.declarePublic('getMultipleApplicantsCSV')
    def getMultipleApplicantsCSV(self):
        """
          Returns a formatted version of the applicants to be used in POD templates
        """
        applicants = self.getApplicants()
        toreturn='<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for applicant in applicants:
            toreturn=toreturn+'%'+applicant.getPersonTitleValue()+'|'+applicant.getName1()+'|'+applicant.getName2()+'|'+applicant.getNumber()+', '+applicant.getStreet()+'|'+applicant.getZipcode()+' '+applicant.getCity()
        toreturn=toreturn+'</CSV>'
        return toreturn
    getMultipleApplicants=getMultipleApplicantsCSV

    security.declarePublic('getMultipleArchitectsCSV')
    def getMultipleArchitectsCSV(self):
        """
          Returns a formatted version of the architects to be used in POD templates
        """
        architects = self.getArchitects()
        toreturn='<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for architect in architects:
            toreturn=toreturn+'%'+architect.getPersonTitleValue()+'|'+architect.getName1()+'|'+architect.getName2()+'|'+architect.getNumber()+', '+architect.getStreet()+'|'+architect.getZipcode()+' '+architect.getCity()
        toreturn=toreturn+'</CSV>'
        return toreturn

    security.declarePublic('getMultipleNotariesCSV')
    def getMultipleNotariesCSV(self):
        """
          Returns a formatted version of the notaries to be used in POD templates
        """
        notaries = self.getNotaryContact()
        toreturn='<CSV>Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2'
        for notary in notaries:
            toreturn=toreturn+'%'+notary.getPersonTitleValue()+'|'+notary.getName1()+'|'+notary.getName2()+'|'+notary.getNumber()+', '+notary.getStreet()+'|'+notary.getZipcode()+' '+notary.getCity()
        toreturn=toreturn+'</CSV>'
        return toreturn

    security.declarePublic('getMultipleRealSubmittersCSV')
    def getMultipleRealSubmittersCSV(self):
        """
          Find who really submitted the request...
        """
        who = self.getWhoSubmitted()
        if who in ['notary', 'both',]:
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
        toreturn=''
        isFirst = True
        for portionOutObj in self.getParcels():
            #add a separator between every parcel
            #either a '\n'
            if not isFirst and linebyline:
                toreturn=toreturn+'\n'
            #or an "and "
            elif not isFirst:
                toreturn=toreturn + ' ' + _('and', 'urban', context=self.REQUEST) + ' '
            toreturn=toreturn+'section '+portionOutObj.getSection()
            toreturn=toreturn+' '+portionOutObj.getRadical()
            if portionOutObj.getBis() !='':
                toreturn=toreturn+'/'+portionOutObj.getBis()
            toreturn=toreturn+portionOutObj.getExposant()
            toreturn=toreturn+portionOutObj.getPuissance()
            isFirst=False
        return toreturn
