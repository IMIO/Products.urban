#!/usr/bin/env python

"""
    call this script to return 4 dictionaries containing:
    - all rubrics big categories along with a textual description
    - all environemnt rubrics, sort
    - all integral and sectorial conditions bound to these rubrics, sorted by type
    - a dictionnary representing the mapping bewteen the rubrics and conditions
"""

import urllib2
import re
import pickle
import bs4


def getRubricsHTMLpages(rubric_ids):
    base_url = 'http://environnement.wallonie.be/cgi/dgrne/aerw/pe/rubri/chx_rub_liste.idc?d12='
    rubrics_html = [urllib2.urlopen('%s%s' % (base_url, rubric_id)).read() for rubric_id in rubric_ids]
    return rubrics_html


def extractRubricsTerm(rubric_ids):
    print 'slurping rubrics...'

    html_pages = getRubricsHTMLpages(rubric_ids)

    rubrics = {}

    for html_page in html_pages:
        body = re.search('\<body.*\</body>', html_page, re.IGNORECASE + re.DOTALL)
        rubrics_soup = bs4.BeautifulSoup(body.group(), from_encoding="iso-8859-1")
        table = rubrics_soup.find_all('table')[-1]
        rows = table.find_all('tr')[1:]
        for row in rows:
            rubric = extractOneRubricTerm(row)
            rubrics[rubric['id']] = rubric

    return rubrics


def extractOneRubricTerm(row):
    columns = row.find_all('td')

    number = columns[1].text
    extraValue = columns[2].text
    description = columns[3].text
    condition_type = columns[4].text.strip()
    condition_id = columns[4].find('a') and columns[4].a.attrs['href'].split('=')[-1] or None
    # use next line if we need to extract more information on the html page of the rubric
    # specificpage_link = columns[0].a.attrs['href']

    rubric = {
        'id': number,
        'number': number,
        'extraValue': extraValue,
        'description': description,
        'condition_type': condition_type,
        'condition_id': condition_id,
    }
    return rubric


def extractRubricsFolders():
    print 'slurping main rubric categories...'

    rubriques_url = 'http://environnement.wallonie.be/cgi/dgrne/aerw/pe/rubri/chx_rub_intro.idc'
    rubriques_html = urllib2.urlopen(rubriques_url)
    rubriques_html = rubriques_html.read()

    form = re.search('\<form.*\</form>', rubriques_html, re.IGNORECASE + re.DOTALL)
    form = form.group()

    rubrics_soup = bs4.BeautifulSoup(form)

    options = rubrics_soup.form.find_all('option')
    folders = [{'id': opt.attrs['value'], 'title': opt.text} for opt in options]

    return folders


def extractCondition(rubric, condition_id, condition_type):

    if not condition_id or condition_type == 'Non':
        return

    condition_soup = getConditionSoup(condition_id)

    title = extractConditionTitle(condition_soup)
    description = extractConditionIntegraltext(condition_soup)

    condition = {
        'id': condition_id,
        'title': title,
        'description': description,
    }

    return condition


def extractConditionTitle(condition_soup):
    table = condition_soup.find_all('table')[1]
    title = table.find_all('tr')[1].b.text

    return title


def extractConditionIntegraltext(condition_soup):
    table = condition_soup.find_all('table')[1]
    # sometimes the link to the full text is not available...
    try:
        fulltext_link = table.find_all('tr')[3].a.attrs['href']
    except:
        return ''
    fulltext_page = urllib2.urlopen(fulltext_link).read()
    body = re.search('\<body.*\</body>', fulltext_page, re.IGNORECASE + re.DOTALL)

    fulltext = bs4.BeautifulSoup(body.group(), from_encoding="iso-8859-1")
    fulltext = str(fulltext)

    return fulltext


def getConditionSoup(condition_id):
    base_url = 'http://environnement.wallonie.be/cgi/dgrne/aerw/pe/rubri/condex.idc?Condexpl_id='
    condition_page = urllib2.urlopen('%s%s' % (base_url, condition_id)).read()
    body = re.search('\<body.*\</body>', condition_page, re.IGNORECASE + re.DOTALL)

    condition_soup = bs4.BeautifulSoup(body.group())

    return condition_soup


def buildMappingAndExtractAllConditions(rubric_terms):
    print 'slurping integral and sectorial conditions...'

    mapping = {}
    conditions = {'CI': {}, 'CS': {}, 'CS-Eau': {}, 'CI/CS': {}}

    for rubric_id, rubric in rubric_terms.iteritems():
        condition_id = rubric.pop('condition_id')
        condition_type = rubric.pop('condition_type')
        # no conditions associated to the rubric
        if not condition_id:
            condition = None
        # this condition has already been extracted from the site
        elif condition_id in conditions[condition_type]:
            condition = conditions[condition_type][condition_id]
        # new condition to extract !
        else:
            condition = extractCondition(rubric, condition_id, condition_type)
            conditions[condition_type][condition_id] = condition

        to_map = condition_type != u'Non' and {'type': condition_type, 'id': condition_id} or None
        mapping[rubric_id] = to_map

    return conditions, mapping


def pickleResult(slurped):
    """ save the result on the file system """

    slurp_filename = 'slurped_dgrne.pickle'
    dgrne_slurp = open(slurp_filename, 'w')
    pickle.dump(slurped, dgrne_slurp)

    print 'pickled result in %s' % slurp_filename


def slurp():
    """ """
    # will be used to create config folders for Rubrics
    main_rubrics = extractRubricsFolders()

    # now get the rubric terms
    rubric_ids = [rubric['id'] for rubric in main_rubrics]
    rubric_terms = extractRubricsTerm(rubric_ids)

    # get the ci/ca and the mapping between rubrics and conditions
    mapping, conditions = buildMappingAndExtractAllConditions(rubric_terms)

    print 'slurping done!'

    slurped = {
        'main_rubrics': main_rubrics,
        'rubric_terms': rubric_terms,
        'conditions': conditions,
        'mapping': mapping,
    }

    pickleResult(slurped)


def main():
    slurp()

if __name__ == "__main__":
    main()
