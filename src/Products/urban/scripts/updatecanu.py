# -*- coding: utf-8 -*-

import os
import glob
import psycopg2
import psycopg2.extras
import sys


def numpolice(sl1):

    NUM = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    i = 0
    sl1 = sl1.strip()
    sl1 = sl1.replace("+", "")
    sl1terms = sl1.split()
    num = sl1terms[len(sl1terms) - 1]
    if num[0] in NUM:
        return num
    else:
        return ""


try:
    login = sys.argv[1]
    password = sys.argv[2]
except:
    sys.exit(
        "\n\nthe correct syntax is: python updatecanu postgres_login postgres_password\n\n"
    )

conn = psycopg2.connect(
    "dbname='urbangis' user=" + login + " host='localhost' password=" + password
)
cur_canu = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_capa = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_map = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
upd_cur = conn.cursor()
# cur_canu.execute('ALTER TABLE canu ADD COLUMN numpolice character varying(15);')
# conn.commit()

cur_canu.execute("select gid,asText(the_geom) as canulocation, the_geom from canu")

recs = cur_canu.fetchall()
print "\n\n Pas d" "inquiètude, cette opération prends beaucoup de temps!!!"

for rec in recs:
    try:
        cur_capa.execute(
            "SELECT * from capa where contains(the_geom, '" + rec["the_geom"] + "')"
        )
    except:
        print "SELECT * from capa where contains(the_geom, '" + rec["the_geom"] + "')"
    res_cur_capa = cur_capa.fetchall()
    if len(res_cur_capa) == 1:
        cur_map.execute(
            "SELECT * from map where capakey='" + res_cur_capa[0]["capakey"] + "'"
        )
        res_cur_map = cur_map.fetchall()
        if len(res_cur_map) == 1:
            upd_cur.execute(
                "update canu set numpolice='"
                + numpolice(res_cur_map[0]["sl1"])
                + "' where gid="
                + str(rec["gid"])
                + ";"
            )
            conn.commit()
        else:
            print "error resmap"
    else:
        print "erreur rescapa"
upd_cur.execute("update canu set numpolice=NULL where numpolice='';")
conn.commit()
