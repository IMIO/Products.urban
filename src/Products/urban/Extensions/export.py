# -*- coding: utf-8 -*-

from DateTime import DateTime

from Products.urban.config import URBAN_TYPES

from plone import api

import os
import shutil
import zipfile

VAR_DIR = "var"
EXPORT_DIR = "{}/export".format(VAR_DIR)


def get_document_templates(licence_types=URBAN_TYPES):

    if "export" not in os.listdir(VAR_DIR):
        os.mkdir(EXPORT_DIR)

    export_path = _export_document_templates(licence_types=licence_types)
    zip_name, zip_file = _zip_folder(export_path)
    _set_header_response(zip_name)
    return zip_file


def _set_header_response(filename):
    site = api.portal.get()
    response = site.REQUEST.RESPONSE
    response.setHeader("Content-type", "application/zip")
    response.setHeader(
        "Content-disposition", 'attachment;filename="{}"'.format(filename)
    )


def _export_document_templates(licence_types=URBAN_TYPES, with_event_structure=True):

    export_path = "{path}/urban_templates-{timestamp}".format(
        path=EXPORT_DIR, timestamp=DateTime().millis()
    )
    os.mkdir(export_path)

    portal_urban = api.portal.get_tool("portal_urban")

    for licence_type in licence_types:
        print("exporting config: {}".format(licence_type.lower()))
        config = portal_urban.get(licence_type.lower())

        licence_path = "{path}/{licence_type}".format(
            path=export_path, licence_type=licence_type.lower()
        )
        os.mkdir(licence_path)

        urbanevents = config.eventconfigs
        for urbanevent in urbanevents.objectValues():
            if api.content.get_state(urbanevent) == "enabled":
                if with_event_structure:
                    event_path = "{path}/{event_name}".format(
                        path=licence_path,
                        event_name=urbanevent.Title().replace("/", " "),
                    )
                    if os.path.isdir(event_path):
                        count = 1
                        while os.path.isdir(event_path + "-%d" % count):
                            count += 1
                        event_path = event_path + "-%d" % count
                    os.mkdir(event_path)
                for doc in urbanevent.objectValues():
                    if api.content.get_state(doc) == "enabled":
                        print(" {} -> {}".format(licence_type.lower(), doc.id))
                        doc_name = "{path}/{name}".format(
                            path=with_event_structure and event_path or licence_path,
                            name=doc.id,
                        )
                        if not doc.id.endswith(".odt"):
                            doc_name += ".odt"

                        doc_export = open(doc_name, "arw")
                        named_file = doc.get_file()
                        named_file = (
                            type(named_file) in [str, tuple]
                            and named_file[0]
                            or named_file
                        )
                        doc_export.write(named_file.data)
                        doc_export.close()

    return export_path


def _zip_folder(path):
    zip_name = "Modèles_urban.zip"
    zip_file = zipfile.ZipFile(zip_name, "w")
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.join(root, file))
    zip_file.close()

    zip_file = open(zip_name, "r")
    payload = zip_file.read()
    zip_file.close()

    shutil.rmtree(path)
    os.remove(zip_name)

    return zip_name, payload
