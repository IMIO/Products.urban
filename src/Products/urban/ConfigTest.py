# encoding: utf-8
from Products.Five import BrowserView
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.Archetypes.BaseFolder import BaseFolder, BaseFolderSchema
from Products.Archetypes.ArchetypeTool import registerType
from AccessControl import ClassSecurityInfo
from zope.interface import implements
import interfaces

from Products.ATContentTypes.content.folder import ATBTreeFolder, ATBTreeFolderSchema


class ConfigTest(ATBTreeFolder, BrowserDefaultMixin):
    """ """

    security = ClassSecurityInfo()
    implements(interfaces.ITestConfig)

    meta_type = "ConfigTest"
    _at_rename_after_creation = True

    schema = ATBTreeFolderSchema.copy()


registerType(ConfigTest, "urban")
