# -*- coding: utf-8 -*-
#
# File: EnvironmentLicence.py
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
from Products.urban.EnvironmentBase import EnvironmentBase
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.DataGridField.SelectColumn import SelectColumn

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.interfaces import ILicenceDeliveryEvent
from Products.urban.utils import setOptionalAttributes
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from collective.datagridcolumns.TextAreaColumn import TextAreaColumn

from zope.i18n import translate

optional_fields =[]
##/code-section module-header

schema = Schema((

    StringField(
        name='authority',
        widget=SelectionWidget(
            label='Authority',
            label_msgid='urban_label_authority',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        vocabulary=UrbanVocabulary('authority', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),
    ReferenceField(
        name='previousLicences',
        widget=ReferenceBrowserWidget(
            label='Previouslicences',
            label_msgid='urban_label_previousLicences',
            i18n_domain='urban',
        ),
        allowed_types=('EnvClassThree', 'EnvClassTwo', 'EnvClassOne'),
        schemata='urban_description',
        multiValued=True,
        relationship='previousLicences',
    ),
    DataGridField(
        name='publicRoadModifications',
        allow_oddeven=True,
        widget=DataGridWidget(
            columns={'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',)), 'modification': TextAreaColumn('Modification'), 'justification': TextAreaColumn('Justification')},
            label='Publicroadmodifications',
            label_msgid='urban_label_publicRoadModifications',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        columns=('street', 'modification', 'justification'),
    ),
    BooleanField(
        name='hasEnvironmentImpactStudy',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Hasenvironmentimpactstudy',
            label_msgid='urban_label_hasEnvironmentImpactStudy',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    BooleanField(
        name='isSeveso',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isseveso',
            label_msgid='urban_label_isSeveso',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    IntegerField(
        name='validityDelay',
        default=20,
        widget=IntegerField._properties['widget'](
            label='Validitydelay',
            label_msgid='urban_label_validityDelay',
            i18n_domain='urban',
        ),
        schemata='urban_description',
    ),
    LinesField(
        name='ftSolicitOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Ftsolicitopinionsto',
            label_msgid='urban_label_ftSolicitOpinionsTo',
            i18n_domain='urban',
        ),
        schemata='urban_description',
        multiValued=1,
        vocabulary=UrbanVocabulary('ftSolicitOpinionsTo', inUrbanConfig=True),
        default_method='getDefaultValue',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

EnvironmentLicence_schema = BaseFolderSchema.copy() + \
    getattr(EnvironmentBase, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
for field in EnvironmentLicence_schema.filterFields(isMetadata=False):
    field.widget.visible = True

EnvironmentLicence_schema['roadMissingPartsDetails'].widget.label_msgid = 'urban_label_complement'
##/code-section after-schema

class EnvironmentLicence(BaseFolder, EnvironmentBase, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IEnvironmentLicence)

    meta_type = 'EnvironmentLicence'
    _at_rename_after_creation = True

    schema = EnvironmentLicence_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('getInquiries')
    def getInquiries(self):
        """
        Inquiry is mandatory for environment licences.
        """
        inquiries = [self]
        other_inquiries = self.objectValues('Inquiry')
        inquiries.extend(list(other_inquiries))
        return inquiries

    security.declarePublic('getApplicants')
    def getApplicants(self):
        """
        """
        applicants = self.getCorporations() or super(EnvironmentLicence, self).getApplicants()
        return applicants

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

    security.declarePublic('updateTitle')
    def updateTitle(self):
        """
           Update the title to clearly identify the licence
        """
        applicants = self.getCorporations() or self.getApplicants()
        if applicants:
            applicantTitle = applicants[0].Title()
        else:
            applicantTitle = translate('no_applicant_defined', 'urban', context=self.REQUEST).encode('utf8')
        title = "%s - %s - %s" % (self.getReference(), self.getLicenceSubject(), applicantTitle)
        self.setTitle(title)
        self.reindexObject(idxs=('Title', 'applicantInfosIndex', 'sortable_title', ))

    security.declarePublic('listLicenceParcels')
    def listLicenceParcels(self):
        parcels = self.objectValues('PortionOut')
        vocabulary = [(parcel.UID(), parcel.Title()) for parcel in parcels]
        return DisplayList(sorted(vocabulary, key=lambda name: name[1]))

    security.declarePublic('previouslicencesBaseQuery')
    def previouslicencesBaseQuery(self):
        return {'object_provides': IEnvironmentBase.__identifier__}

    def getLastLicenceDelivery(self):
        return self._getLastEvent(ILicenceDeliveryEvent)

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')]
        return corporations



registerType(EnvironmentLicence, PROJECTNAME)
# end of class EnvironmentLicence

##code-section module-footer #fill in your manual code here
def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """
    schema.moveField('authority', after='referenceDGATLP')
    schema.moveField('natura2000', after='isSeveso')
    schema.moveField('natura2000Details', after='natura2000')
    schema.moveField('description', after='validityDelay')

finalizeSchema(EnvironmentLicence_schema)
##/code-section module-footer

