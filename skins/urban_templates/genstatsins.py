## Script (Python) "urbainxml"
##title=urbain XML
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=datefrom='',dateto='',listeseule=''
##
from DateTime import DateTime

return context.portal_urban.generateStatsINS(datefrom,dateto)

