# -*- coding: utf-8 -*-


from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.urban import UrbanMessage as _
from Products.urban.UrbanEvent import UrbanEvent
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.urban.config import *
from Products.urban.utils import setOptionalAttributes

##code-section module-header #fill in your manual code here

##/code-section module-header

schema = Schema((

    TextField(
        name='commentForDPA',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label=_('urban_label_commentForDPA', default='CommentForDPA'),
        ),
        default_method='getDefaultText',
        default_content_type='text/html',
        default_output_type='text/x-html-safe',
        optional=True,
    ),

),
)

##code-section after-local-schema #fill in your manual code here
optional_fields = ['commentForDPA']
setOptionalAttributes(schema, optional_fields)
##/code-section after-local-schema

UrbanEventNotice_schema = BaseSchema.copy() + \
    getattr(UrbanEvent, 'schema', Schema(())).copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class UrbanEventNotice(UrbanEvent, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()
    implements(interfaces.IUrbanEventNotice)

    meta_type = 'UrbanEventNotice'
    _at_rename_after_creation = True

    schema = UrbanEventNotice_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods

    def transfer_folder_to_dpa(self):
        print "transfer_folder_to_dpa from the content"

    # Manually created methods


registerType(UrbanEventNotice, PROJECTNAME)
# end of class UrbanEventNotice

##code-section module-footer #fill in your manual code here
##/code-section module-footer

