# encoding: utf-8

from borg.localrole.interfaces import ILocalRoleProvider

from plone import api

from Products.CMFCore.WorkflowCore import WorkflowException

from zope.interface import implements


class GroupNotFoundError(Exception):
    """ """


class RoleNotFoundError(Exception):
    """ """


class LocalRoleAdapter(object):
    """
        borg.localrole adapter to set localrole following type and state configuration
    """
    implements(ILocalRoleProvider)

    mapping = {}

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal):
        """Grant permission for principal"""
        current_state = self.get_state()
        state_config = self.get_roles_mapping_for_state(current_state)
        if not state_config:
            return []
        if not state_config.get(principal, []):
            return ()
        return tuple(state_config.get(principal))

    def getAllRoles(self):
        """Grant permissions"""
        current_state = self.get_state()
        state_config = self.get_roles_mapping_for_state(current_state)
        if not state_config:
            yield ('', ('', ))
            raise StopIteration
        for principal, roles in state_config.items():
            yield (principal, tuple(roles))

    def get_roles_mapping_for_state(self, state):
        """
        Return the group/roles mapping of a given state.
        """
        group_roles_mapping = self.mapping.get(state, {})
        generated_mapping = {}

        for group_name, role_names in group_roles_mapping.iteritems():
            groups = self.compute_group_value(group_name)

            roles = []
            for role in role_names:
                roles.extend(self.compute_role_value(role))
            roles = list(set(roles))

            for group in groups:
                generated_mapping[group] = roles

        return generated_mapping

    def compute_value(self, value_name):
        """
        Values in the mapping can be either the value to return or a method name to
        call to dynamically compute the value.
        """
        if hasattr(self, value_name):
            value_computation_method = getattr(self, value_name)
            value = value_computation_method()
        else:
            value = [value_name]
        return value

    def compute_group_value(self, group_name):
        group_values = self.compute_value(group_name)
        for group_value in group_values:
            if not api.group.get(group_value):
                if hasattr(self, group_name):
                    msg = "Group '{}' computed by '{}' method does not exist.".format(group_value, group_name)
                else:
                    msg = "'{}' is neither an existing group nor a method on mapping object {}.".format(
                        group_name,
                        self,
                    )
                raise GroupNotFoundError(msg)
        return group_values

    def compute_role_value(self, role_name):
        role_values = self.compute_value(role_name)

        portal = api.portal.getSite()
        portal_roles = portal.acl_users.portal_role_manager
        registered_roles = portal_roles.listRoleIds()
        for role_value in role_values:
            if role_value not in registered_roles:
                if hasattr(self, role_name):
                    msg = "Role '{}' computed by '{}' method does not exist.".format(role_value, role_name)
                else:
                    msg = "'{}' is neither an existing role nor a method on mapping object {}.".format(
                        role_name,
                        self,
                    )
                raise RoleNotFoundError(msg)
        return role_values

    def get_state(self):
        """ Return the state of the current object """
        try:
            return api.content.get_state(obj=self.context)
        except (WorkflowException, api.portal.CannotGetPortalError):
            return None
