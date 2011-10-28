# -*- coding: utf-8 -*-
from Products.urban.exportimport import addUrbanEventTypes
from Products.urban.exportimport import addGlobalTemplates

def updateAllUrbanTemplates(context):
    if context.readDataFile('urban_mons_marker.txt') is None:
        return
    addGlobalTemplates(context)
    addUrbanEventTypes(context)

def cleanArchitects(self):
    """
    """

    filePath="/home/srv/zinstances/urban335/src/Products.urban/src/Products/urban/profiles/mons/files/architects_orig.csv"
    outFilePath="/home/srv/zinstances/urban335/src/Products.urban/src/Products/urban/profiles/mons/files/architects.csv"
    separator = ";"

    def isFirstnameFormat(thename):
        #compound name
        if thename.find('-') >= 0:
            for apart in thename.split('-'):
                if not isFirstnameFormat(apart):
                    return False
            #All parts are formatted as firstname
            return True
        #simple name
        if thename[0:1].isupper() and thename[1:-1].islower():
            return True
        return False
    file = open(filePath, 'r')
    outFile = open(outFilePath, 'w')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    outFile.write('"startpoint";"replicata_export_date";"parent";"id";"type";"personTitle";"name1";"name2";"society";"street";"number";"zipcode";"city";"email";"phone";"fax";"nationalRegister"\n')
    outFile.write('"Start point";"Export date";"Parent folder";"Identifier";"Content type";"Titre";"Nom";"Prénom";"Société";"Rue";"Numéro";"Code postal";"Localité";"Email";"Téléphone";"Fax";"Numéro de registre national"\n')
    errors = []
    ids = {}
    for line in file.readlines():
        title, name, firstname, society, addressstreet, addresshousenumber, addresszipcode, addresscity, email, telephone, fax, nrnumber = line.strip().split(separator)
        #work on the address, here, the addressstreet contains informations about the addresshousnumber...
        addressInfos = addressstreet.split(',')
        street = number = ''
        if not addressstreet.strip():
            pass
        elif not len(addressInfos) == 2:
            #errors.append("Address error line %d" % i)
            pass #errors now checked
        else:
            street = addressInfos[0].strip()
#            street = addressstreet
            number = addressInfos[1].strip()
        #work on the name
        firstnames = []
        newname = []
        for part in name.split():
            if isFirstnameFormat(part):
                firstnames.append(part)
            else:
                newname.append(part)
        firstnames = ' '.join(firstnames)
        newname = ' '.join(newname)
        gid = self.plone_utils.normalizeString(str("%s %s"%(newname, firstnames)).lower())
        if ids.has_key(gid):
            errors.append("id '%s' already exists for architect '%s'"%(gid, ids[gid]))
        else:
            ids[gid] = "%s %s"%(newname, firstnames)
        outFile.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (';;', gid, 'Architect', title, newname, firstnames, society, street, number, addresszipcode, addresscity, email, telephone, fax, nrnumber))
        i = i + 1
    file.close()
    outFile.close()
    print '\n'.join(errors)
