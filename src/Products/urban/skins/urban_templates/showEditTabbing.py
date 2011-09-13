## Script (Python) "showEditTabbing"
##title=May the currently connected user access urban?
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##
member = context.portal_membership.getAuthenticatedMember()
return context.Type() in context.portal_urban.getUrbanTypes() and member.has_permission('Modify portal content', context)