# -*- coding: utf-8 -*-

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import BaseFolder
from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import StringField
from Products.Archetypes.atapi import registerType
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.DataGridField import DataGridField
from Products.DataGridField import DataGridWidget
from Products.DataGridField.Column import Column
from collective.datagridcolumns.ReferenceColumn import ReferenceColumn
from zope.i18n import translate
from zope.interface import implements

from Products.urban import UrbanMessage as _
from Products.urban import interfaces
from Products.urban.config import PROJECTNAME
from Products.urban.content.licence.GenericLicence import GenericLicence
from Products.urban.content.Inquiry import Inquiry
from Products.urban.utils import setSchemataForInquiry


schema = Schema((
    StringField(
        name='class',
        widget=SelectionWidget(
            label=_('urban_label_class', default='Class'),
        ),
        vocabulary='listExplosivesPossessionClass',
        required=True,
        schemata='urban_description',
        default_method='getDefaultValue',
    ),
    DataGridField(
        name='businessOldLocation',
        schemata="urban_description",
        widget=DataGridWidget(
            columns={'number': Column("Number"), 'street': ReferenceColumn("Street", surf_site=False, object_provides=('Products.urban.interfaces.IStreet', 'Products.urban.interfaces.ILocality',))},
            helper_js=('datagridwidget.js', 'datagridautocomplete.js'),
            label=_('urban_label_businessOldLocation',
                    default='Old business location'),
        ),
        allow_oddeven=True,
        columns=('number', 'street'),
        validators=('isValidStreetName',),
    ),
))


ExplosivesPossession_schema = BaseFolderSchema.copy() + \
    getattr(GenericLicence, 'schema').copy() + \
    getattr(Inquiry, 'schema').copy() + \
    schema.copy()
setSchemataForInquiry(ExplosivesPossession_schema)
for field in ExplosivesPossession_schema.filterFields(isMetadata=False):
    if field.schemata == 'urban_investigation_and_advices' and field.getName() not in ['solicitOpinionsTo', 'solicitOpinionsToOptional']:
        field.widget.visible = False


class ExplosivesPossession(BaseFolder, GenericLicence, Inquiry, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IExplosivesPossession)

    meta_type = 'ExplosivesPossession'
    _at_rename_after_creation = True

    schema = ExplosivesPossession_schema
    schemata_order = [
        'urban_description',
        'urban_road',
        'urban_location',
        'urban_investigation_and_advices',
    ]

    security.declarePublic('getApplicants')

    def getApplicants(self):
        """
        """
        applicants = self.getCorporations() or super(ExplosivesPossession, self).getApplicants()
        return applicants

    security.declarePublic('getCorporations')

    def getCorporations(self):
        corporations = [corp for corp in self.objectValues('Corporation')]
        return corporations

    security.declarePublic('getApplicantsSignaletic')

    def getApplicantsSignaletic(self, withaddress=False):
        """
        Returns a string representing the signaletic of every applicants
        """
        applicants = self.getApplicants()
        signaletic = ''
        for applicant in applicants:
            # if the signaletic is not empty, we are adding several applicants
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

    security.declarePublic('listExplosivesPossessionClass')

    def listExplosivesPossessionClass(self):
        """
        This vocabulary for field class return the list of classes
        """
        vocabulary = (
            ('first', '1st class'),
            ('second', '2nd class'),
        )
        return DisplayList(vocabulary)


registerType(ExplosivesPossession, PROJECTNAME)


def finalizeSchema(schema, folderish=False, moveDiscussion=True):
    """
       Finalizes the type schema to alter some fields
    """

finalizeSchema(ExplosivesPossession_schema)
