# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def setDefaultFolderManagersEvent(licence, event):
    if licence.checkCreationFlag():
        tool = getToolByName(licence, 'portal_urban')
        licence.setFoldermanagers(tool.getCurrentFolderManager(licence, initials=False))


def postCreationActions(licence, event):
    # set permissions on licence
    _setManagerPermissionOnLicence(licence)
    # check the numerotation need to be incremented
    _checkNumerotation(licence)
    # update the licence title
    updateLicenceTitle(licence, event)


def updateLicenceTitle(licence, event):
    licence.updateTitle()
    licence.reindexObject()


def _setManagerPermissionOnLicence(licence):
    #there is no need for other users than Managers to List folder contents
    #set this permission here if we use the simple_publication_workflow...
    licence.manage_permission('List folder contents', ['Manager', ], acquire=0)


def _checkNumerotation(licence):
    tool = getToolByName(licence, 'portal_urban')
    #increment the numerotation in the tool only if its the one that has been generated
    if tool.generateReference(licence) == licence.getReference():
        tool.incrementNumerotation(licence)
