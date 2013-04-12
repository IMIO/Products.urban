## -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.ZCatalog.interfaces import ICatalogBrain
from plone.memoize import instance

from z3c.table.table import Table, SequenceTable
from z3c.table.value import ValuesMixin
from z3c.table.column import Column
from z3c.table.interfaces import IColumnHeader

from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.i18n import translate

from Products.urban.config import URBAN_TYPES
from Products.urban.browser.interfaces import \
    ILicenceListingTable, IContactTable, IParcelsTable, \
    IEventsTable, IDocumentsTable, IAnnexesTable, \
    ITitleColumn, IActionsColumn, \
    ITitleCell, IActionsCell


class OldListingMacro(BrowserView):
    """
    TO DELETE
    """


class UrbanTable(Table):
    """
    """

    batchProviderName = 'plonebatch'
    startBatchingAt = 0

    @instance.memoize
    def getObject(self, item):
        """
         Our columns expect objects (not brains).
         Sometimes we want to display result from a catalog query and only wake up the objects
         that are currently displayed in the batch table.
         This method allow us to instanciate table with brains but to still access the object when
         it needs to be do be displayed by a column.

         We could have look to override the z3c Table method that 'distributes' the items
         through the different columns and to try to convert brains into objects at this moment
         but the problem is ALL the column objects are created before being rendered (even if
         they are bacthed). The rendering is dynamical but not the 'columns creation'/'items distribution'
         which is done only once at table init (see z3c.table.table.Table setUpRows method)
        """
        if ICatalogBrain.providedBy(item):
            return item.getObject()
        return item


class LicenceListingTable(UrbanTable):
    """
    """
    implements(ILicenceListingTable)

    cssClasses = {'table': 'listing largetable'}
    sortOrder = 'descending'
    batchSize = 20


class AllLicencesListingTable(LicenceListingTable):
    """
     Licence listing for urban main page, we sort on creation date rather than title
    """
    sortOn = 'table-creationdateColumn-1'


class ContactTable(UrbanTable):
    """
    """
    implements(IContactTable)

    cssClasses = {'table': 'listing largetable'}


class ParcelsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IParcelsTable)

    cssClasses = {'table': 'listing largetable'}


class EventsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IEventsTable)

    sortOn = 'table-eventdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class DocumentsTable(UrbanTable, SequenceTable):
    """
    """
    implements(IDocumentsTable)

    sortOn = 'table-creationdateColumn-1'
    cssClasses = {'table': 'listing largetable'}


class AnnexesTable(DocumentsTable):
    """
     Documents and annexes use (almost) the same listing tables
    """
    implements(IAnnexesTable)


class EventDateColumn(Column):
    """
     Implement a column showing the urban event main date
    """

    header = 'label_colname_eventDate'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, item):
        event = self.table.getObject(item)
        date = event.getEventDate().strftime('%d/%m/%Y')
        return date

    def getSortKey(self, item):
        obj = self.table.getObject(item)
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


class TitleColumn(Column):
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

    def renderCell(self, item):
        obj = self.table.getObject(item)
        adapter = queryMultiAdapter((self.context, self.request, obj), ITitleCell)
        if adapter:
            title = adapter.render()
        else:
            portal_workflow = getToolByName(obj, 'portal_workflow')
            url = obj.absolute_url()
            title = obj.Title()
            state = portal_workflow.getInfoFor(obj, 'review_state', '')
            css_class = 'contenttype-%s state-%s' % (obj.portal_type.lower(), state)
            title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title.decode('utf-8')

    def getSortKey(self, item):
        if ICatalogBrain.providedBy(item):
            return item.Title
        else:
            item.Title()


class LicenceTitleColumnHeader():
    """ return the right label to display in Title Column header """
    implements(IColumnHeader)

    def __init__(self, context, request, table, column):
        self.request = request

    def update(self):
        pass

    def render(self):
        return translate('label_colname_Title', 'urban', context=self.request)


class ContactTitleColumnHeader():
    """ return the right label to display in Title Column header """
    implements(IColumnHeader)

    def __init__(self, context, request, table, column):
        self.request = request

    def update(self):
        pass


class ApplicantTitleColumnHeader(ContactTitleColumnHeader):
    """ return the right label to display in Title Column header """

    def render(self):
        label = 'label_colname_applicant_data'
        return translate(label, 'urban', context=self.request)


class ProprietaryTitleColumnHeader(ContactTitleColumnHeader):
    """ return the right label to display in Title Column header """

    def render(self):
        label = 'label_colname_proprietary_data'
        return translate(label, 'urban', context=self.request)


class TitleDisplay():
    """ Base class for Title cell adapter """
    implements(ITitleCell)

    def __init__(self, context, request, obj):
        self.context = context
        self.request = request
        self.obj = obj

    def renderTitleLink(self):
        obj = self.obj
        portal_workflow = getToolByName(obj, 'portal_workflow')
        url = obj.absolute_url()
        title = obj.Title()
        state = portal_workflow.getInfoFor(obj, 'review_state', '')
        css_class = 'contenttype-%s state-%s' % (obj.portal_type.lower(), state)
        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title

    def render(self):
        """ to implement """


class ContacTitleDisplay(TitleDisplay):
    """  Adapts a contact to a TitleCell """

    def render(self):
        contact = self.obj
        title = self.renderTitleLink()
        address = ''
        if contact.getStreet():
            address = '<br /><span>%s %s</span>\n\
                       <br /><span>%s %s</span>' % (contact.getStreet(), contact.getNumber(), contact.getZipcode(), contact.getCity())
            address = address
        title = '%s%s' % (title, address)
        return title


class LicenceTitleDisplay(TitleDisplay):
    """ Adapts a licence to a TitleCell """

    def render(self):
        licence = self.obj
        title = self.renderTitleLink()

        catalog = getToolByName(licence, 'portal_catalog')
        licence_brain = catalog(UID=licence.UID())[0]
        lastkeyevent = licence_brain.last_key_event
        if lastkeyevent:
            title = '%s<br/><span class="discreet">%s</span>' % (title, lastkeyevent)

        return title


class ParcelTitleDisplay(TitleDisplay):
    """ Adapts a parcel to a TitleCell """

    def render(self):
        parcel = self.obj
        css_class_span = parcel.getCSSClass()
        title = self.renderTitleLink()
        title = '<span class="%s">%s</span>' % (css_class_span, title)
        return title


class EventTitleDisplay(TitleDisplay):
    """ Adapts an event to a TitleCell """

    def render(self):
        event = self.obj
        title = self.renderTitleLink()

        user = event.restrictedTraverse('@@plone_portal_state').member()
        suffix = user.has_permission('Modify portal content', event) and '/external_edit' or ''
        documents = []
        for doc in event.getDocuments():
            doc_title = doc.Title()
            doc_link = '%s%s' % (doc.absolute_url(), suffix)
            doc_link = '<br /><a href="%s" class="discreet" style="margin-left:20px">%s</a>' % (doc_link, doc_title)
            documents.append(doc_link)
        documents = ''.join(documents)
        return '%s%s' % (title, documents)


class DocumentTitleDisplay (TitleDisplay):
    """ Adapts an event to a TitleCell """

    def render(self):
        doc = self.obj
        title = doc.Title()
        event = doc.aq_parent
        user = event.restrictedTraverse('@@plone_portal_state').member()
        suffix = user.has_permission('Modify portal content', event) and '/external_edit' or ''
        url = '%s%s' % (doc.absolute_url(), suffix)
        css_class = 'contenttype-%s' % doc.portal_type.lower()
        title = '<a href="%s" class="%s">%s</a>' % (url, css_class, title)
        return title


class CreationDateColumn(Column):
    """
    """

    header = u'label_colname_created'
    weight = 10

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, item):
        obj = self.table.getObject(item)
        return obj.creation_date.strftime('%d/%m/%Y')

    def getSortKey(self, item):
        obj = self.table.getObject(item)
        return obj.creation_date


class CreatorColumn(Column):
    """
    """

    header = u'label_colname_Creator'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, item):
        obj = self.table.getObject(item)
        return ''.join(sorted(obj.listCreators()))

    def getSortKey(self, item):
        obj = self.table.getObject(item)
        return sorted(obj.listCreators())


class FoldermanagerColumn(Column):
    """
    """

    header = u'label_colname_foldermanager'
    weight = 20

    # we got to override the renderHeadCell method, because we got to give the right domain name for translation
    def renderHeadCell(self):
        """Header cell content."""
        return translate(self.header, 'urban', context=self.request)

    def renderCell(self, item):
        obj = self.table.getObject(item)
        foldermanagers = obj.getFoldermanagers()
        return ', '.join([fm.getSignaletic(short=True) for fm in foldermanagers])


class ActionsColumn(Column):
    """
    """
    implements(IActionsColumn)

    weight = 100
    cssClasses = {'th': 'actionsheader'}

    def renderCell(self, item):
        obj = self.table.getObject(item)
        adapter = queryMultiAdapter((self.context, self.request, obj), IActionsCell)
        if adapter:
            actions = adapter.render()
        else:
            portal_url = getToolByName(obj, 'portal_url')
            portal_workflow = getToolByName(obj, 'portal_workflow')
            actions = ['<div  align="right">']

            # first render the workflow changes actions
            transitions = portal_workflow.getTransitionsFor(obj)
            for transition in transitions:
                input_action = '<input type="hidden" name="workflow_action" value="%s" />' % transition['id']
                camefrom = '%s?%s' % (self.request.get('ACTUAL_URL'), self.request.get('QUERY_STRING'))
                input_camefrom = '<input type="hidden" name="came_from" value="%s" />' % camefrom
                image_name = '%s.png' % transition['title']
                if hasattr(obj, image_name):
                    input_icon = '<input type="image" src="%s/%s" title="%s"  i18n:attributes="title" />' % (portal_url(), image_name, transition['id'])
                else:
                    input_icon = '<input type="submit" value="%s"  i18n:attributes="title" />' % transition['id']
                form_action = '%s/content_status_modify' % obj.absolute_url()

                form = '<form style="display: inline" action="%s" i18n_domain="plone">%s%s%s</form>' % (form_action, input_action, input_camefrom, input_icon)
                actions.append(form)

            # then add the edit actions
            portal_membership = getToolByName(obj, 'portal_membership')
            portal_properties = getToolByName(obj, 'portal_properties')
            member = portal_membership.getAuthenticatedMember()

            if member.has_permission('Modify portal content', obj):
                image = '<img src="%s/edit.gif" title="label_edit" i18n:attributes="title" />' % portal_url()
                external_edition = obj.portal_type in ['File', 'UrbanDoc'] and portal_properties.site_properties.ext_editor
                suffix = external_edition and 'external_edit' or 'edit'
                modify_action = '<a class="noPadding" href="%s/%s">%s</a>' % (obj.absolute_url(), suffix, image)
                actions.append(modify_action)

            if member.has_permission('Delete objects', obj):
                image = '<img src="%s/delete_icon.gif" title="label_edit" i18n:attributes="title" title="label_remove"\
                         style="cursor: pointer" onClick="javascript:confirmDeleteObject(this)"/>' % portal_url()
                modify_action = '<a class="urbanDelete noPadding" href="%s/delete_confirmation">%s</a>' % (obj.absolute_url(), image)
                actions.append(modify_action)

            actions.append('</div>')
            actions = ''.join(actions)
        return actions


class ActionsColumnHeader():
    """ return the right label to display in Actions Column header """
    implements(IColumnHeader)

    def __init__(self, context, request, table, column):
        self.request = request

    def update(self):
        pass

    def render(self):
        return translate('actions', 'urban', context=self.request)


class ValuesForContactListing (ValuesMixin):
    """  return contact values from the context """

    @property
    def values(self):
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        query_string = {
            'meta_type': 'Contact',
            'path': {
                'query': '/'.join(context.getPhysicalPath()),
                'depth': 1,
            },
        }
        contacts = catalog(query_string)
        return  contacts


class ValuesForLicenceListing (ValuesMixin):
    """ return licence values from the context  """

    @property
    def values(self):
        licence_brains = self.queryLicences()
        return licence_brains

    def queryLicences(self, **kwargs):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        catalog = getToolByName(context, 'portal_catalog')

        queryString = {
            'portal_type': URBAN_TYPES,
            'path': '/'.join(context.getPhysicalPath()),
        }

        foldermanager = request.get('foldermanager', '')
        if foldermanager:
            queryString['folder_manager'] = foldermanager

        state = request.get('review_state', '')
        if state:
            queryString['review_state'] = state

        queryString.update(kwargs)
        licence_brains = catalog(queryString)
        return licence_brains
