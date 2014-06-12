# -*- coding: utf-8 -*-
#
# File: UrbanEvent.py
#
# Copyright (c) 2014 by CommunesPlone
# Generator: ArchGenXML Version 2.7
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

from Products.urban.config import *

##code-section module-header #fill in your manual code here
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from zope.i18n import translate
from Products.urban.UrbanVocabularyTerm import UrbanVocabulary
from Products.urban.utils import setOptionalAttributes
##/code-section module-header

schema = Schema((

    DateTimeField(
        name='eventDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            label_method="eventDateLabel",
            starting_year=1960,
            label='Eventdate',
            label_msgid='urban_label_eventDate',
            i18n_domain='urban',
        ),
        default_method='getDefaultTime',
    ),
    DateTimeField(
        name='transmitDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Transmitdate',
            label_msgid='urban_label_transmitDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='receiptDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Receiptdate',
            label_msgid='urban_label_receiptDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    StringField(
        name='receivedDocumentReference',
        widget=StringField._properties['widget'](
            label='Receiveddocumentreference',
            label_msgid='urban_label_receivedDocumentReference',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='auditionDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Auditiondate',
            label_msgid='urban_label_auditionDate',
            i18n_domain='urban',
        ),
        optional=True,
    ),
    DateTimeField(
        name='decisionDate',
        widget=DateTimeField._properties['widget'](
            show_hm=False,
            format="%d/%m/%Y",
            starting_year=1960,
            label='Decisiondate',
            label_msgid='urban_label_decisionDate',
            i18n_domain='urban',
        ),
        optional= True,
    ),
    StringField(
        name='decision',
        widget=SelectionWidget(
            label='Decision',
            label_msgid='urban_label_decision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('decisions', inUrbanConfig=False),
    ),
    TextField(
        name='decisionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Decisiontext',
            label_msgid='urban_label_decisionText',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_output_type='text/html',
        optional= True,
    ),
    StringField(
        name='adviceAgreementLevel',
        widget=SelectionWidget(
            format='select',
            label='Adviceagreementlevel',
            label_msgid='urban_label_adviceAgreementLevel',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary='listAdviceAgreementLevels',
    ),
    StringField(
        name='externalDecision',
        widget=SelectionWidget(
            label='Externaldecision',
            label_msgid='urban_label_externalDecision',
            i18n_domain='urban',
        ),
        enforceVocabulary=True,
        optional=True,
        vocabulary=UrbanVocabulary('externaldecisions', inUrbanConfig=False),
    ),
    TextField(
        name='opinionText',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Opiniontext',
            label_msgid='urban_label_opinionText',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_output_type='text/html',
        optional=True,
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
            label_msgid='urban_label_eventRecipient',
            i18n_domain='urban',
        ),
        allowed_types= ('Recipient','Applicant','Architect'),
        optional=True,
        relationship="recipients",
    ),
    ReferenceField(
        name='urbaneventtypes',
        widget=ReferenceBrowserWidget(
            visible=False,
            label='Urbaneventtypes',
            label_msgid='urban_label_urbaneventtypes',
            i18n_domain='urban',
        ),
        allowed_types=('UrbanEventType', 'OpinionRequestEventType'),
        multiValued=0,
        relationship='UrbanEventType',
    ),
    TextField(
        name='pmTitle',
        allowable_content_types=('text/plain',),
        widget=TextAreaWidget(
            label='Pmtitle',
            label_msgid='urban_label_pmTitle',
            i18n_domain='urban',
        ),
        default_content_type='text/plain',
        default_method='getDefaultText',
        default_output_type='text/html',
        optional=True,
    ),
    TextField(
        name='pmDescription',
        allowable_content_types=('text/html',),
        widget=RichWidget(
            label='Pmdescription',
            label_msgid='urban_label_pmDescription',
            i18n_domain='urban',
        ),
        default_method='getDefaultText',
        default_output_type='text/html',
        optional=True,
    ),
    LinesField(
        name='FTsolicitOpinionsTo',
        widget=MultiSelectionWidget(
            format='checkbox',
            label='Ftsolicitopinionsto',
            label_msgid='urban_label_FTsolicitOpinionsTo',
            i18n_domain='urban',
        ),
        optional=True,
        multiValued=1,
        vocabulary=UrbanVocabulary('urbaneventtypes', vocType="OpinionRequestEventType", value_to_use='extraValue'),
    ),

),
)

##code-section after-local-schema #fill in your manual code here
optional_fields = [field.getName() for field in schema.filterFields(isMetadata=False) if field.getName() != 'eventDate']
setOptionalAttributes(schema, optional_fields)
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

    security.declarePublic('getDefaultText')
    def getDefaultText(self, context=None, field=None, html=False):
        if not context or not field:
            return ""
        urban_tool = getToolByName(self, 'portal_urban')
        return urban_tool.getTextDefaultValue(field.getName(), context, html=html, config=self.getUrbaneventtypes())

    def getDefaultTime(self):
        return DateTime()

    def getTemplates(self):
        """
          Returns contained templates (File)
        """
        wf_tool = getToolByName(self, 'portal_workflow')
        return [template for template in self.getUrbaneventtypes().listFolderContents({'portal_type': 'UrbanDoc'})
                if wf_tool.getInfoFor(template, 'review_state') == 'enabled']

    security.declarePublic('eventDateLabel')
    def eventDateLabel(self):
        """
         Returns the variable label
        """
        return self.getUrbaneventtypes().getEventDateLabel()

    security.declarePublic('listAdviceAgreementLevels')
    def listAdviceAgreementLevels(self):
        """
          Vocabulary for field 'adviceAgreementLevels'
        """
        lst=[
             ['agreementlevel_read_advice', translate('agreementlevel_read_advice', 'urban', context=self.REQUEST, default="Read advice")],
             ['agreementlevel_respect_charges', translate('agreementlevel_respect_charges', 'urban', context=self.REQUEST, default="Respect charges")],
            ]

        vocab = []
        #we add an empty vocab value of type "choose a value"
        val = translate('urban', EMPTY_VOCAB_VALUE, context=self, default=EMPTY_VOCAB_VALUE)
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
        if street == None:
            return 'NO ADDRESS FOUND'
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
            while (i<len(name)) and (name[i] not in ['&', ' ']):
                prenom1=prenom1+name[i]
                i=i+1
            if i<len(name) and name[i] != '&':
                i=i+1
            toreturn=prenom1
            if prenom1!='':
                toreturn=toreturn+' '
            toreturn=toreturn+nom1
            if name.rfind('&') > 0:
                while (i<len(name)) and (name[i] != '&'):
                    i=i+1
                if name[i]=='&':
                    toreturn=toreturn+' - M. '
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
        return 'M. %s' % toreturn

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
        return self.listFolderContents(contentFilter={"portal_type": "UrbanDoc"})

    def getAnnexes(self):
        """
          Return the annexes (File) of the UrbanEvent
        """
        return self.listFolderContents(contentFilter={"portal_type": "File"})

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
            street = recipient.getStreet() and recipient.getStreet() or ''
            address = recipient.getAdr1() and recipient.getAdr1() or ''
            toreturn=toreturn+'%'+recipient.getName()+'|'+street+'|'+address
        toreturn=toreturn+'</CSV>'
        return toreturn

    security.declarePublic('getFormattedDate')
    def getFormattedDate(self, date=None, withCityNamePrefix=False, forDelivery=False, translatemonth=True):
        """
          Return the date
          withCityNamePrefix and forDelivery are exclusive in the logic here above
        """
        if not date:
            date = self.getEventDate()
        elif type(date) == str:
            date = self.getField(date).getAccessor(self)()
        tool = getToolByName(self, 'portal_urban')
        formattedDate = tool.formatDate(date, translatemonth=translatemonth)
        cityName = unicode(tool.getCityName(), 'utf-8')
        if withCityNamePrefix:
            return translate('formatted_date_with_cityname', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
        if forDelivery:
            return translate('formatted_date_for_delivery', 'urban', context=self.REQUEST, mapping={'cityName': cityName, 'formattedDate': formattedDate.decode('utf8')}).encode('utf8')
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

    security.declarePublic('getDecision')
    def getDecision(self, theObject=False):
        """
          Returns the decision value or the UrbanVocabularyTerm if theObject=True
        """
        res = self.getField('decision').get(self)
        if res and theObject:
            tool = getToolByName(self, 'portal_urban')
            res = getattr(tool.decisions, res)
        return res

    security.declarePublic('getRenderedText')
    def getRenderedText(self, fieldname=''):
        """
          Returns the decision value or the UrbanVocabularyTerm if theObject=True
        """
        tool = getToolByName(self, 'portal_urban')
        field = self.getField(fieldname)
        accessorname = field.accessor
        text = getattr(self, accessorname)()
        return tool.renderText(text=text, context=self)



registerType(UrbanEvent, PROJECTNAME)
# end of class UrbanEvent

##code-section module-footer #fill in your manual code here
##/code-section module-footer

