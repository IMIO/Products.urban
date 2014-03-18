# -*- coding: utf-8 -*-
#
# File: Contact.py
#
# Copyright (c) 2014 by CommunesPlone
# Generator: ArchGenXML Version 2.7
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
import cgi
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.MasterSelectWidget.MasterBooleanWidget import MasterBooleanWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.validation.interfaces.IValidator import IValidator
from Products.validation import validation


class BelgianNationalRegValidator:
    #Validate a belgian national register number
    implements(IValidator)

    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        #the eID card number is 11 number long, we only accept number and '-' and '.'
        #we test that we only have got numbers and '-' and '.'
        len_value = len(value)

        clean_value = ''.join([c for c in value if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.')])
        if len_value != len(clean_value):
            return "This field only accept numbers, indents or points !"

        clean_value = ''.join([c for c in value if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',)])

        #we check that there are 11 numbers left
        if len(clean_value) != 11:
            return "Your National Register number must be 11 digits long !"

        first_part = int(clean_value[0:9])
        last_part = int(clean_value[9:11])

        #the two last digits is the result of 97 les the modulo by 97 of the 10 first digits
        if last_part != (97 - (first_part % 97)):
            return "This National Register number is not valid !"

        return True

validation.register(BelgianNationalRegValidator('isBelgianNR'))

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

    StringField(
        name='personTitle',
        widget=SelectionWidget(
            label='Persontitle',
            label_msgid='urban_label_personTitle',
            i18n_domain='urban',
        ),
        vocabulary=UrbanVocabulary('persons_titles', vocType='PersonTitleTerm', inUrbanConfig=False),
    ),
    StringField(
        name='name1',
        widget=StringField._properties['widget'](
            label='Name1',
            label_msgid='urban_label_name1',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='name2',
        widget=StringField._properties['widget'](
            label='Name2',
            label_msgid='urban_label_name2',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='society',
        widget=StringField._properties['widget'](
            label='Society',
            label_msgid='urban_label_society',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='representedBySociety',
        default=False,
        widget=MasterBooleanWidget(
            slave_fields=slave_fields_representedby,
            condition="python: here.portal_type == 'Applicant' or here.portal_type == 'Proprietary'",
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
            condition="python: here.portal_type == 'Applicant' or here.portal_type == 'Proprietary'",
            label='Issameaddressasworks',
            label_msgid='urban_label_isSameAddressAsWorks',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='street',
        widget=StringField._properties['widget'](
            label='Street',
            label_msgid='urban_label_street',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='number',
        widget=StringField._properties['widget'](
            label='Number',
            label_msgid='urban_label_number',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='zipcode',
        widget=StringField._properties['widget'](
            label='Zipcode',
            label_msgid='urban_label_zipcode',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='city',
        widget=StringField._properties['widget'](
            label='City',
            label_msgid='urban_label_city',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='country',
        default="belgium",
        widget=SelectionWidget(
            label='Country',
            label_msgid='urban_label_country',
            i18n_domain='urban',
        ),
        vocabulary=UrbanVocabulary('country', vocType='UrbanVocabularyTerm', inUrbanConfig=False),
    ),
    StringField(
        name='email',
        widget=StringField._properties['widget'](
            label='Email',
            label_msgid='urban_label_email',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='phone',
        widget=StringField._properties['widget'](
            label='Phone',
            label_msgid='urban_label_phone',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='fax',
        widget=StringField._properties['widget'](
            label='Fax',
            label_msgid='urban_label_fax',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='registrationNumber',
        widget=StringField._properties['widget'](
            condition="python: here.portal_type == 'Architect'",
            label='Registrationnumber',
            label_msgid='urban_label_registrationNumber',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='nationalRegister',
        widget=StringField._properties['widget'](
            size=30,
            label='Nationalregister',
            label_msgid='urban_label_nationalRegister',
            i18n_domain='urban',
        ),
        validators=('isBelgianNR',),
    ),
    LinesField(
        name='representedBy',
        widget=MultiSelectionWidget(
            condition='python:here.showRepresentedByField()',
            format='checkbox',
            label='Representedby',
            label_msgid='urban_label_representedBy',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        multiValued=1,
        vocabulary='listRepresentedBys',
    ),
    TextField(
        name='claimingText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            condition="python: here.portal_type == 'Claimant'",
            label='Claimingtext',
            label_msgid='urban_label_claimingText',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Contact_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Contact_schema['title'].widget.visible = False
Contact_schema['title'].required = False
##/code-section after-schema

class Contact(BaseContent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IContact)

    meta_type = 'Contact'
    _at_rename_after_creation = True

    schema = Contact_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Generate the title...
        """
        if not self.getName1():
            return self.getSociety()
        if self.getRepresentedBySociety():
            return "%s %s %s repr. par %s" % (self.getPersonTitle(short=True), self.getName1(), self.getName2(), self.getSociety())
        elif self.getSociety():
            return "%s %s %s (%s)" % (self.getPersonTitle(short=True), self.getName1(), self.getName2(), self.getSociety())
        else:
            return "%s %s %s" % (self.getPersonTitle(short=True), self.getName1(), self.getName2())

    security.declarePublic('getSignaletic')
    def getSignaletic(self, short=False, withaddress=False, linebyline=False):
        """
          Returns the contact base signaletic : title and names
        """
        urban_tool = getToolByName(self, 'portal_urban')
        invertnames = urban_tool.getInvertAddressNames()
        nameSignaletic = self._getNameSignaletic(short, linebyline, invertnames=invertnames)
        if not withaddress:
            if not linebyline:
                return nameSignaletic
            else:
                return '<p>%s</p>' % nameSignaletic
        else:
            #escape HTML special characters like HTML entities
            addressSignaletic = self.getAddress(linebyline=linebyline)
            if not linebyline:
                mapping = dict(name=nameSignaletic.decode('utf8'),
                               address=addressSignaletic.decode('utf8'))
                result = translate(
                    u'residing',
                    domain=u'urban',
                    mapping=mapping, context=self.REQUEST
                )
                return result.encode('utf8')
            else:
                #remove the <p></p> from adressSignaletic
                addressSignaletic = addressSignaletic[3:-4]
                return '<p>%s<br />%s</p>' % (nameSignaletic, addressSignaletic)

    def _getNameSignaletic(self, short, linebyline, invertnames=False):
        title = self.getPersonTitleValue(short, extra=False)
        namedefined = self.getName1() or self.getName2()
        names = '%s %s' % (self.getName1(), self.getName2())
        if invertnames and linebyline:
            names = '%s %s' % (self.getName2(), self.getName1())
        namepart = namedefined and names or self.getSociety()
        nameSignaletic = '%s %s' % (title, namepart)
        if len(self.getRepresentedBy()) > 0 or self.getRepresentedBySociety():
            person_title = self.getPersonTitle(theObject=True)
            representatives = self.getRepresentedBySociety() and self.getSociety() or self.displayValue(self.Vocabulary('representedBy')[0], self.getRepresentedBy())
            gender = multiplicity = ''
            represented = 'représenté'
            if person_title:
                gender = person_title.getGender()
                multiplicity = person_title.getMultiplicity()
                if gender == 'male' and multiplicity == 'plural':
                    represented = 'représentés'
                elif gender == 'female' and multiplicity == 'single':
                    represented = 'représentée'
                elif gender == 'female' and multiplicity == 'plural':
                    represented = 'représentées'
            nameSignaletic = '%s %s %s par %s' % (title, namepart, represented, representatives)
        if linebyline:
            #escape HTML special characters like HTML entities
            return cgi.escape(nameSignaletic)
        else:
            return nameSignaletic

    security.declarePublic('isPlural')
    def isPlural(self):
        """
        """
        is_plural = self.getMultiplicity() == 'plural'
        return is_plural

    security.declarePublic('getMultiplicity')
    def getMultiplicity(self):
        """
          Returns the contact person title multiplicity
        """
        person_title = self.getPersonTitle()
        if person_title:
            person_title_field = self.getField('personTitle')
            title_vocabulary = person_title_field.vocabulary
            person_title = title_vocabulary.getAllVocTerms(self)[person_title]
            return person_title.getMultiplicity()
        return None

    security.declarePublic('getAddress')
    def getAddress(self, linebyline=False):
        """
          Returns the contact address
        """
        number = self.getNumber()
        street = self.getStreet()
        zip = self.getZipcode()
        city = self.getCity()
        if not linebyline:
            result = []
            if number:
                result.append("%s," % number)
            if street:
                result.append(street)
            if zip:
                result.append(zip)
            if city:
                result.append(city)
            return ' '.join(result)
        else:
            number = cgi.escape(number)
            street = cgi.escape(street)
            zip = cgi.escape(zip)
            city = cgi.escape(city)
            return "<p>%s, %s<br />%s %s</p>" % (number, street, zip, city)

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
        if self.getPortalTypeName() not in ['Applicant', 'Proprietary']:
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
        if hasattr(parent, 'getNotaryContact'):
            potential_contacts.extend(list(parent.getNotaryContact()))
        if hasattr(parent, 'getGeometricians'):
            potential_contacts.extend(list(parent.getGeometricians()))
        if hasattr(parent, 'getArchitects'):
            potential_contacts.extend(parent.getArchitects())

        vocabulary = [(contact.UID(), contact.Title(),) for contact in potential_contacts]
        return DisplayList(tuple(vocabulary))

    security.declarePublic('getPersonTitle')
    def getPersonTitle(self, short=False, theObject=False):
        """
          Overrides the default personTitle accessor
          Returns the personTitle short version, so 'M' for 'Mister', ...
        """
        #either we need the classic value
        if not short:
            res = self.getField('personTitle').get(self)
            if res and theObject:
                tool = getToolByName(self, 'portal_urban')
                res = getattr(tool.persons_titles, res)
            return res

        #or the short one...
        tool = getToolByName(self, 'portal_urban')
        if hasattr(tool.persons_titles, self.getField('personTitle').get(self)):
            #XXX remove this when everybody will use the Plone4 version (aka Sambreville and La Bruyere)
            try:
                return getattr(tool.persons_titles, self.getField('personTitle').get(self)).getAbbreviation()
            except AttributeError:
                #for old instances, persons_titles are UrbanVocabularyTerms and have no abbreviation...
                #we used the no more existing termKeyStr attribute... that is removed in a migration step
                return getattr(tool.persons_titles, self.getField('personTitle').get(self)).termKeyStr.encode('utf-8')
        else:
            return ''

    security.declarePublic('getPersonTitleValue')
    def getPersonTitleValue(self, short=False, extra=True):
        """
          Returns the personTitle real value.  Usefull for being used in templates
        """
        personTitle = self.getPersonTitle(short, theObject=extra)
        if short:
            return personTitle
        elif extra:
            return personTitle.extraValue
        elif personTitle:
            return self.displayValue(self.Vocabulary('personTitle')[0], personTitle).encode('UTF-8')
        else:
            return ''

    security.declarePublic('getNumber')
    def getNumber(self):
        """
          Overrides the 'number' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if (self.portal_type == "Applicant" or self.portal_type == "Proprietary") and self.getIsSameAddressAsWorks():
            #get the works address
            licence = self.aq_inner.aq_parent
            workLocations = licence.getWorkLocations()
            if not workLocations:
                return ''
            else:
                return workLocations[0]['number']
        else:
            return self.getField('number').get(self)

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
            uid_catalog = getToolByName(self, 'uid_catalog')
            return uid_catalog(UID=workLocationStreetUID)[0].getObject()

    security.declarePublic('getStreet')
    def getStreet(self):
        """
          Overrides the 'street' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if (self.portal_type == "Applicant" or self.portal_type == "Proprietary") and self.getIsSameAddressAsWorks():
            #get the works address
            street = self._getStreetFromLicence()
            if not street:
                return ''
            return street.getStreetName()
        else:
            return self.getField('street').get(self)

    security.declarePublic('getZipcode')
    def getZipcode(self):
        """
          Overrides the 'zipcode' field accessor
        """
        #special behaviour for the applicants if we mentionned that the applicant's address
        #is the same as the works's address
        if (self.portal_type == "Applicant" or self.portal_type == "Proprietary") and self.getIsSameAddressAsWorks():
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
        if (self.portal_type == "Applicant" or self.portal_type == "Proprietary") and self.getIsSameAddressAsWorks():
            #get the works address
            street = self._getStreetFromLicence()
            if not street:
                return ''
            return street.getCity().Title()
        else:
            return self.getField('city').get(self)



registerType(Contact, PROJECTNAME)
# end of class Contact

##code-section module-footer #fill in your manual code here
##/code-section module-footer

