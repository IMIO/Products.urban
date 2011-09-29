# -*- coding: utf-8 -*-
from DateTime import DateTime
from AccessControl import Unauthorized
from Acquisition import aq_base
from zExceptions import BadRequest

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
    #get the folder where we are going the create the streets in
    streetFolder = getattr(self, 'streets')
    #first element is the city and second is the street
    #check if we need to create the city
    cityId = self.plone_utils.normalizeString(city)
    
    if not ex_streets.has_key(city):
        ex_streets[city] = {'zip':zipcode, 'streets':{}}
    #we check if the city has always the same zip
    if ex_streets[city]['zip'] != int(zipcode):
        out.append("! Current record: city '%s', zip '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, zipcode, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))
        out.append("&nbsp;&nbsp;... The existing city '%s' has zip '%s'"%(city, ex_streets[city]['zip']))
    cityTemp = cityId
    counter = 1
    while hasattr(streetFolder, cityId):
        cityId= "%s%d" %(cityTemp, counter)
        counter += 1

    #if the city still does not exist, we create it
    cityObjId = streetFolder.invokeFactory('City', id=cityId, title=city, zipCode=zipcode)
    cityObj = getattr(streetFolder, cityObjId)
    cityObj.reindexObject()

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
        if (enddate is None and bestAddresskey and bestAddresskey == streetdic['bestAddressKey']) or (enddate is not None and bestAddresskey == streetdic['bestAddressKey'] and startdate.Date() == streetdic['startDate'].Date()):
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
                out.append("! Disabled current record because historical: city '%s', name '%s', streetcode '%s', bakey '%s', regroad '%s', startdate '%s', enddate '%s'"%(city, streetname, streetcode, bestAddresskey, regionalroad, startdate, enddate))

    if create:
        streetId = streetTest = self.plone_utils.normalizeString(streetname)
        i = 0
        while hasattr(aq_base(cityObj), streetTest):
            i +=1
            out.append("info: Found existing id '%s' in entity '%s'"%(streetTest, cityObj.Title()))
            streetTest = streetId + str(i)
        streetId = streetTest
        try:
            streetObjId = cityObj.invokeFactory('Street', id=streetId, streetCode=streetcode, streetName=streetname, bestAddressKey=bestAddresskey, startDate=startdate, endDate=enddate, regionalRoad=regionalroad)
            streetObj = getattr(cityObj, streetObjId)
            #if a street has an endDate, we disable it as this should not be
            #used anymore but present for history purpose
            if disable:
                wtool.doActionFor(streetObj, 'disable')
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
        dic[loc_title] = {'zip':locality.getZipCode(), 'streets':{}}
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
