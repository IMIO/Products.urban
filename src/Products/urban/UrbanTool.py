# -*- coding: utf-8 -*-
#
# File: UrbanTool.py
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

from persistent.mapping import PersistentMapping

from Products.Archetypes.atapi import *

from Products.CMFCore.utils import UniqueObject
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from Products.urban.config import *

from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory

import interfaces


##code-section module-header #fill in your manual code here
import logging
logger = logging.getLogger('urban: UrbanTool')
import re
from AccessControl import getSecurityManager
from plone import api
from zope.i18n import translate
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.PageTemplates.Expressions import getEngine
from Products.DataGridField.DataGridField import FixedRow
from Products.DataGridField.FixedColumn import FixedColumn
from Products.urban.utils import getCurrentFolderManager
from Products.urban.config import GENERATED_DOCUMENT_FORMATS
from Products.urban.interfaces import IUrbanVocabularyTerm, IContactFolder
from Products.urban.cartography import config as carto_config
from Products.urban import services

from datetime import date as _date

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
        name='mapUrl',
        widget=StringField._properties['widget'](
            description="Enter the url of the geonode map",
            description_msgid="urban_descr_mapUrl",
            label='Map Url',
            label_msgid='urban_label_mapUrl',
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


UrbanTool_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

for f in UrbanTool_schema.filterFields(schemata='default'):
    f.widget.visible = {"edit": "invisible"}
for f in UrbanTool_schema.filterFields(schemata='metadata'):
    f.widget.visible = {"edit": "invisible"}


class UrbanTool(UniqueObject, OrderedBaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanTool)

    meta_type = 'UrbanTool'
    _at_rename_after_creation = True

    schema = UrbanTool_schema

    def __init__(self, id=None):
        OrderedBaseFolder.__init__(self, 'portal_urban')
        self.setTitle('Urban configuration')

    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()

    security.declarePublic('getDivisionsConfigRows')
    def getDivisionsConfigRows(self):
        """
        """
        rows = []
        if not services.cadastre.can_connect():
            return rows

        cadastre = services.cadastre.new_session()
        for division in cadastre.get_all_divisions():
            division_id = str(division[0])
            name = division[1]
            row = FixedRow(
                keyColumn='division',
                initialData={
                    'division': division_id,
                    'name': name,
                    'alternative_name': name
                }
            )
            rows.append(row)
        cadastre.close()
        return rows

    security.declarePublic('getVocabularyDefaultValue')
    def getVocabularyDefaultValue(self, vocabulary, context, multivalued=False):
        """
         Return the first vocabulary term marked as default value of the vocabulary named vocabulary_name
        """
        empty_value = multivalued and [] or ''
        if isinstance(vocabulary, basestring):
            default_values = []
        else:
            #search in an urbanConfig or in the tool
            voc_terms = vocabulary.getAllVocTerms(context).values()
            default_values = [voc_term.id for voc_term in voc_terms
                              if voc_term.getIsDefaultValue()]
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

    security.declarePublic('contains')
    def contains(self, object_uid):
        """
        Tells if object with UID 'object_uid' is somewhere in portal_urban.
        """
        catalog = api.portal.get_tool('portal_catalog')
        path = '/'.join(self.getPhysicalPath())
        found = bool(len(catalog(UID=object_uid, path={'query': path})))
        return found

    security.declarePublic('createPortionOut')
    def createPortionOut(self, container, division, section='', radical='', bis='', exposant='', puissance='', partie='', outdated=False):
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
        allowedHosts = carto_config.geoserver.get('host')

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
                elif context.getPortalTypeName() in URBAN_TYPES:
                    urbanConfigId = context.getPortalTypeName()
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

    security.declarePublic('getCurrentFolderManagerInitials')
    def getCurrentFolderManagerInitials(self):
        """
          Returns the current FolderManager initials or object
        """
        foldermanager = getCurrentFolderManager()
        if foldermanager:
            return foldermanager.getInitials()
        return ''

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
    def formatDate(self, date=_date.today(), translatemonth=True, long_format=False):
        """
          Format the date for printing in pod templates
        """
        if date:
            if not translatemonth:
                if date.year() < 1900:
                    return '{}/{}/{}'.format(date.day(), date.month(), date.year())
                else:
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
        renderedDescription = text
        for expr in re.finditer('\[\[(.*?)\]\]', text):
            if not renderToNull:
                helper_view = context.aq_parent.restrictedTraverse('document_generation_helper_view')
                data = {
                    'self': helper_view.context,
                    'object': helper_view.real_context,
                    'event': context,
                    'context': helper_view.real_context,
                    'tool': self,
                    'portal': api.portal.getSite(),
                    'view': helper_view,
                }
                ctx = getEngine().getContext(data)
                try:
                    #expr.groups()[0] is the expr without the [[]]
                    python_expr = 'python: {}'.format(expr.groups()[0])
                    res = Expression(python_expr)(ctx)
                except Exception, e:
                    logger.warn("The expression '%s' defined in the UrbanVocabularyTerm at '%s' is wrong! Returned error message is : %s" % (expr.group(), self.absolute_url(), e))
                    res = translate('error_in_expr_contact_admin', 'urban', mapping={'expr': expr.group().decode('utf-8')}, context=self.REQUEST)
                #replace the expression in the description by the result
                #re work with utf8, not with unicode...
                if isinstance(res, unicode):
                    res = res.encode('utf8')
            else:
                res = NULL_VALUE
            if type(res) == tuple:
                res = res[0]
            if type(res) == unicode:
                res = res.encode('utf8')
            renderedDescription = re.sub(re.escape(expr.group()), res, renderedDescription)
        return renderedDescription

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


registerType(UrbanTool, PROJECTNAME)
