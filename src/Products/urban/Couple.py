# -*- coding: utf-8 -*-
#
# File: Couple.py
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
from Products.urban.Applicant import Applicant
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *

import cgi

##code-section module-header #fill in your manual code here
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
##/code-section module-header

schema = Schema((

    StringField(
        name='couplePerson1Name',
        widget=StringField._properties['widget'](
            label='couplePerson1Name',
            label_msgid='urban_label_coupleperson1name',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='couplePerson1Firstname',
        widget=StringField._properties['widget'](
            label='couplePerson1Firstname',
            label_msgid='urban_label_coupleperson1firstname',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='nationalRegisterPerson1',
        widget=StringField._properties['widget'](
            size=30,
            label='NationalregisterPerson1',
            label_msgid='urban_label_nationalRegisterPerson1',
            i18n_domain='urban',
        ),
        validators=('isBelgianNR',),
    ),
    StringField(
        name='couplePerson2Name',
        widget=StringField._properties['widget'](
            label='couplePerson2Name',
            label_msgid='urban_label_coupleperson2name',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='couplePerson2Firstname',
        widget=StringField._properties['widget'](
            label='couplePerson2Firstname',
            label_msgid='urban_label_coupleperson2firstname',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='nationalRegisterPerson2',
        widget=StringField._properties['widget'](
            size=30,
            label='NationalregisterPerson2',
            label_msgid='urban_label_nationalRegisterperson2',
            i18n_domain='urban',
        ),
        validators=('isBelgianNR',),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

Couple_schema = BaseSchema.copy() + \
    getattr(Applicant, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
Couple_schema.delField('name1')
Couple_schema.delField('name2')
Couple_schema.delField('nationalRegister')
Couple_schema.delField('representedBySociety')
Couple_schema.delField('society')
##/code-section after-schema


class Couple(BaseContent, Applicant, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.ICouple)

    meta_type = 'Couple'
    _at_rename_after_creation = True

    schema = Couple_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('Title')
    def Title(self):
        """
           Generate the title...
        """
        return "%s %s-%s %s et %s" % (self.getPersonTitle(short=True), self.getCouplePerson1Name(), self.getCouplePerson2Name(), self.getCouplePerson1Firstname(), self.getCouplePerson2Firstname())

    def _getNameSignaletic(self, short, linebyline, reverse=False, invertnames=False):
        title = self.getPersonTitleValue(short, False, reverse).decode('utf8')
        lastNamePerson1 = self.getCouplePerson1Name().decode('utf-8')
        firstNamePerson1 = self.getCouplePerson1Firstname().decode('utf-8')
        lastNamePerson2 = self.getCouplePerson2Name().decode('utf-8')
        firstNamePerson2 = self.getCouplePerson2Firstname().decode('utf-8')
        namedefined = lastNamePerson1 or firstNamePerson1 or lastNamePerson2 or firstNamePerson2
        names = u'%s-%s %s et %s' % (lastNamePerson1, lastNamePerson2, firstNamePerson1, firstNamePerson2)
        if invertnames:
            names = u'%s et %s %s-%s' % (firstNamePerson1, firstNamePerson2, lastNamePerson1, lastNamePerson2)
        names = names.strip()
        if namedefined: namepart = names
        nameSignaletic = u'%s %s' % (title, namepart)
        nameSignaletic = nameSignaletic.strip()
        if len(self.getRepresentedBy()) > 0:
            person_title = self.getPersonTitle(theObject=True)
            representatives = self.displayValue(self.Vocabulary('representedBy')[0], self.getRepresentedBy())
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

    @property
    def name1(self):
        """
        """
        name1 = "%s - %s" % (self.getCouplePerson1Name(), self.getCouplePerson2Name())
        return name1

    @property
    def name2(self):
        """
        """
        name2 = "%s et %s" % (self.getCouplePerson1Firstname(), self.getCouplePerson2Firstname())
        return name2

    security.declarePublic('getName1')
    def getName1(self):
        """
        redefined getName1 for mailing loop
        """
        return self.name1

    security.declarePublic('getName2')
    def getName2(self):
        """
        redefined getName2 for mailing loop
        """
        return self.name2


registerType(Couple, PROJECTNAME)
# end of class Couple

##code-section module-footer #fill in your manual code here


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
    Finalizes the type schema to alter some fields
    """
    schema.moveField('couplePerson1Name', after='personTitle')
    schema.moveField('couplePerson1Firstname', after='couplePerson1Name')
    schema.moveField('couplePerson2Name', after='couplePerson1Firstname')
    schema.moveField('couplePerson2Firstname', after='couplePerson2Name')
    schema['personTitle'].vocabulary = UrbanVocabulary(
        'persons_titles', vocType='PersonTitleTerm', inUrbanConfig=False, _filter=lambda title: title['multiplicity'] == 'plural'
    )


finalizeSchema(Couple_schema)
##/code-section module-footer
