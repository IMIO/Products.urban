# -*- coding: utf-8 -*-

from plone import api

from Products.Five import BrowserView
from Products.urban.interfaces import IEnvironmentBase
from Products.urban.NOTICe.config import BOUND
from Products.urban.NOTICe.config import GET_ERROR
from Products.urban.NOTICe.config import MATCH
from Products.urban.NOTICe.config import NO_RESULTS
from Products.urban.NOTICe.config import REF_TAG
from Products.urban.NOTICe.config import UNBOUND
from Products.urban.services import NOTICe

from zope.annotation import IAnnotations

import lxml


class NOTICeView(BrowserView):

    def update_open_notifications(self):
        """
        Ask NOTICe for all the open notifications, store them in the site
        registry and try to map them to existing licences.
        """
        portal_urban = api.portal.get_tool('portal_urban')
        annotations = IAnnotations(portal_urban)
        records = annotations.get('Products.urban.NOTICe.open_notifications', {})

        # update current state with any new records
        response = NOTICe.search_notifications(status='EN_ATTENTE_REPONSE')
        if response.status.code == 'SOA0000000':
            notifications = response.notices.notice
            notification_ids = []
            for notification in notifications:
                notice_id = notification.noticeId
                notification_ids.append(notice_id)
                if notice_id not in records:
                    records[notice_id] = {
                        'label': notification.labelType,
                        'urban_reference': '',
                        'licence_UID': '',
                        'status': '',
                    }
            # then make some checks on ALL the records
            status = ''
            for notice_id, record in records.iteritems():
                # clear the current state from old records
                if notice_id not in notification_ids:
                    records.pop(notice_id)
                # try to get a licence reference for the notification
                if not record['urban_reference']:
                    record['urban_reference'], record['status'] = self._get_notification_urban_reference(notice_id)
                # try to map to a urban licence
                if record['urban_reference'] and not record['licence_UID']:
                    reference = record['urban_reference']
                    record['licence_UID'], record['status'] = self._get_licence_UID_by_reference(reference)
                # if a licence is found, try to create a notification task on it
                if record['licence_UID'] and record['status'] == MATCH:
                    record['status'] = self._bind_notification_to_licence(notice_id, record['licence_UID'], record['label'])
            # store the result
            annotations['Products.urban.NOTICe.open_notifications'] = records
        else:
            pass  # handle error: to implements

    def _get_notification_urban_reference(self, notice_id):
        """
        Return the licence reference of a notification notice_id
        """
        try:
            notification = NOTICe.get_notification(notice_id)
        except Exception:
            print "ERROR NOTICe getNotification {}".format(notice_id)
            return '', GET_ERROR
        status = notification.status.code
        if status == 'SOA0000000':
            specific = notification.notice.specific
            tree = lxml.etree.fromstring(specific)
            for node in tree.iter(REF_TAG):
                return node.text, UNBOUND
        elif status == 'SOA0000001':
            return '', NO_RESULTS
        return '', ''

    def _get_licence_UID_by_reference(self, urban_reference):
        """
        Return the UID of licence matching urban_reference
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence_brains = catalog.unrestrictedSearchResults(
            getReference=urban_reference,
            object_provides=IEnvironmentBase.__identifier__,
        )
        if licence_brains and len(licence_brains) == 1:
            return licence_brains[0].UID, MATCH
        return '', UNBOUND

    def _get_licence_by_UID(self, licence_UID):
        """
        """
        catalog = api.portal.get_tool('portal_catalog')
        licence_brains = catalog.unrestrictedSearchResults(UID=licence_UID)
        if licence_brains and len(licence_brains) == 1:
            with api.env.adopt_roles(['Manager']):
                licence = licence_brains[0].getObject()
            return licence

    def _bind_notification_to_licence(self, notice_id, licence_UID, label):
        """
        Try to create a task corresponding to notification 'notice_id'
        on licence 'licence_UID'.
        """
        try:
            notification = NOTICe.get_notification(notice_id)
        except Exception:
            print "ERROR NOTICe getNotification {}".format(notice_id)
            return GET_ERROR
        status = notification.status.code
        if status == 'SOA0000000':
            licence = self._get_licence_by_UID(licence_UID)
            with api.env.adopt_roles(['Manager']):
                api.content.create(
                    container=licence,
                    type='task',
                    id=notice_id,
                    title=label,
                )
            return BOUND
        elif status == 'SOA0000001':
            return NO_RESULTS
        return ''
