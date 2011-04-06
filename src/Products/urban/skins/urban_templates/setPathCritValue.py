## Script (Python) "setPathCritValue"
##title=setPathCritValue
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=path_crit,uid
##
if uid:
    path_crit.setValue(uid)
