# -*- coding: utf-8 -*-
#
# File: UrbanTool.py
#
# Copyright (c) 2013 by CommunesPlone
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

from Products.DataGridField import DataGridField, DataGridWidget
from Products.urban.config import *


from Products.CMFCore.utils import UniqueObject


##code-section module-header #fill in your manual code here
import logging
logger = logging.getLogger('urban: UrbanTool')
import appy.pod.renderer
import psycopg2
import psycopg2.extras
import os
import time
import re
#from urlparse import urlparse
from DateTime import DateTime
from StringIO import StringIO
from AccessControl import getSecurityManager
from Acquisition import aq_base
from zope.i18n import translate
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions
from Products.CMFCore.Expression import Expression, createExprContext
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.CMFPlone.PloneBatch import Batch
from Products.PageTemplates.Expressions import getEngine
from Products.DataGridField.Column import Column
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.FixedColumn import FixedColumn
from Products.urban.utils import getOsTempFolder
from Products.urban.utils import ParcelHistoric
from Products.urban.config import GENERATED_DOCUMENT_FORMATS
from Products.urban.config import GLOBAL_TEMPLATES
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.interfaces import IUrbanVocabularyTerm, IContactFolder

DB_NO_CONNECTION_ERROR = "No DB Connection"
DB_QUERY_ERROR = "Programming error in query"
##/code-section module-header

schema = Schema((

    StringField(
        name='title',
        widget=StringField._properties['widget'](
            visible=False,
            label='Title',
            label_msgid='urban_label_title',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='NISNum',
        widget=StringField._properties['widget'](
            label='Nisnum',
            label_msgid='urban_label_NISNum',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='cityName',
        default='MaCommune',
        widget=StringField._properties['widget'](
            label='Cityname',
            label_msgid='urban_label_cityName',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    DataGridField(
        name='divisionsRenaming',
        widget=DataGridWidget(
            columns={'division': FixedColumn('Division', visible=False), 'name': FixedColumn('Name'), 'alternative_name': Column('Alternative Name')},
            label='Divisionsrenaming',
            label_msgid='urban_label_divisionsRenaming',
            i18n_domain='urban',
        ),
        fixed_rows='getDivisionsConfigRows',
        allow_insert=False,
        allow_reorder=False,
        allow_oddeven=True,
        allow_delete=True,
        schemata='public_settings',
        columns=('division', 'name', 'alternative_name',),
    ),
    BooleanField(
        name='isDecentralized',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isdecentralized',
            label_msgid='urban_label_isDecentralized',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    StringField(
        name='sqlHost',
        widget=StringField._properties['widget'](
            label='Sqlhost',
            label_msgid='urban_label_sqlHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlName',
        widget=StringField._properties['widget'](
            label='Sqlname',
            label_msgid='urban_label_sqlName',
            i18n_domain='urban',
        ),
        required=True,
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlUser',
        widget=StringField._properties['widget'](
            label='Sqluser',
            label_msgid='urban_label_sqlUser',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='sqlPassword',
        widget=PasswordWidget(
            label='Sqlpassword',
            label_msgid='urban_label_sqlPassword',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='webServerHost',
        widget=StringField._properties['widget'](
            label='Webserverhost',
            label_msgid='urban_label_webServerHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='pylonsHost',
        widget=StringField._properties['widget'](
            label='Pylonshost',
            label_msgid='urban_label_pylonsHost',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='mapExtent',
        widget=StringField._properties['widget'](
            description="Enter the 4 coordinates of the map, each coordinate separated by a comma.",
            description_msgid="urban_descr_mapExtent",
            label='Mapextent',
            label_msgid='urban_label_mapExtent',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='unoEnabledPython',
        default="/usr/bin/python",
        widget=StringField._properties['widget'](
            label="Path of a UNO-enabled Python interpreter (ie /usr/bin/python)",
            description="UnoEnabledPython",
            description_msgid="uno_enabled_python",
            label_msgid='urban_label_unoEnabledPython',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    IntegerField(
        name='openOfficePort',
        default=2002,
        widget=IntegerField._properties['widget'](
            description="OpenOfficePort",
            description_msgid="open_office_port",
            label='Openofficeport',
            label_msgid='urban_label_openOfficePort',
            i18n_domain='urban',
        ),
        schemata='admin_settings',
        write_permission=permissions.ManagePortal,
    ),
    StringField(
        name='editionOutputFormat',
        default='odt',
        widget=SelectionWidget(
            label='Editionoutputformat',
            label_msgid='urban_label_editionOutputFormat',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        schemata='public_settings',
        vocabulary=GENERATED_DOCUMENT_FORMATS.keys(),
    ),
    BooleanField(
        name='generateSingletonDocuments',
        default=True,
        widget=BooleanField._properties['widget'](
            label='Generatesingletondocuments',
            label_msgid='urban_label_generateSingletonDocuments',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    BooleanField(
        name='invertAddressNames',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Invertaddressnames',
            label_msgid='urban_label_invertAddressNames',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),
    BooleanField(
        name='usePloneMeetingWSClient',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Useplonemeetingwsclient',
            label_msgid='urban_label_usePloneMeetingWSClient',
            i18n_domain='urban',
        ),
        schemata='public_settings',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanTool_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
for f in UrbanTool_schema.filterFields(schemata='default'):
    f.widget.visible = {"edit": "invisible"}
for f in UrbanTool_schema.filterFields(schemata='metadata'):
    f.widget.visible = {"edit": "invisible"}
##/code-section after-schema

class UrbanTool(UniqueObject, OrderedBaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanTool)

    meta_type = 'UrbanTool'
    _at_rename_after_creation = True

    schema = UrbanTool_schema

    ##code-section class-header #fill in your manual code here
    # XXX constant put on the class to ensure it is close to the method that uses
    # it
    portal_types_per_event_type_type = {
        'Products.urban.interfaces.IInquiryEvent': 'UrbanEventInquiry',
        'Products.urban.interfaces.IOpinionRequestEvent': 'UrbanEventOpinionRequest',
    }
    ##/code-section class-header


    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        OrderedBaseFolder.__init__(self,'portal_urban')
        self.setTitle('Urban configuration')

        ##code-section constructor-footer #fill in your manual code here
        ##/code-section constructor-footer


    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()

        ##code-section post-edit-method-footer #fill in your manual code here
        self.checkDBConnection()
        ##/code-section post-edit-method-footer


    # Methods

    # Manually created methods

    def at_post_create_script(self):
        """
          Post creation hook
        """
        self.checkDBConnection()

    security.declarePublic('getDivisionsConfigRows')
    def getDivisionsConfigRows(self):
        """
        """
        divisions = self.findDivisions(all=False)
        rows = []
        if DB_QUERY_ERROR not in divisions[0].values():
            for division in divisions:
                division_id = str(division['da'])
                name = division['divname']
                row = FixedRow(keyColumn='division', initialData={'division': division_id, 'name': name, 'alternative_name': name})
                rows.append(row)
        return rows

    security.declarePublic('createUrbanEvent')
    def createUrbanEvent(self, licence_uid, urban_event_type_uid):
        """
           Create an urbanEvent on a licence
           XXX this method should be moved to the BuildLicence class
        """
        uid_catalog = getToolByName(self, 'uid_catalog')
        # the licence where the UrbanEvent is created
        licence = uid_catalog(UID=licence_uid)[0].getObject()

        urbanEventType = uid_catalog(UID=urban_event_type_uid)[0].getObject()
        urbanEventType.checkCreationInLicence(licence)

        eventTypeType = urbanEventType.getEventTypeType()
        portal_type = self.portal_types_per_event_type_type.get(eventTypeType, "UrbanEvent")

        newUrbanEventId = licence.invokeFactory(
            portal_type,
            id=self.generateUniqueId(portal_type),
            title=urbanEventType.Title(),
            urbaneventtypes=(urbanEventType, )
        )
        newUrbanEventObj = getattr(licence, newUrbanEventId)
        return self.REQUEST.RESPONSE.redirect(newUrbanEventObj.absolute_url() + '/edit')

    security.declarePublic('createUrbanDoc')
    def createUrbanDoc(self, urban_template_uid, urban_event_uid):
        """
          Create an element in an UrbanEvent
        """
        urbanTemplate = self.uid_catalog(UID=urban_template_uid)[0]
        urbanTemplateObj = urbanTemplate.getObject()
        urbanEvent = self.uid_catalog(UID=urban_event_uid)[0]
        urbanEventObj = urbanEvent.getObject()
        licenceFolder = urbanEventObj.getParentNode()
        fileType = self.getEditionOutputFormat()
        tempFileName = '%s/%s_%f.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(), fileType)
        temp_file_names = {}
        try:
            applicantobj = licenceFolder.getApplicants()[0]
        except:
            applicantobj = None
        portal_url = getToolByName(self, 'portal_url')
        brain = self.portal_catalog(path=portal_url.getPortalPath() + '/' + '/'.join(portal_url.getRelativeContentPath(licenceFolder)), id='depot-de-la-demande')
        try:
            recepisseobj = brain[0].getObject()
        except:
            recepisseobj = None
        brain = self.portal_catalog(path=portal_url.getPortalPath() + '/' + '/'.join(portal_url.getRelativeContentPath(licenceFolder)), id='premier-passage-au-college-communal')
        try:
            collegesubmissionobj = brain[0].getObject()
        except:
            collegesubmissionobj = None
        global_templates = getattr(self, 'globaltemplates')
        #in the global_templates, only some of these templates must be taken into account
        auto_imported_template_ids = ['header.odt', 'footer.odt', 'reference.odt', 'signatures.odt']
        for generic_template in GLOBAL_TEMPLATES:
            #do only import necessary templates if exists...
            if not generic_template['id'] in auto_imported_template_ids or not hasattr(aq_base(global_templates), generic_template['id']):
                continue
            template = getattr(global_templates, generic_template['id'])
            if template and template.size:
                template = StringIO(template)
                temp_file_name = '%s/%s_%f.%s' % (getOsTempFolder(), urbanTemplateObj._at_uid, time.time(), 'odt')
                #remove the '.odt' suffix so terms like "header" can be used in the templates instead of "header.odt"
                temp_file_names[generic_template['id'][: -4]] = temp_file_name
                #we render the template so pod instructions into the generic sub-templates are rendered too
                renderer = appy.pod.renderer.Renderer(template,
                                                      {'self': licenceFolder, 'urbanEventObj': urbanEventObj,
                                                       'applicantobj': applicantobj, 'recepisseobj': recepisseobj,
                                                       'tool': self,
                                                       'template': urbanTemplateObj,
                                                       'collegesubmissionobj': collegesubmissionobj, },
                                                      temp_file_name, pythonWithUnoPath=self.getUnoEnabledPython())
                renderer.run()
        #now that sub-templates are rendered, we can use them in the main pod template and render the entire document
        #we prepare the styles template
        templateStyles = getattr(global_templates, 'styles.odt', None)
        if templateStyles and templateStyles.size:
            templateStyles = StringIO(templateStyles)
        dict_arg = {'self': licenceFolder, 'urbanEventObj': urbanEventObj, 'applicantobj': applicantobj,
                    'recepisseobj': recepisseobj, 'collegesubmissionobj': collegesubmissionobj, 'tool': self,
                    'template': urbanTemplateObj}
        dict_arg.update(temp_file_names)
        renderer = appy.pod.renderer.Renderer(StringIO(urbanTemplateObj), dict_arg,
                                              tempFileName, pythonWithUnoPath=self.getUnoEnabledPython())
        renderer.run()
        # Tell the browser that the resulting page contains ODT
        response = self.REQUEST.RESPONSE
        response.setHeader('Content-type', 'application/%s' % fileType)
        response.setHeader('Content-disposition', 'inline;filename="%s.%s"' % (self.id, fileType))
        # Returns the doc and removes the temp file
        f = open(tempFileName, 'rb')
        doc = f.read()
        f.close()
        os.remove(tempFileName)
        #now we need to generate an available id for the new file
        #the id of the object have to be the same id as the file contained
        #see http: //dev.communesplone.org/trac/ticket/2532
        urbanTemplateObjId = os.path.splitext(urbanTemplateObj.getId())[0]
        proposedId = urbanTemplateObjId + '.%s' % fileType
        i = 1
        while hasattr(aq_base(urbanEventObj), proposedId):
            proposedId = '%s-%d.odt' % (urbanTemplateObjId, i)
            i = i + 1
        newUrbanDoc = urbanEventObj.invokeFactory("UrbanDoc", id=proposedId, title=urbanTemplateObj.Title(), content_type=GENERATED_DOCUMENT_FORMATS[fileType], file=doc)
        newUrbanDoc = getattr(urbanEventObj, newUrbanDoc)
        newUrbanDoc.setFilename(proposedId)
        newUrbanDoc.setFormat(GENERATED_DOCUMENT_FORMATS[fileType])
        newUrbanDoc._at_rename_after_creation = False
        newUrbanDoc.processForm()
        self.REQUEST.set('doc_uid', newUrbanDoc.UID())
        response.redirect(urbanEventObj.absolute_url() + '?doc_uid=' + newUrbanDoc.UID())

    security.declarePublic('getVocabularyDefaultValue')
    def getVocabularyDefaultValue(self, vocabulary_name, context, in_urban_config, multivalued=False):
        """
         Return the first vocabulary term marked as default value of the vocabulary named vocabulary_name
        """
        #search in an urbanConfig or in the tool
        empty_value = multivalued and [] or ''
        if in_urban_config:
            config_folder = getattr(self, self.getUrbanConfig(context).getId())
            if not hasattr(config_folder, vocabulary_name):
                return empty_value
            voc_folder = getattr(config_folder, vocabulary_name)
        else:
            voc_folder = getattr(self, vocabulary_name)
        default_values = [voc_term.id for voc_term in voc_folder.listFolderContents() if voc_term.getIsDefaultValue()]
        return default_values and default_values or empty_value

    security.declarePublic('getTextDefaultValue')
    def getTextDefaultValue(self, fieldname, context, html=False, config=None):
        """
         Return the default text of the field (if it exists)
        """
        if not config:
            config = getattr(self, self.getUrbanConfig(context).getId())
        for prop in config.getTextDefaultValues():
            if 'fieldname' in prop and prop['fieldname'] == fieldname:
                return prop['text']
        return html and '<p></p>' or ''

    security.declarePublic('listVocabulary')
    def listVocabulary(self, vocToReturn, context, vocType=["UrbanVocabularyTerm", "OrganisationTerm"], id_to_use="id", value_to_use="Title", sort_on="getObjPositionInParent", inUrbanConfig=True, allowedStates=['enabled'], with_empty_value=False, with_numbering=True):
        """
           This return a list of elements that is used as a vocabulary
           by some fields of differents classes
        """
        brains = self.listVocabularyBrains(vocToReturn, context, vocType, sort_on, inUrbanConfig, allowedStates, with_empty_value)
        res = []
        if with_empty_value and brains and len(brains) > 1:
            #we add an empty vocab value of type "choose a value" at the beginning of the list
            #except if there is only one value in the list...
            val = translate(EMPTY_VOCAB_VALUE, 'urban', context=self.REQUEST, default=EMPTY_VOCAB_VALUE)
            res.append(('', val))

        for brain in brains:
            #the value to use can be on the brain or on the object
            if hasattr(brain, value_to_use):
                value = getattr(brain, value_to_use)
            else:
                value = getattr(brain.getObject(), value_to_use)
            #special case for 'Title' encoding
            if value_to_use == 'Title':
                value = value.decode('utf-8')
            if with_numbering:
                vocterm = brain.getObject()
                if IUrbanVocabularyTerm.providedBy(vocterm):
                    numbering = vocterm.getNumbering() and '%s - ' % vocterm.getNumbering() or ''
                    value = '%s%s' % (numbering, value)
            #display a special value for elements that are disabled in the configuration
            if brain.review_state == 'disabled':
                value = '~~ %s ~~' % value
            res.append((getattr(brain, id_to_use), value))
        return tuple(res)

    security.declarePrivate('listVocabularyBrains')
    def listVocabularyBrains(self, vocToReturn, context, vocType=["UrbanVocabularyTerm", "OrganisationTerm"], sort_on="getObjPositionInParent", inUrbanConfig=True, allowedStates=['enabled'], with_empty_value=False):
        """
           This return a list of elements that is used as a vocabulary
           by some fields of differents classes
        """
        #search in an urbanConfig or in the tool
        if inUrbanConfig:
            vocPath = "%s/%s/%s" % ('/'.join(self.getPhysicalPath()), self.getUrbanConfig(context).getId(), vocToReturn)
        else:
            vocPath = "%s/%s" % ('/'.join(self.getPhysicalPath()), vocToReturn)
        brains = self.portal_catalog(path=vocPath, sort_on=sort_on, portal_type=vocType, review_state=allowedStates)
        return brains

    security.declarePrivate('listVocabularyObjects')
    def listVocabularyObjects(self, vocToReturn, context, vocType="UrbanVocabularyTerm", id_to_use="id", inUrbanConfig=True,
                              sort_on="getObjPositionInParent", allowedStates=['enabled'], with_empty_value=False):
        brains = self.listVocabularyBrains(vocToReturn, context, vocType=vocType, inUrbanConfig=inUrbanConfig, sort_on=sort_on,
                                           allowedStates=allowedStates, with_empty_value=with_empty_value)
        res = {}
        for brain in brains:
            res[getattr(brain, id_to_use)] = brain.getObject()
        return res

    security.declarePublic('checkPermission')
    def checkPermission(self, permission, obj):
        """
           We must call getSecurityManager() each time we need to check a permission.
        """
        sm = getSecurityManager()
        return sm.checkPermission(permission, obj)

    security.declarePublic('getGlobalSearchTopic')
    def getGlobalSearchTopic(self):
        """
           Return the global search topic
        """
        try:
            topics = getattr(self, 'topics')
            globalSearch = getattr(topics, 'globalsearch')
        except AttributeError:
            return 0
        return globalSearch

    security.declarePublic('getDBConnection')
    def getDBConnection(self, connection_string=None):
        """
           Return the DB connection object
           The passed connection string must contain :
           dbname, user, host, password
        """
        try:
            #if we do not receive a connection string, we take infos from the tool (self)
            if not connection_string:
                conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.getSqlName(), self.getSqlUser(), self.getSqlHost(), self.getSqlPassword()))
            else:
                conn = psycopg2.connect(connection_string)
            return conn
        except psycopg2.OperationalError, error:
            #if we could not connect, return the error
            return error

    security.declarePublic('findDivisions')
    def findDivisions(self, all=True):
        """
           Return the possible divisions
        """
        result = self.queryDB("SELECT da, divname FROM da;")
        if not result:
            return ({'da': DB_QUERY_ERROR, 'divname': DB_QUERY_ERROR}, )
        if all:
            result = [{'da': '', 'divname': translate('all_divisions', 'urban', context=self.REQUEST)}] + result
        return result

    security.declarePublic('queryParcels')
    def queryParcels(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, location=None, prcowner=None,
                     browseold=False, historic=False, fuzzy=True):
        """
         Return the concerned parcels
        """
        query_string = browseold and \
            "SELECT distinct prca, prcc, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
            FROM pas left join da on da.da = pas.da" or \
            "SELECT capa.da as division, divname, prc, section, radical, exposant, bis, puissance, pe as proprietary, \
            adr1 as proprietary_city, adr2 as proprietary_street, sl1 as location \
            FROM map left join capa on map.capakey=capa.capakey left join da on capa.da = da.da "
        conditions = []
        division and conditions.append("%s.da= %s" % (browseold and 'pas' or 'capa', division))
        (section or not fuzzy) and conditions.append("section %s" % (not section and 'is NULL' or "= '%s'" % section))
        (radical or not fuzzy) and conditions.append("radical = %s" % (radical and radical or '0'))
        (bis or not fuzzy) and conditions.append("bis = %s" % (bis and bis or '0'))
        (exposant or not fuzzy) and conditions.append("exposant %s" % (not exposant and 'is NULL' or "= '%s'" % exposant))
        (puissance or not fuzzy) and conditions.append("puissance = %s" % (puissance and puissance or '0'))
        if not browseold:
            prcowner and conditions.append("pe ILIKE '%%%s%%'" % prcowner)
            location and conditions.append("sl1 ILIKE '%%%s%%'" % location)
        if conditions:
            query_string = '%s WHERE %s' % (query_string, ' and '.join(conditions))
        records = self.queryDB(query_string)
        parcels = [ParcelHistoric(**r) for r in records]
        parcels = ParcelHistoric.mergeDuplicate(parcels)
        if historic:
            for i, parcel in enumerate(parcels):
                parcel.buildRelativesChain(self, 'parents')
                parcel.buildRelativesChain(self, 'childs')
        return parcels

    security.declarePublic('queryDB')
    def queryDB(self, query_string, connection_string=None):
        """
           Execute a query and return the result
        """
        self.dbc = self.getDBConnection(connection_string)
        result = []
        if type(self.dbc) == psycopg2._psycopg.connection:
            try:
                dict_cur = self.dbc.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
                dict_cur.execute(query_string + ';')
                for row in dict_cur.fetchall():
                    result = result + [dict(row)]
            except psycopg2.ProgrammingError:
                result = []
                pass
            self.dbc.close()
            delattr(self, 'dbc')
        else:
            ptool = getToolByName(self, "plone_utils")
            ptool.addPortalMessage(_(u"db_connection_error", mapping={u'error': self.dbc}), type="error")
        return result

    def checkDBConnection(self):
        """
           Check if the provided parameters are OK
        """
        #build connection string
        ptool = getToolByName(self, "plone_utils")
        try:
            psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.getSqlName(), self.getSqlUser(), self.getSqlHost(), self.getSqlPassword()))
            ptool.addPortalMessage(_(u"db_connection_successfull"), type='info')
        except psycopg2.OperationalError, e:
            ptool.addPortalMessage(_(u"db_connection_error", mapping={u'error': unicode(e.__str__(), 'utf-8')}), type='error')

    security.declarePublic('mayAccessUrban')
    def mayAccessUrban(self):
        """
          Test if the currently logged in user can access the application
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        sm = getSecurityManager()

        #we could access this method with a script with a Manager proxy role so
        #check that the current user is not an Anonymous user too...
        if sm.checkPermission('View', getattr(portal, 'urban')) and portal.portal_membership.getAuthenticatedMember().getId():
            return True
        else:
            return False

    security.declarePublic('createPortionOut')
    def createPortionOut(self, container, division, section, radical, bis, exposant, puissance, partie, outdated=False):
        """
           Create the PortionOut with given parameters...
        """
        if bis == '0':
            bis = ''
        if len(bis) == 1:
            bis = '0' + bis
        if puissance == '0':
            puissance = ''
        newParcelId = container.invokeFactory("PortionOut", id=self.generateUniqueId('PortionOut'), divisionCode=division,
                                              division=division, section=section, radical=radical, bis=bis, exposant=exposant,
                                              puissance=puissance, partie=partie, outdated=outdated)
        newParcel = getattr(container, newParcelId)
        newParcel._renameAfterCreation()
        newParcel.at_post_create_script()
        self.REQUEST.RESPONSE.redirect(container.absolute_url() + '/view')

    security.declarePublic('getParcelsFromTopic')
    def getParcelsFromTopic(self, topicName):
        """
        """
        try:
            topic = getattr(self.topics, topicName)
        except AttributeError:
            return None

        parcels = []
        for topicItem in topic.queryCatalog():
            topicItemObj = topicItem.getObject()
            if topicItemObj.meta_type == 'BuildLicence':
                for licenceParcel in topicItemObj.getParcels():
                    parcels.append(licenceParcel)
            elif topicItemObj.meta_type == 'PortionOut':
                parcels.append(topicItemObj)
        return parcels

    security.declarePublic('WfsProxy')
    def WfsProxy(self):
        """
           Proxy for WFS query
        """
        import urllib2
        import cgi
        method = self.REQUEST["REQUEST_METHOD"]
        #allowedHosts = ['10.211.55.10: 8080']
        allowedHosts = self.getWebServerHost()

        if method == "POST":
            qs = self.REQUEST["QUERY_STRING"]
            d = cgi.parse_qs(qs)
            if "url" in d:
                url = d["url"][0]
            else:
                self.REQUEST.RESPONSE.setHeader('Content-Type', "text/plain")
                return "Illegal request."
        else:
            fs = cgi.FieldStorage()
            url = fs.getvalue('url', "http: //www.urban%s.com" % self.getNISNum())

        try:
            host = url.split("/")[2]
            if allowedHosts and not host in allowedHosts:
                print "Status: 502 Bad Gateway"
                print "Content-Type: text/plain"
                print
                print "This proxy does not allow you to access that location (%s)." % (host, )
                print

            elif url.startswith("http: //") or url.startswith("https: //"):
                if method == "POST":
                    #length = int(self.REQUEST["CONTENT_LENGTH"])
                    headers = {"Content-Type": self.REQUEST["CONTENT_TYPE"]}
                    body = self.REQUEST["BODY"]

                    r = urllib2.Request(url, body, headers)
                    y = urllib2.urlopen(r, timeout=3)
                else:
                    y = urllib2.urlopen(url, timeout=3)

                # print content type header
                i = y.info()
                if "Content-Type" in i:
                    self.REQUEST.RESPONSE.setHeader('Content-Type', i["Content-Type"])
                else:
                    self.REQUEST.RESPONSE.setHeader('Content-Type', "text/plain")

                data = y.read()

                y.close()
                return data
            else:
                self.REQUEST.RESPONSE.setHeader('Content-Type', "text/plain")
                return "Illegal request."

        except Exception, E:
            self.REQUEST.RESPONSE.setHeader('Content-Type', "text/plain")
            return "Some unexpected error occurred. Error text was: ", E

    security.declarePublic('GetListOfCapaKeyBuffer')
    def GetListOfCapaKeyBuffer(self, parcelleKey, bufferWidth=50):
        """
             Get List of Capakey around a parcell (ex: 92088C0335/00D000)
        """
        qry = """SELECT capakey
                FROM capa
                WHERE st_intersects(
                   capa.the_geom,
                   (
                   SELECT ST_BUFFER(sample.the_geom, %s)
                   FROM (
                        SELECT * FROM CAPA
                        WHERE capa.capakey LIKE '%s'
                        ) AS sample
                   )
                )""" % (bufferWidth, parcelleKey)

        try:
            results = self.queryDB(qry)
        except:
            results = []
        idlist = []
        for res in results:
            idlist.append("capakey='" + res["capakey"] + "'")
        return " OR ".join(idlist)

    security.declarePublic('GetWKTGeomOfBufferParcel')
    def GetWKTGeomOfBufferParcel(self, parcelleKey, bufferWidth=50):
        """
            Get the Geom (in WKT) of the the buffer (ex: 92088C0335/00D000)
        """
        qry = "SELECT astext(ST_BUFFER(the_geom, %s)) AS geom FROM capa WHERE capakey LIKE '%s'" % (bufferWidth, parcelleKey)
        try:
            results = self.queryDB(qry)
        except:
            results = ""

        if(len(results) == 1):
            return results[0]['geom']
        else:
            return ""

    security.declarePublic('getPortletTopics')
    def getPortletTopics(self, context):
        """
          Return a list of topics to display in the portlet
        """
        topics = self.getUrbanConfig(context).topics.objectValues('ATTopic')
        res = []
        for topic in topics:
            res.append(topic)

        return res

    security.declarePublic('getUrbanConfig')
    def getUrbanConfig(self, context, urbanConfigId=None):
        """
          Return the folder containing the necessary paramaters
        """
        #if we received a context, either it is a urban meta_class and we get his portal_type
        #or it is a folder of the urban hierarchy and we use the 'urbanConfigId' property registered
        #on each 'application by type of licence' folder

        #we did not receive anything, we return None...
        if context is None and not urbanConfigId:
            return None
        if urbanConfigId:
            #we received a urbanConfigId...
            pass
        elif not context.getPortalTypeName() in URBAN_TYPES:
            #if the portal_type of the context is not a Licence, we try to
            #get the 'urbanConfigId' property on parents...
            for level in context.absolute_url_path().split('/'):
                if context.hasProperty('urbanConfigId'):
                    urbanConfigId = context.getProperty('urbanConfigId')
                    break
                context = context.getParentNode()
            #if no urbanConfigId was found, we return None...
            if not urbanConfigId:
                return None
        else:
            #we just pick the portal_type of the context...
            urbanConfigId = context.getPortalTypeName()

        #the id of an urbanConfig is the same as the portal_type name of the context in lowercase
        #be sure we have lowercase
        urbanConfigId = urbanConfigId.lower()
        try:
            urbanConfig = getattr(self, urbanConfigId)
            return urbanConfig
        except AttributeError:
            return None

    def generatePrintMap(self, cqlquery, cqlquery2, zoneExtent=None):
        """
        """
        bound_names = {}
        args = {}
        kw = {}
        bound_names['tool'] = self
        bound_names['zoneExtent'] = zoneExtent
        bound_names['cqlquery'] = cqlquery
        bound_names['cqlquery2'] = cqlquery2
        return self.printmap._exec(bound_names=bound_names, args=args, kw=kw)

    def generateMapJS(self, context, cqlquery, cqlquery2, parcelBufferGeom='', zoneExtent=None):
        """
          Return a generated JS file based on the cql query
        """
        #if we do not have a display zone, we return the default mapExtent
        if not zoneExtent:
            zoneExtent = self.getMapExtent()
        bound_names = {}
        args = {}
        kw = {}
        bound_names['tool'] = self
        bound_names['context'] = context
        bound_names['zoneExtent'] = zoneExtent
        bound_names['cqlquery'] = cqlquery
        bound_names['cqlquery2'] = cqlquery2
        bound_names['parcelBufferGeom'] = parcelBufferGeom

        return self.simplemapjs_gen._exec(bound_names=bound_names, args=args, kw=kw)

    security.declarePublic('generateUrbainXML')
    def generateUrbainXML(self, datefrom, dateto, list_only):

        def reverseDate(date):
            split = date.split('/')
            for i in range(len(split)):
                if len(split[i]) == 1:
                    split[i] = '0%s' % split[i]
            split.reverse()
            return '/'.join(split)

        def check(condition, error_message):
            if not condition:
                error.append(error_message)
            return condition

        datefrom = reverseDate(datefrom)
        dateto = reverseDate(dateto)
        catalog = getToolByName(self, 'portal_catalog')
        pw = getToolByName(self, 'portal_workflow')
        results = catalog.searchResults(
            getDecisionDate={'query': (DateTime(datefrom), DateTime(dateto)), 'range': 'minmax'},
            object_provides='Products.urban.interfaces.ITheLicenceEvent',
            portal_type='UrbanEvent'
        )
        results = [brain.getObject() for brain in results if brain.getObject().aq_parent.portal_type in ['BuildLicence', ]]
        xml = []
        error = []
        html_list = []
        xml.append('<?xml version="1.0" encoding="iso-8859-1"?>')
        xml.append('<dataroot>')
        xml.append('  <E_220_herkomst>')
        xml.append('    <E_220_NIS_Gem>%s</E_220_NIS_Gem>' % self.getNISNum())
        xml.append('    <E_220_Periode_van>%s</E_220_Periode_van>' % datefrom.replace("/", ""))
        xml.append('    <E_220_Periode_tot>%s</E_220_Periode_tot>' % dateto.replace("/", ""))
        xml.append('    <E_220_ICT>COM</E_220_ICT>')
        xml.append('  </E_220_herkomst>')
        html_list.append('<HTML><TABLE>')
        for eventObj in results:
            licenceObj = eventObj.getParentNode()
            applicantObj = licenceObj.getApplicants() and licenceObj.getApplicants()[0] or None
            architects = licenceObj.getField('architects') and licenceObj.getArchitects() or []
            if pw.getInfoFor(licenceObj, 'review_state') == 'accepted':
                html_list.append(
                    '<TR><TD>%s  %s</TD><TD>%s</TD></TR>'
                    % (str(licenceObj.getReference()), licenceObj.title.encode('iso-8859-1'),
                    str(eventObj.getDecisionDate()))
                )
                xml.append('  <Item220>')
                xml.append('      <E_220_Ref_Toel>%s</E_220_Ref_Toel>' % str(licenceObj.getReference()))
                parcels = licenceObj.getParcels()
                if check(parcels, 'no parcels found on licence %s' % str(licenceObj.getReference())):
                    xml.append('      <Doc_Afd>%s</Doc_Afd>' % parcels[0].getDivisionCode())
                street = number = None
                if licenceObj.getWorkLocations():
                    number = licenceObj.getWorkLocations()[0]['number']
                    street = catalog.searchResults(UID=licenceObj.getWorkLocations()[0]['street'])
                if check(street, 'no street found on licence %s' % str(licenceObj.getReference())):
                    street = street[0].getObject()
                    xml.append('      <E_220_straatcode>%s</E_220_straatcode>' % str(street.getStreetCode()))
                    xml.append('      <E_220_straatnaam>%s</E_220_straatnaam>' % str(street.getStreetName()).decode('iso-8859-1').encode('iso-8859-1'))
                if number:
                    xml.append('      <E_220_huisnr>%s</E_220_huisnr>' % number)
                worktype = licenceObj.getWorkType() and licenceObj.getWorkType()[0] or ''
                work_types = UrbanVocabulary('folderbuildworktypes').getAllVocTerms(licenceObj)
                worktype_map = {}
                for k, v in work_types.iteritems():
                    worktype_map[k] = v.getExtraValue()
                xml_worktype = ''
                if check(worktype in worktype_map.keys(), 'unknown worktype %s on licence %s' % (worktype, str(licenceObj.getReference()))):
                    xml_worktype = worktype_map[worktype]
                xml.append('      <E_220_Typ>%s</E_220_Typ>' % xml_worktype)
                xml.append('      <E_220_Werk>%s</E_220_Werk>' % licenceObj.licenceSubject.encode('iso-8859-1'))
                strDecisionDate = str(eventObj.getDecisionDate())
                xml.append('      <E_220_Datum_Verg>%s%s%s</E_220_Datum_Verg>' % (strDecisionDate[0: 4], strDecisionDate[5: 7], strDecisionDate[8: 10]))
                xml.append('      <E_220_Instan>COM</E_220_Instan>')
                xml.append('      <PERSOON>')
                xml.append('        <naam>%s %s</naam>' % (applicantObj.getName1().decode('iso-8859-1').encode('iso-8859-1'), applicantObj.getName2().decode('iso-8859-1').encode('iso-8859-1')))
                xml.append('        <straatnaam>%s</straatnaam>' % applicantObj.getStreet().decode('iso-8859-1').encode('iso-8859-1'))
                xml.append('        <huisnr>%s</huisnr>' % applicantObj.getNumber())
                xml.append('        <postcode>%s</postcode>' % applicantObj.getZipcode())
                xml.append('        <gemeente>%s</gemeente>' % applicantObj.getCity().decode('iso-8859-1').encode('iso-8859-1'))
                xml.append('        <hoedanig>DEMANDEUR</hoedanig>')
                xml.append('      </PERSOON>')
                if architects:
                    architectObj = architects[0]
                    list_architects_terms = ["NON REQUIS", "lui-meme", "Eux-memes", "elle-meme", "lui-meme", "lui-même", "lui-meme ", "Lui-meme", "A COMPLETER "]
                    if architectObj.getName1() in list_architects_terms:
                        xml.append('      <PERSOON>')
                        xml.append('        <naam>%s %s</naam>'
                                   % (applicantObj.getName1().encode('iso-8859-1'), applicantObj.name2.encode('iso-8859-1')))
                        xml.append('        <straatnaam>%s</straatnaam>' % applicantObj.getStreet().encode('iso-8859-1'))
                        xml.append('        <huisnr>%s</huisnr>' % applicantObj.getNumber())
                        xml.append('        <postcode>%s</postcode>' % applicantObj.getZipcode())
                        xml.append('        <gemeente>%s</gemeente>' % applicantObj.getCity().encode('iso-8859-1'))
                        xml.append('        <hoedanig>ARCHITECTE</hoedanig>')
                        xml.append('      </PERSOON>')
                    else:
                        xml.append('      <PERSOON>')
                        xml.append('        <naam>%s %s</naam>'
                                   % (architectObj.getName1().decode('iso-8859-1').encode('iso-8859-1'), architectObj.getName2().decode('iso-8859-1').encode('iso-8859-1')))
                        xml.append('        <straatnaam>%s</straatnaam>' % architectObj.getStreet().decode('iso-8859-1').encode('iso-8859-1'))
                        xml.append('        <huisnr>%s</huisnr>' % architectObj.getNumber())
                        xml.append('        <postcode>%s</postcode>' % architectObj.getZipcode())
                        xml.append('        <gemeente>%s</gemeente>' % architectObj.getCity().decode('iso-8859-1').encode('iso-8859-1'))
                        xml.append('        <hoedanig>ARCHITECTE</hoedanig>')
                        xml.append('      </PERSOON>')
                for prc in parcels:
                    xml.append('      <PERCELEN>')
                    try:
                        strRadical = '%04d' % float(prc.getRadical())
                    except:
                        strRadical = '0000'
                    try:
                        strPuissance = '%03d' % float(prc.getPuissance())
                    except:
                        strPuissance = '000'
                    try:
                        strBis = '%02d' % float(prc.getBis())
                    except:
                        strBis = '00'
                    xml.append('        <E_220_percid>%s_%s_%s_%s_%s_%s</E_220_percid>'
                               % (prc.getDivisionCode(), prc.getSection(), strRadical, prc.getExposant(), strPuissance, strBis))
                    xml.append('        <kadgemnr>%s</kadgemnr>' % prc.getDivisionCode())
                    xml.append('        <sectie>%s</sectie>' % prc.getSection())
                    xml.append('        <grondnr>%s</grondnr>' % prc.getRadical())
                    if prc.getExposant() != '':
                        xml.append('        <exponent>%s</exponent>' % prc.getExposant())
                    if prc.getPuissance() != '':
                        xml.append('        <macht>%s</macht>' % prc.getPuissance())
                    if prc.getBis() != '':
                        xml.append('        <bisnr>%s</bisnr>' % prc.getBis())
                    xml.append('      </PERCELEN>')
                xml.append('  </Item220>')
        html_list.append('</TABLE></HTML>')
        xml.append('</dataroot>')
        if list_only:
            output = StringIO()
            output.write(unicode('\n'.join(html_list).replace("&", "&amp;"), 'iso-8859-1').encode('iso-8859-1'))
            return output.getvalue()
        else:
            if error != []:
                return 'Error in these licences: \n%s' % '\n'.join(error)
            else:
                output = StringIO()
                output.write(unicode('\n'.join(xml).replace("&", "&amp;"), 'iso-8859-1').encode('iso-8859-1'))
                return output.getvalue()

    security.declarePublic('getReferenceBrowserSearchAtObj')
    def getReferenceBrowserSearchAtObj(self, at_url):
        """
          Used for referencebrowser_popup overrided in urban
        """
        if not at_url:
            #we are not on an object, use the GenericLicence
            from Products.urban import WorkLocation
            return WorkLocation.WorkLocation_schema
        else:
            return self.restrictedTraverse(at_url)

    security.declarePublic('getReferenceBrowserSearchAtField')
    def getReferenceBrowserSearchAtField(self, at_obj, fieldRealName):
        """
          Used for referencebrowser_popup overrided in urban
        """
        if at_obj.__module__ == "Products.Archetypes.Schema":
            #we have a schema here
            return at_obj[fieldRealName]
        else:
            return at_obj.Schema()[fieldRealName]

    security.declarePublic('generateReference')
    def generateReference(self, obj, **kwargs):
        """
         Generates a reference based on the numerotationTALExpression
        """
        #we get a field like UrbanCertificateBaseNumerotation on self
        #to get the last numerotation for this kind of licence
        licence_config = self.getUrbanConfig(obj)
        if not licence_config:
            return ''
        lastValue = '0'
        #get the last value
        lastValue = licence_config.getNumerotation()
        if str(lastValue).isdigit():
            lastValue = int(lastValue)
            lastValue = lastValue + 1

        #evaluate the numerotationTALExpression and pass it obj, lastValue and self
        data = {
            'obj': obj,
            'tool': self,
            'numerotation': str(lastValue),
            'portal': self.aq_inner.aq_parent,
            'date': DateTime(),
        }
        data.update(kwargs)
        res = ''
        try:
            ctx = getEngine().getContext(data)
            res = Expression(licence_config.getReferenceTALExpression())(ctx)
        except Exception:
            logger.warn('The defined TAL expression about numerotation in portal_urban is wrong!')
        return res

    security.declarePublic('listEventTypes')
    def listEventTypes(self, context, urbanConfigId):
        """
          Returns the eventTypes of an urbanConfigProxy
        """
        urbanConfig = self.getUrbanConfig(context=None, urbanConfigId=urbanConfigId)
        cat = getToolByName(self, 'portal_catalog')
        path = '/'.join(urbanConfig.getPhysicalPath())
        brains = cat(path=path, sort_on='getObjPositionInParent', meta_type=['UrbanEventType', 'OpinionRequestEventType'], review_state="enabled")
        res = []
        #now evaluate the TAL condition for every brain
        for brain in brains:
            event_type = brain.getObject()
            if event_type.canBeCreatedInLicence(context):
                res.append(brain)
        return res

    security.declarePublic('initMap')
    def initMap(self, obj):
        """
          Initialize the map on element
        """
        zoneExtent = None
        parcels = obj.getParcels()
        cqlquery = ''
        if parcels:
            #if we have parcels, display them on a map...
            #generate the 'selectedpo' layer filter based on contained parcels
            for parcel in parcels:
                if cqlquery != '':
                    cqlquery = cqlquery + " or "
                cqlquery = cqlquery + "(section='" + parcel.getSection() + "' and radical=" + parcel.getRadical()
                if parcel.getBis() != '':
                    cqlquery = cqlquery + " and bis=" + parcel.getBis()
                if parcel.getExposant() != '':
                    cqlquery = cqlquery + " and exposant='" + parcel.getExposant() + "'"
                else:
                    cqlquery = cqlquery + " and exposant is NULL"
                if parcel.getPuissance() != '':
                    cqlquery = cqlquery + " and puissance=" + parcel.getPuissance()
                else:
                    cqlquery = cqlquery + " and puissance=0"
                cqlquery = cqlquery + ")"
            cqlquery = '((da = ' + parcel.getDivisionCode() + ') and (' + cqlquery + '))'
            #calculate the zone to display
            strsql = 'SELECT Xmin(selectedpos.extent), Ymin(selectedpos.extent), Xmax(selectedpos.extent), Ymax(selectedpos.extent) FROM (SELECT Extent(the_geom) FROM capa WHERE ' + cqlquery + ') AS selectedpos'
            result = self.queryDB(query_string=strsql)[0]
            try:
                zoneExtent = "%s, %s, %s, %s" % (result['xmin'], result['ymin'], result['xmax'], result['ymax'])
            except:
                zoneExtent = ""

        #return the generated JS code
        return self.generateMapJS(self, cqlquery, '', '', zoneExtent)

    security.declarePublic('generateStatsINS')
    def generateStatsINS(self, datefrom, dateto):
        """
        """
        if (len(datefrom) != 10) or (len(dateto) != 10):
            return 'Date incorrecte'
        datesplited = datefrom.split('/')
        datefrom = datesplited[2] + '/' + datesplited[1] + '/' + datesplited[0]
        datesplited = dateto.split('/')
        dateto = datesplited[2] + '/' + datesplited[1] + '/' + datesplited[0]
        global_templates = getattr(self, 'globaltemplates')
        templateObj = getattr(global_templates, 'statsins.odt')
        catalog = getToolByName(self, 'portal_catalog')
        results = catalog.searchResults(getBeginDate={'query': (DateTime(datefrom), DateTime(dateto)), 'range': 'minmax'}, id='debut-des-travaux', portal_type='UrbanEvent')
        folders = []
        for result in results:
            objResult = result.getObject()
            folderobj = objResult.aq_inner.aq_parent
            if folderobj.getUsage() != 'not_applicable':
                folders.append(folderobj)
        tempFileName = '%s/%s_%f.%s' % (getOsTempFolder(), 'statsins', time.time(), '.odt')
        renderer = appy.pod.renderer.Renderer(StringIO(templateObj), {'self': self, 'folders': folders}, tempFileName)
        renderer.run()
        response = self.REQUEST.RESPONSE
        response.setHeader('Content-Type', 'applications/odt')
        response.setHeader('Content-Disposition', 'inline;filename="statsins.odt"')
        f = open(tempFileName, 'rb')
        res = f.read()
        f.close()
        os.remove(tempFileName)
        return res

    security.declarePublic('decorateHTML')
    def decorateHTML(self, classname, htmlcode):
        """
          This method will decorate a chunk of HTML code with a particular class
          so it can be displayed in different ways in the POD templates
        """
        htmlcode = htmlcode.strip()
        #replace <span by <span class=classname and <p by <p class=classname
        htmlcode = htmlcode.replace("<span", "<span class='%s'" % classname)
        htmlcode = htmlcode.replace("<p", "<p class='%s'" % classname)
        return htmlcode

    security.declarePublic('getEventByEventTypeId')
    def getEventByEventTypeId(self, obj, eventId):
        """
          Return an event corresponding to the passed id
          The passed id is the eventType id the event is linked to
          If more than one event is linked to to same eventType, the last
          created event is returned
        """
        rightEvent = None
        #we keep the newest element if several exist
        lastDate = DateTime('1901/01/01')
        for event in obj.objectValues('UrbanEvent'):
            if event.getUrbaneventtypes().id == eventId:
                if event.getEventDate() > lastDate:
                    lastDate = event.getEventDate()
                    rightEvent = event
                elif rightEvent is None:
                    rightEvent = event
        return rightEvent

    security.declarePublic('validate_unoEnabledPython')
    def validate_unoEnabledPython(self, value):
        """
          Validate the entered uno enabled python path
        """
        import os
        _PY = 'Please specify a file corresponding to a Python interpreter ' \
              '(ie "/usr/bin/python").'
        FILE_NOT_FOUND = 'Path "%s" was not found.'
        VALUE_NOT_FILE = 'Path "%s" is not a file. ' + _PY
        NO_PYTHON = "Name '%s' does not starts with 'python'. " + _PY
        NOT_UNO_ENABLED_PYTHON = '"%s" is not a UNO-enabled Python interpreter. ' \
                                 'To check if a Python interpreter is UNO-enabled, ' \
                                 'launch it and type "import uno". If you have no ' \
                                 'ImportError exception it is ok.'
        if value:
            if not os.path.exists(value):
                return FILE_NOT_FOUND % value
            if not os.path.isfile(value):
                return VALUE_NOT_FILE % value
            if not os.path.basename(value).startswith('python'):
                return NO_PYTHON % value
            if os.system('%s -c "import uno"' % value):
                return NOT_UNO_ENABLED_PYTHON % value
        return

    security.declarePublic('incrementNumerotation')
    def incrementNumerotation(self, obj):
        """
          Increment the numerotation linked to the type of licence 'obj'
          The numerotation in the configuration is a string that contains an integer
        """
        #update the last reference in the configuration
        config = self.getUrbanConfig(obj)
        value = config.getNumerotation()
        if not str(value).isdigit():
            value = '0'
        else:
            value = int(value)
            value = value + 1
        #set the new value
        config.setNumerotation(value)
        self.reindexObject()

    security.declarePublic('getCurrentFolderManager')
    def getCurrentFolderManager(self, initials=True):
        """
          Returns the current FolderManager initials or object
        """
        #the current FolderManager is based on the current Plone User and the
        #ploneUserId defined on the folderManagers for the 'obj' kind of licence
        folderManagersFolder = self.foldermanagers
        pm = getToolByName(self, 'portal_membership')
        currentPloneUserId = pm.getAuthenticatedMember().getId()
        for fm in folderManagersFolder.objectValues('FolderManager'):
            if fm.getPloneUserId() == currentPloneUserId:
                if initials:
                    return fm.getInitials()
                else:
                    return fm
        #if we are here, the current user is using the application without being
        #a foldermanager, like 'admin' for example
        if initials:
            return ''
        return None

    security.declarePublic('getCityName')
    def getCityName(self, prefixed=False):
        """
          Overrides the default getCityName to take a special parameter into account
          'prefixed' will manage the fact that we return de Sambreville or d'Engis
        """
        cityName = self.getField('cityName').get(self)
        if not prefixed:
            return cityName
        else:
            prefix = 'de '
            vowels = ('a', 'e', 'i', 'o', 'u', 'y', )
            for v in vowels:
                if cityName.lower().startswith(v):
                    prefix = "d'"
                    break
            return prefix + cityName

    security.declarePublic('formatDate')
    def formatDate(self, date, translatemonth=True, long_format=False):
        """
          Format the date for printing in pod templates
        """
        if date:
            if not translatemonth:
                return ulocalized_time(date, long_format=long_format, context=self, request=self.REQUEST).encode('utf8')
            else:
                #we need to translate the month and maybe the day (1er)
                year, month, day, hour = str(date.strftime('%Y/%m/%d/%Hh%M')).split('/')
                #special case when the day need to be translated
                #for example in french '1' becomes '1er' but in english, '1' becomes '1st'
                #if no translation is available, then we use the default where me remove foregoing '0'
                #'09' becomes '9', ...
                daymsgid = "date_day_%s" % day
                translatedDay = translate(daymsgid, 'urban', context=self.REQUEST, default=day.lstrip('0')).encode('utf8')
                #translate the month
                #msgids already exist in the 'plonelocales' domain
                monthMappings = {
                    '01': 'jan',
                    '02': 'feb',
                    '03': 'mar',
                    '04': 'apr',
                    '05': 'may',
                    '06': 'jun',
                    '07': 'jul',
                    '08': 'aug',
                    '09': 'sep',
                    '10': 'oct',
                    '11': 'nov',
                    '12': 'dec',
                }
                monthmsgid = "month_%s" % monthMappings[month]
                translatedMonth = translate(monthmsgid, 'plonelocales', context=self.REQUEST).encode('utf8').lower()
            if long_format:
                at_hour = translate('at_hour', 'urban', mapping={'hour': hour}, context=self.REQUEST).encode('utf-8')
                return "%s %s %s %s" % (translatedDay, translatedMonth, year, at_hour)
            else:
                return "%s %s %s" % (translatedDay, translatedMonth, year)
        return ''

    security.declarePublic('queryCatalog')
    def queryCatalog(self, batch, context, specificSearch, theObjects=False, batchlen=20, **kwargs):
        """
          This method is used in the templates to display content in listing tables
          If some kwargs are received, they will update the defined querystring of the specificSearch
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        if specificSearch == 'searchUrbanEvents':
            #search the existing urbanEvents
            queryString = {'object_provides': 'Products.urban.interfaces.IUrbanEvent',
                           'path': '/'.join(context.getPhysicalPath()),
                           'sort_on': 'getObjPositionInParent',
                           'sort_order': 'reverse', }
        elif specificSearch == 'searchPortionOuts':
            #search the existing parcels
            #we can search existing parcels on a licence (directly contained)
            if context.portal_type in URBAN_TYPES:
                depth = 1
            #or on an UrbanEventInquiry where parcels are contained in RecipientCadastre
            else:
                depth = 2
            queryString = {'portal_type': 'PortionOut',
                           'path': {'query': '/'.join(context.getPhysicalPath()), 'depth': depth},
                           'sort_on': 'getObjPositionInParent'}
        elif specificSearch == 'searchClaimants':
            #search the existing claimants
            queryString = {'portal_type': 'Claimant',
                           'path': '/'.join(context.getPhysicalPath()),
                           'sort_on': 'getObjPositionInParent'}
        elif specificSearch == 'searchRecipients':
            #search the existing recipients
            queryString = {'portal_type': 'RecipientCadastre',
                           'path': '/'.join(context.getPhysicalPath()),
                           'sort_on': 'getObjPositionInParent'}
        elif specificSearch == 'searchLinkedDocuments':
            #search the existing recipients
            queryString = {'portal_type': 'UrbanDoc',
                           'path': '/'.join(context.getPhysicalPath()),
                           'sort_on': 'created'}
        elif specificSearch == 'searchLinkedAnnexes':
            #search the existing recipients
            queryString = {'portal_type': 'File',
                           'path': '/'.join(context.getPhysicalPath()),
                           'sort_on': 'created'}

        #update queryString with given kwargs
        queryString.update(kwargs)
        res = portal_catalog(queryString)
        if theObjects:
            objs = []
            for brain in res:
                objs.append(brain.getObject())
            res = objs
        if batch:
            b_start = self.REQUEST.get('b_start', 0)
            batch = Batch(res, batchlen, int(b_start), orphan=0)
            return batch
        else:
            return res

    security.declarePublic('getTextToShow')
    def getTextToShow(self, context, fieldName):
        """
          This method manage long texts and returns a subset of the text if needed
        """
        #the max text length to show, in number of characters
        maxLength = 50

        def checkMaxLength(text):
            '''Check if we need to format the text if it is too long.'''
            utext = unicode(text, 'utf-8')
            isTooLarge = False
            if maxLength and len(utext) > maxLength:
                isTooLarge = True
                return isTooLarge, utext[: maxLength].encode('utf-8') + '...'
            return isTooLarge, utext.encode('utf-8')
        #to be sure that we only have text (usefull for HTML) we get the raw value
        return checkMaxLength(getattr(context, 'getRaw' + fieldName[0].capitalize() + fieldName[1:])())

    security.declarePublic('getUrbanTypes')
    def getUrbanTypes(self):
        """
          Returns the config.URBAN_TYPES so it can be used in templates and conditions
        """
        return URBAN_TYPES

    security.declarePublic('renderText')
    def renderText(self, text, context, renderToNull=False):
        """
          Return the description rendered if it contains elements to render
          An element to render will be place between [[]]
          So we could have something like :
          "Some sample text [[python: object.getSpecialAttribute()]] and some text
          [[object/myTalExpression]] end of the text"
          If renderToNull is True, the found expressions will not be rendered but
          replaced by the nullValue defined below
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        renderedDescription = text
        for expr in re.finditer('\[\[(.*?)\]\]', text):
            if not renderToNull:
                ctx = createExprContext(context.getParentNode(), portal, context)
                try:
                    #expr.groups()[0] is the expr without the [[]]
                    res = Expression(expr.groups()[0])(ctx)
                except Exception, e:
                    logger.warn("The expression '%s' defined in the UrbanVocabularyTerm at '%s' is wrong! Returned error message is : %s" % (expr.group(), self.absolute_url(), e))
                    res = translate('error_in_expr_contact_admin', 'urban', mapping={'expr': expr.group()}, context=self.REQUEST)
                #replace the expression in the description by the result
                #re work with utf8, not with unicode...
                if isinstance(res, unicode):
                    res = res.encode('utf8')
            else:
                res = NULL_VALUE
            if type(res) == tuple:
                res = res[0]
            if type(res) == unicode:
                res = res.encode()
            renderedDescription = re.sub(re.escape(expr.group()), res, renderedDescription)
        return renderedDescription

    security.declarePublic('isScheduleAvailable')
    def isScheduleAvailable(self, context):
        try:
            context.restrictedTraverse('@@schedule')
        except AttributeError:
            return False
        #the schedule is available at the root of the application, any licence folder and any licence
        if context.getLayout() == 'urban_view' or context.getProperty('urbanConfigId') or context.portal_type in URBAN_TYPES:
            return True
        return False

    def isContactFolder(self, folder):
        return IContactFolder.providedBy(folder)

    def _pylonsHostChange(method, self):
        return self.getPylonsHost()

    security.declarePublic('getStaticPylonsHost')
    def getStaticPylonsHost(self):
        """
          Returns the domain name of the pylonsHost attribute
        """
        #res = urlparse(self.getPylonsHost()) #getPylonsHost doesn't contain a valid url beginning with http
        #return '%s: //%s'%(res.scheme, res.netloc)
        return '/'.join(self.getPylonsHost().split('/')[:3])  # don't use os.path!

    security.declarePublic('getParcelInfos')


registerType(UrbanTool, PROJECTNAME)
# end of class UrbanTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer

