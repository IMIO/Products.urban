# -*- coding: utf-8 -*-
import urllib, urllib2
from urlparse import urlparse
from zope import interface
from zope.formlib import namedtemplate
from Products.Five import BrowserView
from Acquisition import aq_inner, aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form._named import named_template_adapter
from Products.urban.config import URBAN_TYPES
from Products.urban.utils import getMd5Signature
import logging
logger = logging.getLogger('urban: Views')

class WMC(BrowserView):
#
#        #return the generated JS code
#        return self.generateMapJS(self, cqlquery,'','', zoneExtent)
    def minx(self):
        return self.xmin
    def miny(self):
        return self.ymin
    def maxx(self):
        return self.xmax
    def maxy(self):
        return self.ymax
    def getLayers(self):
        context=aq_inner(self.context)
        tool=getToolByName(context, "portal_urban")
        defaulturl='http://'+tool.getWebServerHost()+'/geoserver/wms'
        """
        Samples:
        layers = [
#                {'url' : defaulturl,'srs':'EPSG:31370','title':'N° de parcelle','name' : 'urban'+tool.getNISNum()+':canu','format':'image/png','style':'ParcelsNum','hidden': 0},
                ]
        """
        layers = []
        for additional_layer in tool.additional_layers.objectValues():
            if additional_layer.getWMSUrl()=="":
                url=defaulturl
            else:
                url=additional_layer.getWMSUrl()
            hidden = 1
            if additional_layer.getVisibility() == True:
                hidden = 0
            layers.append({'url' : url,'srs':additional_layer.getSRS(),'title':additional_layer.Title,'name' : additional_layer.getLayers(),'format':additional_layer.getLayerFormat(),'style':additional_layer.getStyles(),'hidden': hidden, 'transparency':additional_layer.getTransparency() and 'true' or 'false', 'queryable':additional_layer.getQueryable() and '1' or '0'})
        return layers

    def wmc(self):
        """
          Initialize the map on element
          if no context get the mapextent from config
        """
        zoneExtent = None
        urbantool = getToolByName(self,'portal_urban')
        context = aq_inner(self.context)
        if not hasattr(aq_base(context), "getParcels"):

            try:
                extent = urbantool.getMapExtent().split(',')
                self.xmin=extent[0]
                self.ymin=extent[1]
                self.xmax=extent[2]
                self.ymax=extent[3]
                #zoneExtent = "%s,%s,%s,%s" % (result['xmin'],result['ymin'],result['xmax'],result['ymax'])
            except:
                pass
        else:
            parcels = self.context.getParcels()
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
                result = urbantool.queryDB(query_string=strsql)[0]
                try:
                    self.xmin=result['xmin']
                    self.ymin=result['ymin']
                    self.xmax=result['xmax']
                    self.ymax=result['ymax']
                    #zoneExtent = "%s,%s,%s,%s" % (result['xmin'],result['ymin'],result['xmax'],result['ymax'])
                except:
                    #zoneExtent = ""
                    pass
        self.tmpl=ViewPageTemplateFile("wmc.pt")
        return self.tmpl(self)

class ProxyController(BrowserView):
    urlList = ["localhost:8081","89.16.179.114:8008","89.16.179.114:5000","cartopro2.wallonie.be"]
    def getProxy(self):
        try:
            url = self.request.get("url")
            #infos = urlparse(url)
            params = self.request.form

            params.pop("url")
            self.request.response.setHeader('content-type', 'text/json')
            if params:
                url = url+"?%s" % urllib.urlencode(params)
            conn = urllib2.urlopen(url, timeout=6)
            data = conn.read()
            conn.close()
            return data
        except Exception, msg:
            logger.error("Cannot open url '%s': %s"%(url, msg))

class testmap(ProxyController):
    pass

class TemplatesSummary(BrowserView):
    """
        Get all templates information to give a summary
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.tool = getToolByName(context, 'portal_urban')
        self.tot_count = 0
        self.mod_count = 0
        self.editicon = 'edit.png'
        self.editlink = 'edit'

    def getUrbanDoc(self, folder):
        return folder.listFolderContents(contentFilter={'portal_type':['UrbanDoc']})

    def getGlobalTemplates(self):
        templates = ['globaltemplates']
        for templ in self.getUrbanDoc(self.tool.globaltemplates):
            templates.append({'o':templ, 's':self.isModified(templ)})
            self.tot_count += 1
        if len(templates) > 1 and templates[1]['o'].externalEditorEnabled():
            self.editicon = 'extedit_icon.png'
            self.editlink = 'external_edit'
        return templates

    def getEventsTemplates(self):
        # return something like [[urban_type1, [uet1, {doc1}, {doc2}, ...], [uet2, {doc3}, ...], ...], [urban_type2, [], ...], ...]
        templates=[]
        for urban_type in URBAN_TYPES:
            templ_by_type = [urban_type]
            licenceConfigId = urban_type.lower()
            if not safe_hasattr(self.tool, licenceConfigId): continue
            configFolder = getattr(self.tool, licenceConfigId)
            if not safe_hasattr(configFolder, 'urbaneventtypes'): continue
            uetfolder = getattr(configFolder, 'urbaneventtypes')
            for obj in uetfolder.objectValues('UrbanEventType'):
                templ_by_event = [obj.Title()]
                for templ in self.getUrbanDoc(obj):
                    self.tot_count += 1
                    templ_by_event.append({'o':templ, 's':self.isModified(templ)})
                templ_by_type.append(templ_by_event)
            templates.append(templ_by_type)
        return templates

    def isModified(self, template):
        if not template.hasProperty('md5Modified'):
            return "question-mark.png"
        if template.md5Modified != getMd5Signature(template.data):
            #template manually changed
            self.mod_count += 1
            return "warning.png"
        return None
