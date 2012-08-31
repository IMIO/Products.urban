# -*- coding: utf-8 -*-
from Products.urban.Extensions.access_migration.mapper import PostCreationMapper
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
import subprocess
import inspect
import csv
import os

#
#Migrator
#
class AccessMigrator(object):

    def __init__(self, context, db_name, table_name, object_structure, mapping, path='.',):
        current_directory = os.getcwd()
        self.header = []
        self.errors = {}
        self.sorted_errors = {}
        self.key = ''
        try:
            os.chdir(path)
            self.migration_directory = path
            self.object_structure = object_structure
            self.site = getToolByName(context, 'portal_url').getPortalObject()
            object_names = self._flatten(object_structure)
            self.factories = self._setFactories(object_names, mapping)
            self.mappers = self._setAllMappers(db_name, table_name, object_names, mapping)
            self.allowed_containers = dict([(name, mapping[name]['allowed_containers']) for name in object_names
                                            if 'allowed_containers' in mapping[name].keys()])
        finally:
            os.chdir(current_directory)

    def migrate(self, csvfile, key=''):
        current_directory = os.getcwd()
        self.key = key
        try:
            os.chdir(self.migration_directory)
            lines = csv.reader(csvfile)
            self.header = lines.next()
            for line in lines:
                self.createPloneObjects(self.object_structure, line)
        finally:
            os.chdir(current_directory)

    def createPloneObjects(self, node, line, stack=[]):
        for obj_name, subobjects in node:
            factory_args = {}
            container = stack and stack[-1] or None
            if not container or obj_name not in self.allowed_containers.keys() \
               or (obj_name in self.allowed_containers.keys() and container.portal_type in self.allowed_containers[obj_name]):
                #collect all the data(s) that will be passed to the factory
                for mapper in self.mappers[obj_name]['pre']:
                    factory_args.update(mapper.map(line, container=container))
                #create the object(s)
                factory = self.factories[obj_name]
                objs = factory.create(place=container, **factory_args)
                #update some fields after creation
                for obj in objs:
                    for mapper in self.mappers[obj_name]['post']:
                        mapper.map(line, plone_object=obj, site=self.site)
                    obj.processForm()
                    stack.append(obj)
                    self.createPloneObjects(subobjects, line, stack)
                    stack.pop()

    def logError(self, migrator_locals, location, message, factory_stack, data):
        line_num = int(migrator_locals['lines'].line_num)
        key = self.getData(migrator_locals['line'], self.key)
        migration_step= str(location).split()[0].split('.')[-1]
        stack_display = '\n'.join(['%sid: %s Title: %s' % (''.join(['    ' for i in range(factory_stack.index(obj))]), obj.id, obj.Title()) for obj in factory_stack ])
        msg = 'line %s ( key %s)\n\
 migration substep: %s\n\
 error message: %s\n\
 data: %s\n\
 plone containers stack:\n  %s\n' % (line_num, key, migration_step, message, data, stack_display)
        print msg
        if line_num not in self.errors.keys():
            self.errors[line_num] = []
        self.errors[line_num].append(msg)
        if migration_step not in self.sorted_errors.keys():
            self.sorted_errors[migration_step] = []
        self.sorted_errors[migration_step].append(msg)

    def log(self, migrator_locals, location, message, factory_stack, data):
        pass


    def getData(self, line, cellname):
        return line[self.header.index(cellname)]

    def _setFactories(self, object_names, mappings):
        factories = {}
        for name in object_names:
            settings = mappings[name]['factory']
            factory_class = settings[0]
            args = len(settings) == 2 and settings[1] or {}
            factories[name] = factory_class(self.site, **args)
        return factories

    def _setAllMappers(self, db, table, object_names, mappings):
        all_mappers = {}
        for name in object_names:
            mapping = mappings[name]['mappers']
            all_mappers[name] = self._setMappers(db, table, mapping)
        return all_mappers

    def _setMappers(self, db, table, mapping):
        mappers = {
                'pre':[],
                'post':[],
                }
        for mapper_class, mapper_args in mapping.iteritems():
            #initialize the mapper
            mapper = mapper_class(db, table, self.site, mapper_args)
            if isinstance(mapper, PostCreationMapper):
                mappers['post'].append(mapper)
            else:
                mappers['pre'].append(mapper)
        return mappers

    def _flatten(self, tree):
        def recursiveTraverse(tree, traversal):
            for node, leafs in tree:
                traversal.append(node)
                recursiveTraverse(leafs, traversal)
        order = []
        recursiveTraverse(tree, order)
        return order

