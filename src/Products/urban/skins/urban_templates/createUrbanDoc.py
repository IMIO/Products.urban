## Script (Python) "createUrbanDoc"
##title=Create a file
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urban_template_uid='', urban_event_uid=''
##
return context.portal_urban.createUrbanDoc(urban_template_uid, urban_event_uid)
