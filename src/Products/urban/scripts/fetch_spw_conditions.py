# -*- coding: utf-8 -*-

"""
One-off script to fetch, for every rubric in `Rubriques_PE.xml`, the
sectoral/integral exploitation conditions ("legislation") linked to it by
the SPW permis-environnement site.

"""

import io
import json
import sys
import time
import urllib2

from parse_spw_rubrics import parse_rubrics
from parse_spw_rubrics import safe_id


ENDPOINT = (
    "https://permis-environnement.spw.wallonie.be/home/fiche-rubrique/"
    "area-detail-rubric/detail-dune-rubrique.getRubric.do"
    "?legalText=true&rubricId={identifier}"
)


def fetch_legal_conditions(identifier, retries=3, pause=0.3):
    """Return the `legal` list for one rubric identifier, or [] on failure."""
    url = ENDPOINT.format(identifier=identifier)
    request = urllib2.Request(
        url,
        headers={
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": (
                "https://permis-environnement.spw.wallonie.be/home/"
                "fiche-rubrique.html?rubricId={0}".format(identifier)
            ),
        },
    )
    for attempt in range(retries):
        try:
            response = urllib2.urlopen(request, timeout=10)
            payload = json.load(response)
            return payload.get("legal", [])
        except Exception as exc:
            if attempt == retries - 1:
                sys.stderr.write(
                    "WARNING: failed to fetch conditions for rubricId=%s: %s\n"
                    % (identifier, exc)
                )
                return []
            time.sleep(pause)


def condition_id_from_url(url):
    """Build a stable, Zope-safe id from a condition's legal text url.
    """
    if not url:
        return None
    if "?" in url:
        condition_id = safe_id(url)
    else:
        last_segment = url.rstrip("/").split("/")[-1]
        condition_id = safe_id(last_segment) or safe_id(url)
    return condition_id or None


def build_mapping_and_conditions(xml_path):
    """Return (mapping, conditions):
    - mapping: {rubric_code: [{"type": codeType, "id": condition_id}, ...]}
    - conditions: {codeType: {condition_id: {id, title, url, codeType}}}
    """
    rubrics = parse_rubrics(xml_path)

    mapping = {}
    conditions = {}

    total = len(rubrics)
    for i, rubric in enumerate(rubrics):
        rubric_code = rubric["number"]
        legal_entries = fetch_legal_conditions(rubric["identifier"])

        to_map = []
        for entry in legal_entries:
            code_type = entry.get("codeType") or "autre"
            url = entry.get("url") or ""
            condition_id = condition_id_from_url(url)
            if not condition_id:
                continue

            conditions.setdefault(code_type, {})
            if condition_id not in conditions[code_type]:
                conditions[code_type][condition_id] = {
                    "id": condition_id,
                    "title": entry.get("referenceTextFr") or condition_id,
                    "url": url,
                    "codeType": code_type,
                }

            to_map.append({"type": code_type, "id": condition_id})

        if to_map:
            mapping[rubric_code] = to_map

        if (i + 1) % 50 == 0 or (i + 1) == total:
            sys.stderr.write("... %s/%s rubrics processed\n" % (i + 1, total))

    return mapping, conditions


def main():
    if len(sys.argv) != 3:
        sys.stderr.write(
            "usage: python fetch_spw_conditions.py <Rubriques_PE.xml> <output.json>\n"
        )
        sys.exit(1)

    xml_path, output_path = sys.argv[1], sys.argv[2]
    mapping, conditions = build_mapping_and_conditions(xml_path)

    result = {"mapping": mapping, "conditions": conditions}

    dumped = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)
    if isinstance(dumped, str):
        dumped = dumped.decode("utf-8")
    with io.open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write(dumped)

    total_conditions = sum(len(by_id) for by_id in conditions.values())
    sys.stderr.write(
        "Done: %s rubrics mapped to %s distinct conditions, written to %s\n"
        % (len(mapping), total_conditions, output_path)
    )


if __name__ == "__main__":
    main()
