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

    def __init__(self, dialect='postgresql+psycopg2', user='urb_xxx', host='', db_name='urb_xxx', password='', timeout='120000'):
        super(CadastreService, self).__init__(dialect, user, host, db_name, password, timeout)

        if self.can_connect():
            self._init_table('divisions', column_names=['da', 'divname'])
            self._init_table('pe', column_names=['pe', 'adr1', 'adr2', 'daa'])
            self._init_table('prc', column_names=['prc', 'daa', 'na1', 'capakey'])

            self._init_table(
                'capa',
                column_names=['capakey', 'the_geom']
            )
            self._init_table(
                'parcels',
                column_names=[
                    'capakey',
                    'divcad', 'section', 'primarynumber', 'bisnumber', 'exponentletter', 'exponentnumber', 'partnumber'
                ]
            )
            self._init_table(
                'map',
                column_names=['capakey', 'prc', 'pe', 'adr1', 'adr2', 'sl1', 'na1']
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
        query = self.session.query(self.tables.divisions.da, self.tables.divisions.divname)
        result = query.all()

        return result

    def is_official_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Tell if a reference exists in the cadastral DB (including old parcels).
        """
        parcel = self.query_exact_parcel(division, section, radical, bis, exposant, puissance)
        return bool(parcel)

    def query_parcels(self, division=IGNORE, section=IGNORE, radical=IGNORE, bis=IGNORE,
                      exposant=IGNORE, puissance=IGNORE, location=IGNORE, parcel_owner=IGNORE):
        """
        Return parcels partially matching any defined criterias.
        Any argument with the value IGNORE is ignored.
        """
        query = self._base_query_parcels()
        # filter on parcel reference arguments
        query = self._filter(query, division, section, radical, bis, exposant, puissance)

        # filter on parcel location/proprietary name arguments
        map_ = self.tables.map
        if parcel_owner is not IGNORE:
            query = query.filter(map_.pe.ilike('%{}%'.format(parcel_owner)))
        if location is not IGNORE:
            query = query.filter(map_.sl1.ilike('%{}%'.format(location)))

        records = query.distinct().all()
        parcels = [ActualParcel(**record._asdict()) for record in records]
        return parcels

    def query_exact_parcel(self, division, section=None, radical='', bis='', exposant=None,
                           puissance=''):
        """
        Return the unique parcel exactly matching search criterias.
        """
        query = self._base_query_parcels()
        # filter on parcel reference arguments
        query = self._filter(query, division, section, radical, bis, exposant, puissance)
        try:
            record = query.distinct().one()
        except:
            return
        parcel = ActualParcel(session=self, **record._asdict())
        return parcel

    def query_parcel_by_capakey(self, capakey):
        """
        Return the unique parcel exactly matching capakey 'capakey'.
        """
        query = self._base_query_parcels()
        query = query.filter(self.tables.parcels.capakey == capakey)
        try:
            record = query.distinct().one()
        except:
            return
        parcel = ActualParcel(**record._asdict())
        return parcel

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

        query = self._base_query_parcels()
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

    def _filter(self, query, division=IGNORE, section=IGNORE, radical=IGNORE,
                bis=IGNORE, exposant=IGNORE, puissance=IGNORE):
        divisions = self.tables.divisions
        parcels = self.tables.parcels
        query = division is IGNORE and query or query.filter(divisions.da == division)
        query = section is IGNORE and query or query.filter(parcels.section == section)
        query = radical is IGNORE and query or query.filter(parcels.primarynumber == radical)
        query = bis is IGNORE and query or query.filter(parcels.bisnumber == bis)
        query = exposant is IGNORE and query or query.filter(parcels.exponentletter == exposant)
        query = puissance is IGNORE and query or query.filter(parcels.exponentnumber == puissance)
        return query

    def _base_query_parcels(self):
        """
        """
        parcels = self.tables.parcels
        # parcel reference columns to return (section, division, radical, ...)
        divisions = self.tables.divisions
        # columns to return
        query = self.session.query(
            divisions.divname,
            divisions.da.label('division'),
            parcels.section,
            parcels.primarynumber.label('radical'),
            parcels.exponentletter.label('exposant'),
            parcels.bisnumber.label('bis'),
            parcels.exponentnumber.label('puissance'),
            parcels.capakey,
        )
        # join of given table (pas or capa) and da
        query = query.filter(divisions.da == parcels.divcad)

#        map_ = self.tables.map
        # additional columns to return
#        query = query.add_columns(
#            parcels.capakey,
#            map_.prc,
#            map_.pe.label('proprietary'),
#            map_.adr1.label('proprietary_city'),
#            map_.adr2.label('proprietary_street'),
#            map_.sl1.label('location'),
#            map_.na1.label('usage')
#        )
        # join of capa and map
#        query = query.filter(parcels.capakey == map_.capakey)
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
        raw_values = self.values()
        index = '{:05d}{}{:04d}/{:02d}{}{:03d}'.format(
            int(raw_values[0] or 0),
            raw_values[1],
            int(raw_values[2] or 0),
            int(raw_values[3] or 0),
            raw_values[4] or '_',
            int(raw_values[5] or 0),
        )
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
