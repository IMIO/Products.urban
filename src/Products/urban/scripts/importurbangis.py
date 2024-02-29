# -*- coding: utf-8 -*-

import sys

sys.path[0:0] = [
    # replace the following line with the urbanmap psycopg2 egg path,
    # according you run this script with the urbanmap python
    "/srv/urbanmap/eggs/psycopg2-2.4.2-py2.7-linux-x86_64.egg"
]

import os
import psycopg2
import psycopg2.extras
import sys
import time
import re

virtualenv_dir = "/srv/urbanmap"
urbanmap_dir = " % s/urbanMap" % virtualenv_dir  # directory where urbanmap is installed
pythoneggs_dir = "%s/python-eggs" % virtualenv_dir
config_dir = "%s/config" % urbanmap_dir  # a subdirectory config must be present !
pylon_instances_file = "%s/pylon_instances.txt" % config_dir
pg_address = "localhost:5432"  # set the ip address if the browser clients aren't local
domain_name = (
    "communesplone.be"  # the apache servername will be "urb-commune.communesplone.be"
)
CREATE_APACHE = True


def runCommand(cmd):
    """run an os command and get back the stdout and stderr outputs"""
    os.system(cmd + " >_cmd_pv.out 2>_cmd_pv.err")
    stdout = stderr = []
    try:
        if os.path.exists("_cmd_pv.out"):
            ofile = open("_cmd_pv.out", "r")
            stdout = ofile.readlines()
            ofile.close()
            os.remove("_cmd_pv.out")
        else:
            print ("File %s does not exist" % "_cmd_pv.out")
    except IOError:
        print ("Cannot open %s file" % "_cmd_pv.out")
    try:
        if os.path.exists("_cmd_pv.err"):
            ifile = open("_cmd_pv.err", "r")
            stderr = ifile.readlines()
            ifile.close()
            os.remove("_cmd_pv.err")
        else:
            print ("File %s does not exist" % "_cmd_pv.err")
    except IOError:
        print ("Cannot open %s file" % "_cmd_pv.err")
    return (stdout, stderr)


def convertprc(prc):
    AZ = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    NUM = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    i = 0
    section = ""
    radical = ""
    bis = ""
    exposant = ""
    puissance = ""
    prc = prc.strip()

    try:
        while i <= len(prc) - 1 and prc[i] in AZ:
            section = section + prc[i]
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] == " ":
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] in NUM:
            radical = radical + prc[i]
            i = i + 1
    except:
        pass

    try:
        if prc[i] == "/":
            i = i + 1
            while i <= len(prc) - 1 and prc[i] in NUM:
                bis = bis + prc[i]
                i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] == " ":
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] in AZ:
            exposant = exposant + prc[i]
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1:
            if prc[i] != " ":
                puissance = puissance + prc[i]
            i = i + 1
    except:
        pass
    if bis == "":
        bis = "0"
    if puissance == "":
        puissance = "0"

    return {
        "section": section,
        "radical": radical,
        "bis": bis,
        "exposant": exposant,
        "puissance": puissance,
    }


def convertprcb(prc):
    AZ = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    NUM = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    i = 0
    section = ""
    radical = ""
    bis = ""
    exposant = ""
    puissance = ""
    prc = prc.strip()

    try:
        while i <= len(prc) - 1 and prc[i] in AZ:
            section = section + prc[i]
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] == " ":
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] in NUM:
            radical = radical + prc[i]
            i = i + 1
    except:
        pass

    try:
        if prc[i] == "/":
            i = i + 1
            while i <= len(prc) - 1 and prc[i] in NUM:
                bis = bis + prc[i]
                i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] == " ":
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1 and prc[i] in NUM:
            puissance = puissance + prc[i]
            i = i + 1
    except:
        pass

    try:
        while i <= len(prc) - 1:
            if prc[i] != " ":
                exposant = exposant + prc[i]
            i = i + 1
    except:
        pass
    if bis == "":
        bis = "0"
    if puissance == "":
        puissance = "0"

    return {
        "section": section,
        "radical": radical,
        "bis": bis,
        "exposant": exposant,
        "puissance": puissance,
    }


def numpolice(sl1):
    NUM = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    sl1 = sl1.strip()
    sl1 = sl1.replace("+", "")
    sl1terms = sl1.split()
    num = sl1terms[len(sl1terms) - 1]
    if num[0] in NUM:
        return num
    else:
        return ""


try:
    action = sys.argv[1]
    databasename = sys.argv[2]
    login = sys.argv[3]
    password = sys.argv[4]
    if (
        ((action != "new") and (action != "update"))
        or databasename == ""
        or login == ""
        or password == ""
    ):
        sys.exit(
            "\n\nthe correct syntax is: python importurbangis new_or_update database_name "
            "postgres_login postgres_password\n\n"
        )
except:
    sys.exit(
        "\n\nthe correct syntax is: python importurbangis new_or_update database_name postgres_login "
        "postgres_password\n\n"
    )

allsteps = {
    "A": "creating db, role and tables",
    "B": "managing ck03out.mdb",
    "C": "adapting database with postgis",
    "D": "managing shape files",
    "E": "removing useless logs",
    "F": "altering table capa",
    "G": "updating table capa",
    "H": "altering table pas",
    "I": "updating table pas",
    "J": "managing the_geom",
    "K": "altering table canu",
    "L": "updating table canu",
    "M": "adding views",
    "N": "setting grants on db objects",
    "O": "creating pylon config file",
}
run_steps = sorted(allsteps.keys())
print "Starting at %s" % time.strftime("%H:%M:%S", time.localtime())
print "Here are the steps of the script:"
for step in run_steps:
    print " - %s : %s" % (step, allsteps[step])
print "You can choose to continue an interrupted importation if necessary."
ret = "1"
while ret and ret not in allsteps.keys():
    ret = raw_input(
        "Enter the step's letter from which you want to continue (press <Enter> to run all steps)>"
    ).upper()

# if adapted, can be used to choose step by step
if ret:
    run_steps = run_steps[run_steps.index(ret) :]

print ""
step = "A"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    if action == "new":
        os.system("createdb -O %s %s" % (login, databasename))

conn = psycopg2.connect(
    "dbname='"
    + databasename
    + "' user="
    + login
    + " host='localhost' password="
    + password
)
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
std_cur = conn.cursor()

tablenames = ["NSR", "PAS", "ART", "DA", "LT", "MAP", "NA", "PE", "PRC"]

if step in run_steps:
    if action == "new":
        dict_cur.execute("SELECT ROLNAME FROM PG_ROLES;")
        results = dict_cur.fetchall()
        if databasename not in [res[0] for res in results]:
            std_cur.execute("CREATE ROLE %s LOGIN NOINHERIT;" % databasename)
            std_cur.execute(
                "ALTER USER %s WITH PASSWORD '%s';" % (databasename, databasename)
            )
        dict_cur.execute("SELECT LANNAME FROM PG_LANGUAGE;")
        results = dict_cur.fetchall()
        if "plpgsql" not in [res[0] for res in results]:
            std_cur.execute("CREATE LANGUAGE plpgsql;")
    # can be changed
    if action == "update":
        for tablename in tablenames:
            if tablename != "DA":
                try:
                    std_cur.execute("DROP TABLE " + tablename.lower() + " CASCADE;")
                    conn.commit()
                except Exception, msg:
                    conn.rollback()
                    print "Cannot remove table '%s': %s" % (tablename, msg)
    print "If asked, enter the password of the postgres user '%s'" % login
    os.system("psql -d %s -U %s -f matrice.sql" % (databasename, login))

    conn.commit()

    cont = raw_input("Press anything to continue or x to exit: ")
    if cont in ("x", "X"):
        sys.exit(0)

step = "B"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    out, err = runCommand("mdb-export")
    backend = ""
    if "-I <backend>" in "".join(err):
        backend = "postgres"

    for tablename in tablenames:
        print "Processing table %d/%d ('%s')" % (
            tablenames.index(tablename) + 1,
            len(tablenames),
            tablename,
        )
        tnl = tablename.lower()
        try:
            os.remove("%s.sql" % tnl)
        except:
            pass
        os.system(
            "mdb-export -I %s -q \\' ck03out.mdb %s > %s_temp.sql" % (backend, tnl, tnl)
        )

        # we remove the doublequotes wrapping table name and columns names
        commandesed = (
            'sed "h;s/^.* VALUES //;x;s/^\\(.* VALUES \\).*/\\1/;s/\\x22//g;G;s/\\n//" '
            "%s_temp.sql >%s_temp1.sql" % (tnl, tnl)
        )
        # h : copy the line (actual pattern space) to hold space
        # s/^.* VALUES // : remove the first part of the line
        # x : exchange pattern space and hold space
        # s/^\(.* VALUES \).*/\1/ : replace entire content with first part
        # s/\x22//g : remove doublequotes
        # G : concatenate pattern space, \n and hold space
        # s/\n// : remove \n
        os.system(commandesed)
        # import shutil
        # shutil.copyfile('/srv/import_urban/spa/%s_temp1.sql'%tnl, '/srv/import_urban/spa/%s_oldsed.sql'%tnl)
        if tablename == "PRC":
            commandesed = 'sed "s/in,/\\"in\\",/g" %s_temp1.sql >%s_temp3.sql' % (
                tnl,
                tnl,
            )
            os.system(commandesed)
            commandesed = 'sed "s/14, 56,/n14, n56,/g" %s_temp3.sql >%s_temp4.sql' % (
                tnl,
                tnl,
            )
            os.system(commandesed)
            commandesed = 'sed "s/$/;/" %s_temp4.sql >%s.sql' % (tnl, tnl)
            os.system(commandesed)
            os.remove("%s_temp3.sql" % tnl)
            os.remove("%s_temp4.sql" % tnl)
        elif tablename == "PE":
            commandesed = 'sed "s/, dr+/, dr2/g" %s_temp1.sql >%s_temp3.sql' % (
                tnl,
                tnl,
            )
            os.system(commandesed)
            commandesed = 'sed "s/$/;/" %s_temp3.sql >%s.sql' % (tnl, tnl)
            os.system(commandesed)
            os.remove("%s_temp3.sql" % tnl)
        elif tablename == "MAP":
            commandesed = 'sed "s/, pe+/, pe2/g" %s_temp1.sql >%s_temp3.sql' % (
                tnl,
                tnl,
            )
            os.system(commandesed)
            commandesed = 'sed "s/, prc+/, prc2/g" %s_temp3.sql >%s_temp4.sql' % (
                tnl,
                tnl,
            )
            os.system(commandesed)
            commandesed = "sed 's/$/;/' %s_temp4.sql >%s.sql" % (tnl, tnl)
            os.system(commandesed)
            os.remove("%s_temp3.sql" % tnl)
            os.remove("%s_temp4.sql" % tnl)
        else:
            commandesed = 'sed "s/$/;/" %s_temp1.sql >%s.sql' % (tnl, tnl)
            os.system(commandesed)
        os.remove("%s_temp.sql" % tnl)
        os.remove("%s_temp1.sql" % tnl)
        if not ((tablename == "DA") and (action == "update")):
            os.system("psql -q -d " + databasename + " -f %s.sql" % tnl)
        if tablename == "DA" and action == "new":
            dict_cur.execute("ALTER TABLE da ADD COLUMN divname character varying(50);")
            dict_cur.execute("select da, dan1 from da;")
            results = dict_cur.fetchall()
            for (da, dan1) in results:
                prop = dan1.capitalize()
                number = re.search("(\d+)", prop)
                pos = dan1.find("DIV/")
                if pos >= 0:
                    prop = prop[pos + 4 :]
                    pos = prop.find("/")
                    if pos >= 0:
                        prop = prop[:pos]
                # no locality, remove multiple spaces
                elif prop.find(" ") > 0:
                    prop = " ".join([x for x in prop.split(" ") if x])
                prop = prop.capitalize()
                if prop.endswith(" div"):
                    ville = prop.split(" ")
                    prop = ville[0]
                prop = prop + " (" + number.group(1) + ")"
                divvalue = raw_input(
                    "Enter a divname value for '%s': proposed '%s' (press <Enter> to keep the "
                    "proposed value)>" % (dan1, prop)
                )
                if not divvalue:
                    divvalue = prop
                dict_cur.execute(
                    "update da set divname='%s' where da = %d;"
                    % (divvalue.replace("'", "''"), da)
                )
    conn.commit()

step = "C"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    if action == "new":
        if os.path.exists("/usr/share/postgresql/9.1/contrib/postgis-1.5"):
            os.system(
                "psql -q -d %s -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql"
                % databasename
            )
            os.system(
                "psql -q -d " + databasename + " -f "
                "/usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql"
            )
            os.system(
                "psql -q -d "
                + databasename
                + " -f /usr/share/postgresql/9.1/contrib/postgis_comments.sql"
            )
        elif os.path.exists("/usr/share/postgresql/8.4/contrib/postgis-1.5"):
            os.system(
                "psql -q -d %s -f /usr/share/postgresql/8.4/contrib/postgis-1.5/postgis.sql"
                % databasename
            )
            os.system(
                "psql -q -d " + databasename + " -f "
                "/usr/share/postgresql/8.4/contrib/postgis-1.5/spatial_ref_sys.sql"
            )
            os.system(
                "psql -q -d "
                + databasename
                + " -f /usr/share/postgresql/8.4/contrib/postgis_comments.sql"
            )
        elif os.path.exists("/usr/share/postgresql/8.4/contrib/postgis.sql"):
            os.system(
                "psql -q -d %s -f /usr/share/postgresql/8.4/contrib/postgis.sql"
                % databasename
            )
            os.system(
                "psql -q -d "
                + databasename
                + " -f /usr/share/postgresql/8.4/contrib/spatial_ref_sys.sql"
            )
            os.system(
                "psql -q -d "
                + databasename
                + " -f /usr/share/postgresql/8.4/contrib/postgis_comments.sql"
            )
        elif os.path.exists("/usr/share/postgresql-8.3-postgis"):
            os.system(
                "psql -q -d "
                + databasename
                + " -f  /usr/share/postgresql-8.3-postgis/lwpostgis.sql"
            )
            os.system(
                "psql -q -d "
                + databasename
                + " -f /usr/share/postgresql-8.3-postgis/spatial_ref_sys.sql"
            )
        else:
            print "path for postgis sql files not found"

    conn.commit()
# cont = raw_input("Press anything to continue or x to exit: ")
# if cont in ('x', 'X'):
#    sys.exit(0)

step = "D"
shapefilesnames = (
    "CaBu",
    "CaNu",
    "CaPa",
    "GeLi",
    "GePn",
    "GePt",
    "InLi",
    "InPt",
    "ToLi",
    "ToPt",
)
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    error = False
    for shapefilename in shapefilesnames:
        sfl = shapefilename.lower()
        if action == "update":
            try:
                command = "DROP TABLE %s CASCADE;" % sfl
                dict_cur.execute(command)
                conn.commit()
            except Exception, msg:
                conn.rollback()
                error = True
                print "Cannot execute '%s': %s" % (sfl, msg)
        if os.path.exists("%.sql" % sfl):
            os.remove("%.sql" % sfl)
        os.system(
            "shp2pgsql -I -W ISO-8859-1 -s 31370 B_"
            + shapefilename
            + ".shp "
            + sfl
            + " >"
            + sfl
            + ".sql"
        )

    if error:
        cont = raw_input("Press anything to continue or x to exit: ")
        if cont in ("x", "X"):
            sys.exit(0)

    conn.commit()

step = "E"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    for shapefilename in shapefilesnames:
        try:
            os.remove(shapefilename.lower() + ".log")
        except:
            pass
        os.system(
            "psql -q -o "
            + shapefilename.lower()
            + ".log -d "
            + databasename
            + " -f "
            + shapefilename.lower()
            + ".sql"
        )

    conn.commit()

step = "F"
upd_cur = conn.cursor()
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    dict_cur.execute("ALTER TABLE capa ADD COLUMN da bigint;")
    dict_cur.execute("ALTER TABLE capa ADD COLUMN section character varying(1);")
    dict_cur.execute("ALTER TABLE capa ADD COLUMN radical integer;")
    dict_cur.execute("ALTER TABLE capa ADD COLUMN exposant character varying(1);")
    dict_cur.execute("ALTER TABLE capa ADD COLUMN bis integer;")
    dict_cur.execute("ALTER TABLE capa ADD COLUMN puissance integer;")

    conn.commit()

step = "G"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    dict_cur.execute("select * from map")

    recs = dict_cur.fetchall()
    print "\nPas d" "inquiétude, cette opération prends beaucoup de temps!!!"
    lenrecs = len(recs)
    steps = {
        lenrecs / 5: "1/5",
        (lenrecs / 5) * 2: "2/5",
        (lenrecs / 5) * 3: "3/5",
        (lenrecs / 5) * 4: "4/5",
    }
    i = 0
    for rec in recs:
        if i in steps.keys():
            print "Reached %s" % steps[i]
        i = i + 1
        dict_prc = convertprc(rec["prc"])
        upd_cur.execute(
            "update capa set da="
            + str(rec["daa"])[0:5]
            + ", section='"
            + dict_prc["section"]
            + "', radical="
            + str(dict_prc["radical"])
            + ", exposant='"
            + dict_prc["exposant"]
            + "', bis="
            + dict_prc["bis"]
            + ", puissance="
            + dict_prc["puissance"]
            + " where capakey = '"
            + rec["capakey"]
            + "';"
        )
    print "Reached 5/5"

    upd_cur.execute("update capa set exposant=NULL where exposant='';")
    conn.commit()

step = "H"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    dict_cur.execute('ALTER TABLE pas ADD COLUMN "ID" bigserial;')
    dict_cur.execute('ALTER TABLE pas ADD PRIMARY KEY ("ID");')
    dict_cur.execute("ALTER TABLE pas ADD COLUMN da bigint;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN section character varying(1);")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN radical integer;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN exposant character varying(1);")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN bis integer;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN puissance integer;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN sectionavant character varying(1);")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN radicalavant integer;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN exposantavant character varying(1);")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN bisavant integer;")
    dict_cur.execute("ALTER TABLE pas ADD COLUMN puissanceavant integer;")

    conn.commit()

step = "I"
upd_cur = conn.cursor()
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    dict_cur.execute("select * from pas where ordb <> 9999")

    recs = dict_cur.fetchall()
    lenrecs = len(recs)
    steps = {
        lenrecs / 5: "1/5",
        (lenrecs / 5) * 2: "2/5",
        (lenrecs / 5) * 3: "3/5",
        (lenrecs / 5) * 4: "4/5",
    }
    i = 0

    for rec in recs:
        if i in steps.keys():
            print "Reached %s" % steps[i]
        i = i + 1
        try:
            da = str(rec["das"])[0:5]
            section = str(rec["das"])[5]
            if rec["prca"] is not None:
                dict_prcavant = convertprc(rec["prca"])
                sqlprca = (
                    ", sectionavant='"
                    + dict_prcavant["section"]
                    + "', radicalavant="
                    + str(dict_prcavant["radical"])
                    + ", exposantavant='"
                    + dict_prcavant["exposant"]
                    + "', bisavant="
                    + dict_prcavant["bis"]
                    + ", puissanceavant="
                    + dict_prcavant["puissance"]
                )
            else:
                sqlprca = ""
            dict_prc = convertprcb(section + " " + str(rec["prcb1"]))
            upd_cur.execute(
                "update pas set da="
                + da
                + ", section='"
                + dict_prc["section"]
                + "', radical="
                + str(dict_prc["radical"])
                + ", exposant='"
                + dict_prc["exposant"]
                + "', bis="
                + dict_prc["bis"]
                + ", puissance="
                + dict_prc["puissance"]
                + sqlprca
                + ' where "ID" = '
                + str(rec["ID"])
                + ";"
            )
        except:
            pass

    upd_cur.execute("update pas set exposant=NULL where exposant='';")
    upd_cur.execute("update pas set exposantavant=NULL where exposantavant='';")

    conn.commit()

step = "J"
cur_canu = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_capa = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_map = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
upd_cur = conn.cursor()
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
#   cur_canu.execute('ALTER TABLE canu ADD COLUMN numpolice character varying(15);')
#   conn.commit()

step = "K"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    cur_canu.execute("select gid,asText(the_geom) as canulocation, the_geom from canu")
    recs = cur_canu.fetchall()
    lenrecs = len(recs)
    steps = {
        lenrecs / 5: "1/5",
        (lenrecs / 5) * 2: "2/5",
        (lenrecs / 5) * 3: "3/5",
        (lenrecs / 5) * 4: "4/5",
    }
    i = 0
    print "\nPas d" "inquiétude, cette opération prends beaucoup de temps!!!"
    dict_cur.execute(
        "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='%s';"
        % "canu"
    )
    columns = [
        col["column_name"]
        for col in dict_cur.fetchall()
        if col["column_name"] == "numpolice"
    ]
    if not len(columns):
        dict_cur.execute("ALTER TABLE canu ADD COLUMN numpolice character varying(15);")

    for rec in recs:
        if i in steps.keys():
            print "Reached %s" % steps[i]
        i = i + 1
        try:
            cur_capa.execute(
                "SELECT * from capa where contains(the_geom, '" + rec["the_geom"] + "')"
            )
        except:
            print "SELECT * from capa where contains(the_geom, '" + rec[
                "the_geom"
            ] + "')"
        res_cur_capa = cur_capa.fetchall()
        if len(res_cur_capa) == 1:
            cur_map.execute(
                "SELECT * from map where capakey='" + res_cur_capa[0]["capakey"] + "'"
            )
            res_cur_map = cur_map.fetchall()
            if len(res_cur_map) == 1:
                try:
                    upd_cur.execute(
                        "update canu set numpolice='"
                        + numpolice(res_cur_map[0]["sl1"])
                        + "' where gid="
                        + str(rec["gid"])
                        + ";"
                    )
                except Exception, msg:
                    print (
                        "error when updating numpolice in canu for geom='%s', capakey='%s', gid='%s', "
                        "sl1='%s'"
                        % (
                            rec["the_geom"],
                            res_cur_capa[0]["capakey"],
                            rec["gid"],
                            res_cur_map[0]["sl1"],
                        )
                    )
    print "Reached 5/5"

    conn.commit()

step = "L"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    upd_cur.execute("update canu set numpolice=NULL where numpolice='';")

    conn.commit()

step = "M"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    v_map_capa_cmd = (
        "CREATE OR REPLACE VIEW v_map_capa AS "
        "SELECT map.capakey, map.capakey AS codeparcelle, map.urbainkey, map.daa, map.ord, map.sl1, "
        "map.prc, map.na1, map.co1, map.cod1, map.ri1, map.acj, map.tv, map.prc2, capa.capaty, "
        "capa.shape_area, capa.the_geom, capa.da, capa.section, capa.radical, capa.exposant, capa.bis, "
        'capa.puissance, prc."in", prc.ha1, prc.rscod, '
        "array_to_string(ARRAY( SELECT pe.pe FROM pe WHERE pe.daa = map.daa "
        "  ORDER BY pe.pos), '; '::text) AS pe, "
        "array_to_string(ARRAY( SELECT pe.adr1 FROM pe WHERE pe.daa = map.daa "
        "  ORDER BY pe.pos), '; '::text) AS adr1, "
        "array_to_string(ARRAY( SELECT pe.adr2 FROM pe WHERE pe.daa = map.daa "
        "  ORDER BY pe.pos), '; '::text) AS adr2 "
        "FROM map "
        "LEFT JOIN capa ON map.capakey::text = capa.capakey::text "
        "LEFT JOIN prc ON map.daa = prc.daa AND map.ord::text = prc.ord::text "
        "ORDER BY map.capakey, map.sl1, array_to_string(ARRAY( SELECT pe.pe "
        "  FROM pe WHERE pe.daa = map.daa ORDER BY pe.pos), '; '::text);"
    )

    std_cur.execute(v_map_capa_cmd)

    std_cur.execute(
        "CREATE OR REPLACE VIEW v_sections AS \
 SELECT DISTINCT capa.section, capa.section::text AS section_text  FROM capa;"
    )

    std_cur.execute("CREATE INDEX gelity_idx ON geli (GELITY ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX geptty_idx ON GePt (GEPTTY ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX gepnty_idx ON GePn (GEPNTY ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX inlity_idx ON InLi (INLITY ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX tolity_idx ON ToLi (TOLITY ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX toptty_idx ON ToPt (TOPTTY ASC NULLS LAST);")
    std_cur.execute("CREATE UNIQUE INDEX geli_pk_idx ON GeLi USING btree  (gid);")
    std_cur.execute("CREATE UNIQUE INDEX gept_pk_idx ON GePt USING btree  (gid);")
    std_cur.execute("CREATE UNIQUE INDEX gepn_pk_idx ON GePn USING btree  (gid);")
    std_cur.execute("CREATE UNIQUE INDEX inli_pk_idx ON InLi USING btree  (gid);")
    std_cur.execute("CREATE UNIQUE INDEX toli_pk_idx ON ToLi USING btree  (gid);")
    std_cur.execute("CREATE UNIQUE INDEX topt_pk_idx ON ToPt USING btree  (gid);")
    std_cur.execute("CREATE INDEX cabuty_idx ON cabu (cabuty ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX capaty_idx ON capa (capaty ASC NULLS LAST);")
    std_cur.execute("CREATE INDEX pe_daa_idx ON pe using btree(daa);")
    std_cur.execute("CREATE INDEX map_daa_idx ON map using btree(daa);")

    conn.commit()

step = "N"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    std_cur.execute("REVOKE ALL ON SCHEMA PUBLIC FROM PUBLIC;")
    std_cur.execute("GRANT USAGE ON SCHEMA PUBLIC TO %s;" % databasename)
    std_cur.execute("SELECT OID FROM PG_NAMESPACE where NSPNAME = 'public';")
    rec = std_cur.fetchone()
    if not rec:
        print "error when getting oid of schema 'public'"
    else:
        oid = rec[0]
        # grants on functions and trigger functions
        dict_cur.execute(
            "SELECT PR.PRONAME, PR.PROARGTYPES FROM PG_PROC PR WHERE PROISAGG = FALSE AND "
            "PRONAMESPACE = %s::OID ORDER BY PRONAME;" % oid
        )
        recs = dict_cur.fetchall()
        for rec in recs:
            args = []
            if rec["proargtypes"]:
                for argtype in rec["proargtypes"].split(" "):
                    std_cur.execute(
                        "SELECT TYPNAME FROM PG_TYPE where OID=%s;" % argtype
                    )
                    argname = std_cur.fetchone()[0]
                    args.append(argname)
            std_cur.execute(
                "GRANT EXECUTE ON FUNCTION %s(%s) TO %s"
                % (rec["proname"], ",".join(args), databasename)
            )
    # grants on tables
    dict_cur.execute("SELECT TABLENAME FROM PG_TABLES WHERE SCHEMANAME='public';")
    for rec in dict_cur.fetchall():
        std_cur.execute(
            "GRANT SELECT, REFERENCES, TRIGGER ON TABLE %s TO %s;"
            % (rec["tablename"], databasename)
        )
    # grants on views
    dict_cur.execute("SELECT VIEWNAME FROM PG_VIEWS WHERE SCHEMANAME='public';")
    for rec in dict_cur.fetchall():
        std_cur.execute(
            "GRANT SELECT, REFERENCES, TRIGGER ON TABLE %s TO %s;"
            % (rec["viewname"], databasename)
        )

    conn.commit()

step = "O"
if step in run_steps:
    print "Step %s (%s): %s" % (
        step,
        time.strftime("%H:%M:%S", time.localtime()),
        allsteps[step],
    )
    if urbanmap_dir:
        if not os.path.exists(urbanmap_dir):
            print "Error: urbanmap dir '%s' not exists" % urbanmap_dir
        elif not os.path.exists(config_dir):
            print "Error: config dir '%s' not exists" % config_dir
        else:
            max_port = 5000
            instance_exists = False
            ini_file = os.path.join(config_dir, "%s.ini" % databasename)
            wsgi_file = os.path.join(config_dir, "%s.wsgi" % databasename)
            apache_file = os.path.join(config_dir, "%s.apache" % databasename)
            if os.path.exists(pylon_instances_file):
                ifile = open(pylon_instances_file, "r")
                for line in ifile:
                    line = line.strip("\n")
                    if not line:
                        continue
                    path, file, port = line.split(";")
                    port = int(port)
                    if os.path.join(path, "config", file) == os.path.join(
                        config_dir, databasename
                    ):
                        instance_exists = True
                        max_port = port
                        break
                    if port > max_port:
                        max_port = port
                ifile.close()
            if not max_port or not instance_exists:
                max_port += 1
            if not instance_exists:
                ofile = open(pylon_instances_file, "a")
                ofile.write("%s;%s;%s\n" % (urbanmap_dir, databasename, max_port))
                ofile.close()
                print "Modifying %s" % pylon_instances_file
            import socket

            serverip = socket.gethostbyname(socket.gethostname())
            pathname = os.path.join(os.path.dirname(sys.argv[0]), "config")
            if not os.path.exists(pathname):
                print "Error: base files dir '%s' not exists" % pathname
            if not os.path.exists(ini_file):
                std_cur.execute("select min(admnr) from da;")
                rec = std_cur.fetchone()
                if not rec:
                    print "error when getting admnr from da"
                else:
                    INS = rec[0]
                    print "INS='%s'" % INS
                    ifile = open(os.path.join(pathname, "urbanmap_base.ini"))
                    out = []
                    for line in ifile:
                        outline = line.replace("#PORT#", str(max_port))
                        outline = outline.replace("#INS#", INS)
                        outline = outline.replace(
                            "#MAPFISHPRINTDIR#", os.path.dirname(urbanmap_dir)
                        )
                        outline = outline.replace("#URBANMAPDIR#", urbanmap_dir)
                        outline = outline.replace("#SERVERIP#", serverip)
                        outline = outline.replace(
                            "#APACHESERVER#",
                            "%s.%s" % (databasename.replace("_", "-"), domain_name),
                        )
                        outline = outline.replace(
                            "#SQLALCHEMYURL#",
                            "postgresql://%s:%s@%s/%s"
                            % (databasename, databasename, pg_address, databasename),
                        )
                        out.append(outline)
                    ifile.close()
                    ofile = open(ini_file, "w")
                    for line in out:
                        ofile.write(line)
                    ofile.close()
                    print "Writing %s" % ini_file
            if not os.path.exists(wsgi_file):
                wfile = open(os.path.join(pathname, "urbanmap_base.wsgi"))
                out = []
                for line in wfile:
                    outline = line.replace("#URBANMAPDIR#", urbanmap_dir)
                    outline = outline.replace("#PYTHONEGGCACHE#", pythoneggs_dir)
                    outline = outline.replace("#URBANMAPINI#", ini_file)
                    out.append(outline)
                wfile.close()
                ofile = open(wsgi_file, "w")
                for line in out:
                    ofile.write(line)
                ofile.close()
                print "Writing %s" % wsgi_file
            if CREATE_APACHE and not os.path.exists(apache_file):
                afile = open(os.path.join(pathname, "urbanmap_base.apache"))
                out = []
                for line in afile:
                    outline = line.replace("#URBANMAPDIR#", urbanmap_dir)
                    outline = outline.replace("#VIRTUALENVDIR#", virtualenv_dir)
                    outline = outline.replace("#SERVERIP#", serverip)
                    outline = outline.replace(
                        "#APACHESERVER#",
                        "%s.%s" % (databasename.replace("_", "-"), domain_name),
                    )
                    outline = outline.replace("#URBANMAPWSGI#", wsgi_file)
                    outline = outline.replace(
                        "#APACHEERRORLOG#",
                        os.path.join(config_dir, "%s_error.log" % databasename),
                    )
                    outline = outline.replace(
                        "#APACHEACCESSLOG#",
                        os.path.join(config_dir, "%s_access.log" % databasename),
                    )
                    out.append(outline)
                afile.close()
                ofile = open(apache_file, "w")
                for line in out:
                    ofile.write(line)
                ofile.close()
                print "Writing %s" % apache_file

print "Ending at %s" % time.strftime("%H:%M:%S", time.localtime())
