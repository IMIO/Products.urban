# -*- coding: utf-8 -*-
import urllib, urllib2
from urlparse import urlparse
from zope import interface
from zope.formlib import namedtemplate
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form._named import named_template_adapter

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
        layers = [
                {'url' : defaulturl,'srs':'EPSG:31370','title':'Parcellaire','name' : 'urban'+tool.getNISNum()+':capa','format':'image/png','style':'default','opacity':0.5, 'visibility': True},
                {'url' : defaulturl,'srs':'EPSG:31370','title':'Noms de rue','name' : 'urban'+tool.getNISNum()+':toli','format':'image/png','style':'default','opacity':0.5,'visibility':True},
                {'url' : defaulturl,'srs':'EPSG:31370','title':'N° de parcelle','name' : 'urban'+tool.getNISNum()+':canu','format':'image/png','style':'ParcelsNum','opacity':0.5, 'visiblity':True},
                ]
        for additional_layer in tool.additional_layers.objectValues():
            if additional_layer.getWMSUrl()=="":
                url=defaulturl
            else:
                url=additional_layer.getWMSUrl()
            opacity=1
            if additional_layer.getTransparent() == True:
                opacity=0
            layers.append({'url' : url,'srs':additional_layer.getSRS(),'title':additional_layer.Title,'name' : additional_layer.getLayers(),'format':additional_layer.getLayerFormat(),'style':additional_layer.getStyles(),'opacity':opacity,'visibility':additional_layer.getVisibility()})
        return layers
    def wmc(self):

        """
          Initialize the map on element
        """
        zoneExtent = None
        urbantool = getToolByName(self,'portal_urban')
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
                zoneExtent = "%s,%s,%s,%s" % (result['xmin'],result['ymin'],result['xmax'],result['ymax'])
            except:
                zoneExtent = ""
        self.tmpl=ViewPageTemplateFile("wmc.pt")
        return self.tmpl(self)         


class ProxyController(BrowserView):
    urlList = ["localhost:8081","89.16.179.114:8008","89.16.179.114:5000","cartopro2.wallonie.be"]
    def getProxy(self):
        try:
            url = self.request.get("url")
            infos = urlparse(url) 
            params = self.request.form
            
            try:
                self.urlList.index(infos[1])
            except ValueError, e:
               print e
               return "Someone try to use not valid host for proxy"

            params.pop("url")
            self.request.response.setHeader('content-type', 'text/json')
            conn = urllib2.urlopen(url+"?%s" % urllib.urlencode(params))
            return conn.read()
        except Exception, e:
            print e
        
class testmap(ProxyController):
    pass
