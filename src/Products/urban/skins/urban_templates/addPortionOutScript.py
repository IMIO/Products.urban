## Script (Python) "createurbanevent"
##title=addPortionOutScript
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##
division = context.REQUEST.get('division', None)
section = context.REQUEST.get('section', None)
radical = context.REQUEST.get('radical', None)
bis = context.REQUEST.get('bis', None)
exposant = context.REQUEST.get('exposant', None)
puissance = context.REQUEST.get('puissance', None)
partie = context.REQUEST.get('partie', None)
old= context.REQUEST.get('old', None)
owner = context.REQUEST.get('owner', None)

if not section or not division:
    return context.REQUEST.RESPONSE.redirect(context.absolute_url())

if owner:
    context.portal_urban.createApplicant(licence=context, owner=owner)

return context.portal_urban.createPortionOut(path=context,division=division,section=section,radical=radical,bis=bis,exposant=exposant,puissance=puissance, partie=partie, old=old)
