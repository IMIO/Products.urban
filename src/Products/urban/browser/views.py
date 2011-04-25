# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form._named import named_template_adapter
from zope import interface
from zope.formlib import namedtemplate

class WMC(BrowserView):
    def minx(self):
        return "1"
    def miny(self):
        return "2"
    def maxx(self):
        return "3"
    def maxy(self):
        return "4"
    def getLayers(self):
        context=aq_inner(self.context)
        tool=getToolByName(context, "portal_urban")
        defaulturl='http://'+tool.getWebServerHost()+'/geoserver/wms'
        layers = (
                {'url' : defaulturl,'srs':'ESPG:31370','title':'Parcellaire','name' : 'urban'+tool.getNISNum()+':capa','format':'image/png','style':'default'},
                {'url' : defaulturl,'srs':'ESPG:31370','title':'Noms de rue','name' : 'urban'+tool.getNISNum()+':toli','format':'image/png','style':'default'},
                {'url' : defaulturl,'srs':'ESPG:31370','title':'N de parcelle','name' : 'urban'+tool.getNISNum()+':canu','format':'image/png','style':'ParcelsNum'},
                )
        return layers

referencebrowserwidget_popup = named_template_adapter(ViewPageTemplateFile('templates/referencebrowser_popup.pt'))