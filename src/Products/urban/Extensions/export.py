# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.config import URBAN_TYPES

from plone import api

import os

VAR_DIR = 'var'
EXPORT_DIR = '{}/export'.format(VAR_DIR)


def export_document_templates(licence_types=URBAN_TYPES):

    if 'export' not in os.listdir(VAR_DIR):
        os.mkdir(EXPORT_DIR)

    export_name = '{path}/urban_templates-{timestamp}'.format(
        path=EXPORT_DIR,
        timestamp=DateTime().millis()
    )
    os.mkdir(export_name)

    portal_urban = api.portal.get_tool('portal_urban')

    for licence_type in licence_types:
        print('exporting config: {}'.format(licence_type.lower()))
        config = portal_urban.get(licence_type.lower())

        docs_path = '{path}/{licence_type}'.format(
            path=export_name,
            licence_type=licence_type.lower()
        )
        os.mkdir(docs_path)

        urbanevents = config.urbaneventtypes
        for urbanevent in urbanevents.objectValues():
            for doc in urbanevent.objectValues():
                print(' {} -> {}'.format(licence_type.lower(), doc.id))
                doc_name = '{path}/{name}'.format(
                    path=docs_path,
                    name=doc.id
                )
                doc_export = open(doc_name, 'arw')
                doc_export.write(doc.get_file().data)
                doc_export.close()
