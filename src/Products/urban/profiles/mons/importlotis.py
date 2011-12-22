#!/usr/bin/env python
# -*- coding: latin-1 -*-

from re import search
from re import findall
from re import finditer
from re import IGNORECASE
import csv

def main():
    mergeMultilinesData("lotissements_raw.csv", "mergedlines.csv")
    fillData("mergedlines.csv", "lotissements_final.csv")

def fillData(input_filename, output_filename):
    input_file = file(input_filename)
    output_file = open(output_filename, 'w')
    out = csv.writer(output_file, delimiter=';', quotechar='"')
    i = 0
    for line in csv.reader(input_file, delimiter=';', quotechar='"'):
        #import pdb; pdb.set_trace()
        if i > 0:
            output_file.write('\n')
        newline = ['' for dummy in range(13)]  
        if i > 1 :
            newline[0] = line[0]
            newline[1] = line[1]
            newline[2] = line[2]
            newline[3] = 'lot%i' % i
            newline[4] = line[4]
            newline[5] = line[5]
            label = '%s' % line[6]
            for x in range(13)[7:]:
                if x == 10:
                    label = '%s ref:' % label
                if line[x]:
                    if label:
                        label = '%s %s' % (label, line[x])
                    else:
                        label = '%s' % line[x]
            newline[6] = label
            newline[7] = formatNames(line[13])
            date = formatDates(line[15])
            newline[9] = '%s 00:00:00' % date
            newline[10] = line[16]
            newline[11] = line[17]
            newline[12] = line[18]
        else:
            newline = [part for part in line if part]
        newline = ['"%s"' % string for string in newline]
        output_file.write(';'.join(newline))
        i = i+1
    output_file.close()


def formatNames(written_name):
    match = search("(?:d(?:é|e)livr(?:é|e)(?:\s?:\s?)?)(.*)(?:\s+mandaté(?:\s?:\s?)?)(.*)", written_name, flags=IGNORECASE)
    if match:
        return "%s (mandaté : %s)" %(match.group(1), match.group(2))
    match = search("(?:d(?:é|e)livr(?:é|e)(?:\s?:\s?)?)(.*)", written_name, flags=IGNORECASE)
    if match:
        return match.group(1)
    return written_name


def formatDates(written_date):
    months = {
              "Janvier":"01", "Février":"02", "Mars":"03", "Avril":"04", 
              "Mai":"05", "Juin":"06", "Juillet":"07", "Aout":"08", "Août":"08", 
              "Septembre":"09", "Octobre":"10", "Novembre":"11", "Décembre":"12",
              None:"None"
             }

    clean_dates = []
    #import pdb; pdb.set_trace()
    clean_dates = [uniformizeDate(match) for match in findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}', written_date)]

    matches = finditer( 
        "(?:([0-9]{1,2})\s*)?(?:\s*(janvier|février|mars|avril|mai|juin|juillet|aout|août|septembre|octobre|novembre|décembre))?(?:/|\s+|\()([0-9]{4})",
              written_date, 
              flags=IGNORECASE
                  )
    for match in matches:
        key = None
        if match.group(2):
            key = match.group(2).capitalize()
        date = "%s/%s/%s" % (match.group(1), months[key], match.group(3))
        date = uniformizeDate(date)
        clean_dates.append(date)
    
    date = ""
    if search('avant', written_date, flags=IGNORECASE):
        #import pdb; pdb.set_trace()
        date = oldestDate(clean_dates)
    else:
        date = mostRecentDate(clean_dates)
    return date 

def uniformizeDate(date):
    split = date.split('/')
    newdate = []
    for i in range(3):
        part = split[i]
        if part == 'None':
            part = '01'
        if len(part) == 1:
            part = '0%s' % part
        if i == 2 and len(part) == 2:
            part = '19%s' % part
        newdate.append(part)
    return '/'.join(newdate)

def mostRecentDate(dates):
    mostrecent_date = ""
    if len(dates):
        mostrecent_date = reverseDate(dates[0])
    for date in dates:
        date = reverseDate(date)
        if date > mostrecent_date:
            mostrecent_date = date
    return reverseDate(mostrecent_date)

def oldestDate(dates):
    oldest_date = ""
    if len(dates):
        oldest_date = reverseDate(dates[0])
    for date in dates:
        date = reverseDate(date)
        if date < oldest_date:
            oldest_date = date
    return reverseDate(oldest_date)

def reverseDate(date):
    newdate = date.split('/')
    newdate.reverse()
    return '/'.join(newdate)

def mergeMultilinesData(input_filename, output_filename):
    input_file = file(input_filename)
    out = file(output_filename, 'w')
    i = 0
    concatenate = False
    for line in input_file.readlines():
        if i > 1:
            if line == '\n':
                concatenate = True
            elif concatenate:
                out.write(' ')
                out.write(line.rstrip('\n'))
                concatenate = False
            elif not concatenate:
                out.write('\n')
                out.write(line.rstrip('\n'))
        else:
            if i == 0:
                out.write(line)
            elif i == 1:
                out.write(line.rstrip('\n'))
        i = i+1
    out.close()


if __name__ == "__main__":
    main()
