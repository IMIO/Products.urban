## Script (Python) "getDefaultStreetTitle"
##title=Get the default street title in the search by street
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=workLocationUid
##

if not workLocationUid:
    return ''

brains = context.uid_catalog(UID=workLocationUid)

if brains:
    return brains[0].Title

return ''
