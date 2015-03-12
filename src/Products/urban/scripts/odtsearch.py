#!/usr/bin/env python
# -*- coding: latin-1 -*-

import re
import os
import sys
import zipfile
import mimetypes
import xml.dom.minidom

ALLOWED_ARCHIVE_EXTENSIONS = ('.odt')

verbosity = 0


def searchODTs(filenames, findexpr, replace, destination='tmp', ignorecase=False, recursive=False):
    """
     Search for appyPOD code pattern 'findexpr' in the 'annotations' and 'text input' zones of all the odt files 'filenames'
     Replace the matches by 'replace' if 'dochanges' is True
     Create new files in folder 'destination 'rather than modify original files if 'destination' is given
    """

    result = {}
    search_args = {
        'findexpr': findexpr,
        'ignorecase': ignorecase,
    }
    if replace:
        new_searchargs = {
            'replace_expr': replace,
            'destination': destination,
        }
        search_args.update(new_searchargs)

    if verbosity > 2:
        for k, v in search_args.iteritems():
            if v:
                print k, v

    if replace:
        if recursive:
            recursiveSearchAndReplaceAllODT(filenames, result, search_args)
        else:
            searchAndReplaceAllODT(filenames, result, search_args)
    else:
        if recursive:
            recursiveSearchAllODT(filenames, result, search_args)
        else:
            searchAllODT(filenames, result, search_args)

    displaySearchSummary(result, filenames, findexpr, replace)


def recursiveSearchAndReplaceAllODT(filenames, result, search_args):
    """  recursive call of the search over file folders """

    odt_files, directories = separateDirectoryAndODTfilenames(filenames)

    searchAndReplaceInODTFiles(odt_files, result, search_args)

    for directory in directories:
        files = getFilesOfDirectory(directory)
        recursiveSearchAndReplaceAllODT(files, result, search_args)


def searchAndReplaceAllODT(filenames, result, search_args):
    """
     recursive call of the search over file folders
    """
    odt_files, directories = separateDirectoryAndODTfilenames(filenames)
    searchAndReplaceAllODT(odt_files, result, search_args)

    for directory in directories:
        searchAndReplaceODTFilesOfDirectory(directory, result, search_args)


def recursiveSearchAllODT(filenames, result, search_args):
    """ Search pattern 'findexpr' in odt files matching each regex path/name in 'filenames' """

    odt_files, directories = separateDirectoryAndODTfilenames(filenames)

    searchInODTFiles(odt_files, result, search_args)

    for directory in directories:
        files = getFilesOfDirectory(directory)
        recursiveSearchAllODT(files, result, search_args)


def searchAllODT(filenames, result, search_args):
    """ Search pattern 'findexpr' in odt files matching each regex path/name in 'filenames' """

    odt_files, directories = separateDirectoryAndODTfilenames(filenames)
    searchInODTFiles(odt_files, result, search_args)

    for directory in directories:
        searchODTFilesOfDirectory(directory, result, search_args)


def searchAndReplaceODTFilesOfDirectory(directory, result, search_args):
    odt_files = getODTFilesOfDirectory(directory)
    searchAndReplaceInODTFiles(odt_files, result, search_args)


def searchODTFilesOfDirectory(directory, result, search_args):
    odt_files = getODTFilesOfDirectory(directory)
    searchInODTFiles(odt_files, result, search_args)


def searchAndReplaceInODTFiles(odt_files, result, search_args):
    for odt_file in odt_files:
        searchresult = searchAndReplaceOneODT(odt_file, **search_args)
        if searchresult:
            result[odt_file] = searchresult


def searchInODTFiles(odt_files, result, search_args):
    for odt_file in odt_files:
        xml_tree, searchresult = searchOneODT(odt_file, **search_args)
        if searchresult:
            result[odt_file] = searchresult


def searchOneODT(filename, findexpr, ignorecase=False):
    """
     Search for appyPOD code pattern 'findexpr' in the 'annotations' and 'text input' zones of odt file 'file_name'
    """
    zip_file = openZip(filename, 'r')
    odt_content = None
    if zip_file:
        content_file = openOdtContent(zip_file)
        odt_content = content_file.read()
        zip_file.close()

    if odt_content:
        #search...
        xml_tree = xml.dom.minidom.parseString(odt_content)
        searchresult = searchInOneOdt(xml_tree, filename, findexpr, ignorecase)

        return xml_tree, searchresult


def searchAndReplaceOneODT(filename, findexpr, replace_expr=None, destination=None, ignorecase=False):
    """
     Search for appyPOD code pattern 'findexpr' in the 'annotations' and 'text input' zones of odt file 'file_name'
     Replace the matches by 'replace_expr'
     Create a new file in folder 'destination' rather than modify the original file if 'destination' is given
    """

    zip_file = openZip(filename, 'r')
    xml_tree, searchresult = searchOneODT(filename, findexpr, ignorecase)

    if searchresult:
        newcontent = getNewOdtContent(xml_tree, searchresult, replace_expr)
        createNewOdt(zip_file, newcontent, filename, destination)

    zip_file.close()
    return searchresult


def createNewOdt(old_odt, newcontent, new_odt_name, destination_folder):
    new_odt = openZip(new_odt_name, 'a')
    for name in old_odt.namelist():
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


def getNewOdtContent(xml_tree, searchresult, replace_expr):
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


def searchInOneOdt(xml_tree, filename, findexpr, ignorecase=False):
    if verbosity > 2:
        print "searching text content of '%s'" % filename
    #the two xml tags we want to browse are 'office:annotation' and 'text:text-input', since its the only place
    #where appyPOD code can be written
    result = []
    firstfound = True
    annotations = [node.getElementsByTagName('text:p') for node in xml_tree.getElementsByTagName('office:annotation')]

    result = searchInTextElements(
        elements=annotations,
        filename=filename,
        element_type='commentaire',
        findexpr=findexpr,
        ignorecase=ignorecase
    )
    if result:
        firstfound = False
    expressions = xml_tree.getElementsByTagName('text:text-input')
    result.extend(
        searchInTextElements(
            elements=expressions,
            filename=filename,
            element_type='champ de saisie',
            findexpr=findexpr,
            firstfound=firstfound,
            ignorecase=ignorecase
        )
    )
    return result


def searchInTextElements(elements, filename, element_type, findexpr, firstfound=True, ignorecase=False):
    text_lines = []
    node_groups = [reachTextNodeLevel(element) for element in elements]
    flags = ignorecase and re.I or 0
    i = 1
    for node_group in node_groups:
        for node in node_group:
            if node.nodeType == node.TEXT_NODE:
                text = node.data
                for expr in findexpr:
                    matches = re.finditer(expr, text, flags=flags)
                    match_indexes = [{'start':match.start(), 'end':match.end()} for match in matches]
                    if match_indexes:
                        if firstfound:
                            firstfound = False
                            if verbosity >= 0:
                                print filename
                        text_lines.append({'expr': expr, 'matches': match_indexes, 'XMLnode': node})
                        if verbosity >= 0:
                            for match in match_indexes:
                                printMatch(text,  match['start'], match['end'], findexpr, '%s %i' % (element_type, i))
        i = i + 1
    return text_lines


def directoryPath(directory_name):
    if not directory_name.endswith('/'):
        directory_name = '{}/'.format(directory_name)
    return directory_name


def separateDirectoryAndODTfilenames(filenames):
    odt_files = []
    directories = []

    for filename in filenames:
        if isDirectory(filename):
            directories.append(directoryPath(filename))
        elif isODTFile(filename):
            odt_files.append(filename)

    return odt_files, directories


def getODTFilesOfDirectory(directory):
    odt_files = [directory + filename for filename in os.listdir(directory) if isODTFile(filename)]
    return odt_files


def getFilesOfDirectory(directory):
    filenames = [directory + filename for filename in os.listdir(directory)]
    return filenames


def isODTFile(filename):
    return mimetypes.guess_type(filename)[0] == 'application/vnd.oasis.opendocument.text'


def isDirectory(filename):
    return os.path.isdir(filename)


def printMatch(text, start, end, findexpr, textzone):
    display_line = ['', '', '']
    d_start = 0
    if verbosity < 2 and start > 100:
        d_start = start - 100
        display_line[0] = '...'
    d_end = len(text)
    if verbosity < 2 and end + 100 < len(text):
        d_end = end + 100
        display_line[2] = '...'
    if sys.stdout.isatty():
        text = '%s\033[93m%s\033[0m%s' % (text[d_start:start], text[start:end], text[end:d_end])
    else:
        text = text[d_start:d_end]
    display_line[1] = text
    display_line = ''.join(display_line)
    if len(findexpr) > 1:
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
        else:
            recursiveReachTextNodeLevel(node.childNodes, result)
        return result
    return recursiveReachTextNodeLevel(node, [])


def openZip(filename, mode):
    if verbosity > 2:
        print "opening archive file '%s'" % filename
    try:
        zip_file = zipfile.ZipFile(filename, mode)
    except zipfile.BadZipfile as wrongzipfile:
        print "!!! could not open '%s' : %s" % (filename, wrongzipfile)
        return None
    else:
        return zip_file


def openOdtContent(zip_file):
    if verbosity > 2:
        print "opening text content of '%s'" % zip_file.filename
    try:
        odt_content = zip_file.open('content.xml')
    except KeyError as nocontent:
        print "!!! could not read the content of %s : s%" % (zip_file.filename, nocontent)
        return None
    else:
        return odt_content


def displaySearchSummary(searchresult, filenames, findexpr, replace_expr):
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
                detail = "%ses" % detail
            per_file_detail.append(detail)
        out.append(" : \n%s\n" % '\n'.join(per_file_detail))
    elif len(searchresult) > 1:
        out.append(', ')
    if not verbosity:
        for fileresults in searchresult.values():
            for fileresult in fileresults:
                total_matches = total_matches + len(fileresult['matches'])
    out.append("%i matches" % total_matches)

    print(''.join(out))


################################################################
#parsing arguments code
################################################################
req_version = (2, 7)
cur_version = sys.version_info

if cur_version >= req_version:
    import argparse

    def parseArguments():
        parser = argparse.ArgumentParser(description='Search and replace in comments and input fields of .odt files')
        parser.add_argument('findexpr', action='append')
        parser.add_argument('--replace')
        parser.add_argument('-i', '--ignorecase', action='store_true')
        parser.add_argument('-r', '--recursive', action='store_true')
        parser.add_argument('filenames', nargs='+')
        return parser.parse_args()

    def main():
        arguments = parseArguments()
        arguments = vars(arguments)
        searchODTs(**arguments)

    if __name__ == "__main__":
        main()
