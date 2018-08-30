# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.urban import utils
from Products.Five import BrowserView
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.browser.mapview import MapView
from Products.urban.browser.licence.licenceview import LicenceView
from Products.urban.browser.table.urbantable import DocumentsTable
from Products.urban.browser.table.urbantable import AttachmentsTable
from Products.urban.browser.table.urbantable import ClaimantsTable
from Products.urban.browser.table.urbantable import RecipientsCadastreTable
from Products.urban import services

from plone import api

import csv


class UrbanEventView(BrowserView):
    """
      This manage the view of UrbanEvent
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def getActivatedFields(self):
        """
        Return all the activated fields of this UrbanEvent
        """
        context = aq_inner(self.context)
        linkedUrbanEventType = context.getUrbaneventtypes()
        fields = [i for i in context.schema.fields() if i.schemata == 'default' and not hasattr(i, 'optional') and i.widget.visible and i.widget.visible['view'] == 'visible']
        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            field = context.getField(activatedField)
            fields.append(field)
        return fields

    def getFieldsToShow(self):
        """
        Return fields to display about the UrbanEvent
        """
        fields = [f for f in self.getActivatedFields() if not hasattr(f, 'pm_text_field')]
        return fields

    def getDateCustomLabel(self):
        """
        """
        return self.context.getUrbaneventtypes().getEventDateLabel()

    def getPmFields(self):
        """
        Return activated pm fields to build the pm summary
        """
        fields = [f for f in self.getActivatedFields() if hasattr(f, 'pm_text_field')]
        return fields

    def show_pm_summary(self):
        """
        """
        return bool(self.getPmFields())

    def empty_pm_summary(self):
        """
        """
        fields = self.getPmFields()

        for field in fields:
            text = field.get(self.context)
            if text:
                return False

        return True

    def isTextField(self, field):
        return field.type == 'text'

    def mayAddUrbanEvent(self):
        """
          Return True if the current user may add an UrbanEvent
        """
        context = aq_inner(self.context)
        member = api.portal.get_tool('portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def mayAddAttachment(self):
        """
          Return True if the current user may add an attachment (File)
        """
        context = aq_inner(self.context)
        member = api.portal.get_tool('portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def renderGeneratedDocumentsListing(self):
        event = aq_inner(self.context)
        documents = event.getDocuments()
        if not documents:
            return ''

        documentlisting = DocumentsTable(documents, self.request)
        documentlisting.update()
        return documentlisting.render()

    def renderAttachmentsListing(self):
        event = aq_inner(self.context)
        attachments = event.getAttachments()
        if not attachments:
            return ''

        table = AttachmentsTable(attachments, self.request)
        table.update()
        return table.render()

    def getListOfTemplatesToGenerate(self):
        """
        Return a list of dicts. Each dict contains all the infos needed in the html <href> tag to create the
        corresponding link for document generation
        """
        context = aq_inner(self.context)
        template_list = []
        for template in context.getTemplates():
            if template.can_be_generated(context):
                template_list.append(
                    {
                        'name': template.id.split('.')[0],
                        'title': template.Title(),
                        'class': '',
                        'href': self._generateDocumentHref(context, template),
                    }
                )

        for generated_doc in context.objectValues():
            for template in template_list:
                if generated_doc.id.startswith(template['name']):
                    template['class'] = 'urban-document-already-created'
        return template_list

    def _generateDocumentHref(self, context, template):
        """
        """
        link = "{base_url}/urban-document-generation?template_uid={uid}".format(
            base_url=context.absolute_url(),
            uid=template.UID()
        )
        return link

    def getUrbaneventtypes(self):
        """
          Return the accessor urbanEventTypes()
        """
        context = aq_inner(self.context)
        return context.getUrbaneventtypes()

    def get_state(self):
        return api.content.get_state(self.context)


class UrbanEventInquiryBaseView(UrbanEventView, MapView, LicenceView):
    """
    This manage the base view of UrbanEventInquiry
    """

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def getParcels(self):
        context = aq_inner(self.context)
        return context.getParcels()

    def renderClaimantsListing(self):
        if not self.context.getClaimants():
            return ''
        contactlisting = ClaimantsTable(self.context, self.request)
        contactlisting.update()
        return contactlisting.render()

    def getLinkedInquiry(self):
        context = aq_inner(self.context)
        return context.getLinkedInquiry()

    def getInquiryFields(self):
        """
          This will return fields to display about the Inquiry
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        fields = []
        if not linkedInquiry:
            #this should not happen...
            return None
        displayed_fields = self.getUsedAttributes()
        inquiry_fields = utils.getSchemataFields(linkedInquiry, displayed_fields, 'urban_inquiry')
        for inquiry_field in inquiry_fields:
            if inquiry_field.__name__ == "claimsText":
                #as this text can be very long, we do not want to show it with the other
                #fields, we will display it in the "Claimants" part of the template
                continue
            fields.append(inquiry_field)

        return fields

    def getInquiryReclamationNumbers(self):

        inquiryReclamationNumbers = []
        context = aq_inner(self.context)
        totalOral = 0
        totalWrite = 0
        if context.getClaimants():
            for claimant in context.getClaimants():
                if claimant.getClaimType() == 'oralClaim':
                    totalOral += 1
                elif claimant.getClaimType() == 'writedClaim':
                    totalWrite += 1

        inquiryReclamationNumbers.append(totalOral)
        inquiryReclamationNumbers.append(totalWrite)
        return inquiryReclamationNumbers

    def getLinkToTheInquiries(self):
        """
          This will return a link to the inquiries on the linked licence
        """
        context = aq_inner(self.context)
        return context.aq_inner.aq_parent.absolute_url() + '/#fieldsetlegend-urban_inquiry'

    def getLinkedInquiryTitle(self):
        """
          This will return the title of the linked Inquiry
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        if linkedInquiry:
            if not linkedInquiry.portal_type == 'Inquiry':
                #we do not use Title as this inquiry is the licence
                return linkedInquiry.generateInquiryTitle()
            else:
                return linkedInquiry.Title()

    def import_claimants_from_csv(self):
        portal_urban = api.portal.get_tool('portal_urban')
        site = api.portal.get()
        fieldnames = [
            'personTitle',
            'name1',
            'name2',
            'society',
            'street',
            'number',
            'zipcode',
            'city',
            'country',
            'email',
            'phone',
            'gsm',
            'nationalRegister',
            'claimType',
            'hasPetition',
            'outOfTime',
            'claimDate',
            'claimsText',
        ]

        titles_mapping = {'': ''}
        titles_folder = portal_urban.persons_titles
        for title_obj in titles_folder.objectValues():
            titles_mapping[title_obj.Title()] = title_obj.id

        country_mapping = {'': ''}
        country_folder = portal_urban.country
        for country_obj in country_folder.objectValues():
            country_mapping[country_obj.Title()] = country_obj.id

        claimants_file = open('claimants.csv', 'r')
        reader = csv.DictReader(claimants_file, fieldnames, delimiter=';', quotechar='"')
        claimant_args = [row for row in reader if row['name1']][1:]
        for claimant_arg in claimant_args:
            claimant_arg.pop(None, None)
            # default values
            if not claimant_arg['claimType']:
                claimant_arg['claimType'] = 'writedClaim'
            if not claimant_arg['hasPetition']:
                claimant_arg['hasPetition'] = False
            if not claimant_arg['outOfTime']:
                claimant_arg['outOfTime'] = False
            # mappings
            claimant_arg['personTitle'] = titles_mapping[claimant_arg['personTitle']]
            claimant_arg['country'] = country_mapping[claimant_arg['country']]
            claimant_arg['id'] = site.plone_utils.normalizeString(claimant_arg['name1'] + claimant_arg['name2'])
            count = 0
            while claimant_arg['id'] in self.context.objectIds():
                count += 1
            if count:
                claimant_arg['id'] = claimant_arg['id'] + '-' + str(count)
            # create claimant
            self.context.invokeFactory('Claimant', **claimant_arg)
            print 'imported claimant {id}, {name} {surname}'.format(
                id=claimant_arg['id'],
                name=claimant_arg['name1'],
                surname=claimant_arg['name2'],
            )


class UrbanEventAnnouncementView(UrbanEventInquiryBaseView):
    """
    This manage the view of UrbanEventAnnouncement
    """

    def __init__(self, context, request):
        super(UrbanEventAnnouncementView, self).__init__(context, request)
        plone_utils = api.portal.get_tool('plone_utils')
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils.addPortalMessage(_('This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !'), type="error")
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def getInquiryFields(self):
        """
        This will return fields to display about the Inquiry
        """
        context = aq_inner(self.context)
        linked_inquiry = context.getLinkedInquiry()
        fields_to_display = linked_inquiry.get_inquiry_fields_to_display()
        return fields_to_display


class UrbanEventInquiryView(UrbanEventInquiryBaseView):
    """
    This manage the view of UrbanEventInquiry
    """

    def __init__(self, context, request):
        super(UrbanEventInquiryView, self).__init__(context, request)
        plone_utils = api.portal.get_tool('plone_utils')
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils.addPortalMessage(_('This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !'), type="error")
        if self.hasPOWithoutAddress():
            plone_utils.addPortalMessage(_('There are parcel owners without any address found! Desactivate them!'), type="warning")
        # disable portlets
        self.request.set('disable_plone.rightcolumn', 1)
        self.request.set('disable_plone.leftcolumn', 1)

    def __call__(self):
        if 'find_recipients_cadastre' in self.request.form:
            radius = self.getInquiryRadius()
            return self.getInvestigationPOs(radius)
        return self.index()

    def renderRecipientsCadastreListing(self):
        recipients = self.context.getRecipients()
        if not recipients:
            return ''
        contactlisting = RecipientsCadastreTable(recipients, self.request)
        contactlisting.update()
        return contactlisting.render()

    def getRecipients(self):
        context = aq_inner(self.context)
        return context.getRecipients()

    def hasPOWithoutAddress(self):
        context = aq_inner(self.context)
        for parcel_owner in context.getRecipients(onlyActive=True):
            if not parcel_owner.getStreet() or not parcel_owner.getAdr1():
                return True
        return False

    def getInvestigationPOs(self, radius=0):
        """
        Search parcel owners in a radius of 50 meters...
        """
        #if we do the search again, we first delete old datas...
        #remove every RecipientCadastre
        context = aq_inner(self.context)
        recipients = context.getRecipients()
        if recipients:
            context.manage_delObjects([recipient.getId() for recipient in recipients if recipient.Title()])

        portal_url = api.portal.get_tool('portal_url')
        event_path = portal_url.getPortalPath() + '/' + '/'.join(portal_url.getRelativeContentPath(context))

        licence = context.aq_inner.aq_parent
        cadastre = services.cadastre.new_session()
        neighbour_parcels = cadastre.query_parcels_in_radius(
            center_parcels=licence.getParcels(),
            radius=radius
        )

        for parcel in neighbour_parcels:
            owners = cadastre.query_owners_of_parcel(parcel.capakey)
            for owner in owners:
                pe = owner.pe and str(owner.pe.encode('utf-8')) or ''
                adr1 = owner.adr1 and str(owner.adr1.encode('utf-8')) or ''
                adr2 = owner.adr2 and str(owner.adr2.encode('utf-8')) or ''
                print pe, adr1, adr2
                #to avoid having several times the same Recipient (that could for example be on several parcels
                #we first look in portal_catalog where Recipients are catalogued
                brains = context.portal_catalog(
                    portal_type="RecipientCadastre",
                    path={'query': event_path, },
                    Title=pe.replace('(', ' ').replace(')', ' ')
                )
                if len(brains) > 0:
                    newrecipient = brains[0].getObject()
                else:
                    address = adr1 and adr2 and '{} {}'.format(adr1, adr2)
                    brains = context.portal_catalog(
                        portal_type="RecipientCadastre", path={'query': event_path},
                        getRecipientAddress=address
                    )
                    if len(brains) > 0:
                        newrecipient = brains[0].getObject()
                        newrecipient.setTitle(newrecipient.Title() + ' & ' + pe)
                        newrecipient.setName(newrecipient.getName() + ' - ' + context.parseCadastreName(pe))
                        newrecipient.reindexObject()
                    else:
                        newrecipientname = context.invokeFactory(
                            "RecipientCadastre",
                            id=context.generateUniqueId('RecipientCadastre'),
                            title=owner.pe,
                            name=context.parseCadastreName(pe),
                            adr1=owner.adr1,
                            adr2=owner.adr2,
                            street=context.parseCadastreStreet(adr2),
                            daa=owner.daa
                        )
                        newrecipient = getattr(context, newrecipientname)
                #create the PortionOut using the createPortionOut method...
                with api.env.adopt_roles(['Manager']):
                    context.portal_urban.createPortionOut(container=newrecipient, **parcel.reference_as_dict())
        cadastre.close()
        return context.REQUEST.RESPONSE.redirect(context.absolute_url() + '/#fieldsetlegend-urbaneventinquiry_recipients')

    def getInquiryRadius(self):
        licence = self.context.aq_parent
        if hasattr(licence, 'hasEnvironmentImpactStudy'):
            if licence.getHasEnvironmentImpactStudy():
                return 200
        if hasattr(licence, 'impactStudy'):
            if licence.getImpactStudy():
                return 200
        return 50
