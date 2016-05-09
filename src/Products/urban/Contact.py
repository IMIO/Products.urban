# -*- coding: utf-8 -*-
#
# File: Contact.py
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
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

##code-section module-header #fill in your manual code here
import cgi
from zope.i18n import translate
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.validation.interfaces.IValidator import IValidator
from Products.validation import validation

from plone import api


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
        if self.getSociety():
            return "%s %s %s (%s)" % (self.getPersonTitle(short=True), self.getName1(), self.getName2(), self.getSociety())
        else:
            return "%s %s %s" % (self.getPersonTitle(short=True), self.getName1(), self.getName2())

    security.declarePublic('getSignaletic')
    def getSignaletic(self, short=False, withaddress=False, linebyline=False, reverse=False):
        """
          Returns the contact base signaletic : title and names
        """
        urban_tool = api.portal.get_tool('portal_urban')
        invertnames = urban_tool.getInvertAddressNames()
        nameSignaletic = self._getNameSignaletic(short, linebyline, reverse, invertnames)
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
                if self.isMasculineSingular():
                    result = translate(
                        u'masculine_singular_residing',
                        domain=u'urban',
                        mapping=mapping, context=self.REQUEST
                    )
                elif self.isFeminineSingular():
                    result = translate(
                        u'feminine_singular_residing',
                        domain=u'urban',
                        mapping=mapping, context=self.REQUEST
                    )
                elif self.isFemininePlural():
                    result = translate(
                        u'feminine_plural_residing',
                        domain=u'urban',
                        mapping=mapping, context=self.REQUEST
                    )
                else:
                    result = translate(
                        u'mixed_residing',
                        domain=u'urban',
                        mapping=mapping, context=self.REQUEST
                    )
                return result.encode('utf8')
            else:
                #remove the <p></p> from adressSignaletic
                addressSignaletic = addressSignaletic[3:-4]
                address = '<p>%s<br />%s</p>' % (nameSignaletic, addressSignaletic)
                return address

    def _getNameSignaletic(self, short, linebyline, reverse=False, invertnames=False):
        title = self.getPersonTitleValue(short, False, reverse)
        namedefined = self.getName1() or self.getName2()
        names = '%s %s' % (self.getName1(), self.getName2())
        if invertnames:
            names = '%s %s' % (self.getName2(), self.getName1())
        namepart = namedefined and names or self.getSociety()
        nameSignaletic = '%s %s' % (title, namepart.decode('utf8'))
        nameSignaletic = nameSignaletic.encode('utf8')
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
            if street:
                result.append(street)
            if number:
                result.append(number)
            if zip:
                result.append("%s" % zip)
            if city:
                result.append(city)
            return ' '.join(result)
        else:
            number = cgi.escape(number)
            street = cgi.escape(street)
            zip = cgi.escape(zip)
            city = cgi.escape(city)
            return "<p>%s, %s<br />%s %s</p>" % (street, number, zip, city)

    security.declarePublic('getPersonTitle')
    def getPersonTitle(self, short=False, reverse=False, theObject=False):
        """
          Overrides the default personTitle accessor
          Returns the personTitle short version, so 'M' for 'Mister', ...
        """
        #either we need the classic value
        tool = api.portal.get_tool('portal_urban')
        if not short:
            res = self.getField('personTitle').get(self)
            if res and reverse:
                return getattr(tool.persons_titles, res).getReverseTitle()
            if res and theObject:
                tool = api.portal.get_tool('portal_urban')
                res = getattr(tool.persons_titles, res)
            return res

        #or the short one...
        if hasattr(tool.persons_titles, self.getField('personTitle').get(self)):
            return getattr(tool.persons_titles, self.getField('personTitle').get(self)).getAbbreviation()
        else:
            return ''

    security.declarePublic('getPersonTitleValue')
    def getPersonTitleValue(self, short=False, extra=True, reverse=False):
        """
          Returns the personTitle real value.  Useful for being used in templates
        """
        personTitle = self.getPersonTitle(short, reverse, theObject=extra)
        if type(personTitle) == str:
           personTitle = personTitle and self.displayValue(self.Vocabulary('personTitle')[0], personTitle)
        else:
            personTitle = personTitle.extraValue
        return personTitle

    def isMasculineSingular(self):
        """
        """
        answer = False
        field = self.getField('personTitle')
        titles = field.vocabulary.getAllVocTerms(self)
        title = titles[self.getPersonTitle()]
        if title.getMultiplicity() == 'single':
            if title.getGender() == 'male':
                answer = True
        return answer

    def isFeminineSingular(self):
        """
        """
        answer = False
        field = self.getField('personTitle')
        titles = field.vocabulary.getAllVocTerms(self)
        title = titles[self.getPersonTitle()]
        if title.getMultiplicity() == 'single':
            if title.getGender() == 'female':
                answer = True
        return answer

    def isFemininePlural(self):
        """
        """
        answer = False
        field = self.getField('personTitle')
        titles = field.vocabulary.getAllVocTerms(self)
        title = titles[self.getPersonTitle()]
        if title.getMultiplicity() == 'plural':
            if title.getGender() == 'female':
                answer = True
        return answer



registerType(Contact, PROJECTNAME)
# end of class Contact

##code-section module-footer #fill in your manual code here
##/code-section module-footer

