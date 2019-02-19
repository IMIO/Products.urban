# -*- coding: utf-8 -*-

from imio.schedule.content.logic import AssignTaskUser


class LicenceFolderManager(AssignTaskUser):
    """
    Adapts a TaskContainer(the licence) into a default user
    to assign to its tasks (the licence folder manager).
    """

    def user_id(self):
        licence = self.task_container
        if licence.getFoldermanagers():
            folder_manager = licence.getFoldermanagers()[0]
            return folder_manager.getPloneUserId()
        return 'to_assign'
