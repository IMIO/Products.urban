# -*- coding: utf-8 -*-

from plone.dexterity.browser import edit

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

#    def render(self):
#        return ViewPageTemplateFile("templates/parcel_edit.pt")(self)
