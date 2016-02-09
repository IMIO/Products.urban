# -*- coding: utf-8 -*-

from urban.schedule.content.task_user import AssignTaskUser


class LicenceFolderManager(AssignTaskUser):
    """
    Adapts a TaskContainer(the licence) into a default user
    to assign to its tasks (the licence folder manager).
    """

    def user_id(self, **kwargs):
        licence = self.task_container
        folder_manager = licence.getFoldermanagers()[0]
        return folder_manager.getPloneUserId()
