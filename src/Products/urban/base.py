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
from Products.Archetypes.public import DisplayList

from plone import api
from zope.i18n import translate
from zope.interface import implements
import interfaces


class UrbanBase(object):
    """
      This class manage every methods shared cross different licences
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanBase)

    security.declarePublic('getLicenceConfig')
    def getLicenceConfig(self):
        """
        """
        portal_urban = api.portal.get_tool('portal_urban')
        config = getattr(portal_urban, self.portal_type.lower(), None)
        return config

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
           Return the list of applicants for the Licence
        """
        applicants = [app for app in self.objectValues('Applicant') if app.portal_type == 'Applicant']
        return applicants

    security.declarePublic('getProprietaries')
    def getProprietaries(self):
        """
           Return the list of proprietaries for the Licence
        """
        proprietaries = [pro for pro in self.objectValues('Applicant') if pro.portal_type == 'Proprietary']
        return proprietaries

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
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
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
                signaletic += '<p><strong>%s</strong>' % fm.getSignaletic(short=True)
            else:
                signaletic = '<p><strong>%s</strong>' % fm.getSignaletic(short=True)
            if withGrade:
                signaletic += ' (%s)' % self.displayValue(fm.Vocabulary('grade')[0], fm.getGrade()).encode('utf8')
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
    def getNotariesSignaletic(self, withaddress=False, linebyline=False):
        """
          Returns a string reprensenting the signaletic of every notaries
        """
        notaries = self.getNotaryContact()
        signaletic = ''
        for notary in notaries:
            #if the signaletic is not empty, we are adding several notaries
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += notary.getSignaletic(withaddress=withaddress, linebyline=linebyline)
        return signaletic

    security.declarePublic('getContactsSignaletic')
    def getContactsSignaletic(self, contacts, withaddress=False):
        """
          Returns a string reprensenting the signaletic of every contact
        """
        signaletic = ''
        for contact in contacts:
            #if the signaletic is not empty, we are adding several contacts
            if signaletic:
                signaletic += ' %s ' % translate('and', 'urban', context=self.REQUEST).encode('utf8')
            signaletic += contact.getSignaletic(withaddress=withaddress)
        return signaletic

    security.declarePublic('getArchitectsSignaletic')
    def getArchitectsSignaletic(self, withaddress=False):
        """
          Returns a string reprensenting the signaletic of every architects
        """
        return self.getContactsSignaletic(self.getArchitects(), withaddress=withaddress)

    security.declarePublic('getGeometriciansSignaletic')
    def getGeometriciansSignaletic(self, withaddress=False):
        """
          Returns a string reprensenting the signaletic of every geometricians
        """
        return self.getContactsSignaletic(self.getGeometricians(), withaddress=withaddress)

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
                return translate('request_submitted_by_both', 'urban', context=self.REQUEST, mapping={'notary': unicode(self.getNotariesSignaletic(), 'utf8'), 'applicant': unicode(self.getApplicantsSignaletic(), 'utf8')}).encode('utf8')
            elif who == 'applicant':
                #an applicant submitted the request for himself
                return translate('request_submitted_by_applicant', 'urban', context=self.REQUEST, mapping={'applicant': unicode(self.getApplicantsSignaletic(), 'utf-8')}).encode('utf8')
            elif who == 'notary':
                #a notary submitted the request without an applicant (??? possible ???)
                return translate('request_submitted_by_notary', 'urban', context=self.REQUEST, mapping={'notary': unicode(self.getNotariesSignaletic(), 'utf-8')}).encode('utf8')
            return ''
        elif self.getType() == 'ParceOutLicence':
            return 'test'

    security.declarePublic('getWorkLocationSignaletic')
    def getWorkLocationSignaletic(self):
        """
          Returns a string reprensenting the different worklocations
        """
        catalog = api.portal.get_tool("uid_catalog")
        signaletic = ''
        for wl in self.getWorkLocations():
            #wl is a dict with street as the street obj uid and number as the number in the street
            street = catalog(UID=wl['street'])[0].getObject()
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
                signaletic += "%s, %s - %s %s" % (number, streetName, city.getZipCode(), city.Title())
            else:
                signaletic += "%s - %s %s" % (streetName, city.getZipCode(), city.Title())
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
            'UrbanCertificateBase': 'CU1',
            'UrbanCertificateTwo': 'CU2',
            'EnvClassOne': 'PE1',
            'EnvClassThree': 'DE',
            'Declaration': 'Decl',
            'Division': 'Div',
            'MiscDemand': 'DD',
        }
        if "notaryletter" in self.id:
            return 'Not'
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
        tool = api.portal.get_tool('portal_urban')
        #get the event called 'depot-de-la-demande' and returns the linked eventDate
        depositEvent = self.getLastDeposit()
        if depositEvent:
            tool = api.portal.get_tool('portal_urban')
            return tool.formatDate(depositEvent.getEventDate())
        return translate('warning_no_deposit_date', 'urban', context=self.REQUEST).encode('utf8')

    security.declarePublic('hasSingleApplicant')
    def hasSingleApplicant(self):
        """
            return true or false depending if the licence has several applicants or if the multiplicity
            of the applicant is plural
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) <= 1:
            applicant = applicants[0]
            field = applicant.getField('personTitle')
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == 'single':
                answer = True
        return answer

    def hasSingleMaleApplicant(self):
        """
            return true if the licence has a single male applicant
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) <= 1:
            applicant = applicants[0]
            field = applicant.getField('personTitle')
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == 'single':
                if title.getGender() == 'male':
                    answer = True
        return answer

    def hasSingleFemaleApplicant(self):
        """
            return true if the licence has a single female applicant
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) <= 1:
            applicant = applicants[0]
            field = applicant.getField('personTitle')
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == 'single':
                if title.getGender() == 'female':
                    answer = True
        return answer

    def hasMultipleFemaleApplicants(self):
        """
            return true if the licence has a multiple female applicants
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) > 1:
            answer = True
            for applicant in applicants:
                field = applicant.getField('personTitle')
                titles = field.vocabulary.getAllVocTerms(applicant)
                title = titles[applicant.getPersonTitle()]
                if title.getGender() == 'male':
                    answer = False
        return answer

    def hasMultipleMaleApplicants(self):
        """
            return true if the licence has a multiple male applicants
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) > 1:
            answer = True
            for applicant in applicants:
                field = applicant.getField('personTitle')
                titles = field.vocabulary.getAllVocTerms(applicant)
                title = titles[applicant.getPersonTitle()]
                if title.getGender() == 'female':
                    answer = False
        return answer

    security.declarePublic('hasMultipleApplicants')
    def hasMultipleApplicants(self):
        """
            return true or false depending if the licence has several applicants or if the multiplicity
            of the applicant is plural
        """
        return not self.hasSingleApplicant()

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
        tool = api.portal.get_tool('portal_urban')
        urbanConfig = tool.getUrbanConfig(self)
        termFolderObj = getattr(urbanConfig, termFolder)
        return getattr(termFolderObj, termId)

    security.declarePublic('getPortionOutsText')
    def getPortionOutsText(self, linebyline=False):
        """
          Return a displayable version of the parcels
        """
        toreturn = ''
        isFirst = True
        first_div = None
        first_section = None
        for portionOutObj in self.getParcels():
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
                toreturn += ' n° '
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

    def _getAllEvents(self,  eventInterface=None):
        catalog = api.portal.get_tool('portal_catalog')
        currentPath = '/'.join(self.getPhysicalPath())
        query = {'path': {'query': currentPath,
                          'depth': 1},
                 'meta_type': ['UrbanEvent', 'UrbanEventInquiry'],
                 'sort_on': 'getObjPositionInParent'}
        if eventInterface is not None:
            interfaceName = interfaceToName(self, eventInterface)
            query['object_provides'] = interfaceName
            query.pop('meta_type')
        return [brain.getObject() for brain in catalog(**query)]

    def _getLastEvent(self, eventInterface=None):
        events = self._getAllEvents(eventInterface)
        if events:
            return events[-1]

    security.declarePublic('getUrbanEvents')
    def getUrbanEvents(self):
        """
          Return every contained UrbanEvents (of any type)...
        """
        return self.listFolderContents({'portal_type': ('UrbanEventInquiry', 'UrbanEvent')})

    security.declarePublic('getInquiries')
    def getInquiries(self):
        """
          Returns the existing inquiries
        """
        #the first inquiry is the one defined on self itself
        #if a investigationStart is defined
        #and the others are extra Inquiry object added
        all_inquiries = []
        other_inquiries = self.objectValues('Inquiry')
        #the inquiry on the licence is activated if we have a
        #investigationStart date or if we have extra Inquiry objects
        if other_inquiries or ('investigationStart' in self.schema and self.getInvestigationStart()):
            all_inquiries.append(self)
        all_inquiries.extend(list(other_inquiries))
        return all_inquiries

    security.declarePublic('getUrbanEventInquiries')
    def getUrbanEventInquiries(self):
        """
          Returns the existing UrbanEventInquiries
        """
        return self.listFolderContents({'portal_type': 'UrbanEventInquiry'})

    security.declarePublic('mayShowEditAction')
    def mayShowEditAction(self):
        """
          Edit action condition expression
          We can not show the action if the object is locked or if we are using the tabbing
        """
        selfPhysPath = '/'.join(self.getPhysicalPath())
        #do the test in 2 if to avoid getting the tool if not necessary
        if self.restrictedTraverse(selfPhysPath + '/@@plone_lock_info/is_locked_for_current_user')():
            return False
        tool = api.portal.get_tool('portal_urban')
        if tool.getUrbanConfig(self).getUseTabbingForDisplay():
            return False
        return True

    security.declarePublic('getParcellingsForTemplate')
    def getParcellingsForTemplate(self, withDetails=False):
        """
          Format informations about parcellings to be displayed in templates
        """
        parcellings = self.getParcellings()
        if not parcellings:
            return '-'
        else:
            res = parcellings.Title()
            if withDetails:
                res = "%s - %s" % (res, self.getRawSubdivisionDetails())
            return res

    security.declarePublic('getValueForTemplate')
    def getValueForTemplate(self, field_name, obj=None, subfield=None):
        """
          Return the display value of the given field
        """
        return ', '.join([result for result in self._getValuesForTemplate(field_name=field_name, obj=obj,
                          subfield_name=subfield)])

    security.declarePublic('getValuesForTemplate')
    def getValuesForTemplate(self, field_name, obj=None, subfield=None):
        """
          Return a list of the display values of the given field
        """
        return self._getValuesForTemplate(field_name=field_name, obj=obj, subfield_name=subfield)

    # def displayValuesFromVocForTemplate

    def _getValuesForTemplate(self, field_name='', obj=None, subfield_name=None):
        """
          Return the display value of the given field
        """
        obj = obj and obj or self
        if subfield_name:
            field = obj.getField(field_name)
            if field.vocabulary:
                keys = type(field.getRaw(obj)) in (list, tuple) and field.getRaw(obj) or [field.getRaw(obj)]
                objs = [field.vocabulary.getAllVocTerms(obj).get(key, None) for key in keys]
            else:
                catalog = api.portal.get_tool('portal_catalog')
                objs = [obj_.getObject() for obj_ in catalog(UID=field.getRaw(obj))]
            field_name = subfield_name
            return [self.getValueForTemplate(field_name, obj_) for obj_ in objs]
        return [res for res in self._getValueForTemplate(field_name, obj)]

    def _getValueForTemplate(self, field_name='', obj=None):
        """
          Return the display value of the given field
        """
        obj = obj or self
        displaylist = self._getVocabularyDisplayList(field_name, obj)
        field_value = self._getFieldValue(field_name, obj)
        if not field_value:
            return ''

        if type(field_value) not in (list, tuple):
            val = displaylist and obj.displayValue(displaylist, field_value) or field_value
            if type(val) not in [str, unicode]:
                val = str(val)
            if type(val) is str:
                val = val.decode('utf-8')
            val = translate(val, 'urban', context=self.REQUEST)
            val = translate(val, 'plone', context=self.REQUEST)
            return [val]
        return [obj.displayValue(displaylist, value) for value in field_value]

    def _getFieldValue(self, fieldname, obj):
        def val(fieldname, obj):
            field_object = obj.getField(fieldname)
            field_accessor = field_object.getAccessor(obj)
            field_value = field_accessor()
            return field_value

        if type(fieldname) is str:
            return val(fieldname, obj)
        else:
            vals = set()
            for field in fieldname:
                value = val(field, obj)
                value = type(value) in [list, tuple] and value or [value]
                vals = vals.union(set(value))
            return list(vals)

    def _getVocabularyDisplayList(self, fieldname, obj):
        fieldname = type(fieldname) is str and fieldname or fieldname[0]
        vocabulary = obj.getField(fieldname).vocabulary
        displaylist = None
        if hasattr(vocabulary, 'getDisplayListForTemplate'):
            displaylist = vocabulary.getDisplayListForTemplate(obj)
        elif type(vocabulary) is str:
            displaylist = getattr(obj, vocabulary)()
        elif type(vocabulary) in (list, tuple):
            displaylist = DisplayList(vocabulary)
        return displaylist

    security.declarePublic('listVocabularyForTemplate')
    def listVocabularyForTemplate(self, fieldname, obj=None):
        obj = obj or self
        field = obj.getField(fieldname)
        vocabulary = field.vocabulary
        terms = vocabulary.getAllVocTerms(obj).values()
        return terms

    security.declarePublic('listVocabularyFromConfig')
    def listVocabularyFromConfig(self, voc_name, inUrbanConfig=True):
        """
          List a given vocabulary from the config
        """
        urban_tool = api.portal.get_tool('portal_urban')
        vocabulary = urban_tool.listVocabulary(voc_name, context=self, inUrbanConfig=inUrbanConfig, with_numbering=False)
        return vocabulary
