# -*- coding: utf-8 -*-

from plone import api

from Acquisition import aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.urban import UrbanMessage as _
from Products.urban.config import URBAN_TYPES


class ContactView(BrowserView):
    """
      This manage the view of every Contacts :
      Applicant, Architect, Geometrician, Notary
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def __call__(self):
        context = aq_inner(self.context)
        # either the parent is in URBAN_TYPES
        parent = context.aq_inner.aq_parent
        referer = self.request['HTTP_REFERER']
        from_edit = 'portal_factory' in referer or referer == self.context.absolute_url() + '/edit'
        if parent.portal_type in URBAN_TYPES and from_edit:
            return self.request.RESPONSE.redirect(parent.absolute_url())
        return super(ContactView, self).__call__()

    def getFields(self, exclude=[]):
        """
        """
        def isDisplayable(field):
            if field.getName() in exclude:
                return False
            if not field.widget.visible:
                return False
            return True

        context = aq_inner(self.context)
        schema = context.__class__.schema
        fields = [field for field in schema.getSchemataFields('default') if isDisplayable(field)]

        return fields

    def getLinkToLinkedLicence(self):
        """
          Return a link to the licence or parent folder.
        """
        context = aq_inner(self.context)
        # either the parent is in URBAN_TYPES
        parent = context.aq_inner.aq_parent
        parent_portal_type = parent.portal_type
        if parent_portal_type in URBAN_TYPES:
            return parent.absolute_url()
        # or we have a "came_from_licence_uid" in the REQUEST
        elif context.REQUEST.get('came_from_licence_uid', None):
            came_from_licence_uid = context.REQUEST.get('came_from_licence_uid', None)
            uid_catalog = getToolByName(context, 'uid_catalog')
            linkedLicenceBrains = uid_catalog(UID=came_from_licence_uid)
            linkedLicence = linkedLicenceBrains[0].getObject()
            return linkedLicence.absolute_url()
        else:
            url = parent.absolute_url()
            if self.context.portal_type == 'Claimant':
                url += '#fieldsetlegend-event_inquiry_claimants'
            return url

    def getContactLegendValue(self):
        """
          Generates a label that will be used in the legend of a fieldset
          This value will be translated in the template using i18n:translate=""
        """
        context = aq_inner(self.context)
        return "%s data" % context.portal_type


class RecipientCadastreView(BrowserView):
    """
      This manage the view of every RecipientCadastre
    """

    def __call__(self):
        context = aq_inner(self.context)
        parent = context.aq_inner.aq_parent
        return self.request.RESPONSE.redirect(
            parent.absolute_url() + '/#fieldsetlegend-urbaneventinquiry_recipients'
        )


class CopyRecipientCadastreToClaimantView(BrowserView):
    """
    Copy to claimant view.
    """

    def __call__(self):
        site = api.portal.get()
        plone_utils = api.portal.get_tool('plone_utils')

        recipient = self.context
        inquiry_event = self.context.aq_parent

        claimant_arg = {}
        claimant_arg['name1'] = recipient.name
        claimant_arg['name2'] = recipient.firstname
        claimant_arg['street'] = recipient.street
        claimant_arg['number'] = recipient.number
        claimant_arg['city'] = recipient.city
        claimant_arg['zipcode'] = recipient.zipcode
        claimant_arg['id'] = site.plone_utils.normalizeString("claimant_" + recipient.id)

        catalog = api.portal.get_tool('portal_catalog')
        result = catalog(id=claimant_arg['id'], portal_type='Claimant')
        redirection = self.request.response.redirect(inquiry_event.absolute_url() + '/#fieldsetlegend-urbaneventinquiry_recipients')
        if result:
            plone_utils.addPortalMessage(_('urban_claimant_already_exists'), type="error")
            return redirection

        inquiry_event.invokeFactory('Claimant', **claimant_arg)
        plone_utils.addPortalMessage(
            _('urban_recipient_copied_to_claimants'),
            type="info")

        return redirection
