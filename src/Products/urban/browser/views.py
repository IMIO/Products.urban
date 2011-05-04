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
    def __call__(self):
#        self.context = context
#        self.request = request

        """
          Initialize the map on element
        """
        zoneExtent = None
        uidBuildLicence=self.request.form["uidPlone"]
        pc = getToolByName(self.context, 'portal_catalog')
        resultsItem=pc.searchResults(UID=uidBuildLicence)
        obj=resultsItem[0].getObject()
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
            result = self.context.queryDB(query_string=strsql)[0]
            try:
                self.xmin=result['xmin']
                self.ymin=result['ymin']
                self.xmax=result['xmax']
                self.ymax=result['ymax']
                zoneExtent = "%s,%s,%s,%s" % (result['xmin'],result['ymin'],result['xmax'],result['ymax'])
            except:
                zoneExtent = ""
        self.tmpl=ViewPageTemplateFile("wmc.pt")
        return self.tmpl() 
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
        layers = (
                {'url' : defaulturl,'srs':'EPSG:31370','title':'Parcellaire','name' : 'urban'+tool.getNISNum()+':capa','format':'image/png','style':'default'},
                {'url' : defaulturl,'srs':'EPSG:31370','title':'Noms de rue','name' : 'urban'+tool.getNISNum()+':toli','format':'image/png','style':'default'},
                {'url' : defaulturl,'srs':'EPSG:31370','title':'N° de parcelle','name' : 'urban'+tool.getNISNum()+':canu','format':'image/png','style':'ParcelsNum'},
                )
        return layers
        


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
