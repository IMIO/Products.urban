# -*- coding: utf-8 -*-
#

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.CODT_BuildLicence import CODT_BuildLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.content.licence.EnvClassOne import EnvClassOne

from Products.urban.config import *


##code-section module-header #fill in your manual code here
##/code-section module-header



##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

RoadDecree_schema = CODT_BuildLicence.schema.copy()


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class RoadDecree(CODT_BuildLicence):
    """
    """
    implements(interfaces.IRoadDecree)

    meta_type = 'RoadDecree'

    RoadDecree_schema['roadAdaptation'].schemata = 'urban_road'

    schema = RoadDecree_schema
    ##code-section class-header #fill in your manual code here
    ##/code-section class-header



    def listEnvClassChoices(self):
        vocab = (

        )
        return DisplayList(vocab)


registerType(RoadDecree, PROJECTNAME)


# end of class EnvClassOne

##code-section module-footer #fill in your manual code here

##/code-section module-footer
