## Script (Python) "createUrbanEvent"
##title=Create an UrbanEvent
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=urban_event_type_uid=''
##
return  self.REQUEST.RESPONSE.redirect(context.createUrbanEvent(urban_event_type_uid).absolute_url() + '/edit')
