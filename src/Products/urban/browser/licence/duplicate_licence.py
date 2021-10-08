# -*- coding: utf-8 -*-

from plone import api
from plone.autoform import directives
from plone.z3cform.layout import FormWrapper

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

from z3c.form import button
from z3c.form import form, field
from z3c.form.browser.orderedselect import OrderedSelectWidget

from zope import schema
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory

from Products.urban import UrbanMessage as _
from Products.urban.events.licenceEvents import postCreationActions
from Products.urban.utils import getLicenceFolder


class TabsToDuplicateField(schema.Tuple):
    """
    """


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
    tabs_to_duplicate = TabsToDuplicateField(
        title=_(u'Tabs to duplicate'),
        value_type=schema.Choice(
            vocabulary='urban.vocabularies.licence_tabs',
        ),
        required=False,
    )


class DefaultTabsToDuplicate(object):
    """ """

    def __init__(self, licence, request, form, field, widget):
        self.licence = licence
        self.request = request
        self.form = form
        self.field = field
        self.widget = widget

    def get(self):
        """ To implements."""
        voc_factory = getUtility(IVocabularyFactory, 'urban.vocabularies.licence_tabs')
        tabs_voc = voc_factory(self.licence)
        return tabs_voc.by_token.keys()


class DuplicateLicenceForm(form.Form):

    method = 'get'
    fields = field.Fields(IAddressSearchForm)
    ignoreContext = True

    def updateWidgets(self):
        super(DuplicateLicenceForm, self).updateWidgets()

    @button.buttonAndHandler(u'Duplicate')
    def handleDuplicate(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        site = api.portal.get()
        destination_type = data['destination_type']
        destination_folder = getLicenceFolder(destination_type)
        duplicated_licence_id = destination_folder.invokeFactory(
            destination_type,
            id=site.generateUniqueId(destination_type),
        )
        duplicated_licence = getattr(destination_folder, duplicated_licence_id)
        original_licence = self.context

        if data['duplicate_parcels']:
            for parcel in original_licence.getParcels():
                api.content.copy(source=parcel, target=duplicated_licence)

        if data['duplicate_applicants']:
            for contact in original_licence.objectValues('Applicant'):
                api.content.copy(source=contact, target=duplicated_licence)
            for contact in original_licence.objectValues('Corporation'):
                api.content.copy(source=contact, target=duplicated_licence)

        for tab in data['tabs_to_duplicate']:
            fields = original_licence.schema.getSchemataFields(tab)
            for original_field in fields:
                destination_field = duplicated_licence.getField(original_field.getName())
                if destination_field:
                    destination_mutator = destination_field.getMutator(duplicated_licence)
                    value = original_field.getAccessor(original_licence)()
                    if destination_field.enforceVocabulary:
                        if destination_field.validate(value, duplicated_licence) is not None:
                            continue
                    destination_mutator(value)

        new_subject = data['new_licence_subject']
        if new_subject:
            duplicated_licence.setLicenceSubject(new_subject)
        duplicated_licence.setReference(duplicated_licence.getDefaultReference())
        postCreationActions(duplicated_licence, None)

        duplicated_licence.reindexObject()
        duplicated_licence.processForm()

        return self.request.RESPONSE.redirect(duplicated_licence.absolute_url())


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
