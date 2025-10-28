# encoding: utf-8
from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.folder import ATBTreeFolder
from Products.ATContentTypes.content.folder import ATBTreeFolderSchema
from Products.Archetypes.ArchetypeTool import registerType
from Products.Archetypes.BaseFolder import BaseFolder
from Products.Archetypes.BaseFolder import BaseFolderSchema
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Five import BrowserView
from zope.interface import implements

import interfaces


class ConfigTest(ATBTreeFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ITestConfig)

    meta_type = "ConfigTest"
    _at_rename_after_creation = True

    schema = ATBTreeFolderSchema.copy()


registerType(ConfigTest, "urban")
