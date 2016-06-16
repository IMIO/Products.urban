# encoding: utf-8

from plone import api

from Products.urban.browser.table.column import FoldermanagerColumn
from Products.urban.browser.table.interfaces import ITitleCell
from Products.urban.browser.table.interfaces import ITitleColumn
from imio.dashboard.columns import ActionsColumn

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

    # column not sortable
    sort_index = -1

    def renderCell(self, item):
        task = item.getObject()
        addresses = task.getWorkLocationSignaletic()

        address_render = []
        for address in addresses.split(' et '):
            render = '<span>%s</span>' % address
            address_render.append(render)

        address_render = '<br />'.join(address_render)
        address_render = address_render.decode('utf-8')

        return address_render


class ParcelReferencesColumn(BaseColumn):
    """ display licence parcel references in SearchResultTable """

    # column not sortable
    sort_index = -1

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


class ScheduleColumn(BaseColumn):
    """
    Base class for custom schedule columns.
    """

    # column not sortable
    sort_index = -1

    def query_licence(self, item):
        catalog = api.portal.get_tool('portal_catalog')
        task = item.getObject()
        licence = task.get_container()
        licence_brain = catalog(UID=licence.UID())[0]
        return licence_brain


class TaskLicenceTitleDisplay(TitleDisplay, ScheduleColumn):
    """ Adapts a task to a LicenceTitleCell """

    def render(self):
        licence_brain = self.query_licence(self.brain)
        title = self.column.renderTitleLink(licence_brain)
        return title


class AssignedUserColumn(BaseColumn):
    """ display licence address in SearchResultTable """

    def renderCell(self, item):
        user = item.assigned_user
        group = item.assigned_group

        assigned = user
        if group:
            assigned = '{user} ({group})'.format(
                user=user,
                group=group
            )

        return assigned


class TaskActionsColumn(ActionsColumn):
    """Display actions for the task"""
    params = {
        'showHistory': False,
        'showActions': False,
        'showOwnDelete': False,
        'showEdit': False,
        'showTransitions': False,
        'showChangeOwner': True,
    }
