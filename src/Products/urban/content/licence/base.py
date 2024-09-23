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
__docformat__ = "plaintext"

from collective.delaycalculator import workday
from datetime import date
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import DisplayList

from Products.urban.interfaces import IWorklocationSignaletic
from Products.urban.interfaces import IUrbanEvent
from Products.urban.utils import getCurrentFolderManager as currentFolderManager
from Products.urban.utils import removeItems
from Products.urban.utils import convert_to_utf8
from plone import api
from zope.component import queryAdapter
from zope.component import getUtility
from zope.i18n import translate
from zope.schema.interfaces import IVocabularyFactory
from zope.interface import implements
from Products.urban import interfaces
from urban.vocabulary.vocabularies.base import BaseVocabulary


class UrbanBase(object):
    """
    This class manage every methods shared cross different licences
    """

    security = ClassSecurityInfo()

    implements(interfaces.IUrbanBase)

    security.declarePublic("getLicenceConfig")

    def getLicenceConfig(self):
        """ """
        portal_urban = api.portal.get_tool("portal_urban")
        config = getattr(portal_urban, self.portal_type.lower(), None)
        return config

    security.declarePublic("getApplicants")

    def getApplicants(self):
        """
        Return the list of applicants for the Licence
        """
        applicants = [
            app
            for app in self.objectValues("Applicant")
            if app.portal_type == "Applicant"
            and api.content.get_state(app) == "enabled"
        ]
        corporations = self.getCorporations()
        couples = self.getCouples()
        applicants.extend(couples)
        applicants.extend(corporations)
        return applicants

    security.declarePublic("get_applicants_history")

    def get_applicants_history(self):
        """
        Return the history of applicants for the Licence
        """
        applicants = [
            app
            for app in self.objectValues("Applicant")
            if app.portal_type == "Applicant"
            and api.content.get_state(app) == "disabled"
        ]
        corporations = self.get_corporations_history()
        couples = self.get_couples_history()
        applicants.extend(couples)
        applicants.extend(corporations)
        return applicants

    security.declarePublic("getCorporations")

    def getCorporations(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "Corporation"
            and api.content.get_state(corp) == "enabled"
        ]
        return corporations

    security.declarePublic("get_corporations_history")

    def get_corporations_history(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "Corporation"
            and api.content.get_state(corp) == "disabled"
        ]
        return corporations

    security.declarePublic("getCouples")

    def getCouples(self):
        couples = [
            couple
            for couple in self.objectValues("Couple")
            if couple.portal_type == "Couple"
            and api.content.get_state(couple) == "enabled"
        ]
        return couples

    security.declarePublic("get_couples_history")

    def get_couples_history(self):
        couples = [
            couple
            for couple in self.objectValues("Couple")
            if couple.portal_type == "Couple"
            and api.content.get_state(couple) == "disabled"
        ]
        return couples

    security.declarePublic("getProprietaries")

    def getProprietaries(self):
        """
        Return the list of proprietaries for the Licence
        """
        proprietaries = [
            pro
            for pro in self.objectValues("Applicant")
            if pro.portal_type == "Proprietary"
            and api.content.get_state(pro) == "enabled"
        ]
        corporations = self.getCorporationsProprietary()
        couples = self.getProprietaryCouples()
        proprietaries.extend(couples)
        proprietaries.extend(corporations)
        return proprietaries

    security.declarePublic("get_proprietaries_history")

    def get_proprietaries_history(self):
        """
        Return the history of proprietaries for the Licence
        """
        proprietaries = [
            app
            for app in self.objectValues("Applicant")
            if app.portal_type == "Proprietary"
            and api.content.get_state(app) == "disabled"
        ]
        corporations = self.get_corporation_proprietaries_history()
        couples = self.get_proprietary_couples_history()
        proprietaries.extend(couples)
        proprietaries.extend(corporations)
        return proprietaries

    security.declarePublic("getCorporationsProprietary")

    def getCorporationsProprietary(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "CorporationProprietary"
            and api.content.get_state(corp) == "enabled"
        ]
        return corporations

    security.declarePublic("get_corporation_proprietaries_history")

    def get_corporation_proprietaries_history(self):
        corporations = [
            corp
            for corp in self.objectValues("Corporation")
            if corp.portal_type == "CorporationProprietary"
            and api.content.get_state(corp) == "disabled"
        ]
        return corporations

    security.declarePublic("getProprietaryCouples")

    def getProprietaryCouples(self):
        couples = [
            couple
            for couple in self.objectValues("Couple")
            if couple.portal_type == "ProprietaryCouple"
            and api.content.get_state(couple) == "enabled"
        ]
        return couples

    security.declarePublic("get_proprietary_couples_history")

    def get_proprietary_couples_history(self):
        couples = [
            couple
            for couple in self.objectValues("Couple")
            if couple.portal_type == "ProprietaryCouple"
            and api.content.get_state(couple) == "disabled"
        ]
        return couples

    security.declarePublic("getApplicantsSignaletic")

    def getApplicantsSignaletic(
        self, withaddress=False, linebyline=False, remove_comma=False, withtitle=True
    ):
        """
        Returns a string representing the signaletic of every applicants
        """
        applicants = self.getApplicants() or self.getProprietaries()
        signaletic = ""
        for applicant in applicants:
            # if the signaletic is not empty, we are adding several applicants
            if signaletic:
                signaletic += " %s " % translate(
                    "and", "urban", context=self.REQUEST
                ).encode("utf8")
            signaletic += applicant.getSignaletic(
                withaddress=withaddress,
                linebyline=linebyline,
                remove_comma=False,
                withtitle=withtitle,
            )
        return signaletic

    security.declarePublic("getFolderManagersSignaletic")

    def getFolderManagersSignaletic(
        self, withGrade=False, withParenthesis=True, withEmail=False, withTel=False
    ):
        """
        Returns a string representing the signaletic of every folder managers
        """
        fms = self.getFoldermanagers()
        signaletic = ""
        for fm in fms:
            # if the signaletic is not empty, we are adding several folder managers
            if signaletic:
                signaletic += "<p><strong>%s</strong>" % fm.getSignaletic(short=True)
            else:
                signaletic = "<p><strong>%s</strong>" % fm.getSignaletic(short=True)
            if withGrade:
                if withParenthesis:
                    signaletic += " (%s)" % self.displayValue(
                        fm.Vocabulary("grade")[0], fm.getGrade()
                    )
                else:
                    signaletic += " %s" % self.displayValue(
                        fm.Vocabulary("grade")[0], fm.getGrade()
                    )
            if withEmail:
                signaletic += "<br />%s" % fm.getEmail()
            if withTel:
                signaletic += "<br />%s" % fm.getPhone()
            signaletic += "</p>"
        return signaletic

    security.declarePublic("getReferenceForTemplate")

    def getReferenceForTemplate(self):
        """
        Calculate the reference to be displayed in the templates
        """
        return "Calculated/Reference/%s" % str(self.getReference())

    security.declarePublic("getNotariesSignaletic")

    def getNotariesSignaletic(
        self,
        withaddress=False,
        linebyline=False,
        remove_comma=False,
        inverted_address=False,
    ):
        """
        Returns a string reprensenting the signaletic of every notaries
        """
        notaries = self.getNotaryContact()
        signaletic = ""
        for notary in notaries:
            # if the signaletic is not empty, we are adding several notaries
            if signaletic:
                signaletic += " %s " % translate(
                    "and", "urban", context=self.REQUEST
                ).encode("utf8")
            signaletic += notary.getSignaletic(
                withaddress=withaddress,
                linebyline=linebyline,
                remove_comma=remove_comma,
                inverted_address=inverted_address,
            )
        return signaletic

    security.declarePublic("getContactsSignaletic")

    def getContactsSignaletic(
        self, contacts, withaddress=False, remove_comma=False, inverted_address=False
    ):
        """
        Returns a string reprensenting the signaletic of every contact
        """
        signaletic = ""
        for contact in contacts:
            # if the signaletic is not empty, we are adding several contacts
            if signaletic:
                signaletic += " %s " % translate(
                    "and", "urban", context=self.REQUEST
                ).encode("utf8")
            signaletic += contact.getSignaletic(
                withaddress=withaddress,
                remove_comma=remove_comma,
                inverted_address=inverted_address,
            )
        return signaletic

    security.declarePublic("getCurrentFolderManager")

    def getCurrentFolderManager(self):
        return currentFolderManager()

    security.declarePublic("getRepresentantsSignaletic")

    def getRepresentantsSignaletic(
        self, withaddress=False, remove_comma=False, inverted_address=False
    ):
        """
        Returns a string reprensenting the signaletic of every representant
        """
        return self.getContactsSignaletic(
            self.getRepresentativeContacts(),
            withaddress=withaddress,
            remove_comma=remove_comma,
            inverted_address=inverted_address,
        )

    security.declarePublic("getArchitectsSignaletic")

    def getArchitectsSignaletic(
        self, withaddress=False, remove_comma=False, inverted_address=False
    ):
        """
        Returns a string reprensenting the signaletic of every architects
        """
        return self.getContactsSignaletic(
            self.getArchitects(),
            withaddress=withaddress,
            remove_comma=remove_comma,
            inverted_address=inverted_address,
        )

    security.declarePublic("getGeometriciansSignaletic")

    def getGeometriciansSignaletic(
        self, withaddress=False, remove_comma=False, inverted_address=False
    ):
        """
        Returns a string reprensenting the signaletic of every geometricians
        """
        return self.getContactsSignaletic(
            self.getGeometricians(),
            withaddress=withaddress,
            remove_comma=remove_comma,
            inverted_address=inverted_address,
        )

    security.declarePublic("submittedBy")

    def submittedBy(self):
        """
        Returns a formatted string with data about people that submitted
        3 cases :
        - the applicant submitted the request for himself
        - a notary submitted the request for the applicant
        - a notary submitted the request for himself
        """
        if self.getPortalTypeName() in (
            "UrbanCertificateOne",
            "UrbanCertificateTwo",
            "NotaryLetter",
        ):
            who = self.getWhoSubmitted()
            if who == "both":
                # a notary submitted the request for an applicant
                return translate(
                    "request_submitted_by_both",
                    "urban",
                    context=self.REQUEST,
                    mapping={
                        "notary": unicode(self.getNotariesSignaletic(), "utf8"),
                        "applicant": unicode(self.getApplicantsSignaletic(), "utf8"),
                    },
                ).encode("utf8")
            elif who == "applicant":
                # an applicant submitted the request for himself
                return translate(
                    "request_submitted_by_applicant",
                    "urban",
                    context=self.REQUEST,
                    mapping={
                        "applicant": unicode(self.getApplicantsSignaletic(), "utf-8")
                    },
                ).encode("utf8")
            elif who == "notary":
                # a notary submitted the request without an applicant (??? possible ???)
                return translate(
                    "request_submitted_by_notary",
                    "urban",
                    context=self.REQUEST,
                    mapping={"notary": unicode(self.getNotariesSignaletic(), "utf-8")},
                ).encode("utf8")
            return ""
        elif self.getType() == "ParceOutLicence":
            return "test"

    security.declarePublic("getWorkLocationCities")

    def getWorkLocationCities(self):
        """
        Returns a string reprensenting the different worklocation's cities
        """
        catalog = api.portal.get_tool("uid_catalog")
        cities = ""
        for wl in self.getWorkLocations():
            # wl is a dict with street as the street obj uid and number as the number in the street
            street = catalog(UID=wl["street"])[0].getObject()
            city = street.getParentNode()
            cities += "%s " % (city.Title())
        return cities

    security.declarePublic("getWorkLocationSignaletic")

    def getWorkLocationSignaletic(self, auto_back_to_the_line=False):
        """
        Returns a string reprensenting the different worklocations
        """

        adress_signaletic_adapter = queryAdapter(self, IWorklocationSignaletic)
        if adress_signaletic_adapter:
            return adress_signaletic_adapter.get_signaletic()

        return self.getDefaultWorkLocationSignaletic(auto_back_to_the_line)

    security.declarePublic("getDefaultWorkLocationSignaletic")

    def getDefaultWorkLocationSignaletic(self, auto_back_to_the_line=False):
        """
        Returns a string reprensenting the different worklocations
        """
        catalog = api.portal.get_tool("uid_catalog")
        signaletic = ""

        for wl in self.getWorkLocations():
            # wl is a dict with street as the street obj uid and number as the number in the street
            street_brains = catalog(UID=wl["street"])
            if not street_brains:
                continue
            street = street_brains[0].getObject()
            city = street.getParentNode()
            if street.getPortalTypeName() == "Locality":
                streetName = street.getLocalityName()
            else:
                streetName = street.getStreetName()
            number = wl["number"]
            if signaletic:
                signaletic += " %s " % translate(
                    "and", "urban", context=self.REQUEST
                ).encode("utf8")
            # special case for locality where we clearly specify that this is a locality
            if street.portal_type == "Locality":
                signaletic += (
                    "%s "
                    % translate(
                        "locality_for_worklocation",
                        "urban",
                        context=self.REQUEST,
                        default="locality",
                    ).encode("utf8")
                )
            if number:
                signaletic += "%s %s à %s %s" % (
                    streetName,
                    convert_to_utf8(number),
                    city.getZipCode(),
                    city.Title(),
                )
            else:
                signaletic += "%s - %s %s" % (
                    streetName,
                    city.getZipCode(),
                    city.Title(),
                )
            if auto_back_to_the_line:
                signaletic += "\n"

        return signaletic

    security.declarePublic("getStreetAndNumber")

    def getStreetAndNumber(self, separator=None):
        """
        Returns a string reprensenting the different streets and numbers
        """

        adress_signaletic_adapter = queryAdapter(self, IWorklocationSignaletic)
        if adress_signaletic_adapter:
            return adress_signaletic_adapter.get_street_and_number()

        if separator is None:
            separator = ""
        return self.getDefaultStreetAndNumber(separator=separator)

    security.declarePublic("getDefaultStreetAndNumber")

    def getDefaultStreetAndNumber(self, separator=""):
        """
        Returns a string reprensenting the different streets and numbers
        """
        catalog = api.portal.get_tool("uid_catalog")
        signaletic = ""

        for wl in self.getWorkLocations():
            street_brains = catalog(UID=wl["street"])
            if not street_brains:
                continue
            street = street_brains[0].getObject()
            streetName = street.getStreetName()
            number = wl["number"]
            if number:
                signaletic = "{} {}{} {}".format(
                    signaletic, streetName, separator, convert_to_utf8(number)
                )
            else:
                signaletic = "{} {}".format(signaletic, streetName)

        return signaletic

    security.declarePublic("getStreets")
    
    def getStreets(self):
        """
        Returns a string representing the different streets
        """
        catalog = api.portal.get_tool("uid_catalog")
        signaletic = ""

        for wl in self.getWorkLocations():
            street_brains = catalog(UID=wl["street"])
            if not street_brains:
                continue
            street = street_brains[0].getObject()
            street_name = street.getStreetName()
            signaletic = "{} {}".format(signaletic, street_name)

        return signaletic

    security.declarePublic("hasSingleApplicant")

    def hasSingleApplicant(self):
        """
        return true or false depending if the licence has several applicants or if the multiplicity
        of the applicant is plural
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if len(applicants) <= 1:
            applicant = applicants[0]
            field = applicant.getField("personTitle")
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == "single":
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
            field = applicant.getField("personTitle")
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == "single":
                if title.getGender() == "male":
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
            field = applicant.getField("personTitle")
            titles = field.vocabulary.getAllVocTerms(applicant)
            title = titles[applicant.getPersonTitle()]
            if title.getMultiplicity() == "single":
                if title.getGender() == "female":
                    answer = True
        return answer

    def hasMultipleFemaleApplicants(self):
        """
        return true if the licence has a multiple female applicants
        """
        answer = False
        applicants = self.getApplicants()  # applicant can also be proprietaries..
        if not self.hasSingleApplicant():
            answer = True
            for applicant in applicants:
                field = applicant.getField("personTitle")
                titles = field.vocabulary.getAllVocTerms(applicant)
                title = titles[applicant.getPersonTitle()]
                if title.getGender() != "female":
                    answer = False
        return answer

    security.declarePublic("hasMultipleApplicants")

    def hasMultipleApplicants(self):
        """
        return true or false depending if the licence has several applicants or if the multiplicity
        of the applicant is plural
        """
        return not self.hasSingleApplicant()

    security.declarePublic("getMultipleContactsCSV")

    def getMultipleContactsCSV(self, contacts=[], only_foreign_country=True):
        """
        Returns a formatted version of the applicants to be used in POD templates
        """
        toreturn = "[CSV]Titre|TitreR|Nom|Prenom|AdresseLigne1|AdresseLigne2|Pays"

        portal_urban = api.portal.get_tool("portal_urban")
        country_mapping = {"": ""}
        country_folder = portal_urban.country
        for country_obj in country_folder.objectValues():
            country_mapping[country_obj.id] = country_obj.Title()

        for contact in contacts:
            if (
                only_foreign_country
                and contact.getCountry()
                and contact.getCountry().lower() == "belgium"
            ):
                country = ""
            else:
                country = country_mapping[contact["country"]]
            toreturn = (
                toreturn
                + "%"
                + contact.getPersonTitleValue()
                + "|"
                + contact.getPersonTitleValue(reverse=True)
                + "|"
                + contact.getName1().decode("utf8")
                + "|"
                + contact.getName2().decode("utf8")
                + "|"
                + contact.getStreet().decode("utf8")
                + ", "
                + contact.getNumber()
                + "|"
                + contact.getZipcode()
                + " "
                + contact.getCity().decode("utf8")
                + "|"
                + country
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getMultipleApplicantsCSV")

    def getMultipleApplicantsCSV(self, only_foreign_country=True):
        """
        Returns a formatted version of the applicants to be used in POD templates
        """
        applicants = self.getApplicants()
        return self.getMultipleContactsCSV(applicants, only_foreign_country)

    getMultipleApplicants = getMultipleApplicantsCSV

    security.declarePublic("getMultipleProprietariesCSV")

    def getMultipleProprietariesCSV(self, only_foreign_country=True):
        """
        Returns a formatted version of the proprietaries to be used in POD templates
        """
        proprietaries = self.getProprietaries()
        return self.getMultipleContactsCSV(proprietaries, only_foreign_country)

    security.declarePublic("getMultipleOrganizationCSV")

    def getMultipleOrganizationsCSV(self):
        """
        Returns a formatted version of the organization to be used in POD templates
        """
        organizations = [
            self.getField("solicitOpinionsTo")
            .vocabulary.getAllVocTerms(self)
            .get(key, None)
            for key in self.getSolicitOpinionsTo()
        ]
        toreturn = "[CSV]recipientName|function_department|organization|dispatchInformation|typeAndStreetName_number_box|postcode_locality|country"
        for organization in organizations:
            toreturn = (
                toreturn
                + "%"
                + organization.getRecipientName()
                + "|"
                + organization.getFunction_department()
                + "|"
                + organization.getOrganization()
                + "|"
                + organization.getDispatchInformation()
                + "|"
                + organization.getTypeAndStreetName_number_box()
                + "|"
                + organization.getPostcode_locality()
                + "|"
                + organization.getCountry()
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    getMultipleOrganizations = getMultipleOrganizationsCSV

    security.declarePublic("getMultipleClaimantsCSV")

    def getMultipleClaimantsCSV(self, number_street_inverted=False):
        """
        Returns a formatted version of claimants to be used in POD templates
        """
        tool = api.portal.get_tool("portal_urban")
        claimants = self.getLastEvent(interfaces.IUrbanEventInquiry).getClaimants()
        toreturn = (
            "[CSV]Titre|TitreR|Nom|Prenom|AdresseLigne1|AdresseLigne2|DateReclamation"
        )
        for claimant in claimants:
            street_num = (
                number_street_inverted
                and (
                    claimant.getNumber().decode("utf8")
                    + ","
                    + claimant.getStreet.decode("utf8")
                )
                or (
                    claimant.getStreet().decode("utf8")
                    + ","
                    + claimant.getNumber.decode("utf8")
                )
            )
            toreturn = (
                toreturn
                + "%"
                + claimant.getPersonTitleValue().decode("utf8")
                + "|"
                + claimant.getPersonTitleValue(reverse=True).decode("utf8")
                + "|"
                + claimant.getName1().decode("utf8")
                + "|"
                + claimant.getName2().decode("utf8")
                + "|"
                + street_num
                + "|"
                + claimant.getZipcode().decode("utf8")
                + " "
                + claimant.getCity().decode("utf8")
                + "|"
                + tool.formatDate(claimant.getClaimDate()).decode("utf8")
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getMultipleArchitectsCSV")

    def getMultipleArchitectsCSV(self, number_street_inverted=False):
        """
        Returns a formatted version of the architects to be used in POD templates
        """
        architects = self.getArchitects()
        toreturn = "[CSV]Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2"
        for architect in architects:
            street_num = (
                number_street_inverted
                and (
                    architect.getNumber().decode("utf8")
                    + ","
                    + architect.getStreet.decode("utf8")
                )
                or (
                    architect.getStreet().decode("utf8")
                    + ","
                    + architect.getNumber.decode("utf8")
                )
            )
            toreturn = (
                toreturn
                + "%"
                + architect.getPersonTitleValue()
                + "|"
                + architect.getName1()
                + "|"
                + architect.getName2()
                + "|"
                + street_num
                + "|"
                + architect.getZipcode()
                + " "
                + architect.getCity()
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getMultipleArchitectsCSV")

    def getMultipleGeometriciansCSV(self, number_street_inverted=False):
        """
        Returns a formatted version of the geometricians to be used in POD templates
        """
        geometricians = self.getGeometricians()
        toreturn = "[CSV]Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2"
        for geometrician in geometricians:
            street_num = (
                number_street_inverted
                and (
                    geometrician.getNumber().decode("utf8")
                    + ","
                    + geometrician.getStreet.decode("utf8")
                )
                or (
                    geometrician.getStreet().decode("utf8")
                    + ","
                    + geometrician.getNumber.decode("utf8")
                )
            )
            toreturn = (
                toreturn
                + "%"
                + geometrician.getPersonTitleValue()
                + "|"
                + geometrician.getName1()
                + "|"
                + geometrician.getName2()
                + "|"
                + street_num
                + "|"
                + geometrician.getZipcode()
                + " "
                + geometrician.getCity()
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getMultipleNotariesCSV")

    def getMultipleNotariesCSV(self, number_street_inverted=False):
        """
        Returns a formatted version of the notaries to be used in POD templates
        """
        notaries = self.getNotaryContact()
        toreturn = "[CSV]Titre|Nom|Prenom|AdresseLigne1|AdresseLigne2"
        for notary in notaries:
            street_num = (
                number_street_inverted
                and (
                    notary.getNumber().decode("utf8")
                    + ","
                    + notary.getStreet.decode("utf8")
                )
                or (
                    notary.getStreet().decode("utf8")
                    + ","
                    + notary.getNumber.decode("utf8")
                )
            )
            toreturn = (
                toreturn
                + "%"
                + notary.getPersonTitleValue()
                + "|"
                + notary.getName1()
                + "|"
                + notary.getName2()
                + "|"
                + street_num
                + "|"
                + notary.getZipcode()
                + " "
                + notary.getCity()
            )
        toreturn = toreturn + "[/CSV]"
        return toreturn

    security.declarePublic("getMultipleRealSubmittersCSV")

    def getMultipleRealSubmittersCSV(self):
        """
        Find who really submitted the request...
        """
        who = self.getWhoSubmitted()
        if who in ["notary", "both"]:
            return self.getMultipleNotariesCSV()
        elif who == "applicant":
            return self.getMultipleApplicantsCSV()
        else:
            return ""

    security.declarePublic("getTerm")

    def getTerm(self, termFolder, termId):
        """
        Returns a term object for a given term folder
        """
        tool = api.portal.get_tool("portal_urban")
        urbanConfig = tool.getLicenceConfig(self)
        termFolderObj = getattr(urbanConfig, termFolder)
        return getattr(termFolderObj, termId)

    security.declarePublic("getUrbanEvents")

    def getUrbanEvents(self):
        """
        Return every contained UrbanEvents (of any type)...
        """
        return [
            obj for obj in self.objectValues() if IUrbanEvent.providedBy(obj)
        ]  # UrbanEvent is the meta_type

    security.declarePublic("getUrbanEventOpinionRequests")

    def getUrbanEventOpinionRequests(self):
        """
        Return all UrbanEventOpinionRequests
        """
        return self.listFolderContents({"portal_type": ("UrbanEventOpinionRequest")})

    security.declarePublic("getLastUrbanEventOpinionRequests")

    def getLastUrbanEventOpinionRequests(self):
        """
        Return all UrbanEventOpinionRequests events selected in the last inquiry.
        """
        all_events = self.getUrbanEventOpinionRequests()
        events = [
            evt
            for evt in all_events
            if evt.getLinkedInquiry() == self._get_inquiry_objs(all_=True)[-1]
        ]
        return events

    security.declarePublic("getUrbanEvent")

    def getUrbanEvent(self, title=""):
        """
        Return a specific title's UrbanEvent
        """
        i = 0
        found = False
        urbanEvent = None
        urbanEvents = self.getUrbanEvents()
        while i < len(urbanEvents) and not found:
            if urbanEvents[i].Title() == title:
                found = True
                urbanEvent = urbanEvents[i]
            i = i + 1
        return urbanEvent

    security.declarePublic("containsUrbanEvent")

    def containsUrbanEvent(self, title=""):
        """
        find a specific title's UrbanEvent
        """
        i = 0
        found = False
        urbanEvents = self.getUrbanEvents()
        while i < len(urbanEvents) and not found:
            if urbanEvents[i].Title() == title:
                found = True
            i = i + 1
        return found

    security.declarePublic("mayShowEditAction")

    def mayShowEditAction(self):
        """
        Edit action condition expression
        We can not show the action if the object is locked or if we are using the tabbing
        """
        selfPhysPath = "/".join(self.getPhysicalPath())
        # do the test in 2 if to avoid getting the tool if not necessary
        if self.unrestrictedTraverse(
            selfPhysPath + "/@@plone_lock_info/is_locked_for_current_user"
        )():
            return False
        tool = api.portal.get_tool("portal_urban")
        if tool.getLicenceConfig(self).getUseTabbingForDisplay():
            return False
        return True

    security.declarePublic("getParcellingsForTemplate")

    def getParcellingsForTemplate(self, withDetails=False):
        """
        Format informations about parcellings to be displayed in templates
        """
        parcellings = self.getParcellings()
        if not parcellings:
            return "-"
        else:
            res = parcellings.Title()
            if withDetails:
                res = "%s - %s" % (res, self.getRawSubdivisionDetails())
            return res

    security.declarePublic("getValueForTemplate")

    def getValueForTemplate(self, field_name, obj=None, subfield=None):
        """
        Return the display value of the given field
        """
        return ", ".join(
            [
                result
                for result in self._getValuesForTemplate(
                    field_name=field_name, obj=obj, subfield_name=subfield
                )
            ]
        )

    security.declarePublic("getValuesForTemplate")

    def getValuesForTemplate(self, field_name, obj=None, subfield=None):
        """
        Return a list of the display values of the given field
        """
        return self._getValuesForTemplate(
            field_name=field_name, obj=obj, subfield_name=subfield
        )

    # def displayValuesFromVocForTemplate

    def _getValuesForTemplate(self, field_name="", obj=None, subfield_name=None):
        """
        Return the display value of the given field
        """
        obj = obj and obj or self
        if subfield_name:
            field = obj.getField(field_name)
            if field.vocabulary:
                keys = (
                    type(field.getRaw(obj)) in (list, tuple)
                    and field.getRaw(obj)
                    or [field.getRaw(obj)]
                )
                objs = [
                    field.vocabulary.getAllVocTerms(obj).get(key, None) for key in keys
                ]
            elif field.vocabulary_factory:
                voc_utility = getUtility(IVocabularyFactory, field.vocabulary_factory)
                objs = voc_utility._get_config_vocabulary_values(self.context)
            else:
                catalog = api.portal.get_tool("portal_catalog")
                objs = []
                if field.getRaw(obj):
                    objs = [obj_.getObject() for obj_ in catalog(UID=field.getRaw(obj))]
            field_name = subfield_name
            return [self.getValueForTemplate(field_name, obj_) for obj_ in objs]
        return [res for res in self._getValueForTemplate(field_name, obj)]

    def _getValueForTemplate(self, field_name="", obj=None):
        """
        Return the display value of the given field
        """
        obj = obj or self
        displaylist = self._getVocabularyDisplayList(field_name, obj)
        field_value = self._getFieldValue(field_name, obj)
        if not field_value or not displaylist:
            return ""

        if type(field_value) not in (list, tuple):
            val = (
                displaylist
                and obj.displayValue(displaylist, str(field_value))
                or field_value
            )
            if type(val) not in [str, unicode]:
                val = str(val)
            if type(val) is str:
                val = val.decode("utf-8")
            val = translate(val, "urban", context=self.REQUEST)
            val = translate(val, "plone", context=self.REQUEST)
            return [val]
        return [
            value and obj.displayValue(displaylist, value) or ""
            for value in field_value
        ]

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
        field = obj.getField(fieldname)
        vocabulary = getattr(field, "vocabulary", None)
        if not vocabulary and getattr(field, "vocabulary_factory", None):
            vocabulary = getUtility(IVocabularyFactory, field.vocabulary_factory)
        if not vocabulary:
            return None
        displaylist = None
        if hasattr(vocabulary, "getDisplayListForTemplate"):
            displaylist = vocabulary.getDisplayListForTemplate(obj)
        elif type(vocabulary) is str:
            displaylist = getattr(obj, vocabulary)()
        elif type(vocabulary) in (list, tuple):
            displaylist = DisplayList(vocabulary)
        elif isinstance(vocabulary, BaseVocabulary):
            displaylist = DisplayList(
                [(k, v.title) for k, v in vocabulary(obj).by_value.iteritems()]
            )
        return displaylist

    security.declarePublic("listVocabularyForTemplate")

    def listVocabularyForTemplate(self, fieldname, obj=None):
        obj = obj or self
        field = obj.getField(fieldname)
        vocabulary = field.vocabulary
        terms = vocabulary.getAllVocTerms(obj).values()
        return terms

    security.declarePublic("listVocabularyFromConfig")

    def listVocabularyFromConfig(self, voc_name, inUrbanConfig=True):
        """
        List a given vocabulary from the config
        """
        urban_tool = api.portal.get_tool("portal_urban")
        vocabulary = urban_tool.listVocabulary(
            voc_name, context=self, inUrbanConfig=inUrbanConfig, with_numbering=False
        )
        return vocabulary

    security.declarePublic("workday")

    def workday(
        self, start_date, days=0, holidays=[], weekends=[], unavailable_weekdays=[]
    ):
        return workday(
            date(start_date.year(), start_date.month(), start_date.day()),
            days,
            holidays,
            weekends,
            unavailable_weekdays,
        )

    security.declarePublic("listSolicitOpinionsTo")

    def listSolicitOpinionsTo(self, unless=[]):
        return removeItems(list(self.getValuesForTemplate("solicitOpinionsTo")), unless)

    security.declarePublic("listSolicitOpinionsToOptional")

    def listSolicitOpinionsToOptional(self, unless=[]):
        return removeItems(
            list(self.getValuesForTemplate("solicitOpinionsToOptional")), unless
        )

    security.declarePublic("getFirstGradeIdSfolderManager")

    def getFirstGradeIdSfolderManager(self, gradeId=""):
        folderManager = None
        found = False
        i = 0
        while not found and i < len(self.getFoldermanagers()):
            if self.getFoldermanagers()[i].getGrade() == gradeId:
                found = True
                folderManager = self.getFoldermanagers()[i]
            i = i + 1
        return folderManager

    def get_state(self):
        return api.content.get_state(self)
