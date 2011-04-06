## Script (Python) "createUrbanDoc"
##title=Create a document
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urban_template_uid='',urban_folder_id='',urban_event_uid=''
##
#print urban_folder_id+' t:'+urban_template_uid+' e:'+urban_event_uid
#return printed
return context.portal_urban.createUrbanDoc(urban_folder_id,urban_template_uid,urban_event_uid)
