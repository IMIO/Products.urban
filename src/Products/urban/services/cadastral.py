# -*- coding: utf-8 -*-

from Products.urban.services.base import Service

IGNORE = []


class UnreferencedParcelError(Exception):
    """
    This parcel reference cannot be found in the official cadastre.
    """


class CadastreService(Service):
    """
    """

    def __init__(self, dialect, user, host, db_name, password=''):
        super(CadastreService, self).__init__(dialect, user, host, db_name, password)

        if self.can_connect():
            self.da = self._init_table('da', column_names=['da', 'divname'])
            self.pe = self._init_table('pe', column_names=['pe', 'adr1', 'adr2', 'daa'])
            self.pas = self._init_table(
                'pas',
                column_names=['da', 'section', 'radical', 'exposant', 'bis', 'puissance', 'prcb1', 'prcc', 'prca']
            )
            self.capa = self._init_table(
                'capa',
                column_names=['capakey', 'da', 'section', 'radical', 'exposant', 'bis', 'puissance']
            )
            self.map_ = self._init_table(
                'map',
                column_names=['capakey', 'prc', 'pe', 'adr1', 'adr2', 'sl1']
            )
            # self.prc = self._init_table('prc', column_names=['prc', '', '', '', '', ''])

    def _init_table(self, table_name, column_names):
        table = self.get_table(table_name)
        for column_name in column_names:
            setattr(table, column_name, table.columns[column_name])

        return table

    def get_all_divisions(self):
        """Return all divisions records of da table"""
        session = self.session()
        query = session.query(self.da.da, self.da.divname)
        result = query.all()

        return result

    def is_official_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Tell if a reference exists in the cadastral DB (including old parcels).
        """
        query = self._base_query_parcels(self.pas)
        # filter on parcel reference arguments
        query = self._filter(query, self.pas, division, section, radical, bis, exposant, puissance)
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

        query = self._base_query_parcels(self.capa)
        # filter on parcel reference arguments
        query = self._filter(query, self.capa, division, section, radical, bis, exposant, puissance)
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
        query = self._filter(query, self.capa, division, section, radical, bis, exposant, puissance)

        # filter on parcel location/proprietary name arguments
        map_ = self.map_
        if parcel_owner is not IGNORE:
            query = query.filter(map_.pe.like('%{}%'.format(parcel_owner)))
        if location is not IGNORE:
            query = query.filter(map_.sl1.like('%{}%'.format(location)))

        records = query.all()
        parcels = [ActualParcel(**record._asdict()) for record in records]
        return parcels

    def query_exact_parcel(self, division, section=None, radical='0', bis='0', exposant=None,
                           puissance='0'):
        """
        Return the unique parcel exactly matching search criterias.
        """
        pas = self.pas
        query = self._base_query_parcels(pas)
        # filter on parcel reference arguments
        query = self._filter(query, pas, division, section, radical, bis, exposant, puissance)
        try:
            record = query.distinct().one()
        except:
            return
        parcel = ParcelHistoric(**record._asdict())
        return parcel

    def query_old_parcels(self, division=IGNORE, section=IGNORE, radical=IGNORE, bis=IGNORE,
                          exposant=IGNORE, puissance=IGNORE):
        """
        Return old parcels partially matching any defined criterias.
        Any argument with value IGNORE, will be ignored
        """
        pas = self.pas
        query = self._base_query_parcels(pas)
        # filter on parcel reference arguments
        query = self._filter(query, pas, division, section, radical, bis, exposant, puissance)

        records = query.all()
        parcels = [Parcel(**record._asdict()) for record in records]
        return parcels

    def query_parcel_historic(self, division, section=None, radical='0', bis='0',
                              exposant=None, puissance='0'):
        """
        Return parcel historic of the parcel exactly matching criterias.
        """
        parcel = self.query_exact_parcel(division, section, radical, bis, exposant, puissance)
        if not parcel:
            raise UnreferencedParcelError

        historic = ParcelHistoric(divname=parcel.divname, **parcel.reference_as_dict())
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
        session = self.session()
        pas = self.pas
        opposite_key = sibling_key == 'prca' and 'prcc' or 'prca'
        opposite_sibling_column = getattr(pas, opposite_key)

        # get the prcb1 of current parcel in a subquery
        query_prcb1 = session.query(pas.prcb1.label('current_parcel_id'))
        query_prcb1 = self._filter(query_prcb1, pas, division, section, radical, bis, exposant, puissance)
        subquery = query_prcb1.subquery()

        # search a (sibling) parcel having the opposite sibling column value to 'parcel_key'
        # ex: we search parent parcels having the current parcel as child
        parcel_key = compute_prc(division, section, radical, bis, exposant, puissance)
        query = self._base_query_parcels(pas, session)
        query = query.filter(opposite_sibling_column == parcel_key)
        # exclude the current parcel from the result
        query = query.filter(pas.prcb1 != subquery.c.current_parcel_id)

        records = query.distinct().all()
        return records

    def query_parcels_in_radius(self, center_parcels, radius):
        """
        """
        query = self._base_query_parcels()
        return query

    def _filter(self, query, table, division=IGNORE,  section=IGNORE, radical=IGNORE,
                bis=IGNORE, exposant=IGNORE, puissance=IGNORE):
        da = self.da
        query = query.filter(da.da == division)
        query = section is IGNORE and query or query.filter(table.section == section)
        query = radical is IGNORE and query or query.filter(table.radical == radical,)
        query = bis is IGNORE and query or query.filter(table.bis == bis,)
        query = exposant is IGNORE and query or query.filter(table.exposant == exposant,)
        query = puissance is IGNORE and query or query.filter(table.puissance == puissance,)
        return query

    def _base_query_parcels(self, table, session=None):
        """
        """
        session = session or self.session()
        da = self.da
        # columns to return
        query = session.query(
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

    def _base_query_actual_parcels(self, session=None):
        """
        """
        capa = self.capa
        # parcel reference columns to return (section, division, radical, ...)
        query = self._base_query_parcels(capa, session)

        map_ = self.map_
        # additional columns to return
        query = query.add_columns(
            capa.capakey,
            map_.prc,
            map_.pe.label('proprietary'),
            map_.adr1.label('proprietary_city'),
            map_.sl1.label('location')
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
        self._infos_keys = ['location', 'proprietary', 'proprietary_city', 'proprietary_street']
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

    def __init__(self, **refs):
        super(BaseParcelHistoric, self).__init__(**refs)
        self.parent_node = None
        self.branches = []
        self.level = 0
        self.width = self._init_width()

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

    def __init__(self, child_parcel, **refs):
        super(ParentParcel, self).__init__(**refs)
        self.parent_node = child_parcel
        self.level = child_parcel.level - 1
        self.branches = self._init_parents_historic()
        self.width = self._init_width()

    def _init_parents_historic(self):
        """
        Recursively initialize the chain of all parents parcels
        """
        from Products.urban.services import cadastre

        reference = self.reference_as_dict()
        parcels = cadastre.query_parent_parcels(**reference)
        parents = [ParentParcel(child_parcel=self, **parcel._asdict()) for parcel in parcels]
        return parents

    def display(self):
        return ' '.join(self.values(ignore=['division']))


class ChildParcel(BaseParcelHistoric):
    """
    Class to represent a child parcel of a parcelHistoric.
    """

    def __init__(self, parent_parcel, **refs):
        super(ChildParcel, self).__init__(**refs)
        self.parent_node = parent_parcel
        self.level = parent_parcel.level + 1
        self.branches = self._init_children_historic()
        self.width = self._init_width()

    def _init_children_historic(self):
        """
        Recursively initialize the chain of all children parcels
        """
        from Products.urban.services import cadastre

        reference = self.reference_as_dict()
        parcels = cadastre.query_child_parcels(**reference)
        children = [ChildParcel(parent_parcel=self, **parcel._asdict()) for parcel in parcels]
        return children

    def display(self):
        return ' '.join(self.values(ignore=['division']))


class ParcelHistoric(ParentParcel, ChildParcel):
    """
    Class to represent a parcel query result and all its siblings (parents/childs)
    """

    def __init__(self, **refs):
        super(ChildParcel, self).__init__(**refs)
        self.level = 0
        self.parents = self._init_parents_historic()
        self.children = self._init_children_historic()
        self.branches = self.parents + self.children
        self.width = self._init_width()

    def display(self):
        return super(ChildParcel, self).display()

    def get_all_reference_indexes(self):
        """
        List the reference index values of the parcel and all its siblings
        """
        indexes = [node.to_index() for node in self.all_nodes()]
        return indexes

    def all_nodes(self):
        return self._get_all_nodes([self])

    def all_child_nodes(self):
        return self._get_all_nodes(self.children)

    def all_parent_nodes(self):
        return self._get_all_nodes(self.parents)

    def _get_all_nodes(self, subset=[]):
        to_explore = list(subset)  # clone 'subset' to keep it unaltered
        all_nodes = []
        while to_explore:
            next_node = to_explore.pop()
            all_nodes.append(next_node)
            for sub_node in next_node.branches:
                to_explore.append(sub_node)
        return all_nodes

    def parents_by_level(self):
        """
        See _nodes_by_level.
        """
        return self._nodes_by_level(self.all_parent_nodes())

    def children_by_level(self):
        """
        See _nodes_by_level.
        """
        return self._nodes_by_level(self.all_child_nodes())

    def _nodes_by_level(self, nodes):
        """
        Transform a node list into a dict {x: [n1, n2], y[n3, ...], ...}
        where x is a level and [n1, n2] are nodes of this level.
        """
        by_level = {}
        for node in nodes:
            if node.level in by_level.keys():
                by_level[node.level].append(node)
            else:
                by_level[node.level] = [node]
        return by_level

    def table_display(self):
        """
        Return a matrix representing this tree.
        To be used to easily build an htm table (set <td> colspan
        to element.width)
        """
        class Blank(object):
            def __init__(self, width=1):
                self.width = width

            def display(self):
                return ' '

        def recursive_build_table(table=[[]]):
            """
            Build tables lines by looking on elements of the previous line

                         ...
            newline      | . x . y ...
            previous line| v w . u . . s |
                         | m . . o . p q |
                         |     b . c d   |
            first line   |       a       |
            """
            previous_line = table[-1]
            # base case: the last line is a single big Blank
            if len(previous_line) == 1 and type(previous_line[0]) is Blank:
                return table[:-1]

            line = []
            previous_content = None
            for content in previous_line:
                if type(content) is Blank:
                    new_content = Blank(content.width)
                else:
                    branches = content.branches
                    if branches:
                        for branch in branches[:-1]:
                            line.append(branch)
                        new_content = branches[-1]
                    else:
                        new_content = Blank()
                if type(new_content) is Blank and type(previous_content) is Blank:
                    # merge contigous blanks
                    previous_content.width += new_content.width
                else:
                    line.append(new_content)
                    previous_content = new_content
            # recursive call
            table.append(line)
            return recursive_build_table(table)

        table = [[self]]
        if self.parents:
            table.append(list(self.parents))
            table = recursive_build_table(table)
        table = table[::-1]
        if self.children:
            table.append(list(self.children))
            table = recursive_build_table(table)

        return table
