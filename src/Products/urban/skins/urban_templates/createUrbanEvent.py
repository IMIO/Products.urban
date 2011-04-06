## Script (Python) "createurbanevent"
##title=Create an urbanEvent
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urban_event_type_uid='',urban_folder_id=''
##
print urban_folder_id
return context.portal_urban.createUrbanEvent(urban_folder_id,urban_event_type_uid)
