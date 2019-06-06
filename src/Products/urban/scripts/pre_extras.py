

def configure_urban_site(portal, name='', pghost='localhost',
        dbname='', dbuser='', dbpwd=''):
    """
        creates an urban plone site
    """
    out = []
    sep = '\n'

    def verbose(line):
        out.append(line)

    def error(line):
        out.append("!! %s" % line)

    #configuring portal
    portal.portal_languages.setDefaultLanguage('fr')
    ps = portal.portal_setup
    ps.runAllImportStepsFromProfile('profile-Products.urban:default')
    ps.runAllImportStepsFromProfile('profile-Products.urbanskin:default')
    pu = portal.portal_urban
    if not pu.getSqlHost():
        pu.setSqlHost(pghost)
    if not pu.getCityName():
        pu.setCityName(name.capitalize())
    if not dbname:
        dbname = 'urb_%s' % name
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

    #running extra steps
    ps = portal.portal_setup
    ps.runAllImportStepsFromProfile('profile-Products.urban:extra')

    #running tests steps
    ps.runImportStepFromProfile('profile-Products.urban:tests',
            'urban-addTestObjects', run_dependencies=True)

    #running tests steps
    ps.runImportStepFromProfile('profile-Products.urban:tests',
            'urban-setDefaultValues', run_dependencies=True)

    #adding test licences
    ps.runImportStepFromProfile('profile-Products.urban:tests',
            'urban-addTestLicences', run_dependencies=True)

    return sep.join(out)
