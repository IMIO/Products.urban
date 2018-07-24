# -*- coding: utf-8 -*-
#

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
from Products.urban import interfaces
from Products.urban.content.licence.EnvironmentLicence import EnvironmentLicence
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget
from Products.urban.content.licence.EnvClassOne import EnvClassOne

from Products.urban.config import *


##code-section module-header #fill in your manual code here
##/code-section module-header

schema = Schema((
  StringField(
          name='envclasschoices',
          default='ukn',
          widget=MasterSelectWidget(
                  label='Type de classe d\'environement',
                  label_msgid='urban_label_listenvclasschoices',
                  i18n_domain='urban',
          ),
          schemata='urban_description',
          multiValued=1,
          vocabulary='listEnvClassChoices',
  ),
),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

EnvClassBordering_schema = EnvClassOne.schema.copy() + schema.copy()


##code-section after-schema #fill in your manual code here
##/code-section after-schema

class EnvClassBordering(EnvClassOne):
  """
  """
  implements(interfaces.IEnvClassBordering)

  meta_type = 'EnvClassBordering'

  schema = EnvClassBordering_schema
  ##code-section class-header #fill in your manual code here
  ##/code-section class-header



  def listEnvClassChoices(self):
    vocab = (
      ('ukn', 'Non determiné'),
      ('EnvClassOne', 'classe 1'),
      ('EnvClassTwo', 'classe 2'),
    )
    return DisplayList(vocab)


registerType(EnvClassBordering, PROJECTNAME)


# end of class EnvClassOne

##code-section module-footer #fill in your manual code here

##/code-section module-footer
