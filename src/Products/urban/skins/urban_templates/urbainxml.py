## Script (Python) "urbainxml"
##title=urbain XML
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=datefrom='',dateto='',list_only=''
##
from DateTime import DateTime
if list_only:
    container.REQUEST.RESPONSE.setHeader('content-type', 'text/html')
else:
    container.REQUEST.RESPONSE.setHeader('content-type', 'text/plain')
return context.portal_urban.generateUrbainXML(datefrom, dateto, list_only)

