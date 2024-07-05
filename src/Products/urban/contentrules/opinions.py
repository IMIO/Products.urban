# -*- coding: utf-8 -*-

from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules import PloneMessageFactory as _
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from plone.autoform import directives
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from z3c.form.browser.orderedselect import OrderedSelectWidget
from collective.plonefinder.widgets.referencewidget import FinderSelectWidget
from z3c.form.browser.orderedselect import SequenceChoiceSelectFieldWidget
from zope import schema
from zope.component import adapts, getUtility
from zope.formlib import form
from zope.interface import Interface, implements
from zope.schema.interfaces import IVocabularyFactory


class IOpinionsCondition(Interface):
    """Interface for the configurable aspects of a Event type condition.

    This is also used to create add and edit forms, below.
    """

    opinions_to_ask = schema.List(
        title=_(u"Opinion to ask"),
        required=True,
        value_type=schema.Choice(
            vocabulary="urban.vocabularies.all_opinions_to_ask",
        )
    )
    
    


class OpinionsCondition(SimpleItem):
    """The actual persistent implementation of the Event type condition element."""

    implements(IOpinionsCondition, IRuleElementData)

    opinions_to_ask = []
    element = "urban.conditions.Opinions"

    @property
    def summary(self):
        factory = getUtility(IVocabularyFactory, "urban.vocabularies.all_opinions_to_ask")
        vocabulary = factory(api.portal.get())
        values = [vocabulary.by_value[opinion].title for opinion in list(self.opinions_to_ask)]
        return u"Event Type : {}".format(", ".join(values))


class OpinionsConditionExecutor(object):
    """The executor for this condition.

    This is registered as an adapter in configure.zcml
    """

    implements(IExecutable)
    adapts(Interface, IOpinionsCondition, Interface)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        opinions_to_ask_condition = list(self.element.opinions_to_ask)
        context_uid = self.event.object.getUrbaneventtypes().UID()
        return any([opinion == context_uid for opinion in opinions_to_ask_condition])


class OpinionsAddForm(AddForm):
    """An add form for opinion to ask condition."""

    form_fields = form.FormFields(IOpinionsCondition)
    label = _(u"Add Opinion to ask Condition")
    description = _(
        u"A opinion to ask condition makes the rule apply "
        "only when one of the Opinion to ask slelected correspond to the one of the context"
    )
    form_name = _(u"Configure element")

    def create(self, data):
        c = OpinionsCondition()
        form.applyChanges(c, self.form_fields, data)
        return c


class OpinionsEditForm(EditForm):
    """An edit form for Opinion to ask condition"""

    form_fields = form.FormFields(IOpinionsCondition)
    label = _(u"Edit Opinion to ask Condition")
    description = _(
        u"A opinion to ask condition makes the rule apply "
        "only when one of the Opinion to ask slelected correspond to the one of the context"
    )
    form_name = _(u"Configure element")
