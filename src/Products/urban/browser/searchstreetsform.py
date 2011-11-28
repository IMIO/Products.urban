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

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
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
                                    source = "availableStreets"
                                 )

class SearchStreetsForm(formbase.PageForm):
    form_fields = form.FormFields(ISearchStreetsForm)
    label = u"Recherche de documents par rue"
    description = u""
    streetsFound = []
    template = ViewPageTemplateFile('templates/searchstreetsresults.pt')

    def update(self):
        super(formbase.PageForm, self).update()

    @form.action(u"Rechercher")
    def action_send(self, action, data):
        """
          Do the search
        """
        context = aq_inner(self.context)
        #do only the search if at least a street and a type is selected...
        types = ['BuildLicence', 'Declaration', 'ParcelOutLicence', 'Division', 'NotaryLetter', 'UrbanCertificateBase', 'UrbanCertificateTwo']
        typesToSearch = [typeToSearch for typeToSearch in types if data[typeToSearch]]
        streetUID = data['streetSearch']
        if not typesToSearch or not streetUID:
            plone_utils = getToolByName(context, 'plone_utils')
            if not typesToSearch:
                plone_utils.addPortalMessage(_('Please, select at least one type to search on!'), 'warning')
            if not streetUID:
                plone_utils.addPortalMessage(_('Please, select a street from the list below!'), 'warning')
            return self.template()
        #update results display if any
        catalog = getToolByName(context, 'portal_catalog')
        #perform a search on type
        #thus, glance at each object if street id is included in this latter
        brains = catalog(portal_type=typesToSearch)
        self.streetsFound = []
        for brain in brains:
            licence = brain.getObject()
            workLocations = licence.getWorkLocations()
            for workLocation in workLocations:
                if workLocation['street'] == streetUID:
                    self.streetsFound.append(brain)
                    #it's found, ok, break
                    break

        #for unclear reason base must be reinitialized before returning template
        return self.template()
