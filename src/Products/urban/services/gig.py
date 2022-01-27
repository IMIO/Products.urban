# -*- coding: utf-8 -*-

from Products.urban.services.mysqlbase import MySQLService
from Products.urban.services.mysqlbase import MySQLSession
from datetime import datetime


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
        filenis = '/srv/instances/server_urban25/var/urban/urbanmap.cfg'
        with open(filenis, 'r') as f:
            lines = f.readlines()
        nis = lines[1][4:9]
# variables de test nis_test et parcels_keys car la bdo du gig attend une capakey et un nis de la communne de rebecq or l'instance de test utilise les données de fléron
        nis_test = 25123
        parcels_keys = ['25090A013100E000']
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fileportail = '/srv/instances/server_urban25/var/urban/northwind.cfg'
        with open(fileportail, 'r') as f:
            l = f.readlines()
        user = l[8][5:27]

#        rec_test = "SELECT * FROM customers WHERE id >= 42;"
        for key in parcels_keys:
            try:
#                rec_i = "INSERT INTO customers (company, last_name, first_name, email_address, job_title, business_phone, home_phone, mobile_phone, fax_number, address, city, state_province, zip_postal_code, country_region, web_page, notes, attachments) VALUES ('Company DD', 'Cornick', 'Anna', '{user}', 'Owner', '(123)555-0100', '{today}', NULL, '(123)555-0101', '123 1st Street', 'Seattle', 'WA', '99999', 'USA', '{cap}', '{nis}', '');".format(user=user, today=today, cap=key, nis=nis)
#                query = self.session.execute(rec_i)
                new_rec = "INSERT INTO GIG_TRANSIT (NUM_SIG, user_id, copy_time, work_id, INS) VALUES ('{cap}', '{user}', '{today}', 1, '{nis}');".format(cap=key, user=user, today=today, nis=nis_test)
                query = self.session.execute(new_rec)
            except pymysql.Error, e:
                print("fail to insert: " + str(e))
#        query = self.session.execute(rec_test)
        self.session.commit()
#        result = query.fetchall()

#        new_rec = "INSERT INTO GIG_TRANSIT (NUM_SIG, user_id, copy_time, work_id, INS) VALUES ('25090A013100E000', 'simon.delcourt@imio.be', NOW(), 1, '25123');"
#        rec2 = "SELECT * FROM GIG_TRANSIT WHERE NUM_SIG = '25090A013100E000';"
#        engine.dispose()
#        gig_engine = services.gig.new_session()
        import ipdb; ipdb.set_trace()
