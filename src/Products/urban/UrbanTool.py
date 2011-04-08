# -*- coding: utf-8 -*-
#
# File: UrbanTool.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.5
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


from Products.CMFCore.utils import UniqueObject

    
##code-section module-header #fill in your manual code here
import logging
logger = logging.getLogger('urban: UrbanTool')
from DateTime import DateTime
from StringIO import StringIO
from Products.ZCTextIndex.ParseTree import ParseError
from Products.CMFPlone.i18nl10n import utranslate
from Products.CMFCore.utils import getToolByName
import appy.pod.renderer
import os, time
from StringIO import StringIO
from Products.urban.utils import *
from AccessControl import getSecurityManager
from Acquisition import aq_inner, aq_parent
import time
import psycopg2
import psycopg2.extras
from Products.PageTemplates.Expressions import getEngine
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.i18nl10n import ulocalized_time
from Products.PageTemplates.GlobalTranslationService import getGlobalTranslationService
service = getGlobalTranslationService()
_ = service.translate

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
    ),
    StringField(
        name='cityName',
        widget=StringField._properties['widget'](
            label='Cityname',
            label_msgid='urban_label_cityName',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='isDecentralized',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Isdecentralized',
            label_msgid='urban_label_isDecentralized',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='numerotationTALExpression',
        default="python: obj.getLicenceTypeAcronym() + '/' + date.strftime('%Y') + '/' + numerotation + '/' + tool.getCurrentFolderManager(obj, initials=True)",
        widget=StringField._properties['widget'](
            size=100,
            label='Numerotationtalexpression',
            label_msgid='urban_label_numerotationTALExpression',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='BuildLicenceNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Buildlicencenumerotation',
            label_msgid='urban_label_BuildLicenceNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='ParcelOutLicenceNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Parceloutlicencenumerotation',
            label_msgid='urban_label_ParcelOutLicenceNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='DeclarationNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Declarationnumerotation',
            label_msgid='urban_label_DeclarationNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='UrbanCertificateOneNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Urbancertificateonenumerotation',
            label_msgid='urban_label_UrbanCertificateOneNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='UrbanCertificateTwoNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Urbancertificatetwonumerotation',
            label_msgid='urban_label_UrbanCertificateTwoNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='NotaryLetterNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Notaryletternumerotation',
            label_msgid='urban_label_NotaryLetterNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='EnvironmentalDeclarationNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Environmentaldeclarationnumerotation',
            label_msgid='urban_label_EnvironmentalDeclarationNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='DivisionNumerotation',
        default=0,
        widget=StringField._properties['widget'](
            label='Divisionnumerotation',
            label_msgid='urban_label_DivisionNumerotation',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='sqlHost',
        widget=StringField._properties['widget'](
            label='Sqlhost',
            label_msgid='urban_label_sqlHost',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='sqlName',
        widget=StringField._properties['widget'](
            label='Sqlname',
            label_msgid='urban_label_sqlName',
            i18n_domain='urban',
        ),
        required=True,
    ),
    StringField(
        name='sqlUser',
        widget=StringField._properties['widget'](
            label='Sqluser',
            label_msgid='urban_label_sqlUser',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='sqlPassword',
        widget=PasswordWidget(
            label='Sqlpassword',
            label_msgid='urban_label_sqlPassword',
            i18n_domain='urban',
        ),
    ),
    StringField(
        name='webServerHost',
        widget=StringField._properties['widget'](
            label='Webserverhost',
            label_msgid='urban_label_webServerHost',
            i18n_domain='urban',
        ),
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
    ),
    BooleanField(
        name='usePloneTask',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Useplonetask',
            label_msgid='urban_label_usePloneTask',
            i18n_domain='urban',
        ),
    ),
    BooleanField(
        name='useTabbing',
        default=False,
        widget=BooleanField._properties['widget'](
            label='Usetabbing',
            label_msgid='urban_label_useTabbing',
            i18n_domain='urban',
        ),
    ),
    FileField(
        name='templateHeader',
        widget=FileField._properties['widget'](
            label='Templateheader',
            label_msgid='urban_label_templateHeader',
            i18n_domain='urban',
        ),
        storage=AttributeStorage(),
    ),
    FileField(
        name='templateFooter',
        widget=FileField._properties['widget'](
            label='Templatefooter',
            label_msgid='urban_label_templateFooter',
            i18n_domain='urban',
        ),
        storage=AttributeStorage(),
    ),
    FileField(
        name='templateReference',
        widget=FileField._properties['widget'](
            label='Templatereference',
            label_msgid='urban_label_templateReference',
            i18n_domain='urban',
        ),
        storage=AttributeStorage(),
    ),
    FileField(
        name='templateSignatures',
        widget=FileField._properties['widget'](
            label='Templatesignatures',
            label_msgid='urban_label_templateSignatures',
            i18n_domain='urban',
        ),
        storage=AttributeStorage(),
    ),
    FileField(
        name='templateStatsINS',
        widget=FileField._properties['widget'](
            label='Templatestatsins',
            label_msgid='urban_label_templateStatsINS',
            i18n_domain='urban',
        ),
        storage=AttributeStorage(),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanTool_schema = OrderedBaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
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

    security.declarePublic('createUrbanEvent')
    def createUrbanEvent(self, urban_folder_id, urban_event_type_uid):
        """
           Create an urbanEvent on a licence
        """
        evfolder=getattr(self, urban_folder_id)
        brain=self.uid_catalog(UID=urban_event_type_uid)
        urbanEventTypeObj=brain[0].getObject()
        newUrbanEvent=evfolder.invokeFactory("UrbanEvent",id=self.generateUniqueId('UrbanEvent'),title=urbanEventTypeObj.Title(),urbaneventtypes=(urbanEventTypeObj,))
        newUrbanEventObj=getattr(evfolder,newUrbanEvent)
        return self.REQUEST.RESPONSE.redirect(newUrbanEventObj.absolute_url()+'/edit')

    security.declarePublic('createUrbanDoc')
    def createUrbanDoc(self, urban_folder_id, urban_template_uid, urban_event_uid):
        """
        """
        newDocFolder=getattr(self, urban_folder_id)
        brain=self.uid_catalog(UID=urban_template_uid)
        urbanTemplateObj=brain[0].getObject()
        brain=self.uid_catalog(UID=urban_event_uid)
        urbanEventObj=brain[0].getObject()
        fileType='odt'
        tempFileName = '%s/%s_%f.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(),'.odt')
        tempFileNameHeader = '%s/%s_%f_header.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(),'.odt')
        tempFileNameFooter = '%s/%s_%f_footer.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(),'.odt')
        tempFileNameReference = '%s/%s_%f_reference.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(),'.odt')
        tempFileNameSignatures = '%s/%s_%f_signatures.%s' % (
            getOsTempFolder(), urbanTemplateObj._at_uid, time.time(),'.odt')
        portal_url=getToolByName(self,'portal_url')
        brain=self.portal_catalog(path=portal_url.getPortalPath()+'/'+'/'.join(portal_url.getRelativeContentPath(newDocFolder.aq_inner.aq_parent)),id='depot-de-la-demande')
        try:
            recepisseobj = brain[0].getObject()
        except:
            recepisseobj=None
        brain=self.portal_catalog(path=portal_url.getPortalPath()+'/'+'/'.join(portal_url.getRelativeContentPath(newDocFolder.aq_inner.aq_parent)),id='premier-passage-au-college-communal')
        try:
            collegesubmissionobj= brain[0].getObject()
        except:
            collegesubmissionobj=None
        templateHeader = self.getTemplateHeader()
        if templateHeader:
            templateHeader = StringIO(templateHeader)
            #we render the template so pod instructions into the header template are rendered too
            renderer = appy.pod.renderer.Renderer(templateHeader, {'self': newDocFolder.aq_inner.aq_parent,'urbanEventObj':urbanEventObj,'recepisseobj':recepisseobj,'collegesubmissionobj':collegesubmissionobj,}, tempFileNameHeader, pythonWithUnoPath=self.getUnoEnabledPython())
            renderer.run()
        templateFooter = self.getTemplateFooter()
        if templateFooter:
            templateFooter = StringIO(templateFooter)
            #we render the template so pod instructions into the header template are rendered too
            renderer = appy.pod.renderer.Renderer(templateFooter, {'self': newDocFolder.aq_inner.aq_parent,'urbanEventObj':urbanEventObj,'recepisseobj':recepisseobj,'collegesubmissionobj':collegesubmissionobj,}, tempFileNameFooter, pythonWithUnoPath=self.getUnoEnabledPython())
            renderer.run()
        templateReference = self.getTemplateReference()
        if templateReference:
            templateReference = StringIO(templateReference)
            #we render the template so pod instructions into the header template are rendered too
            renderer = appy.pod.renderer.Renderer(templateReference, {'self': newDocFolder.aq_inner.aq_parent,'urbanEventObj':urbanEventObj,'recepisseobj':recepisseobj,'collegesubmissionobj':collegesubmissionobj,}, tempFileNameReference, pythonWithUnoPath=self.getUnoEnabledPython())
            renderer.run()
        templateSignatures = self.getTemplateSignatures()
        if templateSignatures:
            templateSignatures = StringIO(templateSignatures)
            #we render the template so pod instructions into the header template are rendered too
            renderer = appy.pod.renderer.Renderer(templateSignatures, {'self': newDocFolder.aq_inner.aq_parent,'urbanEventObj':urbanEventObj,'recepisseobj':recepisseobj,'collegesubmissionobj':collegesubmissionobj,}, tempFileNameSignatures, pythonWithUnoPath=self.getUnoEnabledPython())
            renderer.run()
        #now that header and footer are rendered, we can use them in the main pod template and render the entire document
        renderer = appy.pod.renderer.Renderer(StringIO(urbanTemplateObj), {'self': newDocFolder.aq_inner.aq_parent,'urbanEventObj':urbanEventObj,'recepisseobj':recepisseobj,'collegesubmissionobj':collegesubmissionobj, 'tool': self, 'header':tempFileNameHeader, 'footer':tempFileNameFooter, 'reference':tempFileNameReference, 'signatures': tempFileNameSignatures}, tempFileName, pythonWithUnoPath=self.getUnoEnabledPython())
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
        newUrbanDoc=newDocFolder.invokeFactory("File",id=self.generateUniqueId('UrbanEvent'),title=urbanTemplateObj.Title(),content_type='application/vnd.oasis.opendocument.text',file=doc)
        newUrbanDoc=getattr(newDocFolder,newUrbanDoc)
        newUrbanDoc.setFilename(urbanTemplateObj.Title()+'.odt')
        newUrbanDoc.setFormat('application/vnd.oasis.opendocument.text')
        newUrbanDoc.reindexObject()
        self.REQUEST.set('doc_uid',newUrbanDoc.UID())
        response.redirect(newDocFolder.absolute_url()+'?doc_uid='+newUrbanDoc.UID())

    security.declarePublic('listVocabulary')
    def listVocabulary(self, vocToReturn, context, vocType="UrbanVocabularyTerm", inUrbanConfig=True):
        """
           This return a list of elements that is used as a vocabulary
           by some fields of differents classes
        """
        #vocPath = self.portal_url()+'/portal_urban/'+vocToReturn+'/'
        portal_url=getToolByName(self,'portal_url')

        #search in an urbanConfig or in the tool
        if inUrbanConfig:
            vocPath = portal_url.getPortalPath()+'/portal_urban/'+self.getUrbanConfig(context).getId()+'/'+vocToReturn+'/'
        else:
            vocPath = portal_url.getPortalPath()+'/portal_urban/'+vocToReturn+'/'
        brains = self.portal_catalog(path=vocPath, sort_on="getObjPositionInParent", portal_type=vocType, review_state='enabled')
        res=[]
        for brain in brains:
            #if we wrote a termKey, we use it...
            obj = brain.getObject()
            if hasattr(obj, 'termKey') and obj.getTermKey():
                key = str(obj.getTermKey())
            else:
                #... either we use the id...
                key=brain.id
            title=brain.Title
            res.append((key,title))
        return tuple(res)

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

    security.declarePublic('findParcel')
    def findParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, location=None, prcOwner=None, prcHistory=None):
        """
           Return the concerned parcels
        """
        section=section.upper()
        exposant=exposant.upper()
        if prcHistory:
            return []
        else:
            query_string = "SELECT capa.da, divname, prc, section, radical, exposant, bis, puissance, sl1, na1,pe FROM map left join capa on map.capakey=capa.capakey left join da on capa.da = da.da "
            condition = ["WHERE "]
            if division != '0':  #precise division selected
                condition.append('capa.da = %s'%division)
            if section:
                condition.append("section = '%s'"%section)
            if radical:
                condition.append("radical = "+radical)
            if bis:
                condition.append("bis = "+bis)
            if exposant:
                condition.append("exposant = '%s'"%exposant)
            if puissance:
                condition.append("puissance = "+puissance)
            if prcOwner:
                condition.append("pe ILIKE '%%%s%%'"%prcOwner)
            if location:
                condition.append("sl1 ILIKE '%%%s%%'"%location)
            if len(condition) > 1:
                query_string += condition[0]
                query_string += ' and '.join(condition[1:])
            try:
                result = self.queryDB(query_string)
            except:
                result=[]
            if result:
                return result
            else:
                return []

    security.declarePublic('findOldParcel')
    def findOldParcel(self, division=None, section=None, radical=None, bis=None, exposant=None, puissance=None, prcHistory=None, divname=None, prca=None):
        """
        Return the concerned parcels
        """
        if prcHistory:
            toreturn=[{'da':division,'divname':divname,'prca':prca,'sectionavant':section,'radicalavant':radical,'bisavant':bis,'exposantavant':exposant,'puissanceavant':puissance,'level':0}]
            def getOldPrc(div, sect, rad, exp, puis, bis, level):
                query_string = "SELECT distinct prca,pas.da,divname,sectionavant,radicalavant,bisavant,exposantavant,puissanceavant FROM pas left join da on pas.da=da.da WHERE pas.da=%s and section = '%s' AND radical = %s AND exposant = '%s' AND puissance = %s AND bis = %s AND prca is not null AND (section != sectionavant or radical != radicalavant or bis != bisavant or exposant != exposantavant or puissance != puissanceavant)"%(div, sect, rad, exp, puis, bis)
                result = self.queryDB(query_string)
                for dic in result:
                    dic['level'] = level+1
                    toreturn.append(dic)
                    getOldPrc(div, dic['sectionavant'], dic['radicalavant'], dic['exposantavant'], dic['puissanceavant'], dic['bisavant'], level+1)
            getOldPrc(division, section, radical, exposant, puissance, bis, 0)
            return toreturn
        else:
            query_string = "SELECT distinct prca,pas.da,divname,sectionavant,radicalavant,bisavant,exposantavant,puissanceavant FROM pas left join da on pas.da=da.da "
            condition = ["WHERE "]
            if division != '0':  #precise division selected
                condition.append('pas.da = %s'%division)
            if section:
                condition.append("sectionavant = '%s'"%section)
            if radical:
                condition.append("radicalavant = "+radical)
            if bis:
                condition.append("bisavant = "+bis)
            if exposant:
                condition.append("exposantavant = '%s'"%exposant)
            if puissance:
                condition.append("puissanceavant = "+puissance)
            if len(condition) > 1:
                query_string += condition[0]
                query_string += ' and '.join(condition[1:])
            return self.queryDB(query_string)

    security.declarePublic('findParcelHistoric')
    def findParcelHistoric(self, division, section, radical=0, bis=0, exposant='', puissance=0):
        """
           Return the concerned parcels
        """
        toreturn=[]
        query_string = 'SELECT distinct da, sectionavant,radicalavant,bisavant,exposantavant,puissanceavant FROM pas WHERE da ='+division+' and section ILIKE \''+section+'\' and radical='+radical
        if bis:
            query_string=query_string+' and bis=\''+bis+'\''
        if exposant:
            query_string=query_string+' and exposant ILIKE \''+exposant+'\''
        if puissance:
            query_string=query_string+' and puissance='+puissance
        query_string=query_string+' and not (sectionavant ILIKE \''+section+'\' and radicalavant='+radical
        if bis:
            query_string=query_string+' and bisavant=\''+bis+'\''
        if exposant:
            query_string=query_string+' and exposantavant ILIKE \''+exposant+'\''
        if puissance:
            query_string=query_string+' and puissanceavant='+puissance
        query_string=query_string+')'

        result = self.queryDB(query_string)
        for rec in result:
            toreturn=toreturn+[rec]
            if  (rec['radicalavant'] != 0) and not ( (rec['sectionavant']==section) and (rec['radicalavant']==radical) and (rec['exposantavant']==exposant) and (rec['bisavant']==bis) and (rec['puissanceavant']==puissance) ) :
                  toreturn=toreturn+self.findParcelHistoric(division,rec['sectionavant'],str(rec['radicalavant']),str(rec['bisavant']),rec['exposantavant'],str(rec['puissanceavant']))
        return toreturn

    security.declarePublic('findDivisions')
    def findDivisions(self, all=True):
        """
           Return the possible divisions
        """
        result = self.queryDB("SELECT da,divname FROM da;")
        if not result:
            return ((DB_QUERY_ERROR, DB_QUERY_ERROR), )
        if all:
            result = [{'da':'0', 'divname':_('urban', 'all_divisions', context=self, default='All divisions')}] + result
        return result

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
              dict_cur.execute(query_string+';')
              for row in dict_cur.fetchall():
                  result=result+[dict(row)]
          except psycopg2.ProgrammingError:
              result=[]
              pass
          self.dbc.close()
          delattr(self,'dbc')
      else:
          ptool = getToolByName(self, "plone_utils")
          ptool.addPortalMessage(_("plone", u"db_connection_error", mapping={u'error': self.dbc}, context=self, default="There was an error connecting to the DB.  The reported error is : '%s'" % self.dbc), type="error")
      return result

    def checkDBConnection(self):
      """
         Check if the provided parameters are OK
      """
      portal = getToolByName(self, "portal_url").getPortalObject()

      #build connection string
      ptool = getToolByName(self, "plone_utils")
      try:
          dbc = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'" % (self.getSqlName(), self.getSqlUser(), self.getSqlHost(), self.getSqlPassword()))
          ptool.addPortalMessage(_("plone", u"db_connection_successfull", context=self, default="db_connection_successfull"), type='info')
      except psycopg2.OperationalError, e:
          ptool.addPortalMessage(_("plone", u"db_connection_error", context=self, mapping={u'error': unicode(e.__str__(), 'utf-8')}, default="There was an error connecting to the DB.  The reported error is : '%s'" % unicode(e.__str__(), 'utf-8')), type="error")

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
    def createPortionOut(self, path, division, section, radical, bis, exposant, puissance, partie):
        """
           Create the PortionOut with given parameters...
        """
        portal_urban = getToolByName(self,'portal_urban')
        dv=self.queryDB("SELECT da,divname FROM da WHERE da="+division)[0]['divname']
        if bis=='0':
            bis=''
        if len(bis)==1:
            bis='0'+bis
        if puissance=='0':
            puissance=''
        newParcelId = path.invokeFactory("PortionOut",id=self.generateUniqueId('PortionOut'),divisionCode=division,division=dv,section=section,radical=radical,bis=bis,exposant=exposant,puissance=puissance,partie=partie)
        newParcel = getattr(path, newParcelId)
        newParcel._renameAfterCreation()
        newParcel.updateTitle()
        self.REQUEST.RESPONSE.redirect(path.absolute_url()+'/view')

    security.declarePublic('getParcelsFromTopic')
    def getParcelsFromTopic(self, topicName):
        """
        """
        try:
            topic = getattr(self.topics, topicName)
        except AttributeError:
            return None

        parcels=[]
        for topicItem in topic.queryCatalog():
            topicItemObj = topicItem.getObject()
            if topicItemObj.meta_type == 'BuildLicence':
                for licenceParcel in topicItemObj.getParcels():
                    parcels.append(licenceParcel)
            elif topicItemObj.meta_type == 'PortionOut':
                parcels.append(topicItemObj)
        return parcels

    security.declarePublic('getParcelInfos')
    def getParcelInfos(self,capakey):
        parcelInfos={}
        strsql="select * from map where capakey='"+capakey+"'"
        try:
            result = self.queryDB(query_string=strsql)[0]
            divname=self.queryDB("SELECT da,divname FROM da WHERE da="+str(result['daa'])[0:5])[0]['divname']
            parcelInfos['name']=divname+' '+result['prc']
            parcelInfos['ownername']=result['pe']
            parcelInfos['ownerstreet']=result['adr2']
            parcelInfos['ownercity']=result['adr1']
            parcelInfos['type']=result['na1']
            strsql="select * from capa where capakey='"+capakey+"'"
            result = self.queryDB(query_string=strsql)[0]
            parcelInfos['division']=str(result['da'])
            parcelInfos['section']=result['section']
            parcelInfos['radical']=str(result['radical'])
            if result['bis']==0:
                parcelInfos['bis']=''
            else:
                parcelInfos['bis']=str(result['bis'])
            if result['exposant'] != None:
                parcelInfos['exposant']=result['exposant']
            else:
                parcelInfos['exposant']=''
            if result['puissance']==0:
                parcelInfos['puissance']=''
            else:
                parcelInfos['puissance']=str(result['puissance'])
        except:
            pass
        return parcelInfos

    security.declarePublic('WfsProxy')
    def WfsProxy(self):
        """
           Proxy for WFS query
        """
        import urllib2
        import cgi
        method = self.REQUEST["REQUEST_METHOD"]
        #allowedHosts = ['10.211.55.10:8080']
        allowedHosts = self.getWebServerHost()

        if method == "POST":
            qs = self.REQUEST["QUERY_STRING"]
            d = cgi.parse_qs(qs)
            if d.has_key("url"):
                url = d["url"][0]
            else:
                self.REQUEST.RESPONSE.setHeader('Content-Type',"text/plain")
                return "Illegal request."
        else:
            fs = cgi.FieldStorage()
            url = fs.getvalue('url', "http://www.urban%s.com"%self.getNISNum())

        try:
            host = url.split("/")[2]
            if allowedHosts and not host in allowedHosts:
                print "Status: 502 Bad Gateway"
                print "Content-Type: text/plain"
                print
                print "This proxy does not allow you to access that location (%s)." % (host,)
                print

            elif url.startswith("http://") or url.startswith("https://"):
                if method == "POST":
                    length = int(self.REQUEST["CONTENT_LENGTH"])
                    headers = {"Content-Type": self.REQUEST["CONTENT_TYPE"]}
                    body = self.REQUEST["BODY"]

                    r = urllib2.Request(url, body, headers)
                    y = urllib2.urlopen(r)
                else:
                    y = urllib2.urlopen(url)

                # print content type header
                i = y.info()
                if i.has_key("Content-Type"):
                    self.REQUEST.RESPONSE.setHeader('Content-Type',i["Content-Type"])
                else:
                    self.REQUEST.RESPONSE.setHeader('Content-Type',"text/plain")

                data = y.read()

                y.close()
                return data
            else:
                self.REQUEST.RESPONSE.setHeader('Content-Type',"text/plain")
                return "Illegal request."

        except Exception, E:
            self.REQUEST.RESPONSE.setHeader('Content-Type',"text/plain")
            return "Some unexpected error occurred. Error text was:", E

    security.declarePublic('GetListOfCapaKeyBuffer')
    def GetListOfCapaKeyBuffer(self, parcelleKey, bufferWidth=50):
        """
             Get List of Capakey around a parcell (ex:92088C0335/00D000)
        """

        dbcon = self.getDBConnection()
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
                )""" % (bufferWidth,parcelleKey)

        try:
            results = self.queryDB(qry)
        except:
            results=[]
        idlist = []
        for res in results:
            idlist.append("capakey='" + res["capakey"]+"'")
        return " OR ".join(idlist)

    security.declarePublic('GetWKTGeomOfBufferParcel')
    def GetWKTGeomOfBufferParcel(self, parcelleKey, bufferWidth=50):
        """
            Get the Geom (in WKT) of the the buffer (ex:92088C0335/00D000)
        """
        dbcon = self.getDBConnection()
        qry = "SELECT astext(ST_BUFFER(the_geom,%s)) AS geom FROM capa WHERE capakey LIKE '%s'" % (bufferWidth,parcelleKey)

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
        res = None
        try:
            urbanConfig = getattr(self, urbanConfigId)
            return urbanConfig
        except AttributeError:
            return None

    def generatePrintMap(self, cqlquery, cqlquery2, zoneExtent=None):
        """
        """
        bound_names={}
        args={}
        kw={}
        bound_names['tool'] = self
        bound_names['zoneExtent'] = zoneExtent
        bound_names['cqlquery'] = cqlquery
        bound_names['cqlquery2'] = cqlquery2
        return self.printmap._exec(bound_names=bound_names, args=args, kw=kw)

    def generateMapJS(self, context, cqlquery, cqlquery2,parcelBufferGeom='', zoneExtent=None):
        """
          Return a generated JS file based on the cql query
        """
        #if we do not have a display zone, we return the default mapExtent
        if not zoneExtent:
            zoneExtent = self.getMapExtent()
        bound_names={}
        args={}
        kw={}
        bound_names['tool'] = self
        bound_names['context'] = context
        bound_names['zoneExtent'] = zoneExtent
        bound_names['cqlquery'] = cqlquery
        bound_names['cqlquery2'] = cqlquery2
        bound_names['parcelBufferGeom'] = parcelBufferGeom

        return self.simplemapjs_gen._exec(bound_names=bound_names, args=args, kw=kw)

    security.declarePublic('generateUrbainXML')
    def generateUrbainXML(self, datefrom, dateto,listeseule):
        """
        """
        if (len(datefrom) != 10) or (len(dateto) != 10):
            return 'Date incorrecte'
        datesplited=datefrom.split('/')
        datefrom=datesplited[2]+'/'+datesplited[1]+'/'+datesplited[0]
        datesplited=dateto.split('/')
        dateto=datesplited[2]+'/'+datesplited[1]+'/'+datesplited[0]
        catalog = getToolByName(self, 'portal_catalog')
        pw = getToolByName(self, 'portal_workflow')
        results = catalog.searchResults(getDecisionDate = {'query' : (DateTime(datefrom),DateTime(dateto)), 'range' : 'minmax'}, id='delivrance-du-permis-octroi-ou-refus',portal_type = 'UrbanEvent')
        i=1
        xmlError=''
        xmlContent='<?xml version="1.0" encoding="iso-8859-1"?>\n'
        xmlContent=xmlContent+'<dataroot>\n'
        xmlContent=xmlContent+'  <E_220_herkomst>\n'
        xmlContent=xmlContent+'    <E_220_NIS_Gem>'+self.getNISNum()+'</E_220_NIS_Gem>\n'
        xmlContent=xmlContent+'    <E_220_Periode_van>'+datefrom.replace("/","")+'</E_220_Periode_van>\n'
        xmlContent=xmlContent+'    <E_220_Periode_tot>'+dateto.replace("/","")+'</E_220_Periode_tot>\n'
        xmlContent=xmlContent+'    <E_220_ICT>COM</E_220_ICT>\n'
        xmlContent=xmlContent+'  </E_220_herkomst>\n'
        liste=["07103","07106","07105","07108","07111","07112","07/113","7115","07/116","07/117","7120","07/121","7124","7126","7128","786","793iii","795","796","0797","08/01","08/04","08/05","08/06","08/09","08/11","08/13","08/14","08/15","08/17","819","08/21","08/22","08/25","08/27","08/29","08/30","08/31","08/32","08/33","08/34","08/36","08/39","08/42","08/45","08/49","08/16"]
        lsttermarchitect=["NON REQUIS","lui-meme","Eux-memes","elle-meme","lui-meme","lui-meme ","Lui-meme","A COMPLETER "]
        htmllist='<HTML><TABLE>'
        for obj in results:
            eventObj=obj.getObject()
            licenceObj=eventObj.getParentNode()
            applicantObj=licenceObj.getApplicants()[0]
            architectObj=licenceObj.getArchitects()
            if architectObj==None:
                xmlError=xmlError+applicantObj.getName1()+' '+applicantObj.getName2()+'\n'
            worktype=licenceObj.getWorkType()
            if (pw.getInfoFor(licenceObj,'review_state')=='accepted') and (not str(licenceObj.getReference()) in liste):
                htmllist=htmllist+'<TR><TD>'+str(licenceObj.getReference())+'  '+licenceObj.title.encode('iso-8859-1')+'</TD><TD>'+str(eventObj.getDecisionDate())+'</TD></TR>'
                xmlContent=xmlContent+'  <Item220>\n'
                xmlContent=xmlContent+'      <E_220_Ref_Toel>'+str(licenceObj.getReference())+'</E_220_Ref_Toel>\n'
                try:
                    xmlContent=xmlContent+'      <Doc_Afd>'+licenceObj.objectValues('PortionOut')[0].getDivisionCode()+'</Doc_Afd>\n'
                except:
                    xmlError=xmlError+str(licenceObj.getReference())
                if licenceObj.getWorkLocationStreet():
                    xmlContent=xmlContent+'      <E_220_straatcode>'+str(licenceObj.getWorkLocationStreetCode())+'</E_220_straatcode>\n'
                    xmlContent=xmlContent+'      <E_220_straatnaam>'+str(licenceObj.getWorkLocationStreet()).decode('utf-8').encode('iso-8859-1')+'</E_220_straatnaam>\n'
                else:
                    xmlError=xmlError+'pas de rue: '+str(licenceObj.getReference())+' '+licenceObj.licenceSubject.encode('iso-8859-1')+' '+applicantObj.name1.encode('iso-8859-1')+' '+applicantObj.name2.encode('iso-8859-1')+'\n'
                xmlContent=xmlContent+'      <E_220_huisnr>'+licenceObj.getWorkLocationHouseNumber()+'</E_220_huisnr>\n'
                if worktype=='ncmu':
                    xmlWorkType='N_UNI'
                else:
                    if worktype=='ncia':
                        xmlWorkType='N_APPART'
                    else:
                        if worktype=='nca':
                            xmlWorkType='N_AUT'
                        else:
                            if worktype=='tmu':
                                xmlWorkType='T_UNI'
                            else:
                                if worktype=='tia':
                                    xmlWorkType='T_APPART'
                                else:
                                    if worktype=='tab':
                                        xmlWorkType='T_AUT'
                                    else:
                                        if worktype=='dg':
                                            xmlWorkType='DEM'
                                        else:
                                            if worktype=='autres':
                                                xmlWorkType='AUTRE'
                                            else:
                                                if worktype=='tnbg':
                                                    xmlWorkType='T_NBAT'
                                                else:
                                                    xmlError=xmlError+str(licenceObj.getReference())+' '+licenceObj.licenceSubject.encode('iso-8859-1')+' '+applicantObj.name1.encode('iso-8859-1')+' '+applicantObj.name2.encode('iso-8859-1')+'\n'
                xmlContent=xmlContent+'      <E_220_Typ>'+xmlWorkType+'</E_220_Typ>\n'
                xmlContent=xmlContent+'      <E_220_Werk>'+licenceObj.licenceSubject.encode('iso-8859-1')+'</E_220_Werk>\n'
                strDecisionDate=''+str(eventObj.getDecisionDate())
                xmlContent=xmlContent+'      <E_220_Datum_Verg>'+strDecisionDate[0:4]+strDecisionDate[5:7]+strDecisionDate[8:10]+'</E_220_Datum_Verg>\n'
                xmlContent=xmlContent+'      <E_220_Instan>COM</E_220_Instan>\n'
                xmlContent=xmlContent+'      <PERSOON>\n'
                xmlContent=xmlContent+'        <naam>'+applicantObj.name1.encode('iso-8859-1')+' '+applicantObj.name2.encode('iso-8859-1')+'</naam>\n'
                xmlContent=xmlContent+'        <straatnaam>'+applicantObj.street.encode('iso-8859-1')+'</straatnaam>\n'
                xmlContent=xmlContent+'        <huisnr>'+applicantObj.getNumber()+'</huisnr>\n'
                xmlContent=xmlContent+'        <postcode>'+applicantObj.getZipcode()+'</postcode>\n'
                xmlContent=xmlContent+'        <gemeente>'+applicantObj.city.encode('iso-8859-1')+'</gemeente>\n'
                xmlContent=xmlContent+'        <hoedanig>DEMANDEUR</hoedanig>\n'
                xmlContent=xmlContent+'      </PERSOON>\n'
                if architectObj:
                    if architectObj.getName1() in lsttermarchitect:
                        xmlContent=xmlContent+'      <PERSOON>\n'
                        xmlContent=xmlContent+'        <naam>'+applicantObj.name1.encode('iso-8859-1')+' '+applicantObj.name2.encode('iso-8859-1')+'</naam>\n'
                        xmlContent=xmlContent+'        <straatnaam>'+applicantObj.street.encode('iso-8859-1')+'</straatnaam>\n'
                        xmlContent=xmlContent+'        <huisnr>'+applicantObj.getNumber()+'</huisnr>\n'
                        xmlContent=xmlContent+'        <postcode>'+applicantObj.getZipcode()+'</postcode>\n'
                        xmlContent=xmlContent+'        <gemeente>'+applicantObj.city.encode('iso-8859-1')+'</gemeente>\n'
                        xmlContent=xmlContent+'        <hoedanig>ARCHITECTE</hoedanig>\n'
                        xmlContent=xmlContent+'      </PERSOON>\n'
                    else:
                        xmlContent=xmlContent+'      <PERSOON>\n'
                        xmlContent=xmlContent+'        <naam>'+architectObj.name1.encode('iso-8859-1')+' '+architectObj.name2.encode('iso-8859-1')+'</naam>\n'
                        xmlContent=xmlContent+'        <straatnaam>'+architectObj.street.encode('iso-8859-1')+'</straatnaam>\n'
                        xmlContent=xmlContent+'        <huisnr>'+architectObj.getNumber()+'</huisnr>\n'
                        xmlContent=xmlContent+'        <postcode>'+architectObj.getZipcode()+'</postcode>\n'
                        xmlContent=xmlContent+'        <gemeente>'+architectObj.city.encode('iso-8859-1')+'</gemeente>\n'
                        xmlContent=xmlContent+'        <hoedanig>ARCHITECTE</hoedanig>\n'
                        xmlContent=xmlContent+'      </PERSOON>\n'
                for prc in licenceObj.objectValues('PortionOut'):
                    xmlContent=xmlContent+'      <PERCELEN>\n'
                    try:
                        strRadical='%04d'%float(prc.getRadical())
                    except:
                        strRadical='0000'
                    try:
                        strPuissance='%03d'%float(prc.getPuissance())
                    except:
                        strPuissance='000'
                    try:
                        strBis='%02d'%float(prc.getBis())
                    except:
                        strBis='00'
                    xmlContent=xmlContent+'        <E_220_percid>'+prc.getDivisionCode()+'_'+prc.getSection()+'_'+strRadical+'_'+prc.getExposant()+'_'+strPuissance+'_'+strBis+'</E_220_percid>\n'
                    xmlContent=xmlContent+'        <kadgemnr>'+prc.getDivisionCode()+'</kadgemnr>\n'
                    xmlContent=xmlContent+'        <sectie>'+prc.getSection()+'</sectie>\n'
                    xmlContent=xmlContent+'        <grondnr>'+prc.getRadical()+'</grondnr>\n'
                    if prc.getExposant() != '':
                        xmlContent=xmlContent+'        <exponent>'+prc.getExposant()+'</exponent>\n'
                    if prc.getPuissance() != '':
                        xmlContent=xmlContent+'        <macht>'+prc.getPuissance()+'</macht>\n'
                    if prc.getBis() != '':
                        xmlContent=xmlContent+'        <bisnr>'+prc.getBis()+'</bisnr>\n'
                    xmlContent=xmlContent+'      </PERCELEN>\n'

               ## xmlContent = xmlContent+str(i)+': '+'\n'
                i=i+1
                xmlContent=xmlContent+'  </Item220>\n'
        xmlContent=xmlContent+'</dataroot>\n'
        htmllist=htmllist+'</TABLE></HTML>'
        if listeseule:
            output = StringIO()
            output.write(unicode(htmllist.replace("&","&amp;"),'iso-8859-1'))
            return output.getvalue()
        else:
            if xmlError != '':
                return 'Error in these licences:\n\n'+xmlError
            else:
                output = StringIO()
                output.write(unicode(xmlContent.replace("&","&amp;"),'iso-8859-1').encode('iso-8859-1'))
                return output.getvalue()

    security.declarePublic('searchByApplicant')
    def searchByApplicant(self, foldertypes, applicantInfosIndex):
        """
          Find licences with given paramaters
        """
        catalogTool = getToolByName(self, 'portal_catalog')
        res = []
        try:
            res = catalogTool(portal_type=foldertypes, applicantInfosIndex=applicantInfosIndex)
            return res
        except ParseError:
            #in case something like '*' is entered, ZCTextIndex raises an error...
            ptool = getToolByName(self, "plone_utils")
            ptool.addPortalMessage(_("plone", u"please_enter_more_letters", context=self, default="Please enter more letters to do the search"), type="info")
            return res

    security.declarePublic('searchByStreet')
    def searchByStreet(self, foldertypes, workLocationUid):
        """
          Find licences with given paramaters
        """
        #we receive the street uid, look back references and returns the found licences
        if not foldertypes:
            return []
        UidCatalog = getToolByName(self, 'uid_catalog')
        brains = UidCatalog(UID=workLocationUid)
        if brains:
            street = brains[0].getObject()
            #filter on foldertypes
            res = []
            for bref in street.getBRefs():
                if bref.aq_inner.aq_parent.portal_type in foldertypes:
                    res.append(bref.aq_inner.aq_parent)
            return res
        return []

    security.declarePublic('searchByParcel')
    def searchByParcel(self, foldertypes, division, section, radical, bis, exposant, puissance, partie):
        """
          Find parcels with given paramaters and returns the linked licences
        """
        if len(bis)==1:
            bis='0'+bis
        section=section.upper()
        exposant=exposant.upper()
        catalogTool = getToolByName(self, 'portal_catalog')
        #see PortionOut.parcelInfosIndex to see how th index is build
        if partie:
            partiestr = '1'
        else:
            partiestr = '0'
        parcelInfosIndex = '%s,%s,%s,%s,%s,%s,%s' % (division, section, radical, bis, exposant, puissance, '1')
        brains = catalogTool(portal_type=foldertypes, parcelInfosIndex=parcelInfosIndex)
        parcelInfosIndex2 = '%s,%s,%s,%s,%s,%s,%s' % (division, section, radical, bis, exposant, puissance, '0')
        brains = brains + catalogTool(portal_type=foldertypes, parcelInfosIndex=parcelInfosIndex2)
        #if we did not found any real parcel, returns

        oldsparcels=self.findParcelHistoric(division, section, radical, bis, exposant, puissance)
        if (not brains) and (not oldsparcels):
            return []
        parcels = []
        parcels.append(parcelInfosIndex)
        parcels.append(parcelInfosIndex2)
        for oldparcel in oldsparcels:
            parcel = '%s,%s,%s,%s,%s,%s,%s' % (str(oldparcel['da']), oldparcel['sectionavant'], oldparcel['radicalavant'], oldparcel['bisavant'], oldparcel['exposantavant'], oldparcel['puissanceavant'], '0')
            parcelwithpartie = '%s,%s,%s,%s,%s,%s,%s' % (str(oldparcel['da']), oldparcel['sectionavant'], oldparcel['radicalavant'], oldparcel['bisavant'], oldparcel['exposantavant'], oldparcel['puissanceavant'], '1')
            #remove the '0' values
            parcel = parcel.replace(',0,', ',,')
            parcelwithpartie = parcelwithpartie.replace(',0,', ',,')
            parcels.append(parcel)
            parcels.append(parcelwithpartie)
        res = []
        for parcel in parcels:
            brains = catalogTool(portal_type=foldertypes, parcelInfosIndex=parcel)
            res += brains
        #remove brains for wich no parcel at all is defined...
        return [r for r in res if r.parcelInfosIndex]

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
        if at_obj.__module__== "Products.Archetypes.Schema":
            #we have a schema here
            return at_obj[fieldRealName]
        else:
            return at_obj.Schema()[fieldRealName]

    security.declarePublic('generateReference')
    def generateReference(self, obj):
        """
         Generates a reference based on the numerotationTALExpression
        """
        #we get a field like UrbanCertificateBaseNumerotation on self
        #to get the last numerotation for this kind of licence
        fieldObj = self.getField(obj.portal_type + 'Numerotation')
        lastValue = '0'
        if not fieldObj:
            #in some case (a portal_type not equals to the meta_type)
            #the portal_type is not set yet at factory time, try to find it
            fieldObj = self.getField(obj.REQUEST['__factory__info__']['stack'][0] + 'Numerotation')
        if fieldObj:
            #get the last value
            lastValue = fieldObj.getAccessor(self)()
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
        res = ''
        try:
            ctx = getEngine().getContext(data)
            res = Expression(self.getNumerotationTALExpression())(ctx)
        except Exception, e:
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
        brains = cat(path=path, sort_on='getObjPositionInParent', meta_type=['UrbanEventType'], review_state="enabled")
        res = []
        #now evaluate the TAL condition for every brain
        for brain in brains:
            obj = brain.getObject()
            if obj.isApplicable(context):
                res.append(brain)
        return res

    security.declarePublic('initMap')
    def initMap(self, obj):
        """
          Initialize the map on element
        """
        zoneExtent = None
        parcels = obj.getParcels()
        cqlquery=''
        if parcels:
            #if we have parcels, display them on a map...
            #generate the 'selectedpo' layer filter based on contained parcels
            for parcel in parcels:
                if cqlquery !='':
                    cqlquery=cqlquery + " or "
                cqlquery=cqlquery+"(section='"+parcel.getSection()+"' and radical="+parcel.getRadical()
                if parcel.getBis() != '':
                    cqlquery=cqlquery+" and bis="+parcel.getBis()
                if parcel.getExposant() != '':
                    cqlquery=cqlquery+" and exposant='"+parcel.getExposant()+"'"
                else:
                    cqlquery=cqlquery+" and exposant is NULL"
                if parcel.getPuissance() != '':
                    cqlquery=cqlquery+" and puissance="+parcel.getPuissance()
                else:
                    cqlquery=cqlquery+" and puissance=0"
                cqlquery=cqlquery+")"
            cqlquery = '((da = '+parcel.getDivisionCode()+') and ('+cqlquery+'))'
            #calculate the zone to display
            strsql = 'SELECT Xmin(selectedpos.extent),Ymin(selectedpos.extent),Xmax(selectedpos.extent), Ymax(selectedpos.extent) FROM (SELECT Extent(the_geom) FROM capa WHERE '+cqlquery+') AS selectedpos'
            result = self.queryDB(query_string=strsql)[0]
            try:
                zoneExtent = "%s,%s,%s,%s" % (result['xmin'],result['ymin'],result['xmax'],result['ymax'])
            except:
                zoneExtent = ""

        #return the generated JS code
        return self.generateMapJS(self, cqlquery,'','', zoneExtent)

    security.declarePublic('generateStatsINS')
    def generateStatsINS(self, datefrom, dateto):
        """
        """
        portal_url=getToolByName(self,'portal_url')
        if (len(datefrom) != 10) or (len(dateto) != 10):
            return 'Date incorrecte'
        datesplited=datefrom.split('/')
        datefrom=datesplited[2]+'/'+datesplited[1]+'/'+datesplited[0]
        datesplited=dateto.split('/')
        dateto=datesplited[2]+'/'+datesplited[1]+'/'+datesplited[0]
        templateObj=self.getTemplateStatsINS()
        catalog = getToolByName(self, 'portal_catalog')
        results = catalog.searchResults(getBeginDate = {'query' : (DateTime(datefrom),DateTime(dateto)), 'range' : 'minmax'}, id='debut-des-travaux',portal_type = 'UrbanEvent')
        folders=[]
        for result in results:
            objResult=result.getObject()
            folderobj=objResult.aq_inner.aq_parent
            if folderobj.getUsage() != 'not_applicable':
                folders.append(folderobj)
        fileType='odt'
        tempFileName =  tempFileName = '%s/%s_%f.%s' % (getOsTempFolder(), 'statsins', time.time(),'.odt')
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
                elif rightEvent == None:
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
        fieldObj = self.getField(obj.portal_type + 'Numerotation')
        value = fieldObj.getAccessor(self)()
        if not str(value).isdigit():
            value = '0'
        else:
            value = int(value)
            value = value + 1
        #set the new value
        fieldObj.set(self, value)
        self.reindexObject()

    security.declarePublic('getCurrentFolderManager')
    def getCurrentFolderManager(self, obj, initials=True):
        """
          Returns the current FolderManager initials or object
        """
        #the current FolderManager is based on the current Plone User and the
        #ploneUserId defined on the folderManagers for the 'obj' kind of licence
        urbanConfig = self.getUrbanConfig(obj)
        if not urbanConfig:
            return ''
        folderManagersFolder = urbanConfig.foldermanagers
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
            vowels = ('a', 'e', 'i', 'o', 'u', 'y',)
            for v in vowels:
                if cityName.lower().startswith(v):
                    prefix = "d'"
                    break
            return prefix + cityName

    security.declarePublic('formatDate')
    def formatDate(self, date, long_format=None, time_only=None, translatemonth=True):
        """
          Format the date for printing in pod templates
        """
        if date:
            if not translatemonth:
                return ulocalized_time(date, long_format=False, time_only=None, context=self,
                    domain='', request=self.REQUEST)
            else:
                #we need to translate the month and maybe the day (1er)
                year, month, day = str(date.strftime('%Y/%m/%d')).split('/')
                #we try to translate the day in any case...
                #so in french '1' becomes '1er' but in english, '1' becomes '1st',
                #'2' becomes '2nd', ...
                daymsgid = "date_day_%s" % day
                translatedDay = _('urban', daymsgid, context=self, default=day)
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
                translatedMonth = _('plonelocales', monthmsgid, context=self, default=month).lower()
            return "%s %s %s" % (translatedDay, translatedMonth, year)
        return ''



registerType(UrbanTool, PROJECTNAME)
# end of class UrbanTool

##code-section module-footer #fill in your manual code here
##/code-section module-footer

