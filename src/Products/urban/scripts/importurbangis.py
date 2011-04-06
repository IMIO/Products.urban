# -*- coding: utf-8 -*-

import os
import glob
import psycopg2
import psycopg2.extras
import sys


def convertprc(prc):
   
    AZ=['A','B','C','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    NUM=['0','1','2','3','4','5','6','7','8','9','0']
    i=0
    section=''
    radical=''
    bis=''
    exposant=''
    puissance=''
    prc=prc.strip()

    try:
        while i<=len(prc)-1 and prc[i] in AZ:
            section=section+prc[i]
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] == ' ':
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] in NUM:
            radical=radical+prc[i]
            i=i+1
    except:
        pass

    try:
        if prc[i] == '/':
            i=i+1
            while i<= len(prc)-1 and prc[i] in NUM:
                bis=bis+prc[i]
                i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] == ' ':
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] in AZ:
            exposant=exposant+prc[i]
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1:
            if prc[i] != ' ':
                puissance=puissance+prc[i]
            i=i+1
    except:
        pass
    if bis=='':
        bis='0'
    if puissance=='':
        puissance='0'
   
        
    return {'section':section,'radical':radical,'bis':bis,'exposant':exposant,'puissance':puissance}



def convertprcb(prc):
   
    AZ=['A','B','C','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    NUM=['0','1','2','3','4','5','6','7','8','9','0']
    i=0
    section=''
    radical=''
    bis=''
    exposant=''
    puissance=''
    prc=prc.strip()

    try:
        while i<=len(prc)-1 and prc[i] in AZ:
            section=section+prc[i]
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] == ' ':
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] in NUM:
            radical=radical+prc[i]
            i=i+1
    except:
        pass

    try:
        if prc[i] == '/':
            i=i+1
            while i<= len(prc)-1 and prc[i] in NUM:
                bis=bis+prc[i]
                i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] == ' ':
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1 and prc[i] in NUM:
            puissance=puissance+prc[i]
            i=i+1
    except:
        pass

    try:
        while i<= len(prc)-1:
            if prc[i] != ' ':
                exposant=exposant+prc[i]
            i=i+1
    except:
        pass
    if bis=='':
        bis='0'
    if puissance=='':
        puissance='0'
   
        
    return {'section':section,'radical':radical,'bis':bis,'exposant':exposant,'puissance':puissance}

def numpolice(sl1):
   
    NUM=['0','1','2','3','4','5','6','7','8','9','0']
    i=0
    sl1=sl1.strip()
    sl1=sl1.replace('+','')
    sl1terms=sl1.split()
    num=sl1terms[len(sl1terms)-1]
    if num[0] in NUM:
        return num
    else:
        return ''

try:
    login=sys.argv[1]
    password=sys.argv[2]
except:
    sys.exit('\n\nthe correct syntax is: python importurbangis postgres_login postgres_password\n\n')
    
tablenames=('NSR','PAS','ART','DA','PAS','MAP','NA','PE','PRC')
os.system('createdb urbangis')
os.system('createlang plpgsql urbangis')
os.system('psql -d urbangis -f matrice.sql')
for tablename in tablenames:
    try:
        os.remove(tablename.lower()+'.sql')
    except:
        pass
    os.system('mdb-export -I ck03out.mdb '+tablename+' > '+tablename.lower()+'temp.sql')
    commandesed= 'sed "s/\\x27/\\\'\\\'/g" '+tablename.lower()+'temp.sql >'+tablename.lower()+'temp1.sql'
    os.system(commandesed)
    commandesed= 'sed "s/\\x22/\\\'/g" '+tablename.lower()+'temp1.sql >'+tablename.lower()+'temp2.sql'
    os.system(commandesed)    
    if tablename=='PRC':
        commandesed= 'sed "s/in,/\\\"in\\\",/g" '+tablename.lower()+'temp2.sql >'+tablename.lower()+'temp3.sql'
        os.system(commandesed)
        commandesed= 'sed "s/14, 56,/n14, n56,/g" '+tablename.lower()+'temp3.sql >'+tablename.lower()+'temp4.sql'
        os.system(commandesed)        
        commandesed='sed \'s/$/;/\' '+tablename.lower()+'temp4.sql >'+tablename.lower()+'.sql'
        os.system(commandesed)
        os.remove(tablename.lower()+'temp3.sql')
        os.remove(tablename.lower()+'temp4.sql')        
    else:
        if tablename=='PE':
            commandesed= 'sed "s/, dr+/, dr2/g" '+tablename.lower()+'temp2.sql >'+tablename.lower()+'temp3.sql'
            os.system(commandesed)            
            commandesed='sed \'s/$/;/\' '+tablename.lower()+'temp3.sql >'+tablename.lower()+'.sql'
            os.system(commandesed)
            os.remove(tablename.lower()+'temp3.sql')            
        else:
            if tablename=='MAP':
                commandesed= 'sed "s/, pe+/, pe2/g" '+tablename.lower()+'temp2.sql >'+tablename.lower()+'temp3.sql'
                os.system(commandesed)            
                commandesed= 'sed "s/, prc+/, prc2/g" '+tablename.lower()+'temp3.sql >'+tablename.lower()+'temp4.sql'
                os.system(commandesed)            
                commandesed='sed \'s/$/;/\' '+tablename.lower()+'temp4.sql >'+tablename.lower()+'.sql'
                os.system(commandesed)
                os.remove(tablename.lower()+'temp3.sql')            
                os.remove(tablename.lower()+'temp4.sql')            
            else:
                commandesed='sed \'s/$/;/\' '+tablename.lower()+'temp2.sql >'+tablename.lower()+'.sql'
                os.system(commandesed)
    os.remove(tablename.lower()+'temp.sql')
    os.remove(tablename.lower()+'temp1.sql')
    os.remove(tablename.lower()+'temp2.sql')
    os.system('psql -q -d urbangis -f '+tablename.lower()+'.sql')
os.system('psql -q -d urbangis -f /usr/share/postgresql/8.4/contrib/postgis.sql')
os.system('psql -q -d urbangis -f /usr/share/postgresql/8.4/contrib/postgis_comments.sql')
os.system('psql -q -d urbangis -f /usr/share/postgresql/8.4/contrib/spatial_ref_sys.sql')

i=0
zipfiles=glob.glob('./*.zip')  
for zipfile in zipfiles:    
    os.system('unzip -o '+zipfile)    
    shapefilesnames=('CaBu','CaNu','CaPa','CaSh','CaSk','GeLi','GePn','GePt','InLi','InPt','ToLi','ToPt')    
    for shapefilename in shapefilesnames:
        if i==0:
            try:
                os.remove(shapefilename.lower()+'.sql')
            except:
                pass
            importcommand='shp2pgsql -I -W ISO-8859-1'
        else:
            importcommand='shp2pgsql -a -W ISO-8859-1'
        os.system(importcommand+' -s 31300 B_'+shapefilename+'.shp '+shapefilename.lower()+' >>'+shapefilename.lower()+'.sql')                
        os.remove('B_'+shapefilename+'.shp')
        os.remove('B_'+shapefilename+'.shx')
        os.remove('B_'+shapefilename+'.dbf')
    i=i+1
for shapefilename in shapefilesnames:
    try:
        os.remove(shapefilename.lower()+'.log')
    except:
        pass
    os.system('psql -q -o '+shapefilename.lower()+'.log -d urbangis -f '+shapefilename.lower()+'.sql')
conn = psycopg2.connect("dbname='urbangis' user="+login+" host='localhost' password="+password);
dict_cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
upd_cur = conn.cursor()
dict_cur.execute('ALTER TABLE capa ADD COLUMN da bigint;')
conn.commit()
dict_cur.execute('ALTER TABLE capa ADD COLUMN section character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE capa ADD COLUMN radical integer;')
conn.commit()
dict_cur.execute('ALTER TABLE capa ADD COLUMN exposant character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE capa ADD COLUMN bis integer;')
conn.commit()
dict_cur.execute('ALTER TABLE capa ADD COLUMN puissance integer;')
conn.commit()

dict_cur.execute('select * from map')

recs = dict_cur.fetchall()
print '\n\n Pas d''inquiètude, cette opération prends beaucoup de temps!!!'

for rec in recs:
    dict_prc=convertprc(rec['prc'])    
    upd_cur.execute('update capa set da='+str(rec['daa'])[0:5]+', section=\''+dict_prc['section']+'\', radical='+str(dict_prc['radical'])+', exposant=\''+dict_prc['exposant']+'\', bis='+dict_prc['bis']+', puissance='+dict_prc['puissance']+' where capakey = \''+rec['capakey']+'\';')
    conn.commit()
upd_cur.execute('update capa set exposant=NULL where exposant=\'\';')
conn.commit()

dict_cur.execute('ALTER TABLE pas ADD COLUMN "ID" bigserial;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD PRIMARY KEY ("ID");')
conn.commit()

dict_cur.execute('ALTER TABLE pas ADD COLUMN da bigint;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN section character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN radical integer;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN exposant character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN bis integer;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN puissance integer;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN sectionavant character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN radicalavant integer;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN exposantavant character varying(1);')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN bisavant integer;')
conn.commit()
dict_cur.execute('ALTER TABLE pas ADD COLUMN puissanceavant integer;')
conn.commit()
upd_cur = conn.cursor()
dict_cur.execute('select * from pas where ordb <> 9999')

recs = dict_cur.fetchall()

for rec in recs:
    try:
        da=str(rec['das'])[0:5]
        section=str(rec['das'])[5]
        if rec['prca'] != None:
            dict_prcavant=convertprc(rec['prca'])
            sqlprca=', sectionavant=\''+dict_prcavant['section']+'\', radicalavant='+str(dict_prcavant['radical'])+', exposantavant=\''+dict_prcavant['exposant']+'\', bisavant='+dict_prcavant['bis']+', puissanceavant='+dict_prcavant['puissance']
        else:
            sqlprca=''
        dict_prc=convertprcb(section+' '+str(rec['prcb1'])) 
        upd_cur.execute('update pas set da='+da+', section=\''+dict_prc['section']+'\', radical='+str(dict_prc['radical'])+', exposant=\''+dict_prc['exposant']+'\', bis='+dict_prc['bis']+', puissance='+dict_prc['puissance']+sqlprca+' where "ID" = '+str(rec['ID'])+';')
        conn.commit()
    except:
        pass
upd_cur.execute('update pas set exposant=NULL where exposant=\'\';')
conn.commit()
upd_cur.execute('update pas set exposantavant=NULL where exposantavant=\'\';')
conn.commit()
cur_canu = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_capa = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
cur_map = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
upd_cur = conn.cursor()
#cur_canu.execute('ALTER TABLE canu ADD COLUMN numpolice character varying(15);')
#conn.commit()

cur_canu.execute('select gid,asText(the_geom) as canulocation, the_geom from canu')

recs = cur_canu.fetchall()
print '\n\n Pas d''inquiètude, cette opération prends beaucoup de temps!!!'

for rec in recs:
    try:
        cur_capa.execute('SELECT * from capa where contains(the_geom, \''+rec['the_geom']+'\')')
    except:
        print 'SELECT * from capa where contains(the_geom, \''+rec['the_geom']+'\')'
    res_cur_capa=cur_capa.fetchall()
    if len (res_cur_capa) ==1:
        cur_map.execute('SELECT * from map where capakey=\''+res_cur_capa[0]['capakey']+'\'')
        res_cur_map=cur_map.fetchall()
        if len(res_cur_map)==1:
            upd_cur.execute('update canu set numpolice=\''+numpolice(res_cur_map[0]['sl1'])+'\' where gid='+ str(rec['gid']) +';')
            conn.commit()
        else:
            print 'error resmap'
    else:
        print 'erreur rescapa'
upd_cur.execute('update canu set numpolice=NULL where numpolice=\'\';')
conn.commit()

