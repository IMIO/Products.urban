# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def setDefaultFolderManagersEvent(object, event):
    if object.checkCreationFlag():
        tool = getToolByName(object, 'portal_urban')
        object.setFoldermanagers(tool.getCurrentFolderManager(initials=False))
