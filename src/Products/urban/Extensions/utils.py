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
