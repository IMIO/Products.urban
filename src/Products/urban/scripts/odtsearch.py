#!/usr/bin/env python
# -*- coding: latin-1 -*-

import re
import os
import sys
import zipfile
import xml.dom.minidom

ALLOWED_ARCHIVE_EXTENSIONS = ('.odt')


def searchAndReplaceAllODT(file_names, find_expr, replace_expr, destination=None, dochanges=False, ignorecase=False, verbosity=0):
    """
     Search for appyPOD code pattern 'find_expr' in the 'annotations' and 'text input' zones of all the odt files 'file_names'
     Replace the matches by 'replace_expr' if 'dochanges' is True
     Create new files in folder 'destination 'rather than modify original files if 'destination' is given
    """
    args = {'files   :':file_names, 'find    :':find_expr, 'replace :':replace_expr,
            'destination :':destination, 'do changes':dochanges, 'ignore case':ignorecase, 'verbosity :':verbosity}
    if verbosity > 2:
        for k,v in args.iteritems():
            if v :
                print k, v

    result = {}
    for filename in file_names:
        searchresult = searchAndReplaceOneODT(filename=filename, find_expr=find_expr, replace_expr=replace_expr,
                                   destination=destination, dochanges=dochanges, ignorecase=ignorecase, verbosity=verbosity)
        if searchresult:
            result[filename] = searchresult
    displaySearchSummary(result, file_names, find_expr, replace_expr, verbosity)

def searchAndReplaceOneODT(filename, find_expr, replace_expr=None, destination=None, dochanges=False, ignorecase=False, verbosity=0):
    """
     Search for appyPOD code pattern 'find_expr' in the 'annotations' and 'text input' zones of odt file 'file_name'
     Replace the matches by 'replace_expr' if 'dochanges' is True
     Create a new file in folder 'destination' rather than modify the original file if 'destination' is given
    """
    zip_file = openZip(filename, 'r', verbosity)
    odt_content= None
    if zip_file:
        content_file = openOdtContent(zip_file, verbosity)
        odt_content = content_file.read()
    if odt_content:

        #search...
        xml_tree = xml.dom.minidom.parseString(odt_content)
        searchresult = searchInOneOdt(xml_tree, filename, find_expr, ignorecase, verbosity)
        #...and replace
        if dochanges:
            newcontent = getNewOdtContent(xml_tree, searchresult, replace_expr, verbosity)
            new_archive = createNewOdt(zip_file, newcontent, 'test-result.odt', verbosity)
        return searchresult

def createNewOdt(old_odt, newcontent, new_odt_name, verbosity):
    new_odt = openZip(new_odt_name, 'a', verbosity)
    for name in old_odt.namelist():
        #import pdb; pdb.set_trace()
        temp_content = old_odt.read(name)
        temp_file = open('.temp-odtsearch', 'w')
        temp_file.write(temp_content)
        temp_file.close()
        if name != 'content.xml':
            new_odt.write('.temp-odtsearch', name)
        else:
            newfile = open('.content.xml-TEMP', 'w')
            newfile.write(newcontent)
            newfile.close()
            new_odt.write('.content.xml-TEMP', 'content.xml')
            os.remove('.content.xml-TEMP')
    new_odt.close()
    os.remove('.temp-odtsearch')
    return new_odt


def getNewOdtContent( xml_tree, searchresult, replace_expr, verbosity):
    for result in searchresult:
        line = result['XMLnode'].data
        replaced = []
        start = 0
        end = 0
        for match in result['matches']:
            end = match['start']
            replaced.append(line[start:end])
            replaced.append(replace_expr)
            start = match['end']
        replaced.append(line[start:])
        replaced = ''.join(replaced)
        result['XMLnode'].data = replaced
    return xml_tree.toxml('utf-8')

def searchInOneOdt(xml_tree, filename, find_expr, ignorecase, verbosity):
    if verbosity > 2:
        print "searching text content of '%s'" % filename
    #the two xml tags we want to browse are 'office:annotation' and 'text:text-input', since its the only place
    #where appyPOD code can be written
    result = []
    firstfound = True
    annotations = [node.getElementsByTagName('text:p') for node in xml_tree.getElementsByTagName('office:annotation')]
    result = searchInTextElements(elements=annotations, filename=filename, element_type='commentaire',
                                        find_expr=find_expr, ignorecase=ignorecase, verbosity=verbosity)
    if result:
        firstfound = False
    expressions = xml_tree.getElementsByTagName('text:text-input')
    result.extend(searchInTextElements(elements=expressions, filename=filename, element_type='champ de saisie',
                                        find_expr=find_expr, firstfound=firstfound, ignorecase=ignorecase, verbosity=verbosity))
    return result


def searchInTextElements(elements, filename, element_type, find_expr, verbosity=0, ignorecase=False, firstfound=True):
    text_lines = []
    node_groups = [reachTextNodeLevel(element) for element in elements]
    i = 1
    for node_group in node_groups:
        for node in node_group:
            if node.nodeType == node.TEXT_NODE:
                text = node.data
                for expr in find_expr:
                    matches = re.finditer(expr, text)
                    match_indexes = [{'start':match.start(), 'end':match.end()} for match in matches]
                    if match_indexes:
                        if firstfound:
                            firstfound = False
                            if verbosity >= 0:
                                print filename
                        text_lines.append({'expr':expr, 'matches':match_indexes, 'XMLnode':node})
                        if verbosity >= 0:
                            for match in match_indexes:
                                printMatch(text,  match['start'], match['end'], find_expr, '%s %i' % (element_type, i), verbosity)
        i = i+1
    return text_lines

def printMatch(text, start, end, find_expr, textzone, verbosity):
    display_line = ['','','']
    d_start = 0
    if verbosity < 2 and start> 100:
        d_start = start-100
        display_line[0] = '...'
    d_end = len(text)
    if verbosity < 2 and end+100 < len(text):
        d_end = end+100
        display_line[2] = '...'
    if sys.stdout.isatty():
        text = '%s\033[93m%s\033[0m%s' % (text[d_start:start], text[start:end], text[end:d_end])
    else:
        text = text[d_start:d_end]
    display_line[1] = text
    display_line = ''.join(display_line)
    if len(find_expr) > 1:
        print "  %s : %s > %s" % (textzone, text, display_line)
    else:
        print "  %s : %s" % (textzone, display_line)

def reachTextNodeLevel(node):
    def recursiveReachTextNodeLevel(node, result):
        if hasattr(node, '__iter__'):
            for list_element in node:
                recursiveReachTextNodeLevel(list_element, result)
        elif node.nodeType == node.TEXT_NODE:
            result.append(node)
        else :
            recursiveReachTextNodeLevel(node.childNodes, result)
        return result
    return recursiveReachTextNodeLevel(node, [])

def openZip(filename, mode, verbosity):
    if verbosity > 2:
        print "opening archive file '%s'" % filename
    try:
        zip_file = zipfile.ZipFile(filename, mode)
    except zipfile.BadZipfile as wrongzipfile:
        print "!!! could not open '%s' : %s" % (filename, wrongzipfile)
        return None
    else:
        return zip_file

def openOdtContent(zip_file, verbosity):
    if verbosity > 2:
        print "opening text content of '%s'" % zip_file.filename
    try:
        odt_content = zip_file.open('content.xml')
    except KeyError as nocontent:
        print "!!! could not read the content of %s : s%" % (zip_file.filename, nocontent)
        return None
    else:
        return odt_content

def displaySearchSummary(searchresult, file_names, find_expr, replace_expr, verbosity):
    out = []
    total_matches = 0
    if verbosity or len(searchresult) > 1:
        out.append("%i file" % len(searchresult))
        if len(searchresult) > 1:
            out.append('s')
    if verbosity:
        result_filenames = searchresult.keys()
        result_filenames.sort()
        per_file_detail = []
        for filename in result_filenames:
            nbr_matches = 0
            detail = "%s" % filename
            result = searchresult[filename]
            for subresult in result:
                total_matches = total_matches + len(subresult['matches'])
                nbr_matches = nbr_matches + len(subresult['matches'])
            detail = "%s : %i match" % (detail, nbr_matches)
            if nbr_matches > 1:
                detail ="%ses" %detail
            per_file_detail.append(detail)
        out.append(" : \n%s\n" % '\n'.join(per_file_detail))
    elif len(searchresult) > 1:
        out.append(', ')
    if not verbosity:
        for fileresults in searchresult.values():
            for fileresult in fileresults:
                total_matches= total_matches + len(fileresult['matches'])
    out.append("%i matches" % total_matches)

    print(''.join(out))


################################################################
#parsing arguments code
################################################################

