from zope import schema
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.formlib import form

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from DateTime import DateTime

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('Urban')

class IUrbanPortlet(IPortletDataProvider):
    """ 
      A portlet that shows controls of Urban
    """

class Assignment(base.Assignment):
    implements(IUrbanPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return _(u"Urban")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('portlet_urban.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()

    @property
    def available(self):
        """
          Defines if the portlet is available in the context
        """
        return self.context.getLayout() == 'urban_view' and not self.context.id == 'urban'

    def render(self):
        return self._template()

    @memoize
    def getCurrentDateTime(self):
        """
          Returns the current DateTime
        """
        return DateTime()


class AddForm(base.AddForm):
    form_fields = form.Fields(IUrbanPortlet)
    label = _(u"Add Urban Portlet")
    description = _(u"This portlet shows controls of Urban.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IUrbanPortlet)
    label = _(u"Edit Urban Portlet")
    description = _(u"This portlet shows controls of Urban.")

