# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.utils import \
    _updateDefaultCollectionFor
from plone import api
from Products.urban.config import URBAN_TYPES
from Products.urban.interfaces import ILicenceContainer
from Products.urban.setuphandlers import (_, _activate_dashboard_navigation,
                                          _create_dashboard_collection,
                                          setFolderAllowedTypes)
from Products.urban.utils import (getEnvironmentLicenceFolderIds,
                                  getLicenceFolderId,
                                  getUrbanOnlyLicenceFolderIds)
from zExceptions import BadRequest
from zope.interface import alsoProvides


def add_deleted_licence_folder():
    portal = api.portal.get()
    urban_folder = getattr(portal, "urban", None)
    if urban_folder is None:
        return

    setup_root_folder_dashboard(urban_folder)

    urban_folder_names = getUrbanOnlyLicenceFolderIds()
    uniquelicences_names = [
        getLicenceFolderId("UniqueLicence"),
        getLicenceFolderId("CODT_UniqueLicence"),
        getLicenceFolderId("IntegratedLicence"),
        getLicenceFolderId("CODT_IntegratedLicence"),
    ]
    environment_folder_names = getEnvironmentLicenceFolderIds() + uniquelicences_names

    for urban_type in URBAN_TYPES:
        licence_folder_id = getLicenceFolderId(urban_type)

        if hasattr(urban_folder, licence_folder_id):
            continue

        licence_folder = add_licence_folders(
            urban_folder, urban_type, licence_folder_id
        )
        setup_licence_folder_dashboard(licence_folder, urban_type)
        set_default_security(
            licence_folder,
            licence_folder_id,
            urban_folder_names,
            environment_folder_names,
        )


def add_licence_folders(urban_folder, urban_type, licence_folder_id):
    licence_folder_id = urban_folder.invokeFactory(
        "Folder", id=licence_folder_id, title=_(urban_type, "urban")
    )
    licence_folder = getattr(urban_folder, licence_folder_id)
    alsoProvides(licence_folder, ILicenceContainer)
    setFolderAllowedTypes(licence_folder, urban_type)
    # manage the 'Add' permissions...
    try:
        licence_folder.manage_permission(
            "urban: Add %s" % urban_type,
            [
                "Manager",
                "Contributor",
            ],
            acquire=0,
        )
    except ValueError:
        # exception for some portal_types having a different meta_type
        if urban_type in [
            "UrbanCertificateOne",
            "NotaryLetter",
        ]:
            licence_folder.manage_permission(
                "urban: Add UrbanCertificateBase",
                [
                    "Manager",
                    "Contributor",
                ],
                acquire=0,
            )
        if urban_type in [
            "CODT_UrbanCertificateOne",
            "CODT_NotaryLetter",
        ]:
            licence_folder.manage_permission(
                "urban: Add CODT_UrbanCertificateBase",
                [
                    "Manager",
                    "Contributor",
                ],
                acquire=0,
            )
        if urban_type in [
            "EnvClassThree",
        ]:
            licence_folder.manage_permission(
                "urban: Add EnvironmentBase",
                [
                    "Manager",
                    "Contributor",
                ],
                acquire=0,
            )
        if urban_type in ["EnvClassOne", "EnvClassTwo", "EnvClassBordering"]:
            licence_folder.manage_permission(
                "urban: Add EnvironmentLicence",
                [
                    "Manager",
                    "Contributor",
                ],
                acquire=0,
            )
    urban_folder.moveObjectsToBottom([licence_folder_id])

    return licence_folder


def setup_root_folder_dashboard(urban_folder):
    all_licences_collection_id = "collection_all_licences"
    if all_licences_collection_id not in urban_folder.objectIds():
        _create_dashboard_collection(
            urban_folder,
            id=all_licences_collection_id,
            title=_("All", "urban"),
            filter_type=[type for type in URBAN_TYPES],
        )
    urban_folder.moveObjectToPosition(all_licences_collection_id, 0)
    all_licences_collection = getattr(urban_folder, all_licences_collection_id)
    # always reupdate the listed types to URBAN_TYPES
    all_licences_collection.query = [
        {
            "i": "portal_type",
            "o": "plone.app.querystring.operation.selection.is",
            "v": [type for type in URBAN_TYPES],
        }
    ]
    _updateDefaultCollectionFor(urban_folder, all_licences_collection.UID())


def setup_licence_folder_dashboard(licence_folder, urban_type):
    _activate_dashboard_navigation(
        licence_folder, "/dashboard/config/%ss.xml" % urban_type.lower()
    )
    collection_id = "collection_%s" % urban_type.lower()
    no_deposit = ["PatrimonyCertificate", "Inspection"]
    with_deposit_date = urban_type not in no_deposit
    if collection_id not in licence_folder.objectIds():
        setFolderAllowedTypes(licence_folder, "DashboardCollection")
        _create_dashboard_collection(
            licence_folder,
            id=collection_id,
            title=_(urban_type, "urban"),
            filter_type=[urban_type],
            with_deposit_date=with_deposit_date,
        )
        setFolderAllowedTypes(licence_folder, urban_type)
    licence_folder.moveObjectToPosition(collection_id, 0)
    collection = getattr(licence_folder, collection_id)

    _updateDefaultCollectionFor(licence_folder, collection.UID())


def set_default_security(
    licence_folder, licence_folder_id, urban_folder_names, environment_folder_names
):
    # we add a property usefull for portal_urban.getLicenceConfig
    try:
        # we try in case we apply the profile again...
        licence_folder.manage_addProperty(
            "urbanConfigId", licence_folder_id.strip("s"), "string"
        )
    except BadRequest:
        pass
    licence_folder.manage_delLocalRoles(["urban_editors"])
    licence_folder.manage_delLocalRoles(["environment_editors"])
    if licence_folder_id in urban_folder_names:
        licence_folder.manage_addLocalRoles("urban_readers", ("Reader",))
        licence_folder.manage_addLocalRoles("urban_editors", ("Contributor",))
    if licence_folder_id in environment_folder_names:
        licence_folder.manage_addLocalRoles("environment_readers", ("Reader",))
        licence_folder.manage_addLocalRoles("environment_editors", ("Contributor",))
    if licence_folder_id == getLicenceFolderId("Inspection"):
        licence_folder.manage_addLocalRoles("inspection_editors", ("Contributor",))
