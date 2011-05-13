def cleanArchitects(self):
    """
    """
    filePath="/home/gbastien/urban/archis_mons.csv"
    outFilePath="/home/gbastien/urban/archis_mons2.csv"
    separator = ";"

    file = open(filePath, 'r')
    outFile = open(filePath, 'r')
    numberOfRecords = len(file.readlines())
    file.seek(0)
    i = 1
    errors = []
    for line in file.readlines():
        title, name, firstname, society, addressstreet, addresshousenumber, addresszipcode, addresscity, email, telephone, fax, nrnumber = line.strip().split(separator)
        #work on the address, here, the addressstreet contains informations about the addresshousnumber...
        addressInfos = addressstreet.split(',')
        street = number = ''
        if not len(addressInfos) == 2:
            errors.append("Address error line %d" % i)
        else:
            street = addressInfos[0]
            number = addressInfos[1]
        #work on the name
        #humpfff...
        outFile.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s" % title, name, firstname, society, street, number, addresszipcode, addresscity, email, telephone, fax, nrnumber
        i = i + 1
    file.close()
    outFile.close()
