# -*- coding: utf-8 -*-

from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm
from plone.app.contentrules.browser.formhelper import EditForm
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from zope import schema
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.interface import implements
from zope.interface import Interface
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
        config_event_types = []
        event_type_condition = self.element.event_type
        if not event_type_condition:
            return False
        event_config = self.event.object.getUrbaneventtypes()
        if event_config and hasattr(event_config, "eventTypeType"):
            config_event_types = event_config.eventTypeType
        if not self.check_if_iterrable(config_event_types):
            return False
        return event_type_condition in config_event_types

    def check_if_iterrable(self, value):
        if isinstance(value, list) or isinstance(value, tuple):
            return True
        try:
            _ = iter(value)
            return True
        except TypeError:
            return False


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
