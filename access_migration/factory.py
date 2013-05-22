# -*- coding: utf-8 -*-
from Products.urban.Extensions.access_migration import mapper
from Products.CMFPlone.utils import normalizeString

#
# Factories
#


class BaseFactory(object):

    def __init__(self, site, portal_type=''):
        self.site = site
        self.portal_type = portal_type

    def create(self, place=None, **kwargs):
        portal_type = 'portal_type' in kwargs.keys() and kwargs['portal_type'] or self.getPortalType(place, **kwargs)
        container = place and place or self.getCreationPlace(**kwargs)
        if 'id' in kwargs.keys():
            object_id = container.invokeFactory(portal_type, **kwargs)
        else:
            proposed_id = self.getDefaultId(**kwargs)
            object_id = container.invokeFactory(portal_type, id=proposed_id, **kwargs)
        obj = getattr(container, object_id)
        obj._renameAfterCreation()
        return [obj]

    def logError(self, msg, data={}):
        mapper.logError(self, msg, data)

    def getCreationPlace(self, **kwargs):
        return None

    def getPortalType(self, place=None, **kwargs):
        return self.portal_type

    def getDefaultId(self, place, **kwargs):
        portal_type = self.portal_type and self.portal_type or kwargs['portal_type']
        return normalizeString(self.site.generateUniqueId(portal_type))


class MultiObjectsFactory(BaseFactory):

    def create(self, place=None, **kwargs):
        objs = []
        for index, args in kwargs.iteritems():
            if 'id' not in args.keys():
                args['id'] = self.getDefaultId(place, **args)
            objs.append(super(MultiObjectsFactory, self).create(place, **args)[0])
        return objs
