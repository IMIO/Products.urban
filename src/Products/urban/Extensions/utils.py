# -*- coding: utf-8 -*-
#utilities

import os, re

def check_role(self, role='Manager', context=None):
    from Products.CMFCore.utils import getToolByName
    pms = getToolByName(self, 'portal_membership')
    return pms.getAuthenticatedMember().has_role(role, context)

def check_zope_admin():
    from AccessControl.SecurityManagement import getSecurityManager
    user = getSecurityManager().getUser()
    if user.has_role('Manager') and user.__module__ == 'Products.PluggableAuthService.PropertiedUser':
        return True
    return False

###############################################################################

def urban_check_addresses(self, restore=''):
    """
        Check licences addresses: status, saving/restoring
    """
    if not check_zope_admin():
        return "You must be a zope manager to run this script"
    out = []
    details = []
    saved = {}
    do_restore = False
    if restore not in ('', '0', 'False', 'false'):
        do_restore = True

    from Products.CMFCore.utils import getToolByName
    site = getToolByName(self, 'portal_url').getPortalObject()
    uidc = getToolByName(self, 'uid_catalog')

    def dump_dic(outfile, dic):
        ofile = open( outfile, 'w')
        ofile.write(dic.__str__())
        ofile.close()
    def load_dic(infile, dic):
        if os.path.exists(infile):
            ofile = open( infile, 'r')
            dic.update(eval(ofile.read()))
            ofile.close()
    import os
    home = os.environ.get('INSTANCE_HOME') # like .../parts/instance in a buildout env
    save_file = os.path.join(home, '../../saved_addresses.txt') # root of the buildout
    load_dic(save_file, saved)

    brains = site.portal_catalog(portal_type = ['BuildLicence', 'Declaration', 'Division', 'EnvironmentalDeclaration', 'UrbanCertificateOne', 'UrbanCertificateTwo', 'ParcelOutLicence'])
    count_db_lic = count_db_good = count_db_bad =count_db_ns = count_fl_good = count_fl_rest = count_fl_new = 0
    #import ipdb; ipdb.set_trace()
    for brain in brains:
        count_db_lic += 1
        lic = brain.getObject()
        path = brain.getPath()
        addresses = lic.getWorkLocations()
        # the licence isn't yet in the saved dict
        if not saved.has_key(path):
            saved[path] = {'addr':addresses}
            count_db_ns += 1
        # the saved licence contains an address
        elif len(saved[path]['addr']):
            count_fl_good += 1
            if not len(addresses):
                count_fl_rest += 1
                if do_restore:
                    found = True
                    for addr in saved[path]['addr']:
                        if not uidc(UID=addr['street']): found = False
                    if found:
                        lic.setWorkLocations(saved[path]['addr'])
                        details.append("%s: %s"%(path, str(lic.getWorkLocations())))
                    else:
                        details.append("%s: %s !! some streets not found in db"%(path, str(saved[path]['addr'])))
                    #obj.reindexObject()
        # the saved licence doesn't contain any address, we have to complete it
        elif len(addresses):
            count_fl_new += 1
            saved[path]['addr'] = addresses
            
        if len(addresses):
            count_db_good += 1
        else:
            count_db_bad += 1

    dump_dic(save_file, saved)
    out.append("<b>In current db</b>")
    out.append("Number of licences: %d"%count_db_lic)
    out.append("Licences with addresses: %d"%count_db_good)
    out.append("Licences without addresses: %d"%count_db_bad)
    out.append("<br /><b>Compared to saved</b>")
    out.append("Number of licences not yet saved: %d"%count_db_ns)
    out.append("Saved licences with addr: %d"%count_fl_good)
    out.append("Saved licences with new addr: %d"%count_fl_new)
    out.append("Saved licences with addr to restore: %d"%count_fl_rest)
    out += details
    return '<br />\n'.join(out)

###############################################################################

def urban_replace_templates(self, replace_globals=0, replace_events=0):
    """
        Call the updateAllUrbanTemplates from tests profile.
        Must be called with ...?replace_globals=1&replace_events=1 in url to replace all templates
    """
    if not check_zope_admin():
        return "You must be a zope manager to run this script"
    if not replace_globals and not replace_events:
        return "Must be called with some parameters to do something\n" + \
               "-> replace_globals=1 to force replacing globals templates (header, footer, styles, ...)\n" + \
               "-> replace_events=1 to force replacing events templates\n" + \
               "by example ...?replace_events=1\n"
    
    from Products.CMFCore.utils import getToolByName
    ps = getToolByName(self, 'portal_setup')
    ps.runImportStepFromProfile('profile-Products.urban:tests',
            'urban-updateAllUrbanTemplates', run_dependencies=False)
    from datetime import datetime
    return "Finished at %s"%datetime(1973,02,12).now()

###############################################################################

def create_urban_site(self, name='', nis='', pghost='localhost', dbname='', dbuser='', dbpwd='', geohost='', pylonhost=''):
    """
        creates an urban plone site
    """
    if not check_zope_admin():
        return "You must be a zope manager to run this script"
    out = []
    sep = '\n'
    def verbose(line):
        out.append(line)
    def error(line):
        out.append("!! %s"%line)

    if not name:
        #out.append("available properties:%s"%portal.portal_memberdata.propertyItems())
        out.append("call the script followed by those parameters:")
        out.append("-> name=string : mountpoint and site name")
        out.append("-> nis=number : nis number")
        out.append("-> pghost=ip:port : postgres host")
        out.append("-> dbname=string : database name")
        out.append("-> dbuser=string : database user")
        out.append("-> dbpwd=string : database password")
        out.append("-> geohost=ip:port : geoserver host")
        out.append("-> pylonhost=ip:port : pylons server host")
        out.append("by example ...?name=namur&nis=92141&...%s"%sep)
        return sep.join(out)

    #checking we are at the zope root level
    from OFS.Application import Application
    if self.__class__ != Application:
        out.append("You have to run this script at the root ZMI level")
        return sep.join(out)

    #creating mount point
    from Products.ZODBMountPoint.MountedObject import manage_addMounts
    from ZConfig import ConfigurationError
    if name not in self.objectIds('Folder'):
        try:
            manage_addMounts(self, ('/%s'%name,))
            verbose("Created mount point '%s'"%name)
        except ConfigurationError, msg:
            error("Mount point not well configured: '%s'"%msg)
            return sep.join(out)
    mp = getattr(self, name)

    #creating Plone site
    from Products.CMFPlone.factory import addPloneSite
    if name in mp.objectIds('Plone Site'):
        error("Site '%s' already exists"%name)
#        mp.manage_delObjects(ids=[name]) #in test mode
    else:
        try:
            site = addPloneSite(mp, name, title='Application Urbanisme en test', extension_ids=('Products.urban:default','Products.urbanskin:default'), create_userfolder=False, validate_email=False, default_language='fr', setup_content=False)
            verbose("Created plone site '%s'"%name)
        except Exception, msg:
            error("Plone site not created: %s"%msg)
            return sep.join(out)

    #configuring site
    site = getattr(mp, name)
    pu = site.portal_urban
    if not pu.getSqlHost():
        pu.setSqlHost(pghost)
    if not pu.getCityName():
        pu.setCityName(name)
    if nis and not pu.getNISNum():
        pu.setNISNum(nis)
    if not dbname:
        dbname = 'urb_%s'%name
    if not pu.getSqlName():
        pu.setSqlName(dbname)
    if not dbuser:
        dbuser = dbname
    if not pu.getSqlUser():
        pu.setSqlUser(dbuser)
    if not dbpwd:
        dbpwd = dbname
    if not pu.getSqlPassword():
        pu.setSqlPassword(dbpwd)
    if geohost and not pu.getWebServerHost():
        pu.setWebServerHost(geohost)
    if pylonhost and not pu.getPylonsHost():
        pu.setPylonsHost(pylonhost)

    #running extra steps
    ps = site.portal_setup
    #runImportStepFromProfile(self, profile_id, step_id, run_dependencies=True
    ps.runAllImportStepsFromProfile('profile-Products.urban:extra')

    #running tests steps
    ps.runImportStepFromProfile('profile-Products.urban:tests', 'urban-addTestObjects', run_dependencies=True)
    #ps.runAllImportStepsFromProfile('profile-Products.urban:tests', ignore_dependencies=True)

    return sep.join(out)

###############################################################################

def create_site_from_pylon(self, pif='', geohost='', dochange='0'):
    """
        Creates urban sites from pylon configuration files
    """
    if not check_zope_admin():
        return "You must be a zope manager to run this script"
    out = []
    sep = '\n'
    def verbose(line):
        out.append(line)
    def error(line):
        out.append("!! %s"%line)
    pif = '/srv/urbanmap/urbanMap/config/pylon_instances.txt'
    apply=False
    if dochange not in ('', '0', 'False', 'false'):
        apply=True

    out.append("call the script followed by those parameters:")
    out.append("-> pif=string : pylons instances file")
    out.append("-> geohost=ip:port : geoserver host")
    out.append("-> dochange=0 : apply changes")
    out.append("by example ...?dirname=/srv/urbanmap/config %s"%sep)
    if not pif:
        return sep.join(out)

    def retLines(filename):
        try:
            file = open(filename)
            lines = file.readlines()
            file.close()
            return lines
        except Exception, msg:
            error("Problem opening file:%s"%msg)
            return []

    import socket
    serverip = socket.gethostbyname(socket.gethostname())
    nisre = re.compile(r'^ *INS *= *(\d+)',re.I)
    sqlurlre = re.compile(r'^ *sqlalchemy.url *= *postgresql://(\w+):(\w+)@([\d\.\:]+)/(\w+)', re.I)
    urbanmapre = re.compile(r'^ *urbanmap_url *= *http://([\d\.\:]+)',re.I)

    for pifline in retLines(pif):
        pifline = pifline.strip('\n')
        path, dbname, port = pifline.split(';')
        sitename = dbname[4:]
        nis = dbuser = dbpwd = pghost = pylonhost = ''
        inifilename = os.path.join(path, 'config', '%s.ini'%dbname)
        for line in retLines(inifilename):
            line = line.strip('\n')
            if nisre.match(line):
                nis = nisre.match(line).group(1)
            elif sqlurlre.match(line):
                matching = sqlurlre.match(line)
                dbuser = matching.group(1)
                dbpwd = matching.group(2)
                pghost = matching.group(3)
            elif urbanmapre.match(line):
                pylonhost = urbanmapre.match(line).group(1)
        if not geohost:
            geohost = "%s:8080"%serverip
        verbose("name=%s, nis=%s, pghost=%s, dbname=%s, dbuser=%s, dbpwd=%s, geohost=%s, pylonhost=%s"%(sitename, nis, pghost, dbname, dbuser, dbpwd, geohost, pylonhost))
        if apply:
            create_urban_site(self, name=sitename, nis=nis, pghost=pghost, dbname=dbname, dbuser=dbuser, dbpwd=dbpwd, geohost=geohost, pylonhost=pylonhost)

    return sep.join(out)

###############################################################################
