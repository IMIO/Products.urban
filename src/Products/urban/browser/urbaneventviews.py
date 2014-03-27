from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.urban.Inquiry import Inquiry
from Products.urban.browser.mapview import MapView
from Products.urban.browser.table.urbantable import DocumentsTable
from Products.urban.browser.table.urbantable import AnnexesTable
from Products.urban.browser.table.urbantable import ClaimantsTable
from Products.urban.browser.table.urbantable import RecipientsCadastreTable


class UrbanEventView(BrowserView):
    """
      This manage the view of UrbanEvent
    """
    def getData(self):
        """
          This will return data to display about the UrbanEvent
          This returns a tuple where the element [0]
          is an object and the element [1] is a list of attributes
          Example : (context, [field1, field2, field3, ])
        """
        context = aq_inner(self.context)
        linkedUrbanEventType = context.getUrbaneventtypes()
        data = (context, [], )
        for activatedField in linkedUrbanEventType.getActivatedFields():
            if not activatedField:
                continue  # in some case, there could be an empty value in activatedFields...
            data[1].append(activatedField)
        return data

    def mayAddUrbanEvent(self):
        """
          Return True if the current user may add an UrbanEvent
        """
        context = aq_inner(self.context)
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        if member.has_permission('ATContentTypes: Add File', context):
            return True
        return False

    def mayAddAnnex(self):
        """
          Return True if the current user may add an Annex (File)
        """
        context = aq_inner(self.context)
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
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

    def renderAnnexListing(self):
        event = aq_inner(self.context)
        queryString = {
            'portal_type': 'File',
            'path': '/'.join(event.getPhysicalPath()),
            'sort_on': 'created'
        }
        catalog = getToolByName(event, 'portal_catalog')
        annexes = catalog(queryString)
        if not annexes:
            return ''
        annexlisting = AnnexesTable(annexes, self.request)
        annexlisting.update()
        return annexlisting.render()

    def getListOfTemplatesToGenerate(self):
        """
        Return a list of dicts. Each dict contains all the infos needed in the html <href> tag to create the
        corresponding link for document generation
        """
        context = aq_inner(self.context)
        template_list = [{
            'name':template.id.split('.')[0],
            'title':template.Title(),
            'class':'',
            'href':self._generateDocumentHref(context, template),
        }
            for template in context.getTemplates() if template.mayGenerateUrbanDoc(context)]

        for generated_doc in context.objectValues():
            for template in template_list:
                if generated_doc.id.startswith(template['name']):
                    template['class'] = 'urban-document-already-created'
        return template_list

    def _generateDocumentHref(self, context, template):
        """
        """
        return "%s/create_urbandoc?template_uid=%s" % (context.absolute_url(), template.UID())

    def getUrbaneventtypes(self):
        """
          Return the accessor urbanEventTypes()
        """
        context = aq_inner(self.context)
        return context.getUrbaneventtypes()


class UrbanEventInquiryView(UrbanEventView, MapView):
    """
      This manage the view of UrbanEventInquiry
      It is based on the default UrbanEventView
    """
    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.context = context
        self.request = request
        plone_utils = getToolByName(context, 'plone_utils')
        self.linkedInquiry = self.context.getLinkedInquiry()
        if not self.linkedInquiry:
            plone_utils.addPortalMessage(_('This UrbanEventInquiry is not linked to an existing Inquiry !  Define a new inquiry on the licence !'), type="error")
        if self.hasPOWithoutAddress():
            plone_utils.addPortalMessage(_('There are parcel owners without any address found! Desactivate them!'), type="warning")

    def __call__(self):
        if 'find_recipients_cadastre' in self.request.form:
            radius = self.getInquiryRadius()
            return self.getInvestigationPOs(radius)
        return self.index()

    def getParcels(self):
        context = aq_inner(self.context)
        return context.getParcels()

    def renderClaimantsListing(self):
        if not self.context.getClaimants():
            return ''
        contactlisting = ClaimantsTable(self.context, self.request)
        contactlisting.update()
        return contactlisting.render()

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

    def getInquiryData(self):
        """
          This will return data to display about the UrbanEventInquiry
          See UrbanEventView.getData doc string
        """
        context = aq_inner(self.context)
        linkedInquiry = context.getLinkedInquiry()
        if not linkedInquiry:
            #this should not happen...
            return None
        inquiryData = (linkedInquiry, [])
        #we want to display the fields corresponding to the Inquiry
        #the linkedInquiry can be the licence itself or an Inquiry object
        inquiryAttributes = Inquiry.schema.filterFields(isMetadata=False)
        #do not take the 2 first fields into account, it is 'id' and 'title'
        inquiryAttributes = inquiryAttributes[2:]
        for inquiryAttribute in inquiryAttributes:
            inquiryAttributeName = inquiryAttribute.getName()
            if inquiryAttributeName == "claimsText":
                #as this text can be very long, we do not want to show it with the other
                #fields, we will display it in the "Claimants" part of the template
                continue
            inquiryData[1].append(inquiryAttributeName)
        return inquiryData

    def getLinkToTheInquiries(self):
        """
          This will return a link to the inquiries on the linked licence
        """
        context = aq_inner(self.context)
        return context.aq_inner.aq_parent.absolute_url() + '/#fieldsetlegend-urban_investigation_and_advices'

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

    def getInvestigationPOs(self, radius=50):
        """
          Search the parcels in a radius of 50 meters...
        """
        #if we do the search again, we first delete old datas...
        #remove every RecipientCadastre
        context = aq_inner(self.context)
        recipients = context.getRecipients()
        if recipients:
            context.manage_delObjects([recipient.getId() for recipient in recipients if recipient.Title()])

        #then we can go...
        tool = getToolByName(context, 'portal_urban')
        portal_url = getToolByName(context, 'portal_url')
        event_path = portal_url.getPortalPath() + '/' + '/'.join(portal_url.getRelativeContentPath(context))
        strsql = "SELECT da, section, radical, exposant, bis, puissance, capakey FROM capa where intersects(buffer((select memgeomunion(the_geom) from capa where "
        strfilter = ''
        for portionOutObj in context.aq_inner.aq_parent.objectValues('PortionOut'):
            if strfilter != '':
                strfilter = strfilter + " or "
            strfilter = strfilter + "(da = " + portionOutObj.getDivisionCode() + " and section = '" + portionOutObj.getSection() + "' and radical = " + portionOutObj.getRadical()
            if portionOutObj.getBis() != '':
                strfilter = strfilter + " and bis = " + portionOutObj.getBis()
            if portionOutObj.getExposant() != '':
                strfilter = strfilter + " and exposant = '" + portionOutObj.getExposant() + "'"
            if portionOutObj.getPuissance() != '':
                strfilter = strfilter + " and puissance = " + portionOutObj.getPuissance()
            strfilter = strfilter + ")"

        strsql = strsql + strfilter + "), {radius}), capa.the_geom);".format(radius=radius)
        print strsql
        rsportionouts = tool.queryDB(query_string=strsql)
        for rsportionout in rsportionouts:
            print rsportionout
            divisioncode = str(rsportionout['da'])
            section = rsportionout['section']
            radical = str(rsportionout['radical'])
            exposant = rsportionout['exposant']
            bis = str(rsportionout['bis'])
            puissance = str(rsportionout['puissance'])
            if bis == '0':
                bis = ''
            if puissance == '0':
                puissance = ''
            #rspocads = tool.queryDB(query_string = "select * from map left join prc on map.prc = prc.prc where capakey LIKE '" + rsportionout['capakey'] + "'")
            rspocads = tool.queryDB(query_string="select * from map where capakey = '" + rsportionout['capakey'] + "' order by pe")
            for rspocad in rspocads:
                print rspocad
                rspes = tool.queryDB(query_string="select * from pe where daa = " + str(rspocad['daa']) + ";")

                for rspe in rspes:
                    print rspe
                    #to avoid having several times the same Recipient (that could for example be on several parcels
                    #we first look in portal_catalog where Recipients are catalogued
                    brains = context.portal_catalog(portal_type="RecipientCadastre", path={'query': event_path, }, Title=str(rspe['pe']))
                    if len(brains) > 0:
                        newrecipient = brains[0].getObject()
                    else:
                        brains = context.portal_catalog(portal_type="RecipientCadastre", path={'query': event_path, }, getRecipientAddress=(str(rspe['adr1']) + ' ' + str(rspe['adr2'])))
                        if len(brains) > 0:
                            newrecipient = brains[0].getObject()
                            newrecipient.setTitle(newrecipient.Title() + ' & ' + rspe['pe'])
                            newrecipient.setName(newrecipient.getName() + ' - ' + context.parseCadastreName(rspe['pe']))
                            newrecipient.reindexObject()
                        else:
                            newrecipientname = context.invokeFactory("RecipientCadastre", id=context.generateUniqueId('RecipientCadastre'), title=rspe['pe'], name=context.parseCadastreName(rspe['pe']), adr1=rspe['adr1'], adr2=rspe['adr2'], street=context.parseCadastreStreet(rspe['adr2']), daa=rspe['daa'])
                            newrecipient = getattr(context, newrecipientname)
                    #create the PortionOut using the createPortionOut method...
                    context.portal_urban.createPortionOut(container=newrecipient, division=divisioncode, section=section, radical=radical, bis=bis, exposant=exposant, puissance=puissance, partie=False)
        return context.REQUEST.RESPONSE.redirect(context.absolute_url() + '/#fieldsetlegend-urbaneventinquiry_recipients')

    def getInquiryRadius(self):
        if self.context.getHasEnvironmentImpactStudy():
            return 200
        return 50
