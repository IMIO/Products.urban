# encoding: utf-8

from plone.app.contentrules.rule import Rule
from plone.app.contentrules import api as cr_api
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.contentrules.rule.interfaces import IRuleCondition
from plone import api
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.globalrequest import getRequest


class ContentRulesUtils:
    """Utility class to manage Plone content rules programmatically."""

    @staticmethod
    def _get_request(context=None):
        """Return the current request, falling back to ``context.REQUEST``."""
        request = getRequest()
        if request is None and context is not None:
            request = context.REQUEST
        return request

    @staticmethod
    def _get_rule_obj(rule_id):
        """Traverse to the rule object (required for adding conditions/actions)."""
        portal = api.portal.get()
        return portal.restrictedTraverse("++rule++{}".format(rule_id))

    @staticmethod
    def get_storage():
        """Return the ``IRuleStorage`` utility."""
        return getUtility(IRuleStorage)

    @staticmethod
    def get_rule(rule_id):
        """Return a rule by *rule_id*, or ``None`` if it does not exist."""
        storage = ContentRulesUtils.get_storage()
        return storage.get(rule_id)

    @staticmethod
    def rule_exists(rule_id):
        """Check whether a rule with *rule_id* already exists in storage."""
        return rule_id in ContentRulesUtils.get_storage()

    @staticmethod
    def create_content_rule(title, event_interface, rule_id):
        """Create a new content rule and register it in the rule storage.

        Parameters
        ----------
        title : unicode
            Human-readable title of the rule.
        event_interface : interface
            The event interface that triggers the rule.
        rule_id : str
            Unique identifier for the rule.

        Returns
        -------
        str or None
            The *rule_id* of the newly created rule, or ``None`` if a rule
            with that id already exists.
        """
        storage = ContentRulesUtils.get_storage()

        if rule_id in storage:
            return None

        rule = Rule()
        rule.title = title
        rule.event = event_interface
        storage[rule_id] = rule

        return rule_id

    @staticmethod
    def delete_rule(rule_id):
        """Delete a content rule from the rule storage.

        Returns
        -------
        bool
            ``True`` if the rule was deleted, ``False`` if it did not exist.
        """
        storage = ContentRulesUtils.get_storage()
        if rule_id in storage:
            del storage[rule_id]
            return True
        return False

    @staticmethod
    def add_condition(rule_id, condition_name, data):
        """Add a condition to an existing content rule.

        Parameters
        ----------
        rule_id : str
            The id of the target rule.
        condition_name : str
            The registered name of the condition element
            (e.g. ``'urban.conditions.licence_type'``).
        data : dict
            Mapping of condition configuration values.

        Returns
        -------
        The object returned by ``createAndAdd``.
        """
        request = ContentRulesUtils._get_request()
        rule_obj = ContentRulesUtils._get_rule_obj(rule_id)

        condition_element = getUtility(IRuleCondition, name=condition_name)
        adding = getMultiAdapter((rule_obj, request), name="+condition")
        condition_addview = getMultiAdapter(
            (adding, request), name=condition_element.addview
        )
        return condition_addview.createAndAdd(data=data)

    @staticmethod
    def add_action(rule_id, action_name, data):
        """Add an action to an existing content rule.

        Parameters
        ----------
        rule_id : str
            The id of the target rule.
        action_name : str
            The registered name of the action element
            (e.g. ``'plone.actions.Mail'``).
        data : dict
            Mapping of action configuration values.

        Returns
        -------
        The object returned by ``createAndAdd``.
        """
        request = ContentRulesUtils._get_request()
        rule_obj = ContentRulesUtils._get_rule_obj(rule_id)

        action_element = getUtility(IRuleAction, name=action_name)
        adding = getMultiAdapter((rule_obj, request), name="+action")
        action_addview = getMultiAdapter((adding, request), name=action_element.addview)
        return action_addview.createAndAdd(data=data)

    @staticmethod
    def assign_rule(context, rule_id):
        """Assign a content rule to *context*.

        The rule will be **disabled** by default after assignment; call
        :meth:`enable_rule` afterwards if you want it active.
        """
        cr_api.assign_rule(context, rule_id)

    @staticmethod
    def unassign_rule(context, rule_id):
        """Remove a content rule assignment from *context*."""
        cr_api.unassign_rule(context, rule_id)

    @staticmethod
    def enable_rule(context, rule_id, bubbles=True):
        """Enable a rule assignment on *context*.

        Parameters
        ----------
        context : content object
            The object the rule is assigned to.
        rule_id : str
            The id of the rule to enable.
        bubbles : bool
            If ``True`` (default) the rule also applies to sub-folders.
        """
        cr_api.edit_rule_assignment(context, rule_id, bubbles=bubbles, enabled=True)

    @staticmethod
    def disable_rule(context, rule_id, bubbles=True):
        """Disable a rule assignment on *context*.

        Parameters
        ----------
        context : content object
            The object the rule is assigned to.
        rule_id : str
            The id of the rule to disable.
        bubbles : bool
            Kept so the bubbling flag can be changed at the same time.
        """
        cr_api.edit_rule_assignment(context, rule_id, bubbles=bubbles, enabled=False)
