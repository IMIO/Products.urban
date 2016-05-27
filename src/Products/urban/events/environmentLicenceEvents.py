# -*- coding: utf-8 -*-

from DateTime import DateTime

from dateutil.relativedelta import relativedelta

from Products.urban.interfaces import IEnvironmentLicence
from Products.urban.interfaces import IEnvClassThree
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


def createEnvClassThreeExpirationEvent(acknowledgment_event, event):
    """
     When the date of the acknowledgment event is set or is modified, we have
     to create a LicenceExpiration event or update its expiration date if it already exists.
    """
    licence = acknowledgment_event.aq_parent

    if not IEnvClassThree.providedBy(licence):
        return

    expiration_event = licence._getLastEvent(ILicenceExpirationEvent)
    acknowledgment_date = acknowledgment_event.getEventDate()

    if acknowledgment_date:
        expiration_date = _compute_expiration_date(licence, acknowledgment_date)
        if not expiration_event:
            expiration_event = _create_expiration_event(licence)

        expiration_event.setEventDate(expiration_date)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(expiration_event)
    else:
        if expiration_event:
            expiration_event.setEventDate(None)


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
        expiration_date = _compute_expiration_date(licence, notification_date)
        if not expiration_event:
            expiration_event = _create_expiration_event(licence)

        expiration_event.setEventDate(expiration_date)
        catalog = api.portal.get_tool('portal_catalog')
        catalog.reindexObject(expiration_event)
    else:
        if expiration_event:
            expiration_event.setEventDate(None)


def _create_expiration_event(licence):
    config = licence.getUrbanConfig()
    expiration_eventtype = config.getEventTypesByInterface(ILicenceExpirationEvent)[0]

    # set the tal condition to true for creating the expiration event
    TAL_expr = expiration_eventtype.getTALCondition()
    expiration_eventtype.setTALCondition('python: True')
    expiration_event_id = licence.invokeFactory(
        'UrbanEvent',
        id='urbantevent.{}'.format(str(DateTime().millis())),
        title=expiration_eventtype.Title(),
        urbaneventtypes=(expiration_eventtype,),
    )
    expiration_event = getattr(licence, expiration_event_id)
    directlyProvides(expiration_event, ILicenceExpirationEvent)

    # ...then set it back to its previous value
    expiration_eventtype.setTALCondition(TAL_expr)

    return expiration_event


def _compute_expiration_date(licence, notification_date):
    """
     Expiration date = notification_date + years valueDelay
    """
    years = licence.getValidityDelay
    expiration_date = notification_date.asdatetime()
    expiration_date = expiration_date + relativedelta(days=7, years=years)
    expiration_date = DateTime(str(expiration_date))

    return expiration_date
