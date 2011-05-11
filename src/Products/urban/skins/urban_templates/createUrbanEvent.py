## Script (Python) "createUrbanEvent"
##title=Create an UrbanEvent
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urban_event_type_uid='',urban_folder_uid=''
##
return context.portal_urban.createUrbanEvent(urban_folder_uid, urban_event_type_uid)
