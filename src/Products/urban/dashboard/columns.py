# encoding: utf-8

from Products.urban.browser.table.column import FoldermanagerColumn
from Products.urban.browser.table.interfaces import ITitleCell
from Products.urban.browser.table.interfaces import ITitleColumn

from collective.eeafaceted.z3ctable.columns import BaseColumn

from zope.component import queryMultiAdapter
from zope.interface import implements


class FolderManagersColumn(FoldermanagerColumn, BaseColumn):
    """ Turn the urban FoldermanagerColumn into a FacetedColumn."""


class FacetedTitleColumn(BaseColumn):
    """ TitleColumn for imio.dashboard listings."""
    implements(ITitleColumn)

    def renderTitleLink(self, item):
        portal_type = item.portal_type.lower()
        state = item.review_state
        css_class = 'contenttype-%s state-%s' % (portal_type, state)
        url = item.getURL()
        title = item.Title

        title_words = title.split()
        for split in range(len(title_words) / 15):
            title_words.insert(15 * (split + 1), '<br />')
        title = ' '.join(title_words)

        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title

    def renderCell(self, item):
        obj = item.getObject()
        adapter = queryMultiAdapter((self.context, self, item, obj), ITitleCell)
        if adapter:
            title = adapter.render()
        else:
            title = self.renderTitleLink(item)
        return title.decode('utf-8')


class TitleDisplay():
    """ Base class for Title cell adapter """
    implements(ITitleCell)

    def __init__(self, context, column, brain, obj):
        self.context = context
        self.column = column
        self.brain = brain
        self.obj = obj

    def render(self):
        """ to implement """


class LicenceTitleDisplay(TitleDisplay):
    """ Adapts a licence to a TitleCell """

    def render(self):
        title = self.column.renderTitleLink(self.brain)

        lastkeyevent = self.brain.last_key_event
        if lastkeyevent:
            title = '%s<br/><span class="discreet">%s</span>' % (title, lastkeyevent)

        return title


class AddressColumn(BaseColumn):
    """ display licence address in SearchResultTable """

    def renderCell(self, item):
        licence = item.getObject()
        addresses = licence.getWorkLocationSignaletic()

        address_render = []
        for address in addresses.split(' et '):
            render = '<span>%s</span>' % address
            address_render.append(render)

        address_render = '<br />'.join(address_render)
        address_render = address_render.decode('utf-8')

        return address_render


class ParcelReferencesColumn(BaseColumn):
    """ display licence parcel references in SearchResultTable """

    def renderCell(self, item):
        licence = item.getObject()
        parcels = licence.getParcels()

        parcel_render = []
        for parcel in parcels:
            render = '<span>%s</span>' % parcel.Title()
            parcel_render.append(render)

        parcel_render = '<br />'.join(parcel_render)
        parcel_render = parcel_render.decode('utf-8')

        return parcel_render
