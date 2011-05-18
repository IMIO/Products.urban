def cleanArchitects():
    """
    """
#    filePath="/home/gbastien/urban/archis_mons.csv"
    filePath="./files/architects.csv"
#    outFilePath="/home/gbastien/urban/archis_mons2.csv"
    outFilePath="./archis_mons2.csv"
    separator = ";"

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
            errors.append("Address error line %d" % i)
        else:
            street = addressInfos[0].strip()
#            street = addressstreet
            number = addressInfos[1].strip()
        #work on the name
        #humpfff...
        outFile.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (title, name, firstname, society, street, number, addresszipcode, addresscity, email, telephone, fax, nrnumber))
        i = i + 1
    file.close()
    outFile.close()
    print '\n'.join(errors)

if __name__ == '__main__':
    cleanArchitects()
