# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2008 by CommunesPlone
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from zope.interface import Interface
from zope import schema

from zope.formlib import form
from five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.plonefinder.widgets.referencewidget import FinderSelectWidget
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from zope.schema.vocabulary import SimpleVocabulary

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class ISearchStreetsForm(Interface):
    """Define the fields of search street form
    """

    BuildLicence = schema.Bool(title = (u"Permis d'urbanisme"),
                               default = True)
    Declaration = schema.Bool(title = (u"Déclaration"), default = True)
    ParcelOutLicence = schema.Bool(title = (u"Permis d'urbanisation"), default = True)
    Division = schema.Bool(title = (u"Division"), default = True)
    NotaryLetter = schema.Bool(title = (u"Lettre de notaire"), default = True)
    UrbanCertificateBase = schema.Bool(title = (u"Certificat d'urbanisme 1"), default = True)
    UrbanCertificateTwo = schema.Bool(title = (u"Certificat d'urbanisme 2"), default = True)

    streetSearch = schema.Choice (  
                                    title = u"Sélectionner rue",
                                    description = u"Sélectionner une rue à rechercher ",
                                    required = False,
                                    vocabulary = "Available streets"
                                 )

def availableStreets(context):
    voc = UrbanVocabulary('streets', vocType=("Street", "Locality", ), id_to_use="UID", inUrbanConfig=False, browseHistoric=True).getDisplayList(context)
    voc = voc.values()
    voc.sort()
    return SimpleVocabulary.fromValues(voc)

class MyFinderSelectWidget(FinderSelectWidget):
    """
    A widget with a plone_finder link
    for a Sequence field (tuple or list)
    that could reference and upload files
    """
    template = ViewPageTemplateFile('templates/myfinderbase.pt')
    finderlabel = (u'')
    types = ['Street', 'Locality']
    forcecloseoninsert = True

class SearchStreetsForm(formbase.PageForm):
    form_fields = form.FormFields(ISearchStreetsForm)
    label = u"Recherche de documents par rue"
    description = u""
    streetsFound = []
    template = ViewPageTemplateFile('templates/searchstreetsresults.pt')

    def update(self):
        #initialize base root to be locate to streets configuration folder
        """context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        brain = catalog.searchResults(id = 'streets')
        self.streetsBase = aq_inner(brain[0].getObject())"""
        super(formbase.PageForm, self).update()
        #self.widgets['streetSearch'].base = self.streetsBase


    @form.action(u"Rechercher")
    def action_send(self, action, data):
        """search licences
        """
        #update results display if any
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        types = ['BuildLicence', 'Declaration', 'ParcelOutLicence', 'Division', 'NotaryLetter', 'UrbanCertificateBase', 'UrbanCertificateTwo']
        typesToSearch = [typeToSearch for typeToSearch in types if data[typeToSearch]]
        #perform a search on type
        #thus, glance at each object if street id is included in this latter
        brains = catalog.searchResults(portal_type = typesToSearch)
        self.streetsFound = []

        for brain in brains:
            doc = brain.getObject()
            objs = doc.getWorkLocations()
            if objs:
                for obj in objs:
                    if (not data['streetSearch'] or obj['uid'] in  data['streetSearch']):
                        self.streetsFound.append((doc.Title(), brain.getURL()))
            elif not data['streetSearch']:
                self.streetsFound.append((doc.Title(), brain.getURL()))

        #for unclear reason base must be reinitialized before returning template
        self.widgets['streetSearch'].base = self.streetsBase
        return self.template()
