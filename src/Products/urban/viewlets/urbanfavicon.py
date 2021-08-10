from plone.app.layout.links.viewlets import FaviconViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class UrbanFaviconViewlet(FaviconViewlet):
    render = ViewPageTemplateFile("templates/urbanfavicon.pt")
