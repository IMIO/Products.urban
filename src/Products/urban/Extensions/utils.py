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
            site = addPloneSite(mp, name, title='Application Urbanisme en test', extension_ids=('Products.urban:default','Products.urbanskin:default'), create_userfolder=False, validate_email=True, default_language='fr')
            verbose("Created plone site '%s'"%name)
        except Exception, msg:
            error("Plone site not created: %s"%msg)
            return sep.join(out)

    #configuring site
    site = getattr(mp, name)
    pu = site.portal_urban
    pu.setCityName(name)
    pu.setSqlHost(pghost)
    if nis:
        pu.setNISNum(nis)
    if not dbname:
        dbname = 'urb_%s'%name
    pu.setSqlName(dbname)
    if not dbuser:
        dbuser = dbname
    pu.setSqlUser(dbuser)
    if not dbpwd:
        dbpwd = dbname
    pu.setSqlPassword(dbpwd)
    if geohost:
        pu.setWebServerHost(geohost)
    if pylonhost:
        pu.setPylonsHost(pylonhost)

    #running extra step
    ps = site.portal_setup
    ps.runAllImportStepsFromProfile('profile-Products.urban:extra')

    #running tests step
    ps.runAllImportStepsFromProfile('profile-Products.urban:extra')

    return sep.join(out)

###############################################################################

def create_site_from_pylon(self, pif='', geohost=''):
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

    if not pif:
        #out.append("available properties:%s"%portal.portal_memberdata.propertyItems())
        out.append("call the script followed by those parameters:")
        out.append("-> pif=string : pylons instances file")
        out.append("-> geohost=ip:port : geoserver host")
        out.append("by example ...?dirname=/srv/urbanmap/config %s"%sep)
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
        inifilename = os.path.join(path, 'config', dbname)
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
        create_urban_site(self, name=sitename, nis=nis, pghost=pghost, dbname=dbname, dbuser=dbuser, dbpwd=dbpwd, geohost=geohost, pylonhost=pylonhost)

    return sep.join(out)

###############################################################################
