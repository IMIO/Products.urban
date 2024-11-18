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


class ILicenceTypeCondition(Interface):
    """Interface for the configurable aspects of a Event type condition.

    This is also used to create add and edit forms, below.
    """

    licence_type = schema.List(
        title=_(u"Licence Type"),
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
        return u"Licence Type : {}".format(", ".join(values))


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
        if not hasattr(
            self.context,
            "get_parent_licence",
        ):
            return False
        context_type = self.context.get_parent_licence().portal_type
        if context_type is None:
            return False
        condition_types = getattr(self.element, "licence_type", None)
        if not condition_types and not isinstance(condition_types, list):
            return False

        return context_type in condition_types


class LicenceTypeAddForm(AddForm):
    """An add form for opinion to ask condition."""

    form_fields = form.FormFields(ILicenceTypeCondition)
    label = _(u"Add licence type Condition")
    description = _(
        u"A licence type condition makes the rule apply "
        "only when one of the licence type slelected correspond to the one of the context"
    )
    form_name = _(u"Configure element")

    def create(self, data):
        condition = LicenceTypeCondition()
        form.applyChanges(condition, self.form_fields, data)
        return condition


class LicenceTypeEditForm(EditForm):
    """An edit form for Opinion to ask condition"""

    form_fields = form.FormFields(ILicenceTypeCondition)
    label = _(u"Edit Opinion to ask Condition")
    description = _(
        u"A opinion to ask condition makes the rule apply "
        "only when one of the Opinion to ask slelected correspond to the one of the context"
    )
    form_name = _(u"Configure element")
