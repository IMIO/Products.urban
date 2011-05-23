def cleanArchitects():
    """
    """
    filePath="./files/architects.csv"
    outFilePath="./files/architects_splitted.csv"
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
    errors = []
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
                
        #humpfff...
        outFile.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (title, ' '.join(newname), ' '.join(firstnames), society, street, number, addresszipcode, addresscity, email, telephone, fax, nrnumber))
        i = i + 1
    file.close()
    outFile.close()
    print '\n'.join(errors)

#can be run outside Plone
if __name__ == '__main__':
    cleanArchitects()
