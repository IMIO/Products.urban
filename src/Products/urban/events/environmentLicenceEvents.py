# -*- coding: utf-8 -*-

from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import ILicenceExpirationEvent

from plone import api

from zope.interface import directlyProvides


def setExploitationConditions(licence, event):
    """
     A minimal set of integral/sectorial exploitation conditions are determined by the rubrics
     selected on an environment licence.
    """
    rubrics = licence.getRubrics()
    if not rubrics:
        licence.setMinimumLegalConditions([])
    else:
        condition_field = rubrics[0].getField('exploitationCondition')
        conditions_uid = list(set([condition_field.getRaw(rubric) for rubric in rubrics]))
        licence.setMinimumLegalConditions(conditions_uid)


def createLicenceExpirationEvent(decision_event, event):
    """
     When the notifcation date of the decision event is set or is modified, we have
     to create a LicenceExpiration event or update its expiration date if it already exists.
    """
    licence = decision_event.aq_parent

    if not IEnvironmentLicence.providedBy(licence):
        return

    expiration_event = licence._getLastEvent(ILicenceExpirationEvent)
    notification_date = decision_event.getEventDate()

    if notification_date:
        years = licence.getValidityDuration()
        expiration_date = notification_date + years * 365
        while expiration_date.month() < notification_date.month():
            expiration_date += 1
        while expiration_date.day() < notification_date.day():
            expiration_date += 1

        if not expiration_event:
            config = licence.getUrbanConfig()
            expiration_eventtype = config.getEventTypesByInterface(ILicenceExpirationEvent)[0]

            # set the tal condition to true for creating the expiration event
            TAL_expr = expiration_eventtype.getTALCondition()
            expiration_eventtype.setTALCondition('python: True')

            expiration_event = licence.createUrbanEvent(expiration_eventtype.UID())
            directlyProvides(expiration_event, ILicenceExpirationEvent)

            # ...then set it back to its previous value
            expiration_eventtype.setTALCondition(TAL_expr)

        expiration_event.setEventDate(expiration_date)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(expiration_event)
    else:
        if expiration_event:
            expiration_event.setEventDate(None)
