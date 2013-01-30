# -*- coding: utf-8 -*-

import os
import random
import string
import hashlib
from HTMLParser import HTMLParser

def moveElementAfter(object_to_move, container, attr_name, attr_value_to_match):
    new_position = container.getObjectPosition(object_to_move.getId())
    contents = container.objectValues()
    indexes = range(len(contents))
    indexes.reverse()
    for i in indexes:
        if getattr(contents[i], attr_name) == attr_value_to_match and object_to_move != contents[i]:
            new_position = 1 + container.getObjectPosition(contents[i].getId())
            container.moveObjectToPosition(object_to_move.getId(), new_position)
            return

def generatePassword(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))

def getMd5Signature(data):
    md5 = hashlib.md5(data)
    return md5.hexdigest()

def getOsTempFolder():
    tmp = '/tmp'
    if os.path.exists(tmp) and os.path.isdir(tmp):
        res = tmp
    elif os.environ.has_key('TMP'):
        res = os.environ['TMP']
    elif os.environ.has_key('TEMP'):
        res = os.environ['TEMP']
    else:
        raise "Sorry, I can't find a temp folder on your machine."
    return res

def setOptionalAttributes(schema, optional_fields):
    """
      This method set the optional attribute and widget condition on schema fields listed in optional_fields
    """
    for fieldname in optional_fields:
        field = schema.get(fieldname)
        if field is not None:
            setattr(field, 'optional', True)
            field.widget.setCondition("python: here.attributeIsUsed('%s')"%fieldname)

def setSchemataForInquiry(schema):
    """
      Put the the fields coming from Inquiry in a specific schemata
    """
    from Products.urban.Inquiry import Inquiry
    inquiryFields = Inquiry.schema.filterFields(isMetadata=False)
    #do not take the 2 first fields into account, this is 'id' and 'title'
    inquiryFields = inquiryFields[2:]
    for inquiryField in inquiryFields:
        schema[inquiryField.getName()].schemata = 'urban_investigation_and_advices'

from HTMLParser import HTMLParser


#class and function to strip a text from all its HTML tags
class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


#class to retrieve and manipulate more easily parcels and their historic from the cadastral DB
class ParcelHistoric:

    @staticmethod
    def mergeDuplicate(parcel_historics):
        checked = {}
        for i, historic in enumerate(parcel_historics):
            key = historic.key()
            if key in checked.keys():
                parcel_historics[checked[key]].mergeRelatives(historic)
                parcel_historics[i] = None
            else:
                checked[key] = i
        return [parcel for parcel in parcel_historics if parcel]


    def __init__(self, highlight=False, prc='', prca='', prcc='', **refs):
        self.highlight = highlight
        self.parents = self.diffPrc(prca, prc) and [prca] or []
        self.childs = self.diffPrc(prcc, prc) and [prcc] or []
        self.prc = prc
        self.proprietary = refs.get('proprietary', '')
        self.location = refs.get('location', '')
        self.divname = self.division = self.section = self.radical = self.bis =  self.exposant =  self.puissance = ''
        self.refs = ['divname', 'division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        self.setRefs(**refs)

    def __str__(self):
        return ' '.join([getattr(self, attr, '') for attr in self.refs])

    def key(self):
        return self.__str__()

    def buildRelativesChain(self, urban_tool, link_name):
        o_link_name  = link_name == 'parents' and 'childs' or 'parents'
        link = link_name == 'parents' and 'prca' or 'prcc'
        o_link = link == 'prca' and 'prcc' or 'prca'
        division = self.division
        relatives_chain = []
        for prc in getattr(self, link_name):
            section = prc[0]
            prcb1 = prc[1:]
            prcb1 = '%s%s%s' % (prcb1[:-3], ' '.join(['' for i in range(12-len(prcb1))]), prcb1[-3:])
            query_string = "SELECT distinct %s, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
                            FROM pas left join da on da.da = pas.da \
                            WHERE pas.da = %s and section = '%s' and pas.prcb1 = '%s' and pas.%s IS NOT NULL" % (link, division, section, prcb1, o_link)
            records = urban_tool.queryDB(query_string)
            relatives = [ParcelHistoric(**r) for r in records]
            if relatives:
                relative = ParcelHistoric.mergeDuplicate(relatives)[0]
                relative.buildRelativesChain(urban_tool, link_name)
                relative.addRelatives(o_link_name, [self])
                relatives_chain.append(relative)
        setattr(self, link_name, relatives_chain)

    def getSearchRef(self):
        return ','.join([val and str(val) or '' for val in [self.division, self.section, self.radical, self.bis, self.exposant, self.puissance, '0']])

    def getAllSearchRefs(self):
        all_nodes = [n['node'] for n in self.getAllNodes(nodes=all_nodes).values()]
        return [node.getSearchRef() for node in all_nodes]

    def getAllNodes(self, directions=['childs', 'parents'], nodes={}, distance=0):
        nodes[self.key()] = {'node':self, 'distance':distance}
        for direction in directions:
            dist = direction == 'childs' and distance + 1 or distance - 1
            for relative in self.getRelatives(direction):
                if str(relative) not in nodes.keys():
                    relative.getAllNodes(directions, nodes, dist)
        return nodes

    def getParcelAsDictionary(self):
        infos = dict([(ref, getattr(self, ref)) for ref in self.refs])
        infos['highlight'] = self.highlight
        if self.prc:
            infos['prc'] = self.prc
        if self.proprietary:
            infos['proprietary'] = self.proprietary
        if self.location:
            infos['location'] = self.location
        return infos

    def getHistoricForDisplay(self):
        def buildResult(parcel, result, level=0, link='parents'):
            parcel_infos = parcel.getParcelAsDictionary()
            parcel_infos['level'] = level
            if link == 'childs':
                if level !=0 or result == []:
                    result.append(parcel_infos)
            for relative in getattr(parcel, link):
                next_level = link=='parents' and level-1 or level+1
                buildResult(relative, result, next_level, link)
            if link == 'parents':
                result.append(parcel_infos)
            old = parcel.childs and True or False
            parcel_infos['old'] = old
        to_return = []
        buildResult(self, to_return, link='parents')
        buildResult(self, to_return, link='childs')
        min_lvl = abs(min([prc['level'] for prc in to_return]))
        for parcel in to_return:
            parcel['level'] = parcel['level'] + min_lvl
        return to_return

    def mergeRelatives(self, other, link_names=['parents', 'childs']):
        for link_name in link_names:
            existing_relatives= [str(p) for p in getattr(self, link_name)]
            relatives = [relative for relative in getattr(other, link_name) if str(relative) not in existing_relatives]
            self.addRelatives(link_name, relatives)

    def diffPrc(self, prc_ac, prc):
        return prc_ac and prc_ac.replace(' ','')[1:] != prc.replace(' ','') or False

    def setRefs(self, **kwargs):
        for ref in self.refs:
            val = kwargs.get(ref, '') and str(kwargs[ref]) or ''
            setattr(self, ref, val)

    def getRelatives(self, name):
        return getattr(self, '%s' % name, [])

    def addRelatives(self, name, relatives):
        class_attr = getattr(self, name, None)
        if class_attr != None:
            class_attr.extend(relatives)
