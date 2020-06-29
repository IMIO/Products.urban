# -*- coding: utf-8 -*-

from plone.dexterity.browser import edit
from plone.dexterity.browser import view


class ParcelEditForm(edit.DefaultEditForm):
    """
    Parcel custom Edit form.
    """

    def __init__(self, context, request):
        super(ParcelEditForm, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class ParcelView(view.DefaultView):
    """
    Parcel display view to be called with an overlay in z3c.table listings.
    """

    def __init__(self, context, request):
        super(ParcelView, self).__init__(context, request)
        self.context = context
        self.request = request
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)


class ParcelViewRedirects(view.DefaultView):
    """
    Parcel default view redirects to the parent container.
    """

    def __call__(self):
        return self.context.REQUEST.RESPONSE.redirect(
            self.context.aq_parent.absolute_url()
        )
