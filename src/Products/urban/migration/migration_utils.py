# -*- coding: utf-8 -*-
from datetime import datetime
from plone import api


def clean_obsolete_portal_type(portal_type_to_remove=None, report='print'):

    if not portal_type_to_remove:
        return
    portal_types_tool = api.portal.get_tool('portal_types')
    print("***Clean Obsolete Portal Type ***")
    print("***Step 1 Check if portal type object exists ***".format(portal_type_to_remove))

    catalog = api.portal.get_tool('portal_catalog')
    if report and portal_type_to_remove:
        portal_types_objects = [brain.getObject() for brain in catalog(portal_type=portal_type_to_remove)]

        if portal_types_objects:
            if report == 'print':
                for portal_type in portal_types_objects:
                    print(portal_type.absolute_url())
                print("Portal type found : {}".format(len(portal_types_objects)))
            if report == 'csv':
                with open("{}_{}.csv".format(portal_type_to_remove, datetime.today().strftime('%Y_%m_%d_%H_%M_%S')), "a") as file:
                    for portal_type in portal_types_objects:
                        file.write(portal_type.absolute_url() + "\n")
            print("Portal type object found : stop the process".format(portal_type_to_remove))
        else:
            print("Portal type not found in linked catalog : next step!".format(portal_type_to_remove))
            print("***Step 2: Remove the possibility to add the {} portal type object to another portal type ***".format(portal_type_to_remove))
            for portal_type in portal_types_tool:
                if 'allowed_content_types' in portal_types_tool.get(portal_type).__dict__:
                    if portal_type_to_remove in portal_types_tool.get(portal_type).__dict__['allowed_content_types']:
                        allowed_content_types_list = list(portal_types_tool.get(portal_type).__dict__['allowed_content_types'])
                        allowed_content_types_list.remove(portal_type_to_remove)
                        portal_types_tool.get(portal_type).__dict__['allowed_content_types'] = tuple(allowed_content_types_list)

            print("***Step 3: Delete the {} portal type ***".format(portal_type_to_remove))
            portal_type_obj = getattr(portal_types_tool, portal_type_to_remove)
            portal_type_obj.manage_delObjects([portal_type_obj.getId()])
            print("***Done ***")


def delete_plone_objects(portal_type_object_to_delete):
    print("***Delete all {} portal type objects ***".format(portal_type_object_to_delete))

    catalog = api.portal.get_tool('portal_catalog')
    items = [brain.getObject() for brain in catalog(portal_type=portal_type_object_to_delete)]
    print("Found {} items to be purged".format(len(items)))
    count = 0
    for obj in items:
        count += 1
        print("Deleting: {} {}".format(obj.absolute_url(),str(obj.created())))
        obj.aq_parent.manage_delObjects([obj.getId()])
    print("***Done ***")