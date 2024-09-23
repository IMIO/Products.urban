# -*- coding: utf-8 -*-

from Products.urban.services.base import SQLService
from Products.urban.services.base import SQLSession
from plone import api
from plone.memoize import ram
from time import time

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.sql.expression import func

import json

IGNORE = []


class UnreferencedParcelError(Exception):
    """
    This parcel reference cannot be found in the official cadastre.
    """


class CadastreService(SQLService):
    """ """

    def __init__(
        self,
        dialect="postgresql+psycopg2",
        user="urb_xxx",
        host="",
        port="",
        db_name="urb_xxx",
        password="",
        timeout="0",
    ):
        super(CadastreService, self).__init__(
            dialect, user, host, port, db_name, password, timeout
        )

        if self.can_connect():
            self._init_table("divisions", column_names=["da", "divname"])

            self._init_table("capa", column_names=["capakey", "the_geom"])
            self._init_table(
                "parcels",
                column_names=[
                    "propertysituationid",
                    "street_uid",
                    "number",
                    "capakey",
                    "divcad",
                    "section",
                    "primarynumber",
                    "bisnumber",
                    "exponentletter",
                    "exponentnumber",
                    "partnumber",
                    "nature",
                ],
            )
            self._init_table(
                "old_parcels",
                column_names=[
                    "capakey",
                    "divcad",
                    "section",
                    "primarynumber",
                    "bisnumber",
                    "exponentletter",
                    "exponentnumber",
                    "partnumber",
                    "propertysituationid",
                ],
            )
            self._init_table(
                "parcels_genealogy",
                column_names=[
                    "capakey",
                    "predecessors",
                    "successors",
                ],
            )
            self._init_table(
                "parcelsstreets",
                column_names=[
                    "street_uid",
                    "street_situation",
                ],
            )
            self._init_table(
                "global_natures",
                column_names=[
                    "nature_pk",
                    "nature_fr",
                ],
            )
            self._init_table(
                "owners_imp",
                column_names=[
                    "propertysituationidf",
                    "owner_officialid",
                    "owner_name",
                    "owner_firstname",
                    "owner_country",
                    "owner_zipcode",
                    "owner_municipality_fr",
                    "owner_street_fr",
                    "owner_number",
                    "owner_boxnumber",
                    "partner_officialid",
                    "partner_name",
                    "partner_firstname",
                    "partner_country",
                    "partner_zipcode",
                    "partner_municipality_fr",
                    "partner_street_fr",
                    "partner_number",
                    "partner_boxnumber",
                ],
            )


def all_divisions_cache_key(method, self):
    return time() // 86400


class CadastreSession(SQLSession):
    """
    Implements all the sql queries of cadastre DB with sqlalchemy methods
    """

    @ram.cache(all_divisions_cache_key)
    def get_all_divisions(self):
        """Return all divisions records of da table"""
        query = self.session.query(
            self.tables.divisions.da, self.tables.divisions.divname
        )
        result = query.all()

        return result

    def get_parcel_status(self, capakey):
        """
        Tell if a reference exists in the cadastral DB (including old parcels).
        """
        if self.query_parcel_by_capakey(capakey):
            return "actual_parcel"
        elif self.query_old_parcel_by_capakey(capakey):
            return "old_parcel"
        raise UnreferencedParcelError()

    def query_parcels(
        self,
        division=IGNORE,
        section=IGNORE,
        radical=IGNORE,
        bis=IGNORE,
        exposant=IGNORE,
        puissance=IGNORE,
        location=IGNORE,
        street_number=IGNORE,
        parcel_owner=IGNORE,
    ):
        """
        Return parcels partially matching any defined criterias.
        Any argument with the value IGNORE is ignored.
        """
        query = self._base_query_parcels()
        # filter on parcel reference arguments
        query = self._filter(
            query, division, section, radical, bis, exposant, puissance
        )

        # filter on parcel location/proprietary name arguments
        if parcel_owner is not IGNORE:
            parcel_owners = self.tables.owners_imp
            query = query.filter(
                or_(
                    parcel_owners.owner_name.ilike("%{}%".format(parcel_owner)),
                    parcel_owners.owner_firstname.ilike("%{}%".format(parcel_owner)),
                    parcel_owners.partner_name.ilike("%{}%".format(parcel_owner)),
                    parcel_owners.partner_firstname.ilike("%{}%".format(parcel_owner)),
                )
            )
        if location is not IGNORE:
            if street_number is not IGNORE:
                parcels = self.tables.parcels
                query = query.filter(parcels.number.ilike("%{}%".format(street_number)))
            parcel_streets = self.tables.parcelsstreets
            query = query.filter(
                parcel_streets.street_situation.ilike("%{}%".format(location))
            )

        records = query.distinct().all()
        parcels = self.merge_parcel_results(records)
        return parcels

    def query_old_parcels(
        self,
        division=IGNORE,
        section=IGNORE,
        radical=IGNORE,
        bis=IGNORE,
        exposant=IGNORE,
        puissance=IGNORE,
    ):
        """
        Return parcels partially matching any defined criterias.
        Any argument with the value IGNORE is ignored.
        """
        query = self._base_query_old_parcels()
        # filter on parcel reference arguments
        query = self._filter(
            query,
            division,
            section,
            radical,
            bis,
            exposant,
            puissance,
            parcels_table=self.tables.old_parcels,
        )
        records = query.distinct().all()
        parcels = self.merge_parcel_results(records)
        return parcels

    def query_exact_parcel(
        self, division, section=None, radical="", bis="", exposant=None, puissance=""
    ):
        """
        Return the unique parcel exactly matching search criterias.
        """
        query = self._base_query_parcels()
        # filter on parcel reference arguments
        query = self._filter(
            query, division, section, radical, bis, exposant, puissance
        )
        records = query.distinct().all()
        parcels = self.merge_parcel_results(records)
        if len(parcels) != 1:
            return
        return parcels[0]

    def query_parcel_by_capakey(self, capakey):
        """
        Return the unique parcel exactly matching capakey 'capakey'.
        """
        query = self._base_query_parcels()
        query = query.filter(self.tables.parcels.capakey == capakey)
        records = query.distinct().all()
        parcels = self.merge_parcel_results(records)
        if len(parcels) != 1:
            return
        return parcels[0]

    def query_old_parcel_by_capakey(self, capakey):
        """
        Return the unique parcel exactly matching capakey 'capakey'.
        """
        query = self._base_query_old_parcels()
        query = query.filter(self.tables.parcels.capakey == capakey)
        records = query.distinct().all()
        parcels = self.merge_parcel_results(records)
        if len(parcels) != 1:
            return
        return parcels[0]

    def query_parcel_historic(self, capakey):
        parcels_genealogy = self.tables.parcels_genealogy
        query = self.session.query(
            parcels_genealogy.predecessors,
            parcels_genealogy.successors,
        )
        query = query.filter(parcels_genealogy.capakey == capakey)
        records = query.distinct().all()
        if records:
            historic = ParcelHistoric(
                capakey,
                json.loads(records[0][0].replace("'", '"')),
                json.loads(records[0][1].replace("'", '"')),
            )
        else:
            historic = ParcelHistoric(capakey, {}, {})
        return historic

    def query_parcels_wkt(self, parcels):
        """
        Query polygon wkt format of the union of the parcels.
        """
        capa = self.tables.capa

        query_geom = self.session.query(
            func.ST_AsText(func.ST_Union(capa.the_geom).label("geo_union"))
        )

        parcel_filters = []
        for parcel in parcels:
            parcel_filters.append(and_(capa.capakey == parcel.get_capakey()))
        query_geom = query_geom.filter(or_(*parcel_filters))
        records = query_geom.all()
        records = records and records[0][0] or records
        return records

    def query_parcels_in_radius(self, center_parcels, radius):
        """
        Query parcels around 'center_parcels' in a radius of 'radius' m.
        """
        capa = self.tables.capa
        parcels = self.tables.parcels

        query_geom = self.session.query(func.ST_Union(capa.the_geom).label("geo_union"))

        parcel_filters = []
        for parcel in center_parcels:
            parcel_filters.append(and_(capa.capakey == parcel.get_capakey()))
        query_geom = query_geom.filter(or_(*parcel_filters))
        subquery = query_geom.subquery()

        query = self._base_query_parcels()
        query = query.filter(capa.capakey == parcels.capakey)
        query = query.filter(
            func.ST_DWithin(subquery.c.geo_union, capa.the_geom, radius)
        )

        records = query.all()
        parcels_in_radius = self.merge_parcel_results(records)
        return parcels_in_radius

    def normalize_coordinates(self, subquery):
        """
        'subquery' should be a sqlalchemy subquery of this type:
        FROM capa SELECT ST_Extent(the_geom) as coordinates WHERE ...
        """
        ST_Extent = func.ST_Extent
        coordinates = subquery.c.coordinates
        query = self.session.query(
            func.ST_Xmin(ST_Extent(coordinates)),
            func.ST_Ymin(ST_Extent(coordinates)),
            func.ST_Xmax(ST_Extent(coordinates)),
            func.ST_Ymax(ST_Extent(coordinates)),
        )
        result = query.first()

        return result

    def query_map_coordinates(self):
        """
        Query wmc map coordinates.
        """
        query_geom = self.session.query(
            func.ST_Extent(self.tables.capa.the_geom).label("coordinates")
        )
        try:
            coordinates = self.normalize_coordinates(query_geom.subquery())
        except:
            coordinates = [""]
        str_coordinates = ", ".join(coordinates)
        return str_coordinates

    def query_parcels_coordinates(self, parcels):
        """
        Query wmc coordinates of selected parcels.
        """
        capa = self.tables.capa
        ST_Extent = func.ST_Extent

        query_geom = self.session.query(ST_Extent(capa.the_geom).label("coordinates"))
        query_geom = query_geom.filter(capa.da == parcels[0].getDivisionCode())

        parcel_filters = []
        # boilerplate to filter on parcels refs.
        # eg: (section=A AND radical=32 AND ...) OR (section=B AND radical=21 ...) OR (...)
        for parcel in parcels:
            parcel_ref = parcel.reference_as_dict()
            parcel_ref.pop("division")  # filtering on division is done earlier
            parcel_filters.append(
                and_(
                    *[getattr(capa, ref) == val for ref, val in parcel_ref.iteritems()]
                )
            )

        query_geom = query_geom.filter(or_(*parcel_filters))
        coordinates = self.normalize_coordinates(query_geom.subquery())

        return coordinates

    def _filter(
        self,
        query,
        division=IGNORE,
        section=IGNORE,
        radical=IGNORE,
        bis=IGNORE,
        exposant=IGNORE,
        puissance=IGNORE,
        parcels_table=None,
    ):
        divisions = self.tables.divisions
        if parcels_table is not None:
            parcels = parcels_table
        else:
            parcels = self.tables.parcels
        query = division is IGNORE and query or query.filter(divisions.da == division)
        query = section is IGNORE and query or query.filter(parcels.section == section)
        query = (
            radical is IGNORE
            and query
            or query.filter(parcels.primarynumber == radical)
        )
        query = bis is IGNORE and query or query.filter(parcels.bisnumber == bis)
        query = (
            exposant is IGNORE
            and query
            or query.filter(parcels.exponentletter == exposant)
        )
        query = (
            puissance is IGNORE
            and query
            or query.filter(parcels.exponentnumber == puissance)
        )
        return query

    def _base_query_parcels(self):
        """ """
        parcels = self.tables.parcels
        parcel_streets = self.tables.parcelsstreets
        divisions = self.tables.divisions
        owners_imp = self.tables.owners_imp
        natures = self.tables.global_natures
        # parcel reference columns to return (section, division, radical, ...)
        query = self.session.query(
            parcels.section,
            parcels.primarynumber.label("radical"),
            parcels.exponentletter.label("exposant"),
            parcels.bisnumber.label("bis"),
            parcels.exponentnumber.label("puissance"),
            parcels.capakey,
            parcels.street_uid,
            parcels.number,
            parcels.partnumber,
            divisions.divname,
            divisions.da.label("division"),
            parcel_streets.street_situation.label("street_name"),
            owners_imp.owner_officialid.label("owner_id"),
            owners_imp.owner_name,
            owners_imp.owner_firstname,
            owners_imp.owner_country,
            owners_imp.owner_zipcode,
            owners_imp.owner_municipality_fr.label("owner_city"),
            owners_imp.owner_street_fr.label("owner_street"),
            owners_imp.owner_number,
            owners_imp.owner_boxnumber,
            owners_imp.partner_officialid.label("partner_id"),
            owners_imp.partner_name,
            owners_imp.partner_firstname,
            owners_imp.partner_country,
            owners_imp.partner_zipcode,
            owners_imp.partner_municipality_fr.label("partner_city"),
            owners_imp.partner_street_fr.label("partner_street"),
            owners_imp.partner_number,
            owners_imp.partner_boxnumber,
            natures.nature_fr,
        )
        # table joins
        query = query.filter(divisions.da == parcels.divcad)
        query = query.filter(
            parcels.propertysituationid == owners_imp.propertysituationidf
        )
        query = query.filter(parcels.nature == natures.nature_pk)
        query = query.outerjoin(
            parcel_streets, parcels.street_uid == parcel_streets.street_uid
        )

        return query

    def _base_query_old_parcels(self):
        """ """
        parcels = self.tables.old_parcels
        divisions = self.tables.divisions
        owners_imp = self.tables.owners_imp
        # parcel reference columns to return (section, division, radical, ...)
        query = self.session.query(
            parcels.section,
            parcels.primarynumber.label("radical"),
            parcels.exponentletter.label("exposant"),
            parcels.bisnumber.label("bis"),
            parcels.exponentnumber.label("puissance"),
            parcels.capakey,
            parcels.partnumber,
            divisions.divname,
            divisions.da.label("division"),
            owners_imp.owner_officialid.label("owner_id"),
            owners_imp.owner_name,
            owners_imp.owner_firstname,
            owners_imp.owner_country,
            owners_imp.owner_zipcode,
            owners_imp.owner_municipality_fr.label("owner_city"),
            owners_imp.owner_street_fr.label("owner_street"),
            owners_imp.owner_number,
            owners_imp.owner_boxnumber,
            owners_imp.partner_officialid.label("partner_id"),
            owners_imp.partner_name,
            owners_imp.partner_firstname,
            owners_imp.partner_country,
            owners_imp.partner_zipcode,
            owners_imp.partner_municipality_fr.label("partner_city"),
            owners_imp.partner_street_fr.label("partner_street"),
            owners_imp.partner_number,
            owners_imp.partner_boxnumber,
        )
        # table joins
        query = query.filter(divisions.da == parcels.divcad)
        query = query.outerjoin(
            owners_imp, parcels.propertysituationid == owners_imp.propertysituationidf
        )

        return query

    def merge_parcel_results(self, query_result):
        parcels = {}
        for record in query_result:
            if record.capakey not in parcels:
                parcel = Parcel(record.capakey)
                parcels[record.capakey] = parcel
            else:
                parcel = parcels[record.capakey]
            if hasattr(record, "nature_fr"):
                parcel.add_nature(record.nature_fr)
            if hasattr(record, "street_uid"):
                parcel.add_location(
                    record.street_uid,
                    record.street_name or "",
                    record.number
                    and record.number.replace(" ", "").encode("utf-8")
                    or "",
                )
            if record.owner_id:
                parcel.add_owner(
                    record.owner_id,
                    record.owner_name or "",
                    record.owner_firstname or "",
                    record.owner_country or "",
                    record.owner_zipcode or "",
                    record.owner_city or "",
                    record.owner_street or "",
                    record.owner_number or "",
                    record.owner_boxnumber or "",
                )
            if record.partner_id:
                parcel.add_owner(
                    record.partner_id,
                    record.partner_name or "",
                    record.partner_firstname or "",
                    record.partner_country or "",
                    record.partner_zipcode or "",
                    record.partner_city or "",
                    record.partner_street or "",
                    record.partner_number or "",
                    record.partner_boxnumber or "",
                )

        return parcels.values()


class Parcel(object):
    """
    Proxy base class to represent a parcel from query result
    """

    def __init__(self, capakey):
        self.division = (
            self.section
        ) = self.radical = self.bis = self.exposant = self.puissance = ""
        self._reference_keys = [
            "division",
            "section",
            "radical",
            "bis",
            "exposant",
            "puissance",
        ]
        portal_urban = api.portal.get_tool("portal_urban")
        self.divname = portal_urban.get_division_name(capakey[:5])
        self._init_reference(capakey)
        self.capakey = capakey
        self.locations = {}
        self.owners = {}
        self.natures = []

    def _init_reference(self, capakey):
        ref_as_dict = capakey_as_dict(capakey)
        for ref in self._reference_keys:
            val = ref_as_dict.get(ref, "") and unicode(ref_as_dict[ref]) or ""
            val = val.upper().encode("utf-8")
            setattr(self, ref, val)

    def __str__(self):
        return " ".join(self.values())

    def display(self):
        tail = " ".join(self.values(ignore=["division"]))
        display = "{} {}".format(self.divname, tail)
        return display

    def key(self):
        return self.__str__()

    def values(self, ignore=[]):
        return [
            getattr(self, attr, "")
            for attr in self._reference_keys
            if attr not in ignore
        ]

    def reference_as_dict(self):
        return dict(
            [
                (ref, getattr(self, ref))
                for ref in self._reference_keys
                if getattr(self, ref)
            ]
        )

    def add_location(self, street_uid, street_name, number):
        self.locations["{}/{}".format(street_uid, number)] = {
            "street_name": street_name or "",
            "number": number or "",
        }

    def add_owner(
        self,
        owner_id,
        name,
        firstname,
        country,
        zipcode,
        city,
        street,
        number,
        boxnumber,
    ):
        self.owners[owner_id] = {
            "name": name,
            "firstname": firstname,
            "country": country,
            "zipcode": zipcode,
            "city": city,
            "street": street,
            "number": boxnumber and u"{}/{}".format(number, boxnumber) or number,
        }

    def add_nature(self, nature):
        if nature not in self.natures:
            self.natures.append(nature)


class SiblingParcelHistoric(Parcel):
    """
    Base class for parcel historic
    """

    def __init__(self, capakey, parent_node, siblings):
        super(SiblingParcelHistoric, self).__init__(capakey)
        self.parent_node = parent_node
        self.level = parent_node.level - 1
        self.branches = self._init_siblings_historic(siblings)
        self.width = self._init_width()
        self.old = True  # a sibling parcel is ALWAYS old

    def _init_width(self):
        width = sum([node.width for node in self.branches]) or 1
        return width

    @property
    def root(self):
        """
        Return the root node of the this node tree
        """
        parent = self.parent_node
        while parent:
            parent = parent.parent_node
        return parent

    def _init_siblings_historic(self, siblings):
        """
        Recursively initialize the chain of all parents parcels
        """
        branches = [
            SiblingParcelHistoric(capakey, parent_node=self, siblings=tail)
            for capakey, tail in siblings.iteritems()
        ]
        return branches

    def display(self):
        return " ".join(self.values(ignore=["division"]))


class ParcelHistoric(SiblingParcelHistoric):
    """
    Class to represent a parcel query result and all its siblings (parents/childs)
    """

    def __init__(self, capakey, parents, children):
        super(SiblingParcelHistoric, self).__init__(capakey)
        self.level = 0
        self.parents = self._init_siblings_historic(parents)
        self.children = self._init_siblings_historic(children)
        self.branches = self.parents + self.children
        self.width = max(
            sum([n.width for n in self.parents]), sum([n.width for n in self.children])
        )
        self.old = bool(self.children)  # this parcel is old only if it has children

    def display(self):
        return super(ParcelHistoric, self).display()

    def get_all_capakeys(self):
        """
        List the reference index values of the parcel and all its siblings
        """
        indexes = [node.capakey for node in self.all_nodes()]
        return indexes

    def all_nodes(self):
        """
        Return a list of all nodes of this historic.
        """
        to_explore = list([self])
        all_nodes = []
        while to_explore:
            next_node = to_explore.pop()
            all_nodes.append(next_node)
            for sub_node in next_node.branches:
                to_explore.append(sub_node)
        return all_nodes

    def table_display(self):
        """
        Return nested lists representing this parcel tree to easily build
        an html table:
        - the whole nested list is a <table>
        - each line is a <tr>
        - each item of a line is a <td> (with colspan set to item.width)
        """

        class Blank(object):
            def __init__(self, width=1):
                self.width = width

            def display(self):
                return ""

        def recursive_build_table(table=[[]]):
            """
            Build tables lines by looking on elements of the previous line

            first line    |       a       |
                          |     b . c d   |
                          | m . . o . p q |
                          ...
            previous line | v w . u . . s |
            new line      | . x . y ...
            """
            previous_line = table[-1]
            # base case: the last line is a single Blank or is empty
            is_blank_line = len(previous_line) == 1 and type(previous_line[0]) is Blank
            if not previous_line or is_blank_line:
                return table[:-1]

            line = []
            for leaf in previous_line:
                if isinstance(leaf, Parcel) and leaf.branches:
                    for branch in leaf.branches:
                        line.append(branch)
                else:
                    new_blank = Blank(leaf.width)
                    # if left neighbour is also a blank, merge them
                    if line and type(line[-1]) is Blank:
                        line[-1].width += new_blank.width
                    else:
                        line.append(new_blank)
            # recursive call
            table.append(line)
            return recursive_build_table(table)

        table = [[self]]
        for sibling in ["children", "parents"]:
            siblings = list(getattr(self, sibling))
            table.append(siblings)
            width_delta = self.width - sum([s.width for s in siblings])
            if width_delta:
                siblings.append(Blank(width_delta))
            table = recursive_build_table(table)
            table.reverse()

        return table


def capakey_as_dict(capakey):
    """ """
    reference_as_dict = {
        "division": capakey[0:5],
        "section": capakey[5],
        "radical": int(capakey[6:10]) and str(int(capakey[6:10])) or "",
        "bis": int(capakey[11:13]) and str(int(capakey[11:13])) or "",
        "exposant": capakey[13] and capakey[13] or "",
        "puissance": int(capakey[14:17]) and str(int(capakey[14:17])) or "",
    }
    return reference_as_dict
