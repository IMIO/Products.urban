# -*- coding: utf-8 -*-

"""
Replacement for slurp.extractRubricsFolders / extractRubricsTerm.

Parses the reference rubric list provided by the SPW (as used by
NOTICe/Twice) directly from its XML SOAP export (searchRubricResponse).
`parse_rubrics(xml_path)` is meant to be imported and called at migration
time (see Products.urban.migration.update_290.import_spw_rubrics) -- there
is no intermediate JSON file, the XML stays the single source of truth.

The XML only contains the rubrics themselves (no parent category nodes,
no I/S conditions/arrete links -- see fetch_spw_conditions.py for that
part), and sometimes several historical versions of the same rubric code
(distinguished by validityPeriod/endDate): only the currently valid
version of each code is kept.
"""

import re
import xml.etree.ElementTree as ET


NS = {
    'ns4': 'http://soa.spw.wallonie.be/data/common/code/v5',
    'ns5': 'http://soa.spw.wallonie.be/data/business/specific/twice/environmentalLicence/v3',
    'ns6': 'http://soa.spw.wallonie.be/data/common/date/v1',
}


def safe_id(code):
    """Archetypes/Zope object ids only allow letters, digits, '_', '-', '.'."""
    sid = re.sub(r'[^A-Za-z0-9_.\-]+', '_', code)
    return sid.strip('_')


def _text(el, path):
    found = el.find(path, NS)
    return found.text if found is not None else None


def _code(el, path):
    found = el.find(path, NS)
    if found is None:
        return None
    return _text(found, 'ns4:code')


def parse_rubrics(xml_path):
    """Parse the SPW rubric XML export and return a flat list of dicts:
    {id, identifier, category_id, number, extraValue, description}
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rubrics = {}
    for r in root.iter('{%s}rubric' % NS['ns5']):
        identifier = _text(r, 'ns5:identifier')
        rubrics[identifier] = {
            'identifier': identifier,
            'code': _text(r, 'ns5:code'),
            'label': _text(r, 'ns5:label'),
            'completeLabel': _text(r, 'ns5:completeLabel'),
            'officialLabel': _text(r, 'ns5:officialLabel'),
            'classe': _code(r, 'ns5:classe'),
            'beginDate': _text(r, 'ns5:validityPeriod/ns6:beginDate'),
            'endDate': _text(r, 'ns5:validityPeriod/ns6:endDate'),
        }
    by_code = {}
    for r in rubrics.values():
        code = r['code']
        if not code:
            continue
        current = by_code.get(code)
        if current is None:
            by_code[code] = r
            continue
        r_active = r['endDate'] is None
        current_active = current['endDate'] is None
        if r_active and not current_active:
            by_code[code] = r
        elif r_active == current_active and (r['beginDate'] or '') > (current['beginDate'] or ''):
            by_code[code] = r

    out = []
    for code, r in by_code.items():
        if not re.match(r'^[A-Za-z0-9_.\-]+$', code):
            continue
        observation = r['completeLabel'] or r['label'] or r['officialLabel'] or ''
        out.append({
            'id': safe_id(code),
            'identifier': r['identifier'],
            'category_id': safe_id(code.split('.')[0]),
            'number': code,
            'extraValue': r['classe'] or 0,
            'description': observation,
            'exploitationCondition':[],
            'endValidity':r['endDate'],
            'startValidity':r['beginDate'],

        })

    return out
