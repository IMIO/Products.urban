# -*- coding: utf-8 -*-
#
# File: Contact.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
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
from Products.validation.interfaces.IValidator import IValidator
from Products.validation import validation
from Products.CMFCore.utils import getToolByName
from Products.urban.utils import setRawSchema

class BelgianNationalRegValidator:
    #Validate a belgian national register number
    implements(IValidator)
    def __init__(self, name):
        self.name = name
    def __call__(self, value, *args, **kwargs):
        #the eID card number is 11 number long, we only accept number and '-' and '.'
        #we test that we only have got numbers and '-' and '.'
        len_value = len(value)

        clean_value =  ''.join([c for c in value if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9','-','.')])
        if len_value != len(clean_value):
            return "This field only accept numbers, indents or points !"

        clean_value =  ''.join([c for c in value if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9',)])

        #we check that there are 11 numbers left
        if len(clean_value) != 11:
            return "Your National Register number must be 11 digits long !"

        first_part = int(clean_value[0:9])
        last_part = int(clean_value[9:11])

        #the two last digits is the result of 97 les the modulo by 97 of the 10 first digits
        if last_part != (97 - (first_part%97)):
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
        vocabulary='listPersonTitles',
    ),
    StringField(
        name='name1',
        widget=StringField._properties['widget'](
            label='Name1',
            label_msgid='urban_label_name1',
            i18n_domain='urban',
        ),
        searchable=True,
    ),
    StringField(
        name='name2',
        widget=StringField._properties['widget'](
            label='Name2',
            label_msgid='urban_label_name2',
            i18n_domain='urban',            
        ),
        searchable=True,
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
setRawSchema(schema)
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

    security.declarePublic('listPersonTitles')
    def listPersonTitles(self):
        """
          Returns possible person titles
        """
        return DisplayList(self.portal_urban.listVocabulary('persons_titles', self, inUrbanConfig=False))

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Generate the title...
        """
        if not self.getName1():
            return self.getSociety()
        if self.getSociety():
            return "%s %s (%s)" % (self.getName1(), self.getName2(), self.getSociety())
        else:
            return "%s %s" % (self.getName1(), self.getName2())

    security.declarePublic('at_post_create_script')
    def at_post_create_script(self):
        """
           Post create hook...
           XXX This should be replaced by a zope event...
        """
        self.at_post_edit_script()

    security.declarePublic('at_post_edit_script')
    def at_post_edit_script(self):
        """
           Post edit hook...
           XXX This should be replaced by a zope event...
           As the applicant names appear in the parent title, we update it...
        """
        #only update parent's title if an applicant or a proprietary is added
        if not self.portal_type in ['Applicant', 'Proprietary', ]:
            return
        parent = self.getParentNode()
        if parent.portal_type in ["Declaration", "BuildLicence", "ParcelOutLicence", "UrbanCertificateOne", "UrbanCertificateTwo", "NotaryLetter", "EnvironmentalDeclaration", "Division", ]:
            parent.at_post_edit_script()

    security.declarePublic('getSignaletic')
    def getSignaletic(self, withaddress=False, linebyline=False):
        """
          Returns the contact base signaletic : title and names
        """
        nameSignaletic = self._getNameSignaletic(linebyline)
        if not withaddress:
            if not linebyline:
                return nameSignaletic
            else:
                return u'<p>%s</p>' % nameSignaletic
        else:
            #escape HTML special characters like HTML entities
            addressSignaletic = self.getAddress(linebyline=linebyline)
            if not linebyline:
                mapping = dict(name=nameSignaletic, address=addressSignaletic)
                return translate(u'residing',
                    domain=u'urban',
                    mapping=mapping, context=self.REQUEST)
            else:
                #remove the <p></p> from adressSignaletic
                addressSignaletic = addressSignaletic[3:-4]
                return u'<p>%s<br />%s</p>' % (nameSignaletic,
                    addressSignaletic)


    def _getNameSignaletic(self, linebyline):
        title = self.displayValue(self.listPersonTitles(),
            self.getPersonTitle())
        nameSignaletic = u'%s %s %s' % (title, self.getName1(), self.getName2())
        if linebyline:
            #escape HTML special characters like HTML entities
            return cgi.escape(nameSignaletic)
        else:
            return nameSignaletic

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
            return u' '.join(result)
        else:
            number = cgi.escape(number)
            street = cgi.escape(street)
            zip = cgi.escape(zip)
            city = cgi.escape(city)
            return u"<p>%s, %s<br />%s %s</p>" % (number, street, zip, city)

    security.declarePublic('showRepresentedByField')
    def showRepresentedByField(self):
        """
          Only show the representedBy field if the current Contact is an Applicant (portal_type)
        """
        if not self.getPortalTypeName() == 'Applicant':
            return False
        return True

    security.declarePublic('listRepresentedBys')
    def listRepresentedBys(self):
        """
          Returns the list of potential Contacts that could represent the current Contact
          only if it is an "Applicant" as the field will be hidden by the condition on the field otherwise
        """
        #the potential representator are varying upon licence type
        #moreover, as we are using ReferenceField, we can not use getattr...
        lst = []
        if hasattr(self, 'getNotaryContact'):
            lst=lst+list(self.getNotaryContact())
        if hasattr(self, 'getGeometricians'):
            lst=lst+list(self.getGeometricians())
        if hasattr(self, 'getArchitects'):
            lst=lst+self.getArchitects()

        vocab = []
        for elt in lst:
            vocab.append((elt.UID(), elt.Title()))
        return DisplayList(tuple(vocab))

    security.declarePublic('getPersonTitleValue')
    def getPersonTitleValue(self):
        """
          Returns the personTitle real value.  Usefull for being used in templates
        """
        return self.displayValue(self.listPersonTitles(), self.getPersonTitle())

    security.declarePublic('getPersonTitle')
    def getPersonTitle(self, short=False):
        """
          Overrides the default personTitle accessor
          Returns the personTitle short version, so 'M' for 'Mister', ...
        """
        #either we need the classic value
        if not short:
            return self.getField('personTitle').get(self)
        #or the short one...
        tool = getToolByName(self, 'portal_urban')
        if hasattr(tool.persons_titles, self.getField('personTitle').get(self)):
            return getattr(tool.persons_titles, self.getField('personTitle').get(self)).getTermKeyStr()
        else:
            return ''



registerType(Contact, PROJECTNAME)
# end of class Contact

##code-section module-footer #fill in your manual code here
##/code-section module-footer
