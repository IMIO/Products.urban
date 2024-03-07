# -*- coding: utf-8 -*-

from plone import api

from Products.urban import UrbanMessage as _
from Products.urban.config import URBAN_TYPES
from Products.urban.interfaces import IGenericLicence

from zope.i18n import translate

import json


def _get_licence_states(licence_type):
    """ """
    portal_wf = api.portal.get_tool("portal_workflow")
    workflow = portal_wf.getWorkflowsFor(licence_type)[0]
    states = workflow.states.objectIds()

    return states


class UrbanExportMethod(object):
    """ """

    def __init__(self, context, request):
        self.context = context
        self.request = request


class get_licence_types(UrbanExportMethod):
    """ """

    def __call__(self):
        """ """
        licence_types = dict(
            [(translate(_(t), context=self.request), t) for t in URBAN_TYPES]
        )
        licence_types = json.dumps(licence_types)
        return licence_types


class get_licence_states(UrbanExportMethod):
    """ """

    def __call__(self):
        """ """
        if not hasattr(self.request, "licence_type"):
            msg = (
                "should be called with licence_type argument "
                + "eg: ../get_licence_states?licence_type=BuildLicence"
            )
            return msg

        licence_type = self.request.licence_type
        if licence_type not in URBAN_TYPES:
            msg = "licence_type should be one of the following: %s" % ", ".join(
                URBAN_TYPES
            )
            return msg

        states = _get_licence_states(licence_type)

        return json.dumps(states)


class export_licences(UrbanExportMethod):
    """ """

    def __call__(self):
        """ """

        catalog = api.portal.get_tool("portal_catalog")
        query = {"object_provides": IGenericLicence.__identifier__}

        error = self._check_args(query)
        if error:
            return error

        with api.env.adopt_roles(["Manager"]):
            licence_brains = catalog(**query)

            licences_export = []
            for brain in licence_brains:
                licence_record = {}
                licence = brain.getObject()

                licence_record["id"] = licence.getId()
                licence_record["licence_type"] = licence.portal_type
                licence_record["reference"] = licence.getReference()
                licence_record["subject"] = licence.getLicenceSubject()
                licence_record["state"] = api.content.get_state(licence)
                licence_record["addresses"] = []
                for addr in licence.getWorkLocations():
                    street_brains = catalog(UID=addr["street"])[0].Title
                    if len(street_brains) != 1:
                        continue
                    street_name = street_brains[0].Title
                    licence_record["addresses"].append(
                        {"street": street_name, "number": addr["number"]}
                    )
                licence_record["capakeys"] = [
                    l.get_capakey() for l in licence.getOfficialParcels()
                ]
                licence_record["applicants"] = self._applicant_records(licence)
                licence_record["creation_date"] = str(licence.creation_date)
                decision_event = (
                    hasattr(licence, "getLastTheLicence")
                    and licence.getLastTheLicence()
                    or None
                )
                if decision_event:
                    licence_record["decision_date"] = str(
                        licence.getLastTheLicence().getDecisionDate()
                    )
                    licence_record[
                        "decision"
                    ] = licence.getLastTheLicence().getDecision()
                licence_record["last_modification"] = str(brain.modified)

                licences_export.append(licence_record)

            return json.dumps(licences_export)

    def _applicant_records(self, licence):
        """ """
        applicants = []
        for applicant in licence.getApplicants() or licence.getProprietaries():
            title_field = applicant.getField("personTitle")
            title_voc = title_field.vocabulary.getDisplayList(applicant)
            applicants.append(
                {
                    "title": title_voc.getValue(applicant.getPersonTitle()),
                    "firstname": applicant.getName2(),
                    "name": applicant.getName1(),
                }
            )

        return applicants

    def _check_args(self, query):
        """ """
        licence_type = self.request.get("licence_type", None)
        if licence_type and licence_type not in URBAN_TYPES:
            msg = "licence_type should be one of the following: %s" % ", ".join(
                URBAN_TYPES
            )
            return msg
        elif licence_type:
            query["portal_type"] = licence_type

            licence_state = self.request.get("licence_state", None)
            available_states = _get_licence_states(licence_type)
            if licence_state and licence_state not in available_states:
                msg = "licence_state should be one of the following: %s" % ", ".join(
                    available_states
                )
                return msg
            elif licence_state:
                query["review_state"] = licence_state
