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


class CreateUrbanDoc(UrbanObjectBaseFactory):

    def create(self):
        template_uid = self.request.form['template_uid']
        urban_doc = self.createUrbanDoc(template_uid)
        return urban_doc

    def createUrbanDoc(self, template_uid):
        """
          Create an element in an UrbanEvent
        """
        uid_catalog = api.portal.get_tool('uid_catalog')

        container = self.context
        odt_template_brain = uid_catalog(UID=template_uid)[0]
        odt_template = odt_template_brain.getObject()

        urban_doc = createObject('GeneratedUrbanDoc', container, odt_template)

        return urban_doc

    def redirect(self, urban_doc):
        portal_urban = api.portal.get_tool('portal_urban')
        file_type = portal_urban.getEditionOutputFormat()
        # Tell the browser that the resulting page contains ODT
        response = self.request.response
        response.setHeader('Content-type', 'application/%s' % file_type)
        response.setHeader('Content-disposition', 'inline;filename="%s.%s"' % ('portal_urban', file_type))

        self.request.set('doc_uid', urban_doc.UID())

        return response.redirect(self.context.absolute_url() + '?doc_uid=' + urban_doc.UID())
