# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
import re
from DateTime import DateTime
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent
from .utils import convert_to_europe_brussels
from .interfaces import ICODT_ParcelOutLicence


def after_term_deactivate(obj, event):
    if (
        not event.transition
        or event.transition.id not in ["disable"]
        or obj != event.object
    ):
        return
    obj.setEndValidity(datetime(*datetime.now().date().timetuple()[0:3]))


def post_save_event_parceloutlicence(obj, event):
    
    if not ICODT_ParcelOutLicence.providedBy(obj.aq_parent):
        return

    parent_container = api.content.get(path="/Urban/urban/parcellings")
    title = getattr(obj.aq_parent, "title", None)
    reference_dgatlp = getattr(obj.aq_parent, "referenceDGATLP", None)
    reference = getattr(obj.aq_parent, "reference", None)
    label = getattr(obj.aq_parent, "licenceSubject", None)
    match = re.search(r" - ([^-]+)$", title)
    if match is not None:
        subdivider_name = match.group(1)
    else:
        subdivider_name = ""

    is_favorable = obj.getDecision() == "favorable"
    if not is_favorable:
        return
    else:
        approbation_date = obj.getEventDate()
        authorization_date = obj.decisionDate

        # format dates
        if isinstance(approbation_date, DateTime):
            approbation_date = convert_to_europe_brussels(approbation_date)

        if isinstance(authorization_date, DateTime):
            authorization_date = convert_to_europe_brussels(authorization_date)

        found_parcelling = api.content.find(
            context=parent_container,
            communalReference=reference,
            portal_type="Parcelling",
        )
        if found_parcelling and len(found_parcelling) > 0:
            found_parcelling = found_parcelling[0].getObject()
            # Update fields
            found_parcelling.title = title
            found_parcelling.label = label
            found_parcelling.subdividerName = subdivider_name
            found_parcelling.communalReference = reference
            found_parcelling.DGO4Reference = reference_dgatlp
            found_parcelling.approvalDate = approbation_date
            found_parcelling.authorizationDate = authorization_date

        else:
            # If the object doesn't exist, create a new one
            api.content.create(
                container=parent_container,
                type="Parcelling",  # Type of content to create
                title=title,
                label=label,
                subdividerName=subdivider_name,
                communalReference=reference,
                DGO4Reference=reference_dgatlp,
                approvalDate=approbation_date,
                authorizationDate=authorization_date,
            )
