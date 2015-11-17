# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.config import URBAN_TYPES

from plone import api

import os
import shutil
import zipfile

VAR_DIR = 'var'
EXPORT_DIR = '{}/export'.format(VAR_DIR)


def get_document_templates(licence_types=URBAN_TYPES):

    if 'export' not in os.listdir(VAR_DIR):
        os.mkdir(EXPORT_DIR)

    export_path = _export_document_templates(licence_types=licence_types)
    zip_name, zip_file = _zip_folder(export_path)
    _set_header_response(zip_name)
    return zip_file


def _set_header_response(filename):
    site = api.portal.get()
    response = site.REQUEST.RESPONSE
    response.setHeader('Content-type', 'application/zip')
    response.setHeader(
        'Content-disposition',
        'attachment;filename="{}"'.format(filename)
    )


def _export_document_templates(licence_types=URBAN_TYPES):

    export_path = '{path}/urban_templates-{timestamp}'.format(
        path=EXPORT_DIR,
        timestamp=DateTime().millis()
    )
    os.mkdir(export_path)

    portal_urban = api.portal.get_tool('portal_urban')

    for licence_type in licence_types:
        print('exporting config: {}'.format(licence_type.lower()))
        config = portal_urban.get(licence_type.lower())

        docs_path = '{path}/{licence_type}'.format(
            path=export_path,
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

    return export_path


def _zip_folder(path):
    zip_name = 'Modèles_urban.zip'
    zip_file = zipfile.ZipFile(zip_name, 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()

    zip_file = open(zip_name, 'r')
    payload = zip_file.read()
    zip_file.close()

    shutil.rmtree(path)
    os.remove(zip_name)

    return zip_name, payload
