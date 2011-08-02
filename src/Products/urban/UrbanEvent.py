# -*- coding: utf-8 -*-
#
# File: UrbanEvent.py
#
# Copyright (c) 2011 by CommunesPlone
# Generator: ArchGenXML Version 2.6
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#

__author__ = """Gauthier BASTIEN <gbastien@commune.sambreville.be>, Stephan GEULETTE
<stephan.geulette@uvcw.be>, Jean-Michel Abe <jm.abe@la-bruyere.be>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces

from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin

from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import \
    ReferenceBrowserWidget
from Products.urban.config import *

##code-section module-header #fill in your manual code here
from DateTime import DateTime
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate as _
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='eventDate',
        default=DateTime(),
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            condition="python:here.attributeIsUsed('eventDate')",
            format="%d/%m/%Y",
            label='Eventdate',
            label_msgid='urban_label_eventDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='receiptDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            condition="python:here.attributeIsUsed('receiptDate')",
            format="%d/%m/%Y",
            label='Receiptdate',
            label_msgid='urban_label_receiptDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='receivedDocumentReference',
        widget=StringField._properties['widget'](
            condition="python:here.attributeIsUsed('receivedDocumentReference')",
            label='Receiveddocumentreference',
            label_msgid='urban_label_receivedDocumentReference',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='adviceAgreementLevel',
        widget=SelectionWidget(
            condition="python:here.attributeIsUsed('adviceAgreementLevel')",
            format='select',
            label='Adviceagreementlevel',
            label_msgid='urban_label_adviceAgreementLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary='listAdviceAgreementLevels',
    ),
    ReferenceField(
        name='eventRecipient',
        widget=ReferenceBrowserWidget(
            label='Destinataire',
            allow_search=1,
            allow_browse=0,
            show_indexes=1,
            show_index_selector=1,
            available_indexes={'getFirstname':'First name','getSurname': 'Surname'},
            wild_card_search=True,
            condition="python:here.attributeIsUsed('eventRecipient')",
            label_msgid='urban_label_eventRecipient',
            i18n_domain='urban',
        ),
        allowed_types= ('Recipient','Applicant','Architect'),
        optional=True,
        relationship="recipients",
    ),
    StringField(
        name='decision',
        widget=SelectionWidget(
            condition="python:here.attributeIsUsed('decision')",
            label='Decision',
            label_msgid='urban_label_decision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary='listDecisions',
    ),
    DateTimeField(
        name='decisionDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            condition="python:here.attributeIsUsed('decisionDate')",
            format="%d/%m/%Y",
            label='Decisiondate',
            label_msgid='urban_label_decisionDate',
            i18n_domain='urban',
        ),
        optional= True,
    ),
    TextField(
        name='decisionText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            condition="python:here.attributeIsUsed('decisionText')",
            label='Decisiontext',
            label_msgid='urban_label_decisionText',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        optional= True,
    ),
    DateTimeField(
        name='explanationsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            condition="python:here.attributeIsUsed('explanationsDate')",
            format="%d/%m/%Y",
            label='Explanationsdate',
            label_msgid='urban_label_explanationsDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='claimsDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            condition="python:here.attributeIsUsed('claimsDate')",
            format="%d/%m/%Y",
            label='Claimsdate',
            label_msgid='urban_label_claimsDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    TextField(
        name='claimsText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        widget=RichWidget(
            condition="python:here.attributeIsUsed('claimsText')",
            label='Claimstext',
            label_msgid='urban_label_claimsText',
            i18n_domain='urban',
        ),
        default_output_type='text/html',
        optional= True,
    ),
    ReferenceField(
        name='urbaneventtypes',
        widget=ReferenceBrowserWidget(
            visible=False,
            label='Urbaneventtypes',
            label_msgid='urban_label_urbaneventtypes',
            i18n_domain='urban',
        ),
        allowed_types=('UrbanEventType',),
        multiValued=0,
        relationship='UrbanEventType',
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema

UrbanEvent_schema = BaseFolderSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
UrbanEvent_schema['title'].widget.condition="python:here.showTitle()"
##/code-section after-schema

class UrbanEvent(BaseFolder, BrowserDefaultMixin):
    """
    """
    security = ClassSecurityInfo()

    implements(interfaces.IUrbanEvent)

    meta_type = 'UrbanEvent'
    _at_rename_after_creation = True

    schema = UrbanEvent_schema

    ##code-section class-header #fill in your manual code here
    #implements(interfacesToImplement)
    aliases = {
        '(Default)'  : 'UrbanEvent_view',
        'view'       : '(Default)',
        'index.html' : '(Default)',
        'edit'       : 'UrbanEvent_edit',
        'properties' : 'base_metadata',
        'sharing'    : '',
        }
    ##/code-section class-header

    # Methods

    # Manually created methods

    security.declarePublic('listDecisions')
    def listDecisions(self):
        """
         Returns the list of decisions from the configuration
        """
        urbantool = getToolByName(self,'portal_urban')
        return DisplayList(urbantool.listVocabulary('decisions', self, inUrbanConfig=False))

    security.declarePublic('listAdviceAgreementLevels')
    def listAdviceAgreementLevels(self):
        """
          Vocabulary for field 'adviceAgreementLevels'
        """
        lst=[
             ['agreementlevel_read_advice', _('agreementlevel_read_advice', 'urban', context=self.REQUEST, default="Read advice")],
             ['agreementlevel_respect_charges', _('agreementlevel_respect_charges', 'urban', context=self.REQUEST, default="Respect charges")],
            ]
        vocab = []

        #we add an empty vocab value of type "choose a value"
        val = _('urban', EMPTY_VOCAB_VALUE, context=self, default=EMPTY_VOCAB_VALUE)
        vocab.append(('', val))

        for elt in lst:
            vocab.append((elt[0], elt[1]))
        return DisplayList(tuple(vocab))

    security.declarePublic('isInt')
    def isInt(self, s):
        """
          Check if 's' is an integer, return True or False...
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    security.declarePublic('parseCadastreStreet')
    def parseCadastreStreet(self, street):
        """
           Return a parsed version of data from Cadastre so we obtain something
           more beautiful to display
        """
        print '\n\n Street: '+street
        i=0
        toreturn=''
        while (i < len(street)) and (street[i] !=','):
            toreturn=toreturn+street[i]
            i=i+1
        if i < len(street):
            while (i<len(street)) and (not self.isInt(street[i])):
                i=i+1
            toreturn=toreturn+' '
        while i < len(street):
            toreturn=toreturn+street[i]
            i=i+1
        return toreturn

    security.declarePublic('parseCadastreName')
    def parseCadastreName(self, name):
        """
        """
        print '\n\nName: '+name
        i=0
        nom1=''
        prenom1=''
        nom2=''
        prenom2=''
        toreturn=''
        if name.rfind(',') > 0:
            while (i<len(name)) and (name[i] != ','):
                nom1=nom1+name[i]
                i=i+1
            if i<len(name):
                i=i+1
            while (i<len(name)) and (name[i] != ' '):
                i=i+1
            if i<len(name):
                i=i+1
            while (i<len(name)) and (name[i] != ' '):
                prenom1=prenom1+name[i]
                i=i+1
            if i<len(name):
                i=i+1
            toreturn=prenom1
            if prenom1!='':
                toreturn=toreturn+' '
            toreturn=toreturn+nom1
            if name.rfind('&') > 0:
                while (i<len(name)) and (name[i] != '&'):
                    i=i+1
                if name[i]=='&':
                    toreturn=toreturn+' OU '
                    i=i+1
                while (i<len(name)) and (name[i] != ','):
                    nom2=nom2+name[i]
                    i=i+1
                if i<len(name):
                    i=i+1
                while (i<len(name)) and (name[i] != ' '):
                    i=i+1
                if i<len(name):
                    i=i+1
                while (i<len(name)) and (name[i] != ' '):
                    prenom2=prenom2+name[i]
                    i=i+1
                toreturn=toreturn+prenom2
                if prenom2 != '':
                    toreturn=toreturn+' '
                toreturn=toreturn+nom2
        else:
            toreturn=name
        return toreturn

    security.declarePublic('addInvestigationPOs')
    def addInvestigationPOs(self):
        """
          Search the parcels in a radius of 50 meters...
        """
        #if we do the search again, we first delete old datas...
        #remove every RecipientCadastre
        recipients = self.getRecipients()
        if recipients:
            self.manage_delObjects([recipient.getId() for recipient in recipients])

        #then we can go...
        tool=getToolByName(self,'portal_urban')
        portal_url=getToolByName(self,'portal_url')
        event_path=portal_url.getPortalPath()+'/'+'/'.join(portal_url.getRelativeContentPath(self))
        strsql = "SELECT da, section,radical,exposant,bis,puissance,capakey FROM capa where intersects(buffer((select memgeomunion(the_geom) from capa where "
        strfilter=''
        for portionOutObj in self.aq_inner.aq_parent.objectValues('PortionOut'):
            if strfilter !='':
                strfilter=strfilter + " or "
            strfilter=strfilter+"(da="+portionOutObj.getDivisionCode()+" and section='"+portionOutObj.getSection()+"' and radical="+portionOutObj.getRadical()
            if portionOutObj.getBis() != '':
                strfilter=strfilter+" and bis="+portionOutObj.getBis()
            if portionOutObj.getExposant() != '':
                strfilter=strfilter+" and exposant='"+portionOutObj.getExposant()+"'"
            if portionOutObj.getPuissance() != '':
                strfilter=strfilter+" and puissance="+portionOutObj.getPuissance()
            strfilter=strfilter+")"

        strsql=strsql+strfilter+"),50), capa.the_geom);"
        print strsql
        rsportionouts=tool.queryDB(query_string=strsql)
        for rsportionout in rsportionouts:
            print rsportionout
            divisioncode=str(rsportionout['da'])
            section=rsportionout['section']
            radical=str(rsportionout['radical'])
            exposant=rsportionout['exposant']
            bis=str(rsportionout['bis'])
            puissance=str(rsportionout['puissance'])
            if bis == '0':
                bis = ''
            if puissance == '0':
                puissance = ''
            #rspocads=tool.queryDB(query_string="select * from map left join prc on map.prc=prc.prc where capakey LIKE '"+rsportionout['capakey']+"'")
            rspocads=tool.queryDB(query_string="select * from map where capakey = '"+rsportionout['capakey']+"' order by pe")
            for rspocad in rspocads:
                print rspocad
                rspes=tool.queryDB(query_string="select * from pe where daa = "+str(rspocad['daa'])+";")

                for rspe in rspes:
                    print rspe
                    #to avoid having several times the same Recipient (that could for example be on several parcels
                    #we first look in portal_catalog where Recipients are catalogued
                    brains=self.portal_catalog(portal_type="RecipientCadastre", path={'query':event_path,}, Title=str(rspe['pe']))
                    if len(brains) > 0:
                        newrecipient=brains[0].getObject()
                    else:
                        brains=self.portal_catalog(portal_type="RecipientCadastre", path={'query': event_path,}, getRecipientAddress=(str(rspe['adr1'])+' '+str(rspe['adr2'])))
                        if len(brains) > 0:
                            newrecipient=brains[0].getObject()
                            newrecipient.setTitle(newrecipient.Title()+' & '+rspe['pe'])
                            newrecipient.setName(newrecipient.getName()+' OU '+self.parseCadastreName(rspe['pe']))
                            newrecipient.reindexObject()
                        else:
                            newrecipientname = self.invokeFactory("RecipientCadastre",id=self.generateUniqueId('RecipientCadastre'),title=rspe['pe'],name=self.parseCadastreName(rspe['pe']),adr1=rspe['adr1'],adr2=rspe['adr2'],street=self.parseCadastreStreet(rspe['adr2']),daa=rspe['daa'])
                            newrecipient=getattr(self,newrecipientname)
                    #create the PortionOut using the createPortionOut method...
                    self.portal_urban.createPortionOut(path=newrecipient,division=divisioncode, section=section, radical=radical, bis=bis, exposant=exposant, puissance=puissance, partie=False)
        return self.REQUEST.RESPONSE.redirect(self.absolute_url()+'/view')

    security.declarePublic('initMap')
    def initMap(self):
        """
        """
        tool=getToolByName(self,'portal_urban')
        cqlquery2=''
        cqlquery=''
        zoneExtent = ''
        if self.objectValues('RecipientCadastre'):
            for portionOutObj in self.aq_inner.aq_parent.objectValues('PortionOut'):
                if cqlquery2 !='':
                    cqlquery2=cqlquery2 + " or "
                cqlquery2=cqlquery2+"(section='"+portionOutObj.getSection()+"' and radical="+portionOutObj.getRadical()
                if portionOutObj.getBis() != '':
                    cqlquery2=cqlquery2+" and bis="+portionOutObj.getBis()
                if portionOutObj.getExposant() != '':
                    cqlquery2=cqlquery2+" and exposant='"+portionOutObj.getExposant()+"'"
                if portionOutObj.getPuissance() != '':
                    cqlquery2=cqlquery2+" and puissance="+portionOutObj.getPuissance()
                cqlquery2=cqlquery2+")"
            strsql = 'SELECT Xmin(selectedpos.extent),Ymin(selectedpos.extent),Xmax(selectedpos.extent), Ymax(selectedpos.extent) FROM (SELECT Extent(the_geom) FROM capa WHERE '+cqlquery2+') AS selectedpos'

            try:
                result = tool.queryDB(query_string=strsql)[0]
                zoneExtent = "%s,%s,%s,%s" % (result['xmin']-100,result['ymin']-100,result['xmax']+100,result['ymax']+100)
            except:
                pass

            strsql = "select distinct asText(buffer((select memgeomunion(the_geom) from capa where "+cqlquery2+"),50)) as bufferpolygon from capa;"
            bufferpolygon=tool.queryDB(query_string=strsql)[0]['bufferpolygon']

            cqlquery='intersects(the_geom,'+bufferpolygon+')'

            #generate a Layer with these datas
            #this layer will be used in the PageTemplate generating the mapfile
        #return the generated JS code
        return self.portal_urban.generateMapJS(self, cqlquery, cqlquery2,'', zoneExtent)

    def getRecipients(self):
        """
          Return the recipients of the UrbanEvent
        """
        return self.objectValues('RecipientCadastre')

    def getInvestigationLetterFile(self):
        """
          Return the recipients of the UrbanEvent
        """
        portal_url=getToolByName(self,'portal_url')
        docpath=portal_url.getPortalPath()+'/'+'/'.join(portal_url.getRelativeContentPath(self))
        brain=self.portal_catalog(path=docpath+'/',Title='Lettre')
        try:
            print docpath+'/'+'\n'
            print brain[0].getObject().Title()
            return brain[0].getObject()
        except:
            return None

    def getDocuments(self):
        """
          Return the documents (File) of the UrbanEvent
        """
        return self.objectValues('ATBlob')

    def getBeginDate(self):
        """
          Return the beginDate of the UrbanEvent
        """
        return self.getEventDate()

    def getEndDate(self):
        """
          Return the endDate of the UrbanEvent
        """
        urbanEventType = self.getUrbaneventtypes()
        beginDate = self.getBeginDate()
        #get the linked UrbanEventType
        if not urbanEventType or not beginDate:
            return None

        #get de deadLineDelay
        deadLineDelay = urbanEventType.getDeadLineDelay()
        #if there is no delay, we return the beginDate...
        if not deadLineDelay:
            return self.getBeginDate()

        #check if we have an integer as deadLineDelay
        if not str(deadLineDelay).isdigit():
            return self.getBeginDate()

        endDate = beginDate + deadLineDelay
        return endDate

    security.declarePublic('RecipientsCadastreCSV')
    def RecipientsCadastreCSV(self):
        """
          Generates a fake CSV file used in POD templates
        """
        recipients=self.objectValues('RecipientCadastre')
        toreturn='<CSV>TitreNomPrenom|AdresseLigne1|AdresseLigne2'
        wft = getToolByName(self, 'portal_workflow')
        for recipient in recipients:
            #do not take "disabled" recipients into account
            if wft.getInfoFor(recipient, 'review_state') == 'disabled':
                continue
            toreturn=toreturn+'%'+recipient.getName()+'|'+recipient.getStreet()+'|'+recipient.getAdr1()
        toreturn=toreturn+'</CSV>'
        return toreturn

    security.declarePublic('getFormattedDate')
    def getFormattedDate(self, date=None, withCityNamePrefix=False, forDelivery=False, translatemonth=True):
        """
          Return the date
          withCityNamePrefix and forDelivery are exclusive in the logic here above
        """
        #if we did not pass any DateTime, then we use the self 'eventDate' field
        if not date:
            date = self.getEventDate()
        tool = getToolByName(self, 'portal_urban')
        formattedDate = tool.formatDate(date, translatemonth=translatemonth)
        cityName = unicode(tool.getCityName(), 'utf-8')
        if withCityNamePrefix:
            return _('formatted_date_with_cityname', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
        if forDelivery:
            return _('formatted_date_for_delivery', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
        return formattedDate

    def attributeIsUsed(self, attrName):
        """
        """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return attrName in self.getUrbaneventtypes().getActivatedFields()
        else:
            return False

    def showTitle(self):
        """
        """
        urbanEventType = self.getUrbaneventtypes()
        if urbanEventType:
            return urbanEventType.getShowTitle()
        else:
            return False



registerType(UrbanEvent, PROJECTNAME)
# end of class UrbanEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer

