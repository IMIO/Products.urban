## Script (Python) "checkPortionOutSearch"
##title=Create a document
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##

#check if the portionOutSearch script is OK
#check that the DB is connected
request = context.REQUEST

if not context.portal_urban.getDBConnection():
    from Products.CMFPlone import PloneMessageFactory as _
    ptool = context.plone_utils
    ptool.addPortalMessage(_(u"db_not_connected_error", default="An error occured with the database.  Please contact the system administrator.  The database does not seem to be connected"), 'error')
    return request.RESPONSE.redirect(request.HTTP_REFERER)
return request.RESPONSE.redirect('%s/portionsOutSearch' % request.URL1)
