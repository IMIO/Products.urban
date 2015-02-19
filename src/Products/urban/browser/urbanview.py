# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName

from Products.Five import BrowserView

from Products.urban import UrbanMessage as _
from Products.urban.browser.table.urbantable import LicenceListingTable
from Products.urban.browser.table.urbantable import AllLicencesListingTable
from Products.urban.config import ORDERED_URBAN_TYPES
from Products.urban import utils

from plone import api

from zope.i18n import translate


class UrbanView(BrowserView):
    """
      This manage the view of urban
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def isUrbanManager(self):
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        return member.has_role('Manager') or member.has_role('Editor', getToolByName(context, 'portal_urban'))

    def renderLicenceListing(self):
        context = aq_inner(self.context)
        if context.getProperty('urbanConfigId'):
            licencelisting = LicenceListingTable(self.context, self.request)
        else:
            licencelisting = AllLicencesListingTable(self.context, self.request)
        licencelisting.update()
        return '%s%s' % (licencelisting.render(), licencelisting.renderBatch())

    def getDefaultSort(self):
        context = aq_inner(self.context)
        if context.getProperty('urbanConfigId'):
            return 'sortable_title'
        else:
            return 'created'

    def getArgument(self, key_to_match, default=''):
        request = aq_inner(self.request)
        if type(key_to_match) == list:
            return dict([(key, request.get(key, '')) for key in key_to_match])
        request = aq_inner(self.request)
        return request.get(key_to_match, default)

    def listFolderManagers(self):
        """
          Returns the available folder managers
        """
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban')
        currentfoldermanager = utils.getCurrentFolderManager()
        currentfoldermanager_uid = currentfoldermanager and currentfoldermanager.UID() or ''
        foldermanagers = urban_tool.foldermanagers.objectValues()

        foldermanagers = [(fm.UID(), fm.Title().split('(')[0]) for fm in foldermanagers if fm.UID() != currentfoldermanager_uid]

        return foldermanagers

    def amIFolderManager(self):
        """
         Return the folder manager bound to the current plone id user if it exists
        """
        return utils.getCurrentFolderManager()

    def listAvailableStates(self):
        """
         return available licence states
        """
        return ['in_progress', 'accepted', 'refused', 'incomplete']

    def listBatchSizes(self):
        """
        """
        return ['20', '30', '50', '100']


class UrbanRootView(UrbanView):
    """
      This manage the view of urban root folder
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request

    def getLicenceTypes(self):
        return ORDERED_URBAN_TYPES

    def getLicenceCreationURL(self, licencetype):
        context = aq_inner(self.context)
        base_url = context.absolute_url()
        folder_id = utils.getLicenceFolderId(licencetype)
        url = '{base_url}/{folder_id}/createObject?type_name={licencetype}'.format(
            base_url=base_url, folder_id=folder_id, licencetype=licencetype)
        return url

    def mayAddLicence(self, licencetype):
        licence_folder = utils.getLicenceFolder(licencetype)
        return licencetype in [t.id for t in licence_folder.allowedContentTypes()]

    def getLinkClass(self, licencetype):
        return "content-shortcuts contenttype-{}".format(licencetype.lower())

    def getLicenceFolderLink(self, licencetype):
        klass = self.getLinkClass(licencetype)
        href = utils.getLicenceFolder(licencetype).absolute_url()
        folder_id = utils.getLicenceFolderId(licencetype)
        link_content = translate(_(folder_id), context=self.request)
        link_template = u'<a class="{klass}" href="{href}">{link_content}</a>'
        link = link_template.format(
            klass=klass,
            href=href,
            link_content=link_content,
        )
        return link

    def getLicenceCreationLink(self, licencetype):
        if not self.mayAddLicence(licencetype):
            return ''
        href = self.getLicenceCreationURL(licencetype)
        link_template = (
            u'<a href="{href}" id="create-{licencetype}-link">'
            u'<img class="urban-add-icon" src="icon_add.gif" /></a>'
        )
        link = link_template.format(
            href=href,
            licencetype=licencetype,
        )
        return link


class MayAccessUrban(BrowserView):
    """
     This view is is used in the python expresssion to evaluate the display
     of 'portal_tabs' actions (see profiles/default/actions.xml)
    """

    def __call__(self):
        """
          Test if the current user can acess urban view
        """
        portal = api.portal.get()
        sm = getSecurityManager()

        return sm.checkPermission('View', getattr(portal, 'urban'))
