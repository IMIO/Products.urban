# -*- coding: utf-8 -*-

from Products.urban.services.mysqlbase import MySQLService
from Products.urban.services.mysqlbase import MySQLSession
from Products.urban.config import ExternalConfig
from datetime import datetime
from plone import api


class GigService(MySQLService):
    """
    Service specific to gig database, contain queries
    """

    def __init__(
        self,
        dialect="mysql+pymysql",
        user="GIG_TRANS",
        host="",
        db_name="sigped",
        password="",
        timeout="",
    ):
        password = password or user
        super(GigService, self).__init__(
            dialect, user, host, db_name, password, timeout
        )


class GigSession(MySQLSession):
    """
    Implements all the sql queries of cadastre DB with sqlalchemy methods
    """

    def insert_parcels(self, capakeys):
        """
        Do the insert query of the parcel capakeys into gig db.
        """
        parcels_keys = [c.replace("/", "") for c in capakeys]
        mail_record = api.portal.get_registry_record(
            "Products.urban.browser.gig_coring_settings.IGigCoringLink.mail_mapping"
        )
        user_current = api.user.get_current().id
        user_mail = ""
        for the_user in mail_record:
            if the_user.get("user_id") == user_current:
                user_mail = the_user.get("mail_gig")
        if not user_mail:
            user_mail = api.user.get_current().getProperty("email")
        map_cfg = ExternalConfig("urbanmap")
        nis = map_cfg.urbanmap["nis"]
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for key in parcels_keys:
            new_rec = "INSERT INTO GIG_TRANSIT (NUM_SIG, user_id, copy_time, work_id, INS) VALUES ('{cap}', '{user}', '{today}', 1, '{nis}');".format(
                cap=key, user=user_mail, today=today, nis=nis
            )
            query = self.session.execute(new_rec)
        self.session.commit()
