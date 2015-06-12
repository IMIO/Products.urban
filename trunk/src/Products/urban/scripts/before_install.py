from optparse import OptionParser

from OFS.Folder import manage_addFolder

def makeMountPoint(app, id):
    from Products.ZODBMountPoint.MountedObject import manage_addMounts
    if id not in app.objectIds('Folder'):
        manage_addMounts(app, ('/%s' % id,))
        import transaction
        transaction.commit()


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    makeMountPoint(app, args[0])
