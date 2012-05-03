# -*- coding: utf-8 -*-
from DateTime import DateTime
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base
from zExceptions import BadRequest
from re import search
from re import finditer

#utilities
def check_role(self, role='Manager', context=None):
    from Products.CMFCore.utils import getToolByName
    pms = getToolByName(self, 'portal_membership')
    return pms.getAuthenticatedMember().has_role(role, context)

def createStreet(self, city, zipcode, streetcode, streetname, bestAddresskey=0, startdate=None, enddate=None, regionalroad='', ex_streets={}):
    """
      Creates a Street with given parameters
    """
    out = []
    from Products.CMFCore.utils import getToolByName
    wtool = getToolByName(self, 'portal_workflow')
    utool = getToolByName(self, 'portal_urban')
    #get the folder where we are going the create the streets in
    streetFolder = getattr(utool, 'streets')
    #first element is the city and second is the street
    #check if we need to create the city
    cityId = self.plone_utils.normalizeString(city)
    
    if not ex_streets.has_key(city):
        ex_streets[city] = {'cityId':'', 'zip':zipcode, 'streets':{}}
    #we check if the city has always the same zip
    if ex_streets[city]['zip'] != zipcode:
        out.append("! Current record: city '%s', zip '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, zipcode, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
        out.append("&nbsp;&nbsp;... The existing city '%s' has zip '%s'"%(city, ex_streets[city]['zip']))
    cityTemp = cityId
    counter = 1
    if ex_streets[city]['cityId'] == '':
        while hasattr(streetFolder, cityId):
            cityId= "%s%d" %(cityTemp, counter)
            counter += 1
        ex_streets[city]['cityId']=cityId
        #if the city doesnt exist we create it
        cityObjId = streetFolder.invokeFactory('City', id=cityId, title=city, zipCode=zipcode)
        cityObj = getattr(streetFolder, cityId)
        cityObj.reindexObject()
    cityId =  ex_streets[city]['cityId']
    cityObj = getattr(streetFolder, cityId)

    #transform dates into DateTimes
    if startdate:
        startdate=DateTime(startdate.__str__())
    if enddate:
        enddate=DateTime(enddate.__str__())

    #some checks
    create = True
    disable = False
    for street in ex_streets[city]['streets'].keys():
        streetdic = ex_streets[city]['streets'][street]
        diff_reg_road = False
        #current record is already existing
        #not an historical record: bakey is not 0 and is unique
        #historical record: bakey + begindate is unique
        if (enddate is None and bestAddresskey and bestAddresskey == streetdic['bestAddressKey'] and streetdic['endDate'] is None) or (enddate is not None and bestAddresskey == streetdic['bestAddressKey'] and startdate.Date() == streetdic['startDate'].Date()):
            #the current record already exists, we don't create it again
            create = False
            #!!! TO BE DONE WHEN UPDATING
            #!!! WE NEED TO COMPARE EACH FIELD TO UPDATE INFO IN CASE OF DIFFERENCE
            out.append("> Existing record: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
        else:
            #current record is not an historical record
            if enddate is None:
                ### we check if the street name is already used !
                #no comparison if existing street is disabled
                if streetdic['state'] == 'enabled' and streetdic['streetName'] == streetname:
                    #if the two records are identical except the regional road, we choose to disable record with reg road
                    #already identicals: city, zipcode, commune, street
                    #streetcode must be identicals, current reg road and existing reg road must be different
                    #we disable the record with a regional road
                    if streetcode == streetdic['streetCode'] and regionalroad != streetdic['regionalRoad']:
                        if regionalroad and not streetdic['regionalRoad']:
                            disable = True
                            diff_reg_road = True
                            out.append("! Disabled current record because <> reg road: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
                            out.append("&nbsp;&nbsp;... existing: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s', state '%s', <a href='%s'>url</a>"%(city, streetname, streetdic['streetCode'], streetdic['bestAddressKey'], streetdic['regionalRoad'], streetdic['startDate'], streetdic['endDate'], streetdic['state'], streetdic['obj'].absolute_url()))
                        elif not regionalroad and streetdic['regionalRoad']:
                            diff_reg_road = True
                            if streetdic['state'] == 'enabled':
                                wtool.doActionFor(streetdic['obj'], 'disable')
                                out.append("! Disabled existing record because <> reg road: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s', state '%s', <a href='%s'>url</a>"%(city, streetname, streetdic['streetCode'], streetdic['bestAddressKey'], streetdic['regionalRoad'], streetdic['startDate'], streetdic['endDate'], streetdic['state'], streetdic['obj'].absolute_url()))
                                out.append("&nbsp;&nbsp;... Current record: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
                    #if we haven't found a different reg road case, we report an error
                    if not diff_reg_road:
                        out.append("! Current record: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
                        out.append("&nbsp;&nbsp;... Found same street name '%s' in city '%s': streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s', state '%s', <a href='%s'>url</a>"%(streetname, city, streetdic['streetCode'], streetdic['bestAddressKey'], streetdic['regionalRoad'], streetdic['startDate'], streetdic['endDate'], streetdic['state'], streetdic['obj'].absolute_url()))

                ### we check if the street code is already used !
                #current streetcode can be '0', we don't check this street code. 
                if not diff_reg_road and streetcode and streetcode != '0':
                    #no comparison if existing street is disabled
                    if streetdic['state'] == 'enabled' and streetdic['streetCode'] == streetcode:
                        out.append("! Current record: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
                        out.append("&nbsp;&nbsp;... Found same street code '%s' in city '%s': name '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s', state '%s', <a href='%s'>url</a>"%(streetcode, city, streetdic['streetName'], streetdic['bestAddressKey'], streetdic['regionalRoad'], streetdic['startDate'], streetdic['endDate'], streetdic['state'], streetdic['obj'].absolute_url()))
            else:
                disable = True

    if create:
        streetId = streetTest = self.plone_utils.normalizeString(streetname)
        i = 0
        while hasattr(aq_base(cityObj), streetTest):
            i +=1
            if not disable: #no need to warn for an historical record: normal case
                out.append("info: Found existing id '%s' in entity '%s'"%(streetTest, cityObj.Title()))
            streetTest = streetId + str(i)
        streetId = streetTest
        try:
            streetObjId = cityObj.invokeFactory('Street', id=streetId, streetCode=streetcode, streetName=streetname, bestAddressKey=bestAddresskey, startDate=startdate, endDate=enddate, regionalRoad=regionalroad)
            streetObj = getattr(cityObj, streetObjId)
            #if a street has an endDate, we disable it as this should not be
            #used anymore but present for history purpose
            if disable or (enddate and enddate < DateTime()):
                wtool.doActionFor(streetObj, 'disable')
                out.append("! Disabled current record because historical: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
            streetObj.reindexObject()
            #we add the current record in the existing streets dictionary for next checks
            ex_streets[city]['streets'][streetObjId] = {'streetCode' : streetcode,
                                                        'streetName' : streetname,
                                                        'bestAddressKey' : bestAddresskey,
                                                        'startDate' : startdate,
                                                        'endDate' : enddate,
                                                        'regionalRoad' : regionalroad,
                                                        'state' : wtool.getInfoFor(streetObj, 'review_state'),
                                                        'obj' : streetObj,
                }
        except Exception, msg:
            out.append("!! Problem during creation of street id '%s', code '%s' in city '%s': name '%s', bakey '%s': %s"%(streetId, streetcode, city, streetname, bestAddresskey, msg))

    return out

def load_existing_streets(self, dic):
    """
      stores in a dictionnary informations about existing streets
    """
    from Products.CMFCore.utils import getToolByName
    tool = getToolByName(self, 'portal_urban')
    wtool = getToolByName(self, 'portal_workflow')
    out = ['Existing streets in Plone']
    localities = tool.streets.objectValues('City')
    for locality in localities:
        loc_title = locality.Title()
        dic[loc_title] = {'cityId':locality.id, 'zip':locality.getZipCode(), 'streets':{}}
        cnt_ba = cnt_man = 0
        streets = dic[loc_title]['streets']
        for street in locality.objectValues('Street'):
            id = street.getId()
            if streets.has_key(id): #never, id is unique in a folder
                out.append("Loading existing streets: existing id '%s' in locality '%s'"%(id,locality))
            if street.getBestAddressKey():
                cnt_ba += 1
            else:
                cnt_man += 1
            streets[id] = { 'streetCode' : street.getStreetCode(),
                            'streetName' : street.getStreetName(),
                            'bestAddressKey' : street.getBestAddressKey(),
                            'startDate' : street.getStartDate(),
                            'endDate' : street.getEndDate(),
                            'regionalRoad' : street.getRegionalRoad(),
                            'state' : wtool.getInfoFor(street, 'review_state'),
                            'obj' : street,
                        }
            if street.getEndDate() is not None and wtool.getInfoFor(street, 'review_state') == 'enabled':
                out.append("! Found an history street enabled! : locality '%s', street '%s', <a href='%s'>url</a>"%(loc_title, street.Title(), street.absolute_url()))
        out.append("Locality: '%s', bestaddress streets:%d, manual streets:%d"%(loc_title, cnt_ba, cnt_man))
    if out: out[-1] += '<br />'
    return out

def import_streets_fromdb(self, cityName='', password=''):
    """
      Method for importing streets from a PostgreSQL db
      We need the zipCode
      CityName, ZipCode, StreetCode, StreetName
      In the portal_urban.streets folder, we create a hierarchy of
      'City's containing 'Street's
    """
    if not check_role(self):
        return "You must have a manager role to run this script"

    out = ['<html>']
    lf = '<br />'
    if not cityName and not password:
        #out.append("available properties:%s"%portal.portal_memberdata.propertyItems())
        out.append("You must call the script followed by needed parameters:")
        out.append("-> cityName=... name of the commune")
        out.append("-> password=... postgres password of bestaddressreader")
        out.append("by example ...?cityName=La Bruyère&password=lebonmotdepasse<br/>")
        return lf.join(out)

    from Products.CMFCore.utils import getToolByName
    tool = getToolByName(self, 'portal_urban')
    if tool is None:
        return "No portal_urban found on this site: is urban installed?"
    if not hasattr(tool, 'streets'):
        return "The 'streets' folder does not exist in portal_urban!"

    ex_streets = {}
    ret = load_existing_streets(self, ex_streets)
    out += ret

    #every informations about the db connection are public...
    connection_string = "dbname='bestaddress' host='villesetcommunes.all2all.org' user='bestaddressreader' password='%s'" % password
#    connection_string = "dbname='bestaddress' host='localhost' user='bestaddressreader' password='%s'" % password
    query_string = "SELECT * from urban_addresses WHERE commune='%s' order by short_entity" % cityName
    results = tool.queryDB(query_string, connection_string)
    if not results:
        return "No record found for city name '%s', maybe mispelled ?" % cityName
    numberOfRecords = len(results)
    out.append("%d streets found in the database" % numberOfRecords)
    i = 1
    for result in results:
        print "Importing street %d of %d" % (i, numberOfRecords)
        city = result['short_entity']
        zipcode = result['zip']
        streetcode = result['national_code']
        streetname = result['street']
        bestAddresskey = result['key']
        startdate = result['begin_date']
        enddate = result['end_date']
        regionalroad = result['regional_road']
        ret = createStreet(tool, city, zipcode, streetcode, streetname, bestAddresskey, startdate, enddate, regionalroad, ex_streets)
        out += ret
        i = i+1
    return lf.join(out) + '</html>'

def import_streets_fromfile(self, filePath=None, separator=';'):
    """
      Method for importing streets from a file
      The CSV needs to have the following format :
      CityName, ZipCode, StreetCode, StreetName
      An example is available in the Extensions/streets.txt file of Products.urban
      In the portal_urban.streets folder, we create a hierarchy of
      'City's containing 'Street's
    """
    if not self.portal_type == 'UrbanTool':
        raise Unauthorized, "This script must be called on portal_urban!"
    if not hasattr(self, 'streets'):
        raise AttributeError, "The streets folder does not exist in portal_urban!"

    #if no filePath is defined, take the streets.txt file stored here
    if not filePath:
        import Products.urban.Extensions as ext, os
        filePath = ext.__path__[0] + '/streets.txt'
        if not os.path.isfile(filePath):
            raise ImportError, "The streets.txt file does not exist in Products.urban.Extensions.  Try using your own file by passing it as parameter to this ExternalMethod."

    ex_streets = {}
    ret = load_existing_streets(self, ex_streets)
    if ret:
        print '\n'.join(ret)

    file = open(filePath, 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    for line in file.readlines():
        print "Importing street %d of %d" % (i, numberOfRecords)
        city, zipcode, streetcode, streetname = line.strip().split(separator)
        ret = createStreet(self, city, zipcode, streetcode, streetname, ex_streets=ex_streets)
        if ret:
            print '\n'.join(ret)
        i = i+1
    file.close()
    return "%d streets have been imported" % numberOfRecords

def import_localities_fromfile(self, filePath=None, separator=';'):
    """
      Method for importing localities from a file
      The CSV needs to have the following format :
      title and alsoCalled (with '\n' to separate the elements)
      An example is available in the Extensions/localities.txt file of Products.urban
      In the portal_urban.streets folder, we create a hierarchy of
      'City's containing 'Locality's
    """
    if not self.portal_type == 'UrbanTool':
        raise Unauthorized, "This script must be called on portal_urban!"
    if not hasattr(self, 'streets'):
        raise AttributeError, "The streets folder does not exist in portal_urban!"

    #if no filePath is defined, take the localities.txt file stored here
    if not filePath:
        import Products.urban.Extensions as ext, os
        filePath = ext.__path__[0] + '/localities.txt'
        if not os.path.isfile(filePath):
            raise ImportError, "The localities.txt file does not exist in Products.urban.Extensions.  Try using your own file by passing it as parameter to this ExternalMethod."

    file = open(filePath, 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    streetFolder = getattr(self, 'streets')
    for line in file.readlines():
        print "Importing locality %d of %d" % (i, numberOfRecords)
        i = i + 1
        city, zipcode, localityName, alsoCalled = line.strip().split(separator)
        cityId = self.plone_utils.normalizeString(city)
        if not hasattr(aq_base(streetFolder), cityId):
            #if the city still does not exist, we create it
            cityObjId = streetFolder.invokeFactory('City', id=cityId, title=city, zipCode=zipcode)
            cityObj = getattr(streetFolder, cityObjId)
            cityObj.reindexObject()
        else:
            cityObj = getattr(streetFolder, cityId)
            try:
                localityId = self.plone_utils.normalizeString(localityName)
                localityObjId = cityObj.invokeFactory('Locality', id=localityId, localityName=localityName, alsoCalled='\n'.join(alsoCalled.split('|')))
                localityObj = getattr(cityObj, localityObjId)
            except BadRequest:
                print ("The locality with id '%s' already exists!" % (localityId))
                file.close()
    file.close()

def import_architects(self, filePath=None, separator=';'):
    """
      Method for importing streets
      The CSV needs to have the following format :
      Title (Gender), Name, Society, FirstName, AddressStreet, AddressHouseNumber, AddressZipCode, AddressCity, Email, Telephone, Fax, NRNumber
      An example is available in the Extensions/architects.txt file of Products.urban
      In the urban.architects folder, we create a list of 'Architect's
    """
    if not self.portal_type == 'UrbanTool':
        raise Unauthorized, "This script must be called on portal_urban!"
    #check that the 'architects' folder exists at the upper level
    if not hasattr(self.aq_parent.aq_inner.urban, 'architects'):
        raise AttributeError, "The architects folder does not exist in 'urban' folder!"

    #if no filePath is defined, take the architects.txt file stored here
    if not filePath:
        import Products.urban.Extensions as ext, os
        filePath = ext.__path__[0] + '/architects.txt'
        if not os.path.isfile(filePath):
            raise ImportError, "The architects.txt file does not exist in Products.urban.Extensions.  Try using your own file by passing it as parameter to this ExternalMethod."

    file = open(filePath, 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    #get the folder where we are going the create the architects in
    architectsFolder = getattr(self.aq_inner.aq_parent.urban, 'architects')
    for line in file.readlines():
        print "Importing architect %d of %d" % (i, numberOfRecords)
        title, name, firstname, society, addressstreet, addresshousenumber, addresszipcode, addresscity, email, telephone, fax, nrnumber = line.strip().split(separator)
        architectId = self.plone_utils.normalizeString("%s-%s" % (name, firstname))
        if not hasattr(architectsFolder, architectId):
            #if the architect still does not exist, we create it
            dict = {
                    'personTitle': title,
                    'name1': name,
                    'name2': firstname,
                    'society': society,
                    'street': addressstreet,
                    'number': addresshousenumber,
                    'zipcode': addresszipcode,
                    'city': addresscity,
                    'email': email,
                    'phone': telephone,
                    'fax': fax,
                    'nationalRegister': nrnumber,
                   }
            architectObjId = architectsFolder.invokeFactory('Architect', id=architectId, **dict)
            architectObj = getattr(architectsFolder, architectObjId)
            architectObj.reindexObject()
        i = i+1
    file.close()

def importBuildlicences(self):
    site = self.aq_inner.aq_parent
    if self.id != 'urban' or site.getPortalTypeName() != 'Plone Site':
        raise Unauthorized, "This script must be called on urban main page"

    csvfile = site.test2
    lines = csvfile.raw.splitlines()
    mapping = []
    data_start = 1
    for headline in lines:
        headline = headline.split(';')
        if headline[0]:
            data_start = data_start+1
            if headline[0] == 'DATA':
                break
            mapping.append(headline)
    
    licence_type = mapping[0][0]
    licence_container = getattr(self, '%ss' % licence_type.lower())
    field_mapping = mapping[0]
    foldermanager = site.portal_urban.foldermanagers.foldermanager1
    dummy_licence_id = licence_container.invokeFactory(licence_type, id=site.generateUniqueId('dummy'), 
                                                       usage='for_habitation', foldermanagers=[foldermanager])
    dummy_licence = getattr(licence_container, dummy_licence_id)
    dummies_objects = {licence_type:dummy_licence}
    for line in lines[data_start:]:
        data = line.split(';')
        lkws = [{'foldermanagers':[foldermanager], 'usage':'usage_not_applicable'}]
        for i in range(len(data))[1:]:
            field = field_mapping[i]
            if field:
                if hasattr(dummy_licence, field):
                    lkws[0][field] = data[i]     
                else:
                    lkws = globals()[field](dummy_licence, lkws, data[i])
        #import ipdb; ipdb.set_trace()
        licence_id = licence_container.invokeFactory(licence_type, id=site.generateUniqueId('oldlicence'), **lkws[0])
        licence = getattr(licence_container, licence_id)
        for subobject_mapping in mapping[1:]:
            subobject_type = subobject_mapping[0]
            if subobject_type not in dummies_objects.keys():
                dummy_subobject_id = dummy_licence.invokeFactory(subobject_type, id=site.generateUniqueId('dummy_%s' % subobject_type))
                dummies_objects[subobject_type] = getattr(dummy_licence, dummy_subobject_id)
            kws = [{}]
            empty_data = True
            for i in range(len(data))[1:]:
                field = subobject_mapping[i]
                if field:
                    if data[i]:
                        empty_data = False
                    if hasattr(dummies_objects[subobject_type], field):
                        kws[0][field] = data[i]     
                    else:
                        kws = globals()[field](licence, kws, data[i])
            #import ipdb; ipdb.set_trace()
            if not empty_data:
                for kw in kws:
                    subobject_id = licence.invokeFactory(subobject_type, id=site.generateUniqueId(subobject_type), **kw)
                    subobject = getattr(licence, subobject_id)
                    subobject.processForm()
        licence.processForm()

        print ('Done! : licence %s %s' % (lkws[0]['reference'], lkws[0]['licenceSubject']))

    return lines

def parseDivision(context, kws, raw_division):
    division_fields = []
    div_map = {'4':['62106', "Villers-L'Evêque"], '2':['62039', 'Fooz'], '5':['62077', 'Othee'], '1':['62006', 'Awans'], '3':['62053', 'Hognoul']}
    if raw_division not in div_map:
        return kws
    division_fields.append({'divisionCode':div_map[raw_division][0]})
    division_fields.append({'division':div_map[raw_division][1]})
    for dic in division_fields:
        kws[0].update(dic)
    return kws

def parseRadicalAndExposant(context, kws, raw_radical):
    last_radical = ''
    matches = finditer('(\d{1,4})(?:/?(\d{0,2}))([a-zA-Z]?)(\d?)', raw_radical)
    kw = kws[0]
    for match in matches:
        fields = {'radical':'', 'bis':'', 'exposant':'', 'puissance':''}
        if match.group(1):
            last_radical = match.group(1)
        fields['radical'] = last_radical
        fields['bis'] = match.group(2)
        fields['exposant'] = match.group(3)
        fields['puissance'] = match.group(4)
        new_kw = kw.copy()
        for k,v in fields.items():
            if v:
                new_kw.update({k:v}) 
        kws.append(new_kw)
    if len(kws) > 1:
        kws.pop(0)
    return kws

def parseDecisionDate(context, kws, raw_date):
    if not raw_date:
        return []
    splitted_date = raw_date.split('/')
    date = None
    if len(splitted_date[0]) == len(splitted_date[2]) == 2:
        date = DateTime('20%s 00:00:00 GMT+1' % ('/'.join(splitted_date)))
    elif len(splitted_date[2]) == 4:
        splitted_date.reverse()
        for part in splitted_date:
            if len(part) == 1:
                part = '0%s' % part
        date = DateTime('%s 00:00:00 GMT+1' % ('/'.join(splitted_date)))
    kws[0].update({'decisionDate':date})
    kws[0].update({'eventDate':date})
    return kws

def parseDecision(context, kws, decision_text):
    if not decision_text:
        return kws
    urban_tool = getToolByName(context, 'portal_urban')
    urban_event_type = getattr(urban_tool.buildlicence.urbaneventtypes, 'rapport-du-college')
    urban_event_fields = [{'title':urban_event_type.Title()},{'urbaneventtypes':(urban_event_type,)}]
    if 'octroi' in decision_text or 'Octroi' in decision_text:
        urban_event_fields.append({'decision':'favorable'})
        changeWorkflowState(context, 'accepted')
    else:
        urban_event_fields.append({'decision':'defavorable'})
        changeWorkflowState(context, 'refused')
    urban_event_fields.append({'decisionText':decision_text})
    for dic in urban_event_fields:
        kws[0].update(dic)
    return kws 

def parseApplicantName(context, kws, raw_name):
    name_fields = []
    names = raw_name.split(',')
    titles = {'Mr et Mme':'madam_and_mister', 'Mr & Mme':'madam_and_mister', 'Mme':'madam', 'Mr':'mister'}
    for name in names:
        match = search('^\s*(Mr et Mme|Mr & Mme|Mme|Mr)(.*)', name)
        if match:
            name = match.group(2)
            title = titles[match.group(1)]
            name_fields.append({'personTitle':title})
        match = search("%s%s" % ('(?:^\s*([A-Z]+-?[A-Z]*)\s+([A-Z](?:\.?-[A-Z]\.?|.+[a-z]+\S?|\.)))',
                                 '|(?:^\s*([A-Z](?:\.?-[A-Z]\.?|.+[a-z]+\S?|\.))\s+([A-Z]+-?[A-Z]*))'), name)
        if match:
            name1 = match.group(1) or match.group(4)
            name2 = match.group(2) or match.group(3)
            name_fields.append({'name1':name1})
            name_fields.append({'name2':name2})
        else:
            match = search('\s*(.*)\s*', name)
            name1 = match.group()
            name_fields.append({'name1':name1})
    for dic in name_fields:
        kws[0].update(dic)
    return kws

def parseWorkLocations(context, kws, raw_adress):
    catalog= getToolByName(context, 'portal_catalog')
    site = getToolByName(context, 'portal_url').getPortalObject()
    urban_streets_path = '/'.join(site.portal_urban.streets.getPhysicalPath())
    noisy_words = set(('du', 'de', 'le', 'la', 'les', 'à'))
    numbers = city = adress = '' 

    match = search('([^,]*),\s*(.*)\s+(\w+$)', raw_adress)
    if match:
        city = match.group(3).capitalize()
        adress = match.group(1).split()
        numbers = match.group(2)
    else :
        match = search('([^,]*)\s+(\w+$)', raw_adress)
        if match:
            city = match.group(2).capitalize()
            adress = match.group(1).split()
    street_keywords = [word.capitalize() for word in adress if word not in noisy_words] 
    street_keywords.append(city)
    streets_brains = catalog(
                             portal_type = 'Street', 
                             path = {'query':urban_streets_path, 'depth': 2},
                             Title = street_keywords
                            )
    worklocation = {}
    if numbers:
        worklocation.update({'number':numbers})
    if len(streets_brains) == 1:
        streetUID = streets_brains[0].getObject().getUID()
        worklocation.update({'street':streetUID})
    else:
        error(context, 'no street "%s" found' % ' '.join(adress), kws)
    kws[0].update({'workLocations':(worklocation,)})
    return kws

def parseLicenceSubject(context, kws, raw_subject):
    kws[0].update({'licenceSubject':raw_subject.capitalize()})
    return kws

def parseReference(context, kws, raw_reference):
    kws[0].update({'reference':'PU %s' % raw_reference})
    return kws

def changeWorkflowState(context, new_state):
    workflow_tool = getToolByName(context,'portal_workflow')
    status = workflow_tool.getInfoFor(context,'review_state')
    if status == new_state:
        return context
    wf_def = workflow_tool.getWorkflowsFor(context)[0]
    wf_id= wf_def.getId()
    state = workflow_tool.getStatusOf(wf_id,context)
    state['review_state'] = new_state
    workflow_tool.setStatusOf(wf_id, context, state.copy())
    return context

def error(licence, msg, kws):
    reference = ''
    if 'reference' in kws[0].keys():
        reference = kws[0]['reference']
    else:
        reference = licence.getReference()
    print('licence %s has the following error : %s' % (reference, msg))

def restoreWorklocations(self):
    site = self.aq_inner.aq_parent
    if self.id != 'urban' or site.getPortalTypeName() != 'Plone Site':
        raise Unauthorized, "This script must be called on urban main page"

    csvfile = site.test2
    lines = csvfile.raw.splitlines()
    mapping = []
    data_start = 1
    for headline in lines:
        headline = headline.split(';')
        if headline[0]:
            data_start = data_start+1
            if headline[0] == 'DATA':
                break
            mapping.append(headline)
    
    licence_type = mapping[0][0]
    licence_container = getattr(self, '%ss' % licence_type.lower())
    field_mapping = mapping[0]

 
