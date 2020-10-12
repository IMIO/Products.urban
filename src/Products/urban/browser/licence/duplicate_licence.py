# -*- coding: utf-8 -*-

# from plone import api
from plone.autoform import directives
from plone.z3cform.layout import FormWrapper

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form import button
from z3c.form import form, field
from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope.interface import Interface
from zope import schema
from Products.urban import UrbanMessage as _


class IAddressSearchForm(Interface):

    destination_type = schema.Choice(
        title=_(u'Destination type'),
        vocabulary='urban.vocabularies.licence_types',
        required=True,
        default='',
    )

    new_licence_subject = schema.TextLine(
        title=_(u'New licence subject'),
        required=False
    )

    duplicate_parcels = schema.Bool(
        title=_(u'Duplicate parcels'),
        default=True,
        required=False,
    )

    duplicate_applicants = schema.Bool(
        title=_(u'Duplicate applicants'),
        default=True,
        required=False,
    )

    directives.widget('tabs_to_duplicate', OrderedSelectWidget)
    tabs_to_duplicate = schema.Tuple(
        title=_(u'Tabs to duplicate'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.licence_tabs',
        ),
        required=False,
    )


class DuplicateLicenceForm(form.Form):

    method = 'get'
    fields = field.Fields(IAddressSearchForm)
    ignoreContext = True

    def updateWidgets(self):
        super(DuplicateLicenceForm, self).updateWidgets()

    @button.buttonAndHandler(u'Duplicate')
    def handleSearch(self, action):
        data, errors = self.extractData()
        if errors:
            return False


class DuplicateLicenceFormView(FormWrapper):
    """
    """
    form = DuplicateLicenceForm
    index = ViewPageTemplateFile('templates/duplicate_licence.pt')

    def __init__(self, context, request):
        super(DuplicateLicenceFormView, self).__init__(context, request)
        # disable portlets on licences
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def search_submitted(self):
        """
        """
        form_inputs = self.form_instance.extractData()[0]
        submitted = any(form_inputs.values())
        return submitted

    def get_search_args(self):
        """
        """
        form_inputs = self.form_instance.extractData()[0]
        return form_inputs

    def update(self):
        super(DuplicateLicenceFormView, self).update()
