from Products.Five import BrowserView

from plone import api

from zope.component import createObject


class UrbanObjectBaseFactory(BrowserView):
    """
     Use a named traversable adapter (in this case, a browserview w/o any html template)
     to be able to create an UrbanObject through a simple http form request.

     eg: http://mysite.be/mycontext/createurbanobject?id=42&Title=trololo
     should create an 'UrbanObject' into mycontext
    """

    def __call__(self):
        urban_object = self.create()
        http_redirection = self.redirect(urban_object)
        return http_redirection

    def create(self):
        """" to implements """

    def redirect(self, urban_object):
        return self.request.response.redirect(self.context.absolute_url())


class CreateUrbanEvent(UrbanObjectBaseFactory):

    def create(self):
        uid_catalog = api.portal.get_tool('uid_catalog')
        eventtype_uid = self.request.form['urban_event_type_uid']
        eventtype_brain = uid_catalog(UID=eventtype_uid)[0]
        eventtype = eventtype_brain.getObject()

        urban_event = createObject('UrbanEvent', self.context, eventtype)

        return urban_event

    def redirect(self, urban_event):
        return self.request.response.redirect(urban_event.absolute_url() + '/edit')
