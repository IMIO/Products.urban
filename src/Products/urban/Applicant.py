# -*- coding: utf-8 -*-
#
# File: Applicant.py
#
# Copyright (c) 2015 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.urban.widget.select2widget import MultiSelect2Widget
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban.Contact import Contact
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget

from plone import api

import cgi

slave_fields_address = (
    # if isSameAddressAsWorks, hide the address related fields
    {
        'name': 'street',
        'action': 'show',
        'hide_values': (False, ),
    },
    {
        'name': 'number',
        'action': 'show',
        'hide_values': (False, ),
    },
    {
        'name': 'zipcode',
        'action': 'show',
        'hide_values': (False, ),
    },
    {
        'name': 'city',
        'action': 'show',
        'hide_values': (False, ),
    },
    {
        'name': 'country',
        'action': 'show',
        'hide_values': (False, ),
    },
    {
        'name': 'showWorkLocationsAddress',
        'action': 'show',
        'hide_values': (True, ),
    },
)

slave_fields_representedby = (
    # applicant is either represented by a society or by another contact but not both at the same time
    {
        'name': 'representedBy',
        'action': 'show',
        'hide_values': (False, ),
    },
)

##/code-section module-header

schema = Schema((

    BooleanField(
        name='representedBySociety',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_representedby,
            label='Representedbysociety',
            label_msgid='urban_label_representedBySociety',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='isSameAddressAsWorks',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_address,
            label='Issameaddressasworks',
            label_msgid='urban_label_isSameAddressAsWorks',
            i18n_domain='urban',
        ),
    ),
    LinesField(
        name='representedBy',
        widget=MultiSelect2Widget(
            format='checkbox',
            label='Representedby',
            label_msgid='urban_label_representedBy',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        multiValued=1,
        vocabulary='listRepresentedBys',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Applicant_schema = BaseSchema.copy() + \
    getattr(Contact, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class Applicant(BaseContent, Contact, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IApplicant)

    meta_type = 'Applicant'
    _at_rename_after_creation = True

    schema = Applicant_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Generate the title...
        """
        if self.getRepresentedBySociety():
            return "%s %s %s repr. par %s" % (self.getPersonTitle(short=True), self.getName1(), self.getName2(), self.getSociety())
        else:
            return "%s %s %s" % (self.getPersonTitle(short=True), self.getName1(), self.getName2())

    security.declarePublic('getNumber')
    def getNumber(self):
        """
          Overrides the 'number' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if self.getIsSameAddressAsWorks():
            #get the works address
            licence = self.aq_inner.aq_parent
            workLocations = licence.getWorkLocations()
            if not workLocations:
                return ''
            else:
                return workLocations[0]['number']
        else:
            return self.getField('number').get(self)

    security.declarePublic('getZipcode')
    def getZipcode(self):
        """
          Overrides the 'zipcode' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if self.getIsSameAddressAsWorks():
            #get the works address
            street = self._getStreetFromLicence()
            if not street:
                return ''
            return str(street.getCity().getZipCode())
        else:
            return self.getField('zipcode').get(self)

    security.declarePublic('getCity')
    def getCity(self):
        """
          Overrides the 'city' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if self.getIsSameAddressAsWorks():
            #get the works address
            street = self._getStreetFromLicence()
            if not street:
                return ''
            return street.getCity().Title()
        else:
            return self.getField('city').get(self)

    def _getStreetFromLicence(self):
        """
          Get the street of the first workLocations on the licence
          This is usefull if the address of self is the same as the address of the workLocation
        """
        licence = self.aq_inner.aq_parent
        workLocations = licence.getWorkLocations()
        if not workLocations:
            return ''
        else:
            workLocationStreetUID = workLocations[0]['street']
            uid_catalog = api.portal.get_tool('uid_catalog')
            return uid_catalog(UID=workLocationStreetUID)[0].getObject()

    security.declarePublic('getStreet')
    def getStreet(self):
        """
          Overrides the 'street' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if self.getIsSameAddressAsWorks():
            #get the works address
            street = self._getStreetFromLicence()
            if not street:
                return ''
            return street.getStreetName()
        else:
            return self.getField('street').get(self)

    security.declarePublic('showRepresentedByField')
    def showRepresentedByField(self):
        """
        Only show the representedBy field if the current Contact is an Applicant (portal_type)
        and only for some URBAN_TYPES
        """
        parent = self.aq_inner.aq_parent
        #if the Contact is just created, we are in portal_factory.The parent is a TempFolder
        if parent.portal_type == 'TempFolder':
            parent = parent.aq_parent.aq_parent
        if not parent.portal_type in ['BuildLicence', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'Division']:
            return False
        if hasattr(parent, 'getArchitects') and not parent.getArchitects():
            return False
        if hasattr(parent, 'getNotaryContact') and not parent.getNotaryContact():
            return False
        return True

    security.declarePublic('getRepresentedBy')
    def getRepresentedBy(self):
        for contact_uid in self.getField('representedBy').getRaw(self):
            if contact_uid not in self.listRepresentedBys().keys():
                return ()
        return self.getField('representedBy').getRaw(self)

    security.declarePublic('listRepresentedBys')
    def listRepresentedBys(self):
        """
          Returns the list of potential Contacts that could represent the current Contact
          only if it is an "Applicant" as the field will be hidden by the condition on the field otherwise
        """
        #the potential representator are varying upon licence type
        #moreover, as we are using ReferenceField, we can not use getattr...
        potential_contacts = []
        parent = self.aq_inner.aq_parent
        if 'notaryContact' in parent.schema:
            potential_contacts.extend(list(parent.getNotaryContact()))
        if 'geometricians' in parent.schema:
            potential_contacts.extend(list(parent.getGeometricians()))
        if 'architects' in parent.schema:
            potential_contacts.extend(parent.getArchitects())

        vocabulary = [(contact.UID(), contact.Title(),) for contact in potential_contacts]
        return DisplayList(tuple(vocabulary))

    def _getNameSignaletic(self, short, linebyline, reverse=False, invertnames=False):
        title = self.getPersonTitleValue(short, linebyline, reverse)
        name1 = self.getName1().decode('utf-8')
        name2 = self.getName2().decode('utf-8')
        namedefined = name1 or name2
        names = u'%s %s' % (name1, name2)
        if invertnames:
            names = u'%s %s' % (name2, name1)
        names = names.strip()
        namepart = namedefined and names or self.getSociety().decode('utf-8')
        nameSignaletic = u'%s %s' % (title, namepart)
        if len(self.getRepresentedBy()) > 0 or self.getRepresentedBySociety():
            person_title = self.getPersonTitle(theObject=True)
            representatives = self.getRepresentedBySociety() and self.getSociety() or self.displayValue(self.Vocabulary('representedBy')[0], self.getRepresentedBy())
            gender = multiplicity = ''
            represented = u'représenté'
            if person_title:
                gender = person_title.getGender()
                multiplicity = person_title.getMultiplicity()
                if gender == 'male' and multiplicity == 'plural':
                    represented = u'représentés'
                elif gender == 'female' and multiplicity == 'single':
                    represented = u'représentée'
                elif gender == 'female' and multiplicity == 'plural':
                    represented = u'représentées'
            nameSignaletic = u'%s %s %s par %s' % (title, namepart, represented, representatives.decode('utf-8'))
        if linebyline:
            #escape HTML special characters like HTML entities
            return cgi.escape(nameSignaletic)
        else:
            return nameSignaletic



registerType(Applicant, PROJECTNAME)
# end of class Applicant

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('representedBySociety', after='society')
    schema.moveField('isSameAddressAsWorks', after='representedBySociety')

finalizeSchema(Applicant_schema)
##/code-section module-footer

