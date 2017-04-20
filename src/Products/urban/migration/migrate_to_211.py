# encoding: utf-8
from Products.CMFCore.utils import getToolByName
from Products.urban.interfaces import IBuildLicence
from plone import api
from zope.component import createObject
try:
    from Products.urban.setuphandlers import setupTest
except:
    def setupTest():
        raise NotImplementedError("Can't find setupTest from Products.urban.setuphandlers")
import logging

logger = logging.getLogger('urban: migrations')


def AddFolderTest(context):
    """
    @param context:
    @return:
    """
    # setupTest(context)



def migrate(context):
    logger = logging.getLogger('urban: migrate to 2.1.1')
    logger.info("starting migration steps")
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runAllImportStepsFromProfile('profile-Products.urban:default')
    logger.info("reinstalling urban done!")
    AddFolderTest(api.portal.get())
    logger.info("migration done!")