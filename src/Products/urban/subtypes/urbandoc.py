# -*- coding: utf-8 -*-

from Products.CMFPlone import PloneMessageFactory as _
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import FileWidget
from Products.validation import V_REQUIRED
from Products.ContentTypeValidator.validator import ContentTypeValidator

from plone.app.blob.subtypes.file import SchemaExtender
from plone.app.blob.subtypes.file import ExtensionBlobField

#  We customise 'file' field by adding a validator (to check the content is an odt file) on it.


class UrbanDocExtender(SchemaExtender):

    fields = [
        ExtensionBlobField(
            'file',
            required=True,
            primary=True,
            searchable=True,
            accessor='getFile',
            mutator='setFile',
            index_method='getIndexValue',
            languageIndependent=True,
            storage=AnnotationStorage(migrate=True),
            default_content_type='application/octet-stream',
            validators=(('isNonEmptyFile', V_REQUIRED), ('checkFileMaxSize', V_REQUIRED)),
            widget=FileWidget(
                label=_(u'label_file', default=u'File'),
                description=_(u''),
                show_content_type=False,)
        ),
    ]

    fields[0].validators.append(ContentTypeValidator(('application/vnd.oasis.opendocument.text',)))

    def getFields(self):
        return self.fields
