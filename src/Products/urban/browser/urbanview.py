from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.urban.browser.urbantable import LicenceListingTable, AllLicencesListingTable


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
        currentfoldermanager = urban_tool.getCurrentFolderManager(initials=False)
        currentfoldermanager_uid = currentfoldermanager and currentfoldermanager.UID() or ''
        foldermanagers = urban_tool.foldermanagers.objectValues()
        return [(fm.UID(), fm.Title().split('(')[0]) for fm in foldermanagers if fm.UID() != currentfoldermanager_uid]

    def amIFolderManager(self):
        """
         return the folder manager bound to the current plone id user if it exists
        """
        context = aq_inner(self.context)
        urban_tool = getToolByName(context, 'portal_urban')
        return urban_tool.getCurrentFolderManager(initials=False)

    def listAvailableStates(self):
        """
         return available licence states
        """
        return ['in_progress', 'accepted', 'refused', 'incomplete']

    def listBatchSizes(self):
        """
        """
        return ['20', '30', '50', '100']


class UrbanViewMacros(BrowserView):
    """
      This manage the macros of urban view
    """
