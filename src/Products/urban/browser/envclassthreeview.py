from Acquisition import aq_inner
from Products.urban.browser.licenceview import LicenceView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class EnvClassThreeView(LicenceView):
    """
      This manage the view of EnvClassThree
    """
    def __init__(self, context, request):
        super(LicenceView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        if not self.context.getParcels():
            plone_utils.addPortalMessage(_('warning_add_a_parcel'), type="warning")
        if not self.context.getProprietaries():
            plone_utils.addPortalMessage(_('warning_add_a_proprietary'), type="warning")
        if self.hasOutdatedParcels():
            plone_utils.addPortalMessage(_('warning_outdated_parcel'), type="warning")

    def getRubrics(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        rubric_uids = context.getField('rubrics').getRaw(context)
        rubric_brains = catalog(UID=rubric_uids)
        return ['<p>%s</p>%s' % (brain.Title.split(':')[0], brain.Description) for brain in rubric_brains]

class EnvClassThreeMacros(LicenceView):
    """
      This manage the macros of EnvClassThree
    """
