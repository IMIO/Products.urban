# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IContextWrapper
from zope import schema
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
from zope.schema.interfaces import IVocabularyFactory


class ILicenceTypeCondition(Interface):
    """Interface for the configurable aspects of a Event type condition.

    This is also used to create add and edit forms, below.
    """

    licence_type = schema.List(
        title=_(u"Event's parent licence types"),
        required=True,
        value_type=schema.Choice(
            vocabulary="urban.vocabularies.licence_types",
        ),
    )


class LicenceTypeCondition(SimpleItem):
    """The actual persistent implementation of the Event type condition element."""

    implements(ILicenceTypeCondition, IRuleElementData)

    licence_type = []
    element = "urban.conditions.licence_type"

    @property
    def summary(self):
        factory = getUtility(IVocabularyFactory, "urban.vocabularies.licence_types")
        vocabulary = factory(api.portal.get())
        values = [
            vocabulary.by_value[opinion].title for opinion in list(self.licence_type)
        ]
        return u"Event's parent licence types : {}".format(", ".join(values))


class LicenceTypeConditionExecutor(object):
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    implements(IExecutable)
    adapts(Interface, ILicenceTypeCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        event_object = self.event.object
        if IContextWrapper.providedBy(event_object):
            event_object = aq_inner(event_object.context)

        if not hasattr(
            event_object,
            "get_parent_licence",
        ):
            return False
        parent_type = event_object.get_parent_licence().portal_type
        if parent_type is None:
            return False
        condition_types = getattr(self.element, "licence_type", None)
        if not condition_types or not isinstance(condition_types, list):
            return False

        return parent_type in condition_types


class LicenceTypeAddForm(AddForm):
    """An add form for event's parent licence types condition."""

    form_fields = form.FormFields(ILicenceTypeCondition)
    label = _(u"Add event's parent licence types condition")
    description = _(
        u"An event's parent licence type condition causes the rule to apply "
        "only when one of the selected event's parent licence types matches that of the parent event."
    )
    form_name = _(u"Configure element")

    def create(self, data):
        condition = LicenceTypeCondition()
        form.applyChanges(condition, self.form_fields, data)
        return condition


class LicenceTypeEditForm(EditForm):
    """An edit form for event's parent licence types condition"""

    form_fields = form.FormFields(ILicenceTypeCondition)
    label = _(u"Edit event's parent licence types condition")
    description = _(
        u"An event's parent licence type condition causes the rule to apply "
        "only when one of the selected event's parent licence types matches that of the parent event."
    )
    form_name = _(u"Configure element")
