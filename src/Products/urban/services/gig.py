# -*- coding: utf-8 -*-

from Products.urban.services.mysqlbase import MySQLService
from Products.urban.services.mysqlbase import MySQLSession


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
        import ipdb; ipdb.set_trace()
        parcels_keys = [c.replace('/', '') for c in capakeys]
        filenis = '/srv/instances/server_urban25/var/urban/urbanmap.cfg'
        with open(filenis, 'r') as f:
            lines = f.readlines()
        nis = lines[1][4:]
#        new_rec = "INSERT INTO GIG_TRANSIT (NUM_SIG, user_id, copy_time, work_id, INS) VALUES ('25090A013100E000', 'simon.delcourt@imio.be', NOW(), 1, '25123');"
#        rec2 = "SELECT * FROM GIG_TRANSIT WHERE NUM_SIG = '25090A013100E000';"
#        resinsert = session.execute(new_rec)
#        resselect = session.execute(rec2)
#        session.commit()
#        resselect.fetchall()
#        session.close()
#        engine.dispose()
#        gig_engine = services.gig.new_session()
