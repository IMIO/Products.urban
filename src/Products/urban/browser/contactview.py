from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
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
        self.request.set("disable_plone.rightcolumn", 1)
        self.request.set("disable_plone.leftcolumn", 1)

    def __call__(self):
        context = aq_inner(self.context)
        # either the parent is in URBAN_TYPES
        parent = context.aq_inner.aq_parent
        referer = self.request["HTTP_REFERER"]
        from_edit = (
            "portal_factory" in referer
            or referer == self.context.absolute_url() + "/edit"
        )
        if parent.portal_type in URBAN_TYPES and from_edit:
            return self.request.RESPONSE.redirect(parent.absolute_url())
        return super(ContactView, self).__call__()

    def getFields(self, exclude=[]):
        """ """

        def isDisplayable(field):
            if field.getName() in exclude:
                return False
            if not field.widget.visible:
                return False
            return True

        context = aq_inner(self.context)
        schema = context.__class__.schema
        fields = [
            field
            for field in schema.getSchemataFields("default")
            if isDisplayable(field)
        ]

        return fields

    def getLinkToLinkedLicence(self):
        """
        Return a link to the licence if available
        (protected by showLinkToLinkedLicence below)
        """
        context = aq_inner(self.context)
        # either the parent is in URBAN_TYPES
        parent = context.aq_inner.aq_parent
        parent_portal_type = parent.portal_type
        if parent_portal_type in URBAN_TYPES:
            return parent.absolute_url()
        # or we have a "came_from_licence_uid" in the REQUEST
        elif context.REQUEST.get("came_from_licence_uid", None):
            came_from_licence_uid = context.REQUEST.get("came_from_licence_uid", None)
            uid_catalog = getToolByName(context, "uid_catalog")
            linkedLicenceBrains = uid_catalog(UID=came_from_licence_uid)
            linkedLicence = linkedLicenceBrains[0].getObject()
            return linkedLicence.absolute_url()
        else:
            return parent.absolute_url()

    def showLinkToLinkedLicence(self):
        """
        Check if we have what necessary to show a link to the linked licence :
        either the parent is a licence, or we have a "came_from_licence_uid" in
        the REQUEST
        """
        context = aq_inner(self.context)
        res = False
        # we can show the link back to the reference if we are on an URBAN_TYPES
        # or on an UrbanEventInquiry (Claimants)
        allowed_parent_types = URBAN_TYPES + ["UrbanEventInquiry"]
        if context.aq_inner.aq_parent.portal_type in allowed_parent_types:
            res = True
        elif "came_from_licence_uid" in context.REQUEST:
            came_from_licence_uid = context.REQUEST.get("came_from_licence_uid", None)
            # check if we really have a 'came_from_licence_uid'
            if came_from_licence_uid:
                uid_catalog = getToolByName(context, "uid_catalog")
                linkedLicenceBrains = uid_catalog(UID=came_from_licence_uid)
                if linkedLicenceBrains:
                    res = True
        return res

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
            parent.absolute_url() + "#fieldsetlegend-urbaneventinquiry_recipients"
        )
