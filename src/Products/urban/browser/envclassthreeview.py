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

    def getInquiriesForDisplay(self):
        """
          Returns the inquiries to display on the buildlicence_view
          This will move to the buildlicenceview when it will exist...
        """
        context = aq_inner(self.context)
        inquiries = context.getInquiries()
        if not inquiries:
            #we want to display at least the informations about the inquiry
            #defined on the licence even if no data have been entered
            inquiries.append(context)
        return inquiries

    def getRubrics(self):
        """
        display the rubrics number, their class and then the text
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        rubric_uids = context.getField('rubrics').getRaw(context)
        rubric_brains = catalog(UID=rubric_uids)
        rubrics = [brain.getObject() for brain in rubric_brains]
        rubrics_display = ['<p>%s</p>%s' % (rub.getNumber(), rub.Description()) for rub in rubrics]
        return rubrics_display

    def _sortConditions(self, conditions):
        """
        sort exploitation conditions in this order: CI/CS, CI, CS
        """
        order = ['CI/CS', 'CI', 'CS', 'CS-Eau']
        sorted_conditions = dict([(val, [],) for val in order])
        for cond in conditions:
            val = cond.getExtraValue()
            sorted_conditions[val].append({'type': val, 'url': cond.absolute_url() + '/description/getRaw', 'title': cond.Title()})
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
