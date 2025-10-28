from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.links.viewlets import FaviconViewlet


class UrbanFaviconViewlet(FaviconViewlet):
    render = ViewPageTemplateFile("templates/urbanfavicon.pt")
