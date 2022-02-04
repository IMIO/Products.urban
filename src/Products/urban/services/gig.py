# -*- coding: utf-8 -*-

from Products.urban.services.mysqlbase import MySQLService
from Products.urban.services.mysqlbase import MySQLSession
from datetime import datetime
from plone import api


class GigService(MySQLService):
    """
    Service specific to gig database, contain queries
    """
    def __init__(self, dialect='mysql+pymysql', user='urb_xxx', host='', db_name='urb_xxx', password='', timeout='120000'):
        super(GigService, self).__init__(dialect, user, host, db_name, password, timeout)


class GigSession(MySQLSession):
    """
    Implements all the sql queries of cadastre DB with sqlalchemy methods
    """

    def insert_parcels(self, capakeys):
        """
        Do the insert query of the parcel capakeys into gig db.
        """
        parcels_keys = [c.replace('/', '') for c in capakeys]
        mail_record = api.portal.get_registry_record(
                'Products.urban.browser.gig_coring_settings.IGigCoringLink.mail_mapping')
        user_mail = mail_record[0].get('mail_gig')
        if not user_mail or user_mail == '':
            user_mail = api.user.get_current().getProperty('email')
        filenis = '/srv/instances/testcarottage_urb25/var/urban/urbanmap.cfg'
        with open(filenis, 'r') as f:
            lines = f.readlines()
        nis = lines[1][4:9]
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key in parcels_keys:
            new_rec = "INSERT INTO GIG_TRANSIT (NUM_SIG, user_id, copy_time, work_id, INS) VALUES ('{cap}', '{user}', '{today}', 1, '{nis}');".format(cap=key, user=user_mail, today=today, nis=nis)
            query = self.session.execute(new_rec)
        self.session.commit()
