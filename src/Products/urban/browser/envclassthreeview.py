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
        if not self.context.getApplicants():
            plone_utils.addPortalMessage(_('warning_add_a_proprietary'), type="warning")
        if self.hasOutdatedParcels():
            plone_utils.addPortalMessage(_('warning_outdated_parcel'), type="warning")

    def getRubrics(self):
        """
        display the rubrics number, their class and then the text
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        rubric_uids = context.getField('rubrics').getRaw(context)
        rubric_brains = catalog(UID=rubric_uids)
        return ['<p>%s</p>%s' % (brain.Title.split(':')[0], brain.Description) for brain in rubric_brains]

    def _sortConditions(self, conditions):
        """
        sort exploitation conditions in this order: CI & CS, CI, CS
        """
        order = ['CI & CS', 'CI', 'CS']
        sorted_conditions = dict([(val, [],) for val in order])
        for cond in conditions:
            val = cond.getExtraValue()
            sorted_conditions[val].append({'type':val, 'url':cond.absolute_url(), 'title':cond.Title()})
        sort = []
        for val in order:
            sort.extend(sorted_conditions[val])
        return sort

    def getMinimumConditions(self):
        """
        sort the conditions from the field 'minimumLegalConditions'  by type (integral, sectorial, ...)
        """
        context = aq_inner(self.context)
        min_conditions = context.getMinimumLegalConditions()
        return self._sortConditions(min_conditions)

    def getAdditionalConditions(self):
        """
        sort the conditions from the field 'additionalLegalConditions'  by type (integral, sectorial, ...)
        """
        context = aq_inner(self.context)
        sup_conditions = context.getAdditionalLegalConditions()
        return self._sortConditions(sup_conditions)

class EnvClassThreeMacros(LicenceView):
    """
      This manage the macros of EnvClassThree
    """
