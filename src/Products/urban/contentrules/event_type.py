# -*- coding: utf-8 -*-

from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.autoform import directives
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from z3c.form.browser.orderedselect import OrderedSelectWidget
from zope import schema
from zope.component import adapts, getUtility
from zope.formlib import form
from zope.interface import Interface, implements
from zope.schema.interfaces import IVocabularyFactory


class IEventTypeCondition(Interface):
    """Interface for the configurable aspects of a Event type condition.

    This is also used to create add and edit forms, below.
    """

    event_type = schema.Choice(
        title=_(u"Event Type"),
        vocabulary="urban.vocabularies.event_types",
        required=True,
    )


class EventTypeCondition(SimpleItem):
    """The actual persistent implementation of the Event type condition element."""

    implements(IEventTypeCondition, IRuleElementData)

    event_type = ""
    element = "urban.conditions.EventType"

    @property
    def summary(self):
        factory = getUtility(IVocabularyFactory, "urban.vocabularies.event_types")
        vocabulary = factory(api.portal.get())
        return u"Event Type : {}".format(vocabulary.by_value[self.event_type].title)


class EventTypeConditionExecutor(object):
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    implements(IExecutable)
    adapts(Interface, IEventTypeCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        event_type_condition = self.element.event_type
        config_event_types = self.event.object.getUrbaneventtypes().eventType
        if not config_event_types:
            config_event_types = []
        return event_type_condition in config_event_types


class EventTypeAddForm(AddForm):
    """An add form for event type condition."""

    form_fields = form.FormFields(IEventTypeCondition)
    label = _(u"Add Event type Condition")
    description = _(
        u"A Event type condition makes the rule apply "
        "only if Event type correspond to the one from the context."
    )
    form_name = _(u"Configure element")

    def create(self, data):
        c = EventTypeCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class EventTypeEditForm(EditForm):
    """An edit form for Event type condition"""

    form_fields = form.FormFields(IEventTypeCondition)
    label = _(u"Edit Event type Condition")
    description = _(
        u"A Event type condition makes the rule apply "
        "only if Event type correspond to the one from the context."
    )
    form_name = _(u"Configure element")
