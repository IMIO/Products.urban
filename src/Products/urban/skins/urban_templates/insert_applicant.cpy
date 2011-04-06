## Script (Python) "content_edit"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=id=''
##

context.content_edit_impl(state, id)
return context.REQUEST.RESPONSE.redirect(context.getParentNode().absolute_url())
#return context.go_back()