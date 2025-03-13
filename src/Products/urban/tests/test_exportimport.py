#  -*- coding: utf-8 -*-
from Products.CMFPlone.utils import base_hasattr
from Products.urban.Extensions.imports import createStreet
from Products.urban.browser.exportimport.import_config import ConfigImportContent
from Products.urban.testing import URBAN_TESTS_CONFIG
from plone import api

import json
import os
import unittest2 as unittest


class TestStreetImports(unittest.TestCase):

    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        portal = self.layer["portal"]
        self.utool = portal.portal_urban
        self.wtool = portal.portal_workflow
        self.streets = self.utool.streets

    def testCreateStreet(self):
        ex_streets = {}
        # createStreet(self, city, zipcode, streetcode, streetname, bestAddresskey, startdate, enddate, regionalroad, ex_streets)

        # create a first street, historical one
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "0",
                "Rue de l'Estampage",
                7090730,
                "2010/09/07",
                "2011/08/04",
                "",
                ex_streets,
            )
        # checking once the city folder creation
        self.failUnless(base_hasattr(self.streets, "awans"))
        awans = getattr(self.streets, "awans")
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-lestampage"))
        rue1 = getattr(awans, "rue-de-lestampage")
        # checking state
        self.assertEquals(self.wtool.getInfoFor(rue1, "review_state"), "disabled")
        # create a second street, new version of the recent one
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "1091",
                "Rue de l'Estampage",
                7090730,
                "2011/08/04",
                None,
                "",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-lestampage1"))
        rue2 = getattr(awans, "rue-de-lestampage1")
        self.assertEquals(self.wtool.getInfoFor(rue2, "review_state"), "enabled")
        self.assertEquals(self.wtool.getInfoFor(rue1, "review_state"), "disabled")

        # create the same first street => nothing must be done
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "0",
                "Rue de l'Estampage",
                7090730,
                "2010/09/07",
                "2011/08/04",
                "",
                ex_streets,
            )
        # checking creation
        self.failIf(base_hasattr(awans, "rue-de-lestampage2"))
        self.assertEquals(len(awans.objectIds()), 2)
        # create the same second street => nothing must be done
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "1091",
                "Rue de l'Estampage",
                7090730,
                "2011/08/04",
                None,
                "",
                ex_streets,
            )
        # checking creation
        self.failIf(base_hasattr(awans, "rue-de-lestampage2"))
        self.assertEquals(len(awans.objectIds()), 2)

        # create a new street, the actual first and after the historical
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "1032",
                "Rue de la Chaudronnerie",
                7090729,
                "2011/08/04",
                None,
                "",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-la-chaudronnerie"))
        rue3 = getattr(awans, "rue-de-la-chaudronnerie")
        self.assertEquals(self.wtool.getInfoFor(rue3, "review_state"), "enabled")
        # create a new street, historical
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "0",
                "Rue de la Chaudronnerie",
                7090729,
                "2010/09/07",
                "2011/08/04",
                "",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-la-chaudronnerie1"))
        rue4 = getattr(awans, "rue-de-la-chaudronnerie1")
        self.assertEquals(self.wtool.getInfoFor(rue4, "review_state"), "disabled")
        self.assertEquals(self.wtool.getInfoFor(rue3, "review_state"), "enabled")

        # create a new street, regional road first and after without
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "1025",
                "Rue de Bruxelles",
                7020318,
                "2010/09/07",
                None,
                "N3",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-bruxelles"))
        rue5 = getattr(awans, "rue-de-bruxelles")
        self.assertEquals(self.wtool.getInfoFor(rue5, "review_state"), "enabled")
        # create a new street, same street name but without regional road
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "1025",
                "Rue de Bruxelles",
                7020319,
                "2010/09/07",
                None,
                "",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-bruxelles1"))
        rue6 = getattr(awans, "rue-de-bruxelles1")
        self.assertEquals(self.wtool.getInfoFor(rue6, "review_state"), "enabled")
        self.assertEquals(
            self.wtool.getInfoFor(rue5, "review_state"), "disabled"
        )  # previous street has been disabled

        # create a new street, without regional road first and after with one
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "5000",
                "Rue de Namur",
                7020320,
                "2010/09/07",
                None,
                "",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-namur"))
        rue7 = getattr(awans, "rue-de-namur")
        self.assertEquals(self.wtool.getInfoFor(rue7, "review_state"), "enabled")
        # create a new street, same street name but with regional road
        with api.env.adopt_roles(["Manager"]):
            createStreet(
                "Awans",
                4340,
                "5000",
                "Rue de Namur",
                7020321,
                "2010/09/07",
                None,
                "N4",
                ex_streets,
            )
        # checking creation
        self.failUnless(base_hasattr(awans, "rue-de-namur1"))
        rue8 = getattr(awans, "rue-de-namur1")
        self.assertEquals(self.wtool.getInfoFor(rue8, "review_state"), "disabled")
        self.assertEquals(
            self.wtool.getInfoFor(rue7, "review_state"), "enabled"
        )  # previous street is unchanged


class TestExportImportContent(unittest.TestCase):
    layer = URBAN_TESTS_CONFIG

    def setUp(self):
        self.portal = self.layer["portal"]
        self.utool = self.portal.portal_urban
        self.add_globaltemplates_to_event()

    def get_template_parameter(self, folder):
        self.globaltemplates_id_list = {
            "logo.odt": "a46d50ed-9070-4d7b-8422-a02d20adb0db",
            "header.odt": "589d6268-1d93-416c-a8ac-271f6595c234",
            "footer.odt": "9bc708e9-bbc7-4b1f-ac44-03e555885af0",
            "signatures.odt": "bdb59fd7-8983-4f5c-ba8d-8f7e850e978d",
        }
        globaltemplates = getattr(self.utool, "globaltemplates", None)
        if globaltemplates is None:
            return []
        sub_urbantemplates = getattr(globaltemplates, folder, None)
        if sub_urbantemplates is None:
            return []
        globaltemplates_contents = sub_urbantemplates.contentItems()
        globaltemplates_parameter = []
        for id, globaltemplate in globaltemplates_contents:
            if id not in self.globaltemplates_id_list:
                continue
            setattr(globaltemplate, "_plone.uuid", self.globaltemplates_id_list[id])
            globaltemplate.reindexObject(idxs=["UID"])
            globaltemplates_parameter.append(
                {
                    "do_rendering": True,
                    "template": globaltemplate.UID(),
                    "pod_context_name": id.split(".")[0],
                }
            )
        return globaltemplates_parameter

    def add_globaltemplates_to_event(self):
        urbantemplates = self.get_template_parameter("urbantemplates")
        brains = api.content.find(context=self.utool, portal_type="UrbanTemplate")

        for brain in brains:
            urbantemplate_obj = brain.getObject()
            urbantemplate_obj.merge_templates = urbantemplates

    def get_data(self, file):
        directory_path = os.path.dirname(os.path.realpath(__file__))
        json_file = os.path.normpath(os.path.join(directory_path, "json", file))
        data = None
        with open(json_file, "r") as f:
            data = json.load(f)
        return data

    def test_import_template_no_other_document(self):
        data = self.get_data("urban_template_test_no_other_document.json")

        with api.env.adopt_roles(["Manager"]):
            import_urban_config = ConfigImportContent(self.utool, self.portal.REQUEST)
            import_urban_config.import_to_current_folder = False
            import_urban_config.handle_existing_content = 0
            import_urban_config.limit = None
            import_urban_config.commit = None
            import_urban_config.import_old_revisions = False
            import_urban_config.fix_parent_path = True
            import_urban_config.import_in_same_instance = False
            import_urban_config.import_to_current_lic_config_folder = False
            import_urban_config.handle_missing_parent = 0

            import_urban_config.start()
            import_urban_config.do_import(data)
            import_urban_config.finish()

            template_imported_uid = "a6011644490b401288a4b06262dcede8"
            template_imported_obj = api.content.get(UID=template_imported_uid)
            merge_templates = template_imported_obj.merge_templates
            merge_templates = {
                merge_template["pod_context_name"]: merge_template["template"]
                for merge_template in merge_templates
            }
            self.assertEquals(
                merge_templates["footer"], "9bc708e9-bbc7-4b1f-ac44-03e555885af0"
            )
            self.assertEquals(
                merge_templates["header"], "589d6268-1d93-416c-a8ac-271f6595c234"
            )

    def test_import_template_same_procedure_type(self):
        data = self.get_data("urban_template_test_same_procedure_type.json")

        with api.env.adopt_roles(["Manager"]):
            import_urban_config = ConfigImportContent(self.utool, self.portal.REQUEST)
            import_urban_config.import_to_current_folder = False
            import_urban_config.handle_existing_content = 0
            import_urban_config.limit = None
            import_urban_config.commit = None
            import_urban_config.import_old_revisions = False
            import_urban_config.fix_parent_path = True
            import_urban_config.import_in_same_instance = False
            import_urban_config.import_to_current_lic_config_folder = False
            import_urban_config.handle_missing_parent = 0

            import_urban_config.start()
            import_urban_config.do_import(data)
            import_urban_config.finish()

            template_imported_uid = "96c6baa97c7d47958415100d73dde04a"
            template_imported_obj = api.content.get(UID=template_imported_uid)
            merge_templates = template_imported_obj.merge_templates

            merge_templates = {
                merge_template["pod_context_name"]: merge_template["template"]
                for merge_template in merge_templates
            }
            self.assertEquals(
                merge_templates["footer"], "9bc708e9-bbc7-4b1f-ac44-03e555885af0"
            )
            self.assertEquals(
                merge_templates["header"], "589d6268-1d93-416c-a8ac-271f6595c234"
            )

    def test_import_template_same_event(self):
        data = self.get_data("urban_template_test_same_event.json")

        with api.env.adopt_roles(["Manager"]):
            import_urban_config = ConfigImportContent(self.utool, self.portal.REQUEST)
            import_urban_config.import_to_current_folder = False
            import_urban_config.handle_existing_content = 0
            import_urban_config.limit = None
            import_urban_config.commit = None
            import_urban_config.import_old_revisions = False
            import_urban_config.fix_parent_path = True
            import_urban_config.import_in_same_instance = False
            import_urban_config.import_to_current_lic_config_folder = False
            import_urban_config.handle_missing_parent = 0

            import_urban_config.start()
            import_urban_config.do_import(data)
            import_urban_config.finish()

            template_imported_uid = "ce2735a774b84383bcd41d68a1c59f63"
            template_imported_obj = api.content.get(UID=template_imported_uid)
            merge_templates = template_imported_obj.merge_templates
            merge_templates = {
                merge_template["pod_context_name"]: merge_template["template"]
                for merge_template in merge_templates
            }
            self.assertEquals(
                merge_templates["footer"], "9bc708e9-bbc7-4b1f-ac44-03e555885af0"
            )
            self.assertEquals(
                merge_templates["header"], "589d6268-1d93-416c-a8ac-271f6595c234"
            )
