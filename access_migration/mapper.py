# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
import subprocess
import inspect
import csv

#
# Mappers
#
class BaseMapper(object):

    def __init__(self, db_name, table_name, site):
        self.db_name = db_name
        self.header = self._extractHeader(table_name)
        self.site = site
        self.catalog = getToolByName(site, 'portal_catalog')

    def _extractHeader(self, table_name):
        query = "Select * from %s Where CLEF = ''" % table_name
        return self._query(query, withheader=True).next()

    def _query(self, query, withheader=False):
        table = subprocess.Popen(['mdb-sql', self.db_name, '-p', '-d', ';'], stdin= subprocess.PIPE, stdout=subprocess.PIPE)
        temp = open('temp', 'w')
        pos = withheader and 1 or 2
        temp.write('\n'.join(table.communicate(query)[0].split('\n')[pos:-2]))
        temp = open('temp', 'r')
        result = csv.reader(temp, delimiter=';')
        return result

    def logError(self, msg, data={}):
        logError(self, msg, data)


class SimpleMapper(BaseMapper):

    def __init__(self, db_name, table_name, site, args, **kwargs):
        super(SimpleMapper, self).__init__(db_name, table_name, site)
        self.bijections = []
        for bijection in args:
            self.bijections.append((bijection['to'], self.header.index(bijection['from']),))

    def map(self, line, **kwargs):
        return dict([(bij[0], line[bij[1]],) for bij in self.bijections])


class Mapper(BaseMapper):

    def __init__(self, db_name, table_name, site, args, **kwargs):
        super(Mapper, self).__init__(db_name, table_name, site)
        sources = type(args['from']) == str and [args['from']] or args['from']
        self.sources = dict([(source_name, self.header.index(source_name),) for source_name in sources if source_name])
        self.destinations = type(args['to']) == str and [args['to']] or args['to']
        self.line = ''

    def getData(self, cellname, line=''):
        line = line and line or self.line
        return line[self.sources[cellname]]

    def map(self, line, **kwargs):
        self.line = line
        mapped = {}
        for dest in self.destinations:
            mapping_method = 'map%s' % dest.capitalize()
            if hasattr(self, mapping_method):
                mapped[dest] = getattr(self, mapping_method)(line, **kwargs)
            else:
                print '%s: NO MAPPING METHOD FOUND' % self
                print 'target field : %s' % dest
        return mapped


class PostCreationMapper(Mapper):

    def __init__(self, db_name, table_name, site, args, **kwargs):
        super(PostCreationMapper, self).__init__(db_name, table_name, site, args, **kwargs)
        self.allowed_containers = 'allowed_containers' in args.keys() and args['allowed_containers'] or []

    def map(self, line, plone_object, **kwargs):
        if self.allowed_containers and plone_object.portal_type not in self.allowed_containers:
            return
        self.line = line
        for dest in self.destinations:
            mapping_method = 'map%s' % dest.capitalize()
            if hasattr(self, mapping_method):
                mutator = plone_object.getField(dest).getMutator(plone_object)
                value = getattr(self, mapping_method)(line, plone_object, **kwargs)
                mutator(value)
            else:
                print '%s: NO MAPPING METHOD FOUND' % self
                print 'target field : %s' % dest


class SecondaryTableMapper(Mapper):

    def __init__(self, db_name, table_name, site, args, mappers_module=None):
        args['from'] = 'from' in args.keys() and args['from'] or [args['KEY']]
        args['to'] = 'to' in args.keys() and args['to'] or []
        super(SecondaryTableMapper, self).__init__(db_name, table_name, site, args)
        self.key = args['KEY']
        self.secondary_table = args['table']
        self.mappers = self._setMappers(args['mappers'])

    def _setMappers(self, mappers_dscr):
        mappers = []
        for mapper_class, mapper_args in mappers_dscr.iteritems():
            mapper = mapper_class(self.db_name, self.secondary_table, self.site, mapper_args)
            mappers.append(mapper)
        return mappers

    def map(self, line, **kwargs):
        objects_args = {}
        key_value = self.getData(self.key, line)
        db_query = "Select * from %s Where CLEF = '%s'" % (self.secondary_table, key_value)
        i = 0
        for line in self._query(db_query):
            args = {}
            for mapper in self.mappers:
                args.update(mapper.map(line, **kwargs))
            objects_args[str(i)] = args
            i = i + 1
        return objects_args

#
#Loggers
#
def log(migration_object, message, data={}):
    factory_stack = _getLocals('createPloneObjects')['stack']
    migrator_locals = _getLocals('migrate')
    migrator = migrator_locals['self']
    migrator.log(migrator_locals, migration_object, message, factory_stack, data)

def logError(migration_object, message, data={}):
    factory_stack = _getLocals('createPloneObjects')['stack']
    migrator_locals = _getLocals('migrate')
    migrator = migrator_locals['self']
    migrator.logError(migrator_locals, migration_object, message, factory_stack, data)

def _getLocals(fun_name):
    stack = inspect.stack()
    locales = None
    for line in stack:
        if line[3] == fun_name:
            locales = line[0].f_locals
            break
    return locales
