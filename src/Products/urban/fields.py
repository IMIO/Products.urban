# -*- coding: utf-8 -*-

from AccessControl import getSecurityManager
from Products.Archetypes import atapi


class SetOnceStringField(atapi.StringField):
    """StringField with "write once" semantics in the UI.

    Editable while empty (i.e. typically in the creation form); once a
    value is stored, the edit form hides the field.

    Managers can still edit the field at any time.

    Trusted code can still change the value via the generated mutator / field.set().
    """

    _properties = atapi.StringField._properties.copy()

    def isWritable(self, instance):
        # either the field is still empty
        if not self.getRaw(instance):
            return True
        # or you have admin rights
        return bool(getSecurityManager().checkPermission("Manage portal", instance))

    def checkPermission(self, mode, instance):
        if mode == "w" and not self.isWritable(instance):
            return False
        return atapi.StringField.checkPermission(self, mode, instance)
