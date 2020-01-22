# -*- coding: utf-8 -*-

from Products.urban.services.base import SQLService
from Products.urban.services.base import SQLSession
from plone.memoize import ram
from time import time

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy.sql.expression import func

IGNORE = []


class UnreferencedParcelError(Exception):
    """
    This parcel reference cannot be found in the official cadastre.
    """


class CadastreService(SQLService):
    """
    """

    def __init__(self, dialect='postgresql+psycopg2', user='urb_xxx', host='', port='', db_name='urb_xxx', password='', timeout='120000'):
        super(CadastreService, self).__init__(dialect, user, host, port, db_name, password, timeout)

        if self.can_connect():
            self._init_table('da', column_names=['da', 'divname'])
            self._init_table('pe', column_names=['pe', 'adr1', 'adr2', 'daa'])
            self._init_table('prc', column_names=['prc', 'daa', 'na1', 'capakey'])
            self._init_table(
                'pas',
                column_names=['da', 'section', 'radical', 'exposant', 'bis', 'puissance', 'prcb1', 'prcc', 'prca']
            )
            self._init_table(
                'capa',
                column_names=['capakey', 'da', 'section', 'radical', 'exposant', 'bis', 'puissance', 'the_geom']
            )
            self._init_table(
                'map',
                column_names=['capakey', 'prc', 'pe', 'adr1', 'adr2', 'sl1', 'na1']
            )


def all_divisions_cache_key(method, self):
    return time() // 3600


class CadastreSession(SQLSession):
    """
    Implements all the sql queries of cadastre DB with sqlalchemy methods
    """

    @ram.cache(all_divisions_cache_key)
    def get_all_divisions(self):
        """Return all divisions records of da table"""
        query = self.session.query(self.tables.da.da, self.tables.da.divname)
        result = query.all()

        return result

    def is_official_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Tell if a reference exists in the cadastral DB (including old parcels).
        """
        query = self._base_query_parcels(self.tables.pas)
        # filter on parcel reference arguments
        query = self._filter(query, self.tables.pas, division, section, radical, bis, exposant, puissance)
        records = query.all()
        return bool(records)

    def is_outdated_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Tell if a reference exists in the cadastral DB of actual parcels.
        If the reference is not known of the db, raise UnreferencedParcelError exception.
        """
        if not self.is_official_parcel(division, section, radical, bis, exposant, puissance):
            raise UnreferencedParcelError

        query = self._base_query_parcels(self.tables.capa)
        # filter on parcel reference arguments
        query = self._filter(query, self.tables.capa, division, section, radical, bis, exposant, puissance)
        records = query.all()
        return bool(records)

    def query_parcels(self, division=IGNORE, section=IGNORE, radical=IGNORE, bis=IGNORE,
                      exposant=IGNORE, puissance=IGNORE, location=IGNORE, parcel_owner=IGNORE):
        """
        Return parcels partially matching any defined criterias.
        Any argument with the value IGNORE is ignored.
        """
        query = self._base_query_actual_parcels()
        # filter on parcel reference arguments
        query = self._filter(query, self.tables.capa, division, section, radical, bis, exposant, puissance)

        # filter on parcel location/proprietary name arguments
        map_ = self.tables.map
        if parcel_owner is not IGNORE:
            query = query.filter(map_.pe.ilike('%{}%'.format(parcel_owner)))
        if location is not IGNORE:
            query = query.filter(map_.sl1.ilike('%{}%'.format(location)))

        records = query.distinct().all()
        parcels = [ActualParcel(**record._asdict()) for record in records]
        return parcels

    def query_exact_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Return the unique parcel exactly matching search criterias.
        """
        pas = self.tables.pas
        query = self._base_query_parcels(pas)
        # filter on parcel reference arguments
        query = self._filter(query, pas, division, section, radical, bis, exposant, puissance)
        try:
            record = query.distinct().one()
        except:
            return
        parcel = ParcelHistoric(session=self, **record._asdict())
        return parcel

    def query_parcel_by_capakey(self, capakey):
        """
        Return the unique parcel exactly matching capakey 'capakey'.
        """
        query = self._base_query_actual_parcels()
        query = query.filter(self.tables.map.capakey == capakey)
        try:
            record = query.distinct().one()
        except:
            return
        parcel = ActualParcel(**record._asdict())
        return parcel

    def query_old_parcels(self, division=IGNORE, section=IGNORE, radical=IGNORE, bis=IGNORE,
                          exposant=IGNORE, puissance=IGNORE):
        """
        Return old parcels partially matching any defined criterias.
        Any argument with value IGNORE, will be ignored
        """
        pas = self.tables.pas
        query = self._base_query_parcels(pas)
        # filter on parcel reference arguments
        query = self._filter(query, pas, division, section, radical, bis, exposant, puissance)

        records = query.distinct().all()
        parcels = [Parcel(**record._asdict()) for record in records]
        return parcels

    def query_parcel_historic(self, division, section=None, radical='0', bis='0',
                              exposant=None, puissance='0'):
        """
        Return parcel historic of the parcel exactly matching criterias.
        """
        parcel = self.query_exact_parcel(division, section, radical, bis, exposant, puissance)
        if not parcel:
            str_parcel = '{} {} {} {} {} {}'.format(
                division,
                section,
                radical,
                bis,
                exposant,
                puissance
            )
            raise UnreferencedParcelError(str_parcel)

        historic = ParcelHistoric(session=self, divname=parcel.divname, **parcel.reference_as_dict())
        return historic

    def query_parent_parcels(self, division, section=None, radical='0', bis='0',
                             exposant=None, puissance='0'):
        """
        Return parents parcels of a given parcel reference.
        """
        parent_parcels = self.query_sibling_parcels(
            division, section, radical, bis, exposant, puissance, sibling_key='prca'
        )
        return parent_parcels

    def query_child_parcels(self, division, section=None, radical='0', bis='0',
                            exposant=None, puissance='0'):
        """
        Return child parcels of a given parcel reference.
        """
        child_parcels = self.query_sibling_parcels(
            division, section, radical, bis, exposant, puissance, sibling_key='prcc'
        )
        return child_parcels

    def query_sibling_parcels(self, division, section=None, radical='0', bis='0',
                              exposant=None, puissance='0', sibling_key=''):
        """
        Return parents/childs parcels of a given parcel reference.

        sibling_key = prca => query parents parcels
        sibling_key = prcc => query for children parcels
        """
        pas = self.tables.pas
        opposite_key = sibling_key == 'prca' and 'prcc' or 'prca'
        opposite_sibling_column = getattr(pas, opposite_key)

        # get the prcb1 of current parcel in a subquery
        query_prcb1 = self.session.query(pas.prcb1.label('current_parcel_id'))
        query_prcb1 = self._filter(query_prcb1, pas, division, section, radical, bis, exposant, puissance)
        subquery = query_prcb1.subquery()

        # search a (sibling) parcel having the opposite sibling column value to 'parcel_key'
        # ex: we search parent parcels having the current parcel as child
        parcel_key = compute_prc(division, section, radical, bis, exposant, puissance)
        query = self._base_query_parcels(pas)
        query = query.filter(pas.da == division)
        query = query.filter(opposite_sibling_column == parcel_key)
        # exclude the current parcel from the result
        query = query.filter(pas.prcb1 != subquery.c.current_parcel_id)

        records = query.distinct().all()
        return records

    def query_parcels_wkt(self, parcels):
        """
        Query polygon wkt format of the union of the parcels.
        """
        capa = self.tables.capa

        query_geom = self.session.query(func.ST_AsText(func.ST_MemUnion(capa.the_geom).label('geo_union')))

        parcel_filters = []
        for parcel in parcels:
            parcel_ref = parcel.reference_as_dict()
            parcel_filters.append(
                and_(
                    capa.da == parcel_ref.pop('division'),
                    *[getattr(capa, ref) == val for ref, val in parcel_ref.iteritems()]
                )
            )
        query_geom = query_geom.filter(or_(*parcel_filters))
        records = query_geom.all()
        records = records and records[0][0] or records
        return records

    def query_parcels_in_radius(self, center_parcels, radius):
        """
        Query parcels around 'center_parcels' in a radius of 'radius' m.
        """
        capa = self.tables.capa

        query_geom = self.session.query(func.ST_MemUnion(capa.the_geom).label('geo_union'))

        parcel_filters = []
        for parcel in center_parcels:
            parcel_ref = parcel.reference_as_dict()
            parcel_filters.append(
                and_(
                    capa.da == parcel_ref.pop('division'),
                    *[getattr(capa, ref) == val for ref, val in parcel_ref.iteritems()]
                )
            )
        query_geom = query_geom.filter(or_(*parcel_filters))
        subquery = query_geom.subquery()

        query = self._base_query_actual_parcels()
        query = query.filter(
            func.ST_Intersects(func.ST_Buffer(subquery.c.geo_union, radius), capa.the_geom)
        )

        records = query.all()
        parcels_in_radius = [ActualParcel(**record._asdict()) for record in records]
        return parcels_in_radius

    def query_owners_of_parcel(self, capakey):
        """
        Return estate owners of a given parcel.
        """

        pe = self.tables.pe
        prc = self.tables.prc

        query = self.session.query(pe.pe, pe.adr1, pe.adr2, pe.daa)
        query = query.filter(pe.daa == prc.daa)
        query = query.filter(prc.capakey == capakey)

        result = query.all()
        return result

    def query_wmc(self, parcels):
        """
        """

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
            func.ST_Extent(self.tables.capa.the_geom).label('coordinates')
        )
        try:
            coordinates = self.normalize_coordinates(query_geom.subquery())
        except:
            coordinates = ['']
        str_coordinates = ', '.join(coordinates)
        return str_coordinates

    def query_parcels_coordinates(self, parcels):
        """
        Query wmc coordinates of selected parcels.
        """
        capa = self.tables.capa
        ST_Extent = func.ST_Extent

        query_geom = self.session.query(ST_Extent(capa.the_geom).label('coordinates'))
        query_geom = query_geom.filter(capa.da == parcels[0].getDivisionCode())

        parcel_filters = []
        # boilerplate to filter on parcels refs.
        # eg: (section=A AND radical=32 AND ...) OR (section=B AND radical=21 ...) OR (...)
        for parcel in parcels:
            parcel_ref = parcel.reference_as_dict()
            parcel_ref.pop('division')  # filtering on division is done earlier
            parcel_filters.append(
                and_(
                    *[getattr(capa, ref) == val for ref, val in parcel_ref.iteritems()]
                )
            )

        query_geom = query_geom.filter(or_(*parcel_filters))
        coordinates = self.normalize_coordinates(query_geom.subquery())

        return coordinates

    def _filter(self, query, table, division=IGNORE, section=IGNORE, radical=IGNORE,
                bis=IGNORE, exposant=IGNORE, puissance=IGNORE):
        da = self.tables.da
        query = division is IGNORE and query or query.filter(da.da == division)
        query = section is IGNORE and query or query.filter(table.section == section)
        query = radical is IGNORE and query or query.filter(table.radical == radical)
        query = bis is IGNORE and query or query.filter(table.bis == bis)
        query = exposant is IGNORE and query or query.filter(table.exposant == exposant)
        query = puissance is IGNORE and query or query.filter(table.puissance == puissance)
        return query

    def _base_query_parcels(self, table):
        """
        """
        da = self.tables.da
        # columns to return
        query = self.session.query(
            da.divname,
            da.da.label('division'),
            table.section,
            table.radical,
            table.exposant,
            table.bis,
            table.puissance,
        )
        # join of given table (pas or capa) and da
        query = query.filter(da.da == table.da)
        return query

    def _base_query_actual_parcels(self):
        """
        """
        capa = self.tables.capa
        # parcel reference columns to return (section, division, radical, ...)
        query = self._base_query_parcels(capa)

        map_ = self.tables.map
        # additional columns to return
        query = query.add_columns(
            capa.capakey,
            map_.prc,
            map_.pe.label('proprietary'),
            map_.adr1.label('proprietary_city'),
            map_.adr2.label('proprietary_street'),
            map_.sl1.label('location'),
            map_.na1.label('usage')
        )
        # join of capa and map
        query = query.filter(capa.capakey == map_.capakey)
        return query


def compute_prc(division, section='', radical='', bis='', exposant='', puissance=''):
    """
    Boilerplate to construct a parcel prc key (prca or prcc) value
    """
    parcel_key = ''
    blank = 0
    if section:
        parcel_key = section

    blank += 4
    if radical and radical != '0':
        blank -= len(radical)
        parcel_key = '{}{}{}'.format(parcel_key, blank * ' ', radical)
        blank = 0

    blank += 3
    if bis and bis != '0':
        zero = 2 - len(bis)
        parcel_key = '{}/{}{}'.format(parcel_key, zero * '0', bis)
        blank = 0

    blank += 1
    if exposant:
        blank -= len(exposant)
        parcel_key = '{}{}{}'.format(parcel_key, blank * ' ', exposant)
        blank = 0

    blank += 3
    if puissance and puissance != '0':
        blank -= len(puissance)
        parcel_key = '{}{}{}'.format(parcel_key, blank * ' ', puissance)
        blank = 0

    return parcel_key


class Parcel(object):
    """
    Proxy base class to represent a parcel from query result
    """

    def __init__(self, **reference):
        self.division = self.section = self.radical = self.bis = self.exposant = self.puissance = ''
        self._reference_keys = ['division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        divname = reference.get('divname', '')
        self.divname = type(divname) is unicode and divname.encode('utf-8') or divname
        self._init_reference(**reference)

    def _init_reference(self, **kwargs):
        for ref in self._reference_keys:
            val = kwargs.get(ref, '') and unicode(kwargs[ref]) or ''
            val = val.upper().encode('utf-8')
            setattr(self, ref, val)

    def __str__(self):
        return ' '.join(self.values())

    def display(self):
        tail = ' '.join(self.values(ignore=['division']))
        display = '{} {}'.format(self.divname, tail)
        return display

    def key(self):
        return self.__str__()

    def values(self, ignore=[]):
        return [getattr(self, attr, '') for attr in self._reference_keys if attr not in ignore]

    def to_index(self):
        index = ','.join(self.values())
        index = '{},0'.format(index)
        return index

    def reference_as_dict(self):
        return dict([(ref, getattr(self, ref)) for ref in self._reference_keys if getattr(self, ref)])

    @property
    def as_prca(self):
        """
        Return prca representation value of this parcel
        """
        reference = self.reference_as_dict()
        prca = compute_prc(**reference)
        return prca

    @property
    def as_prcc(self):
        """
        Return prcc representation value of this parcel
        """
        reference = self.reference_as_dict()
        prcc = compute_prc(**reference)
        return prcc


class ActualParcel(Parcel):
    """
    Class to represent query result of an actual parcel.
    """
    def __init__(self, capakey, **infos):
        super(ActualParcel, self).__init__(**infos)
        self.capakey = capakey
        self.location = self.proprietary = self.proprietary_city = self.proprietary_street = ''
        self._infos_keys = ['location', 'proprietary', 'proprietary_city', 'proprietary_street', 'usage']
        self._init_infos(**infos)

    def _init_infos(self, **kwargs):
        for ref in self._infos_keys:
            val = kwargs.get(ref, '') and unicode(kwargs[ref]) or ''
            val = val.encode('utf-8')
            if val not in['divname', 'division']:
                val = val.upper()
            setattr(self, ref, val)


class BaseParcelHistoric(Parcel):
    """
    Base class for parcel historic
    """

    def __init__(self, session=None, **refs):
        super(BaseParcelHistoric, self).__init__(session=session, **refs)
        from Products.urban.services import cadastre
        self.session = session or cadastre.new_session()
        self.parent_node = None
        self.branches = []
        self.level = 0
        self.width = self._init_width()
        self.old = False  # is an old parcel if it has children

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


class ParentParcel(BaseParcelHistoric):
    """
    Class to represent a parent parcel of a parcelHistoric.
    """

    def __init__(self, child_parcel, session=None, **refs):
        super(ParentParcel, self).__init__(session=session, **refs)
        self.parent_node = child_parcel
        self.level = child_parcel.level - 1
        self.branches = self._init_parents_historic()
        self.width = self._init_width()
        self.old = True  # a parent parcel is ALWAYS old

    def _init_parents_historic(self):
        """
        Recursively initialize the chain of all parents parcels
        """
        reference = self.reference_as_dict()
        parcels = self.session.query_parent_parcels(**reference)
        parents = [ParentParcel(child_parcel=self, session=self.session, **parcel._asdict()) for parcel in parcels]
        return parents

    def display(self):
        return ' '.join(self.values(ignore=['division']))


class ChildParcel(BaseParcelHistoric):
    """
    Class to represent a child parcel of a parcelHistoric.
    """

    def __init__(self, parent_parcel, session=None, **refs):
        super(ChildParcel, self).__init__(session=session, **refs)
        self.parent_node = parent_parcel
        self.level = parent_parcel.level + 1
        self.branches = self._init_children_historic()
        self.width = self._init_width()
        self.old = bool(self.branches)  # this parcel is old only if it has children

    def _init_children_historic(self):
        """
        Recursively initialize the chain of all children parcels
        """
        reference = self.reference_as_dict()
        parcels = self.session.query_child_parcels(**reference)
        children = [ChildParcel(parent_parcel=self, session=self.session, **parcel._asdict()) for parcel in parcels]
        return children

    def display(self):
        return ' '.join(self.values(ignore=['division']))


class ParcelHistoric(ParentParcel, ChildParcel):
    """
    Class to represent a parcel query result and all its siblings (parents/childs)
    """

    def __init__(self, session=None, **refs):
        super(ChildParcel, self).__init__(session=session, **refs)
        self.level = 0
        self.parents = self._init_parents_historic()
        self.children = self._init_children_historic()
        self.branches = self.parents + self.children
        self.width = max(
            sum([n.width for n in self.parents]),
            sum([n.width for n in self.children])
        )
        self.old = bool(self.children)  # this parcel is old only if it has children

    def display(self):
        return super(ChildParcel, self).display()

    def get_all_reference_indexes(self):
        """
        List the reference index values of the parcel and all its siblings
        """
        indexes = [node.to_index() for node in self.all_nodes()]
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
                return ''

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
        for sibling in ['children', 'parents']:
            siblings = list(getattr(self, sibling))
            table.append(siblings)
            width_delta = self.width - sum([s.width for s in siblings])
            if width_delta:
                siblings.append(Blank(width_delta))
            table = recursive_build_table(table)
            table.reverse()

        return table


def parse_cadastral_reference(capakey):
    """
    """
    reference_as_dict = {
        'division': capakey[0:5],
        'section': capakey[5],
        'radical': int(capakey[6:10]) and str(int(capakey[6:10])) or '',
        'bis': int(capakey[11:13]) and str(int(capakey[11:13])) or '',
        'exposant': capakey[13] and capakey[13] or '',
        'puissance': int(capakey[14:17]) and str(int(capakey[14:17])) or '',
    }
    return reference_as_dict
