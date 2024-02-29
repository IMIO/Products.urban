# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api

import logging

logger = logging.getLogger("urban: migrations utils")


def clean_obsolete_portal_type(portal_type_to_remove=None, report="print"):

    if not portal_type_to_remove:
        return
    portal_types_tool = api.portal.get_tool("portal_types")
    logger.info("***Clean Obsolete Portal Type ***")
    logger.info(
        "***Step 1 Check if portal type object exists ***".format(portal_type_to_remove)
    )

    catalog = api.portal.get_tool("portal_catalog")
    portal_types_objects = [
        brain.getObject() for brain in catalog(portal_type=portal_type_to_remove)
    ]

    if portal_types_objects:
        if report == "print":
            for portal_type in portal_types_objects:
                logger.info(portal_type.absolute_url())
            logger.info("Portal type found : {}".format(len(portal_types_objects)))
        if report == "csv":
            with open(
                "{}_{}.csv".format(
                    portal_type_to_remove,
                    datetime.today().strftime("%Y_%m_%d_%H_%M_%S"),
                ),
                "a",
            ) as file:
                for portal_type in portal_types_objects:
                    file.write(portal_type.absolute_url() + "\n")
        logger.info(
            "Portal type object found : stop the process".format(portal_type_to_remove)
        )
    else:
        logger.info(
            "Portal type not found in linked catalog : next step!".format(
                portal_type_to_remove
            )
        )
        logger.info(
            "***Step 2: Remove the possibility to add the {} portal type object to another portal type ***".format(
                portal_type_to_remove
            )
        )
        for portal_type in portal_types_tool:
            if hasattr(portal_types_tool.get(portal_type), "allowed_content_types"):
                if (
                    portal_type_to_remove
                    in portal_types_tool.get(portal_type).allowed_content_types
                ):
                    allowed_content_types_list = list(
                        portal_types_tool.get(portal_type).allowed_content_types
                    )
                    allowed_content_types_list.remove(portal_type_to_remove)
                    portal_types_tool.get(portal_type).allowed_content_types = tuple(
                        allowed_content_types_list
                    )

        logger.info(
            "***Step 3: Delete the {} portal type ***".format(portal_type_to_remove)
        )
        if hasattr(portal_types_tool, portal_type_to_remove):
            portal_type_obj = getattr(portal_types_tool, portal_type_to_remove)
            portal_type_obj.manage_delObjects([portal_type_obj.getId()])
        logger.info("***Done ***")


def delete_plone_objects(portal_type_object_to_delete):
    logger.info(
        "***Delete all {} portal type objects ***".format(portal_type_object_to_delete)
    )

    catalog = api.portal.get_tool("portal_catalog")
    items = [
        brain.getObject() for brain in catalog(portal_type=portal_type_object_to_delete)
    ]
    logger.info("Found {} items to be deleted".format(len(items)))
    api.content.delete(objects=items)
    logger.info("***Done ***")
