# -*- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.urban import UrbanMessage as _
from plone import api
from plone.stringinterp.adapters import BaseSubstitution
from plone.stringinterp.adapters import UserEmailSubstitution
from zope.component import adapter


@adapter(IContentish)
class FolderManagersMail(BaseSubstitution):

    category = _(u"Urban")
    description = _(u"Folder Manager E-mail")

    def get_folder_manager(self):
        curr_context = self.context
        while not hasattr(curr_context, "getFoldermanagers"):
            curr_context = aq_parent(curr_context)
            if IPloneSiteRoot.providedBy(curr_context):
                return None
        getFoldermanagers = getattr(curr_context, "getFoldermanagers", None)
        if not getFoldermanagers:
            return None
        return getFoldermanagers()

    def get_mail_from_folder_manager(self, folder_manager):
        current_user_mail = UserEmailSubstitution(self.context)
        if not folder_manager:
            return current_user_mail()
        email = folder_manager.getRawEmail()
        if email or email != "":
            return email
        plone_user_id = folder_manager.ploneUserId
        if not plone_user_id or plone_user_id == "":
            return current_user_mail()
        user = api.user.get(username=plone_user_id)
        if not user:
            return current_user_mail()
        email = user.getProperty("email", None)
        if not email:
            return current_user_mail()
        return email

    def safe_call(self):
        folder_managers = self.get_folder_manager()
        if not folder_managers:
            return ''
        output = ", ".join(
            list(
                set(
                    [
                        self.get_mail_from_folder_manager(folder_manager)
                        for folder_manager in folder_managers
                        if self.get_mail_from_folder_manager(folder_manager) != u""
                    ]
                )
            )
        )
        return output
