# -*- coding: utf-8 -*-

from Products.urban import UrbanMessage as _
from StringIO import StringIO
from datetime import datetime
from DateTime import DateTime

import csv
import re
import unicodedata
import logging

claimants_csv_fieldnames = [
    "personTitle",
    "name1",
    "name2",
    "society",
    "street",
    "number",
    "zipcode",
    "city",
    "country",
    "email",
    "phone",
    "gsm",
    "nationalRegister",
    "claimType",
    "hasPetition",
    "outOfTime",
    "claimDate",
    "claimingText",
    "wantDecisionCopy",
]

CLAIMANT_HEADER_LABELS = [
    ("personTitle", u"Titre (sel.)"),
    ("name1", u"Nom"),
    ("name2", u"Prénom"),
    ("society", u"Société"),
    ("street", u"Rue"),
    ("number", u"N° de police"),
    ("zipcode", u"Code postal (num.)"),
    ("city", u"Localité"),
    ("country", u"Pays (sel.)"),
    ("email", u"E-mail"),
    ("phone", u"Téléphone"),
    ("gsm", u"GSM"),
    ("nationalRegister", u"N° registre national"),
    ("claimType", u"Type de réclamation"),
    ("hasPetition", u"Pétition"),
    ("outOfTime", u"Hors délai"),
    ("claimDate", u"Date de réception"),
    ("claimingText", u"Texte de la réclamation"),
    ("wantDecisionCopy", u"Souhaite une copie de la décision"),
]

BOOLEAN_FIELDS = ("hasPetition", "outOfTime", "wantDecisionCopy")
TRUE_VALUES = set(["vrai", "true", "oui", "yes", "1", "o", "x"])
FALSE_VALUES = set(["faux", "false", "non", "no", "0", "n", ""])

CLAIM_TYPE_VALUES = {
    "ecrite": u"Écrite",
    "orale": u"Orale",
}
CLAIM_TYPE_MAPPING = {
    u"Écrite": "writedClaim",
    u"Orale": "oralClaim",
}
CLAIM_DATE_FORMATS = (
    "%m/%d/%Y",
    "%m-%d-%Y",
    "%m/%d/%y",
    "%m-%d-%y",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y-%m-%d",
    "%d.%m.%Y",
    "%d/%m/%y",
    "%d-%m-%y",
    "%y-%m-%d",
    "%d.%m.%y",
)
CLAIM_DATE_STORAGE_FORMAT = "%d/%m/%Y"

IDENTITY_FIELDS = ("name1", "name2", "society", "nationalRegister")
COMPARABLE_FIELDS = [f for f in claimants_csv_fieldnames if f != "claimingText"]

logger = logging.getLogger("Products.urban import utils")


def _strip_accents(text):
    if not isinstance(text, unicode):
        text = text.decode("utf-8", "ignore")
    normalized = unicodedata.normalize("NFKD", text)
    return u"".join(c for c in normalized if not unicodedata.combining(c))


def _normalize_label(label):
    label = (label or "").strip().strip('"').strip("'")
    label = _strip_accents(label).lower()
    label = re.sub(r"[^a-z0-9]+", " ", label).strip()
    return label


def _field_accessor_name(field):
    return "get" + field[0].upper() + field[1:]


def _field_mutator_name(field):
    return "set" + field[0].upper() + field[1:]


def _get_existing_value(claimant_obj, field):
    accessor = getattr(claimant_obj, _field_accessor_name(field), None)
    if accessor is None:
        return None
    try:
        return accessor()
    except Exception:
        return None


def _to_comparable_date(value):
    """Normalize a date-ish value (raw CSV string or a Zope DateTime
    object) to a plain (year, month, day) tuple for comparison,
    or None if it can't be parsed."""
    if not value:
        return None
    if isinstance(value, DateTime):
        return (value.year(), value.month(), value.day())
    for fmt in CLAIM_DATE_FORMATS:
        try:
            parsed = datetime.strptime(unicode(value).strip(), fmt)
            return (parsed.year, parsed.month, parsed.day)
        except (ValueError, TypeError):
            continue
    return None


def _values_match(existing_value, csv_value, field=None):
    if not existing_value or not csv_value:
        return True
    if field == "claimDate":
        existing_date = _to_comparable_date(existing_value)
        csv_date = _to_comparable_date(csv_value)
        if existing_date is None or csv_date is None:
            return True  # unparsable, don't block a match on it
        return existing_date == csv_date
    return _normalize_label(unicode(existing_value)) == _normalize_label(
        unicode(csv_value)
    )


def _comparable_row_value(field, row, titles_mapping=None, country_mapping=None):
    if field == "claimType":
        raw = row.get("claimType")
        return CLAIM_TYPE_MAPPING.get(raw, raw)
    if field == "personTitle" and titles_mapping is not None:
        raw = row.get("personTitle")
        return titles_mapping.get(raw, raw)
    if field == "country" and country_mapping is not None:
        raw = row.get("country")
        return country_mapping.get(raw, raw)
    return row.get(field)


NORMALIZED_LABEL_TO_FIELDNAME = dict(
    (_normalize_label(label), fieldname) for fieldname, label in CLAIMANT_HEADER_LABELS
)


def handle_boolean_value(value):
    if isinstance(value, bool):
        return value
    normalized = _normalize_label(value)
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    raise ValueError(value)


def normalize_claim_type(value):
    if not value:
        return u"Écrite"  # existing default, kept as-is
    normalized = _normalize_label(value)
    if normalized in CLAIM_TYPE_VALUES:
        return CLAIM_TYPE_VALUES[normalized]
    raise ValueError(value)


def parse_claim_date(value):
    value = (value or "").strip()
    for fmt in CLAIM_DATE_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue
    raise ValueError(value)


def is_plausible_date(value):
    """Only checks the value can be parsed as SOME date in a known
    format — doesn't resolve day/month ambiguity, doesn't reformat.
    The original string is kept untouched, same as before our changes;
    the Archetypes DateField widget resolves the actual interpretation."""
    value = (value or "").strip()
    for fmt in CLAIM_DATE_FORMATS:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            continue
    return False


def _detect_delimiter_and_fieldnames(header_line):
    """Try ',' then ';', keep whichever recognizes the most columns.
    Returns (delimiter, fieldnames); fieldnames[i] is the internal field
    name, or None if the file's column isn't recognized (it will then
    be ignored)."""
    best = None
    for delimiter in (",", ";"):
        raw_tokens = next(
            csv.reader(StringIO(header_line), delimiter=delimiter, quotechar='"')
        )
        fieldnames = [
            NORMALIZED_LABEL_TO_FIELDNAME.get(_normalize_label(token))
            for token in raw_tokens
        ]
        matched = sum(1 for f in fieldnames if f)
        if best is None or matched > best[1]:
            best = (delimiter, matched, fieldnames)
    return best[0], best[2]


def parse_and_validate_claimants_csv(raw_data):
    """Parse the raw CSV once, return (rows, errors).
    rows: list of dicts with already-normalized values (bool, date,
          claimType); columns missing from the file are simply absent
          from the dict (not an error).
    errors: list of i18n messages, one entry per invalid value."""
    raw_data = _decode_csv_data(raw_data)
    lines = raw_data.splitlines()
    if not lines:
        return [], [_(u"The imported file is empty.")]

    delimiter, fieldnames = _detect_delimiter_and_fieldnames(lines[0])
    if not any(fieldnames):
        return [], [
            _(
                u"The imported file couldn't be read properly. "
                u"Please verify its structure and try again."
            )
        ]

    final_fieldnames = [
        fn if fn else u"_ignored_%s" % idx for idx, fn in enumerate(fieldnames)
    ]
    reader = csv.DictReader(
        StringIO(raw_data),
        fieldnames=final_fieldnames,
        delimiter=delimiter,
        quotechar='"',
    )
    raw_rows = list(reader)[1:]  # skip the header line
    raw_rows = [
        row
        for row in raw_rows
        if row.get("name1") or row.get("name2") or row.get("society")
    ]

    rows = []
    errors = []
    for line_number, row in enumerate(raw_rows, start=2):
        row_errors = []
        clean_row = dict(row)

        for field in BOOLEAN_FIELDS:
            try:
                clean_row[field] = handle_boolean_value(row.get(field))
            except ValueError:
                row_errors.append((field, row.get(field)))

        try:
            clean_row["claimType"] = normalize_claim_type(row.get("claimType"))
        except ValueError:
            row_errors.append(("claimType", row.get("claimType")))

        claim_date = row.get("claimDate")
        if claim_date:
            if not is_plausible_date(claim_date):
                row_errors.append(("claimDate", claim_date))
            try:
                clean_row["claimDate"] = parse_claim_date(claim_date).strftime(
                    CLAIM_DATE_STORAGE_FORMAT
                )
            except ValueError:
                row_errors.append(("claimDate", claim_date))

        if row_errors:
            for field, value in row_errors:
                errors.append(
                    _(
                        u'line ${line}, field ${field}: invalid value "${value}"',
                        mapping={
                            u"line": line_number,
                            u"field": field,
                            u"value": value,
                        },
                    )
                )
        else:
            rows.append(clean_row)

    return rows, errors


def _decode_csv_data(raw_data):
    """Normalize the raw CSV bytes to valid utf-8 bytes.
    French Excel exports are often cp1252/latin-1 instead of utf-8."""
    if raw_data.startswith("\xef\xbb\xbf"):  # strip BOM if present
        raw_data = raw_data[3:]

    try:
        raw_data.decode("utf-8")
        return raw_data  # already valid utf-8 bytes
    except UnicodeDecodeError:
        pass

    try:
        return raw_data.decode("cp1252").encode("utf-8")
    except UnicodeDecodeError:
        # last resort: don't crash the whole import on a single bad byte
        return raw_data.decode("utf-8", "replace").encode("utf-8")


def find_matching_claimant(context, row, titles_mapping=None, country_mapping=None):
    candidates = [
        obj for obj in context.objectValues() if obj.portal_type == "Claimant"
    ]
    for candidate in candidates:
        has_identity_overlap = any(
            row.get(f)
            and _get_existing_value(candidate, f)
            and _values_match(_get_existing_value(candidate, f), row.get(f), field=f)
            for f in IDENTITY_FIELDS
        )
        if not has_identity_overlap:
            continue

        conflicts = [
            f
            for f in COMPARABLE_FIELDS
            if not _values_match(
                _get_existing_value(candidate, f),
                _comparable_row_value(f, row, titles_mapping, country_mapping),
                field=f,
            )
        ]
        if not conflicts:
            return candidate
    return None


def merge_missing_fields(claimant_obj, row, titles_mapping=None, country_mapping=None):
    updated = False
    for field in claimants_csv_fieldnames:
        existing_value = _get_existing_value(claimant_obj, field)
        csv_value = _comparable_row_value(field, row, titles_mapping, country_mapping)
        if not existing_value and csv_value:
            mutator = getattr(claimant_obj, _field_mutator_name(field), None)
            if mutator:
                mutator(csv_value)
                updated = True
    if updated:
        claimant_obj.reindexObject()
    return updated
