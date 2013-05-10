## -*- coding: utf-8 -*-

from DateTime import DateTime

from z3c.table.column import Column, GetAttrColumn
from z3c.table.interfaces import IColumnHeader

from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from Products.urban.browser.interfaces import ITitleColumn, IActionsColumn, \
    ILocalityColumn, IStreetColumn, IUrbanColumn, IAddressColumn, IParcelReferencesColumn, \
    ITitleCell, IActionsCell


class UrbanColumn(Column):
    """ base class for a column that expect a ItemForUrbanTable item  """
    implements(IUrbanColumn)

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)


class EventDateColumn(UrbanColumn):
    """
     Implement a column showing the urban event main date
    """

    header = 'label_colname_eventDate'
    weight = 20

    def renderCell(self, urbanlist_item):
        event = urbanlist_item.getObject()
        date = event.getEventDate().strftime('%d/%m/%Y')
        return date

    def getSortKey(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        return obj.getEventDate()


class RelatedLicencesColumn(Column):
    """
     Implement a column that provides a link to all the licences related to any parcel of the item
    """

    header = 'parcelLinkedLicences'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, parcel):
        if not parcel.hasRelatedLicences():
            return '-'
        else:
            url = parcel.aq_parent.absolute_url()
            id = parcel.getId()
            img = '<img  src="linkedfolders.png" class="urban-linkedfolders-icon"/>'
            link = '<a class="link-overlay" href="%s/@@parcelrecordsview?id=%s">%s</a>' % (url, id, img)
            cell = '<span id="urban-parcel-related-licences">%s</span' % link
            return cell


class TitleColumn(UrbanColumn):
    """
    """
    implements(ITitleColumn)

    header = 'label_colname_Title'
    weight = 1

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        header = queryMultiAdapter((self.context, self.request, self.table, self), IColumnHeader)
        if header:
            header.update()
            return header.render()
        return translate(self.header, 'urban', context=self.request)

    def renderTitleLink(self, urbanlist_item):
        portal_type = urbanlist_item.getPortalType().lower()
        state = urbanlist_item.getState()
        css_class = 'contenttype-%s state-%s' % (portal_type, state)
        url = urbanlist_item.getURL()
        title = urbanlist_item.Title()
        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title

    def renderCell(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        adapter = queryMultiAdapter((self.context, self, urbanlist_item, obj), ITitleCell)
        if adapter:
            title = adapter.render()
        else:
            title = self.renderTitleLink(urbanlist_item)
        return title.decode('utf-8')

    def getSortKey(self, urbanlist_item):
        return urbanlist_item.Title()


class TitleColumnHeader():
    """ return the right label to display in Title Column header """
    implements(IColumnHeader)

    def __init__(self, context, request, table, column):
        self.request = request
        self.label = ''

    def update(self):
        """ to implement"""

    def render(self):
        return translate(self.label, 'urban', context=self.request)


class LicenceTitleColumnHeader(TitleColumnHeader):
    """ return the right label to display in Title Column header """

    def update(self):
        self.label = 'label_colname_Title'


class ApplicantTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_applicant_data'


class ProprietaryTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_proprietary_data'


class NotaryTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_notary_data'


class ArchitectTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_architect_data'


class GeometricianTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_geometrician_data'


class ClaimantTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_claimant_data'


class RecipientCadastreTitleColumnHeader(TitleColumnHeader):

    def update(self):
        self.label = 'label_colname_name'


class TitleDisplay():
    """ Base class for Title cell adapter """
    implements(ITitleCell)

    def __init__(self, context, column, urbanlist_item, obj):
        self.context = context
        self.column = column
        self.urbanlist_item = urbanlist_item
        self.obj = obj

    def render(self):
        """ to implement """


class ContacTitleDisplay(TitleDisplay):
    """  Adapts a contact to a TitleCell """

    def render(self):
        contact = self.obj
        title = self.column.renderTitleLink(self.urbanlist_item)

        address = ''
        street = contact.getStreet()
        number = contact.getNumber()
        if street or number:
            address = '<br /><span>%s %s</span>' % (street, number)

        zipcode = contact.getZipcode()
        city = contact.getCity()
        if zipcode or city:
            address = '%s<br /><span>%s %s</span>' % (address, zipcode, city)

        title = '%s%s' % (title, address)
        return title


class LicenceTitleDisplay(TitleDisplay):
    """ Adapts a licence to a TitleCell """

    def render(self):
        licence_brain = self.urbanlist_item.getRawValue()
        title = self.column.renderTitleLink(self.urbanlist_item)

        lastkeyevent = licence_brain.last_key_event
        if lastkeyevent:
            title = '%s<br/><span class="discreet">%s</span>' % (title, lastkeyevent)

        return title


class ParcelTitleDisplay(TitleDisplay):
    """ Adapts a parcel to a TitleCell """

    def render(self):
        parcel = self.obj
        css_class_span = parcel.getCSSClass()
        title = self.column.renderTitleLink(self.urbanlist_item)
        title = '<span class="%s">%s</span>' % (css_class_span, title)
        return title


class EventTitleDisplay(TitleDisplay):
    """ Adapts an event to a TitleCell """

    def render(self):
        event = self.obj
        title = self.column.renderTitleLink(self.urbanlist_item)

        suffix = self.urbanlist_item.canBeEdited() and '/external_edit' or ''
        documents = []
        for doc in event.getDocuments():
            doc_title = doc.Title()
            doc_link = '%s%s' % (doc.absolute_url(), suffix)
            doc_link = '<br /><a href="%s" class="discreet" style="margin-left:20px">%s</a>' % (doc_link, doc_title)
            documents.append(doc_link)
        documents = ''.join(documents)
        return '%s%s' % (title, documents)


class DocumentTitleDisplay(TitleDisplay):
    """ Adapts an event to a TitleCell """

    def render(self):
        doc = self.obj
        title = doc.Title()
        suffix = self.urbanlist_item.canBeEdited() and '/external_edit' or ''
        url = '%s%s' % (doc.absolute_url(), suffix)
        css_class = 'contenttype-%s' % doc.portal_type.lower()
        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title


class RecipientCadastreTitleDisplay(TitleDisplay):
    """ Adapts an event to a TitleCell """

    def render(self):
        recipient = self.obj
        urbanlist_item = self.urbanlist_item

        portal_type = recipient.portal_type.lower()
        state = urbanlist_item.getState()
        css_class = 'contenttype-%s state-%s' % (portal_type, state)
        title = recipient.getName()
        title = '<span class="%s">%s</span>' % (css_class, title)

        secondary_title = recipient.Title()
        secondary_title = '<span class="discreet">%s</span>' % secondary_title

        title = '%s<br />%s' % (title, secondary_title)

        return title


class CreationDateColumn(Column):

    header = u'label_colname_created'
    weight = 10

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)


class ObjectCreationDateColumn(CreationDateColumn):
    """ """

    def renderCell(self, obj):
        return obj.creation_date.strftime('%d/%m/%Y')

    def getSortKey(self, obj):
        return obj.creation_date


class BrainCreationDateColumn(CreationDateColumn):
    """ """

    def renderCell(self, brain):
        date = DateTime(brain.CreationDate)
        return date.strftime('%d/%m/%Y')

    def getSortKey(self, brain):
        date = DateTime(brain.CreationDate)
        return date


class CreatorColumn(Column):
    """
    """

    header = u'label_colname_Creator'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, obj):
        return ''.join(sorted(obj.listCreators()))

    def getSortKey(self, urbanlist_item):
        return urbanlist_item.getObject.listCreators()


class FoldermanagerColumn(Column):
    """
    """

    header = u'label_colname_foldermanager'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, urbanlist_item):
        obj = urbanlist_item.getObject()
        foldermanagers = obj.getFoldermanagers()
        foldermanager_names = ', '.join([fm.getSignaletic(short=True) for fm in foldermanagers])
        foldermanager_names = foldermanager_names.decode('utf-8')
        return foldermanager_names


class ActionsColumn(UrbanColumn):
    """
    """
    implements(IActionsColumn)

    weight = 100
    cssClasses = {'th': 'actionsheader'}
    header = 'actions'

    def renderCell(self, urbanlist_item):
        item = urbanlist_item.getObject()
        adapter = queryMultiAdapter((self.context, self.request, urbanlist_item, item), IActionsCell)
        if adapter:
            actions = adapter.render()
        else:
            base_url = urbanlist_item.getTool('portal_url')()
            object_url = urbanlist_item.getURL()

            action_links = ['<div  align="right">']
            # first render the workflow changes actions
            transitions = urbanlist_item.getWorkflowTransitions()
            for transition in transitions:
                image_name = '%s.png' % transition['title']
                translation = translate(transition['id'], 'plone', context=self.request)

                if hasattr(item, image_name):
                    input_icon = '<input type="image" src="%s/%s" title="%s" />' % (base_url, image_name, translation)
                else:
                    input_icon = '<input type="submit" value="%s" />' % translation

                form_action = '%s/content_status_modify' % object_url
                input_action = '<input type="hidden" name="workflow_action" value="%s" />' % transition['id']
                camefrom = '%s?%s' % (self.request.get('ACTUAL_URL'), self.request.get('QUERY_STRING'))
                input_camefrom = '<input type="hidden" name="came_from" value="%s" />' % camefrom

                form = '<form style="display: inline" action="%s" i18n_domain="plone">%s%s%s</form>' % (form_action, input_action, input_camefrom, input_icon)

                action_links.append(form)

            # then add the edit actions
            actions = urbanlist_item.getActions()

            if 'edit' in actions:
                action = actions['edit']
                image = '<img src="%s/edit.gif" title="label_edit" i18n:attributes="title" />' % base_url
                edit_action = '<a class="noPadding" href="%s/%s">%s</a>' % (object_url, action, image)
                action_links.append(edit_action)

            if 'delete' in actions:
                action = actions['delete']
                image = '<img src="%s/delete_icon.gif" title="label_edit" i18n:attributes="title" title="label_remove"\
                         style="cursor: pointer" onClick="javascript:confirmDeleteObject(this)"/>' % base_url
                delete_action = '<a class="urbanDelete noPadding" href="%s/%s">%s</a>' % (object_url, action, image)
                action_links.append(delete_action)

            action_links.append('</div>')
            action_links = ''.join(action_links)
        return action_links


class LocalityColumn(GetAttrColumn):
    """  """
    implements(ILocalityColumn)

    attrName = 'adr1'
    header = 'label_colname_adr1'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)


class StreetColumn(Column):
    """  """
    implements(IStreetColumn)

    attrName = 'street'
    header = 'label_colname_street'
    weight = 30

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, recipient):

        street = '<span>%s</span>' % recipient.getStreet()
        secondary_street = '<span class="discreet">%s</span>' % recipient.getAdr2()
        street = '%s<br />%s' % (street, secondary_street)

        return street.decode('utf-8')


class AddressColumn(UrbanColumn):
    """ display licence address in SearchResultTable """
    implements(IAddressColumn)

    header = 'label_colname_address'
    weight = 2

    def renderCell(self, urbanlist_item):
        licence = urbanlist_item.getObject()
        addresses = licence.getWorkLocationSignaletic()

        address_render = []
        for address in addresses.split(' et '):
            render = '<span>%s</span>' % address
            address_render.append(render)

        address_render = '<br />'.join(address_render)

        return address_render


class ParcelReferencesColumn(UrbanColumn):
    """ display licence parcel references in SearchResultTable """
    implements(IParcelReferencesColumn)

    header = 'label_colname_parcelrefs'
    weight = 6

    def renderCell(self, urbanlist_item):
        licence = urbanlist_item.getObject()
        parcels = licence.getParcels()

        parcel_render = []
        for parcel in parcels:
            render = '<span>%s</span>' % parcel.Title()
            parcel_render.append(render)

        parcel_render = '<br />'.join(parcel_render)

        return parcel_render
