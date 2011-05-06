# ------------------------------------------------------------------------------
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

# ------------------------------------------------------------------------------
class portletFirefox(ViewletBase):
    '''This viewlet displays the firefox-text if browser isn't firefox.'''    
    index = ViewPageTemplateFile("portlet_firefox.pt")
