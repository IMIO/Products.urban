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
from Products.Five.formlib import formbase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.plonefinder.widgets.referencewidget import FinderSelectWidget

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

class ISearchStreetsForm(Interface):
    """Define the fields of search street form
    """

    buildLicence = schema.Bool(title = (u"Permis d'urbanisme"),)
    declare = schema.Bool(title = (u"Déclaration"),)
    buildingLicence = schema.Bool(title = (u"Permis d'urbanisation"),)
    division = schema.Bool(title = (u"Division"),)
    notary = schema.Bool(title = (u"Lettre de notaire"),)
    buildCertificate1 = schema.Bool(title = (u"Certificat d'urbanisme 1"),)
    buildCertificate2 = schema.Bool(title = (u"Certificat d'urbanisme 2"),)


    streetSearch = schema.Tuple (title=u"Sélectionne rue",
                                    description =u"Sélectionne une rue à rechercher ",
                                    default= ()
                                    )

class SearchStreetsForm(formbase.PageForm):
    form_fields = form.FormFields(ISearchStreetsForm)
    form_fields['streetSearch'].custom_widget = FinderSelectWidget
    label = u"Rechercher une rue"
    description = u""

    @form.action(u"Rechercher")
    def action_send(self, action, data):
        """search licences
        """
        context = aq_inner(self.context)
        urltool = getToolByName(context, 'portal_url')
        portal = urltool.getPortalObject()
        self.request.response.redirect(portal.absolute_url())
