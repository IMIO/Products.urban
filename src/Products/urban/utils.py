# -*- coding: utf-8 -*-

import os
import random
import string
import hashlib
from HTMLParser import HTMLParser

from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES

from plone import api


def getLicenceSchema(licencetype):
    if licencetype not in URBAN_TYPES:
        return None
    types_tool = api.portal.get_tool('portal_types')
    type_info = types_tool.getTypeInfo(licencetype)
    metatype = type_info.getProperty('content_meta_type')
    module_name = 'Products.urban.%s' % metatype
    attribute = "%s_schema" % metatype
    module = __import__(module_name, fromlist=[attribute])
    return getattr(module, attribute)


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
    elif 'TMP' in os.environ:
        res = os.environ['TMP']
    elif 'TEMP' in os.environ:
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
            field.widget.setCondition("python: here.attributeIsUsed('%s')" % fieldname)


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

    def __init__(self, prc='', prca='', prcc='', **refs):
        self.parents = prca and [prca] or []  # self.diffPrc(prca, prc) and [prca] or []
        self.childs = prcc and [prcc] or []  # self.diffPrc(prcc, prc) and [prcc] or []
        self.prc = prc
        self.proprietary = refs.get('proprietary', '')
        self.proprietary_city = refs.get('proprietary_city', '')
        self.proprietary_street = refs.get('proprietary_street', '')
        self.location = refs.get('location', '')
        self.divname = self.division = self.section = self.radical = self.bis = self.exposant = self.puissance = ''
        self.refs = ['divname', 'division', 'section', 'radical', 'bis', 'exposant', 'puissance']
        self.setRefs(**refs)

    def __str__(self):
        return ' '.join([getattr(self, attr, '') for attr in self.refs])

    def key(self):
        return self.__str__()

    def buildRelativesChain(self, urban_tool, relationship, all_nodes=None):
        if all_nodes is None:
            all_nodes = {}

        o_relationship = relationship == 'parents' and 'childs' or 'parents'
        link = relationship == 'parents' and 'prca' or 'prcc'
        o_link = link == 'prca' and 'prcc' or 'prca'
        division = self.division
        relation = self.getRelatives(relationship)

        self.clearShortcuts(relationship, urban_tool, link, division)

        relatives_chain = []
        for prc in relation:
            section = prc[0]
            radical_bis = prc[1:8]
            exposant = len(prc) > 8 and prc[8] or ''
            puissance = len(prc) > 11 and prc[9:12] or '   '
            prcb1 = '%s%s%s' % (radical_bis, puissance, exposant)
            query_string = "SELECT distinct %s, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
                            FROM pas left join da on da.da = pas.da \
                            WHERE pas.da = %s and section = '%s' and pas.prcb1 = '%s' and pas.%s IS NOT NULL" % (link, division, section, prcb1, o_link)

            records = urban_tool.queryDB(query_string)

            relatives = [ParcelHistoric(**r) for r in records]

            if relatives:
                relative = ParcelHistoric.mergeDuplicate(relatives)[0]
                relative_ref = str(relative)
                if relative_ref in all_nodes:
                    relative = all_nodes[relative_ref]
                else:
                    relative.buildRelativesChain(urban_tool, relationship, all_nodes)
                    all_nodes[relative_ref] = relative
                relative.addRelatives(o_relationship, [self])
                relatives_chain.append(relative)
        setattr(self, relationship, relatives_chain)

    def clearShortcuts(self, relationship, urban_tool, link, division):
        relation = self.getRelatives(relationship)
        shortcut = [relation.pop(relation.index(ref)) for ref in relation if not self.diffPrc(ref)]
        ref = shortcut and shortcut[0] or None
        if shortcut:
            section = ref[0]
            radical_bis = ref[1:8]
            exposant = len(ref) > 8 and ref[8] or ''
            puissance = len(ref) > 11 and ref[9:12] or '   '
            prcb1 = '%s%s%s' % (radical_bis, puissance, exposant)
            query_string = "SELECT distinct %s, prcb1 as prc, da.divname, pas.da as division, section, radical, exposant, bis, puissance \
                            FROM pas left join da on da.da = pas.da \
                            WHERE pas.da = %s and section = '%s' and pas.prcb1 = '%s' and pas.%s != '%s'" \
                            % (link, division, section, prcb1, link, ref)

            records = urban_tool.queryDB(query_string)

            relatives = [ParcelHistoric(**r) for r in records]

            if relatives:
                relative = ParcelHistoric.mergeDuplicate(relatives)[0]
                for new_relative in relative.getRelatives(relationship):
                    if new_relative not in relation:
                        relation.append(new_relative)

    def getIndexableRef(self):
        return ','.join([val and str(val) or '' for val in [self.division, self.section, self.radical, self.bis, self.exposant, self.puissance, '0']])

    def getAllIndexableRefs(self):
        all_nodes = {}
        all_nodes = [n['node'] for n in self.getAllNodes(nodes=all_nodes).values()]
        return [node.getIndexableRef() for node in all_nodes]

    def getAllNodes(self, directions=['childs', 'parents'], nodes={}, distance=0):
        nodes[self.key()] = {'node': self, 'distance': distance}
        for direction in directions:
            dist = direction == 'childs' and distance + 1 or distance - 1
            for relative in self.getRelatives(direction):
                if str(relative) not in nodes.keys():
                    relative.getAllNodes(directions, nodes, dist)
        return nodes

    def getParcelAsDictionary(self):
        infos = dict([(ref, getattr(self, ref)) for ref in self.refs])
        infos['old'] = self.childs and True or False
        if self.prc:
            infos['prc'] = self.prc
        if self.proprietary:
            infos['proprietary'] = self.proprietary
            infos['proprietary_city'] = self.proprietary_city
            infos['proprietary_street'] = self.proprietary_street
        if self.location:
            infos['location'] = self.location
        return infos

    def getHistoricForDisplay(self):
        display = []
        historic = self.listHistoric()
        delta = abs(min(historic.keys()))
        historic = sorted(list(historic.iteritems()))
        for level, parcels in historic:
            for parcel in parcels:
                parcel_display = parcel.getParcelAsDictionary()
                parcel_display['level'] = delta + level
                parcel_display['highlight'] = (level == 0)
                display.append(parcel_display)
        return display

    def listHistoric(self):
        def buildLevel(result, relationship, level=0):
            if relationship == 'parents':
                previous_level = level + 1
                next_level = level - 1
            else:
                previous_level = level - 1
                next_level = level + 1

            previousparcels = result[previous_level]

            level_parcels = set()

            for p_parcel in previousparcels:
                for parcel in p_parcel.getRelatives(relationship):
                    level_parcels.add(parcel)

            level_parcels = list(level_parcels)

            if level_parcels:
                result[level] = level_parcels
                buildLevel(result, relationship, next_level)

        result = {0: [self]}
        buildLevel(result, 'parents', level=-1)
        buildLevel(result, 'childs', level=1)
        return result

    def mergeRelatives(self, other, relationships=['parents', 'childs']):
        for relationship in relationships:
            existing_relatives = [str(relative) for relative in getattr(self, relationship)]
            relatives = [relative for relative in getattr(other, relationship) if str(relative) not in existing_relatives]
            self.addRelatives(relationship, relatives)

    def diffPrc(self, prc_ac):
        radical_bis = prc_ac[1:8]
        exposant = len(prc_ac) > 8 and prc_ac[8] or ''
        puissance = len(prc_ac) > 11 and prc_ac[9:12] or '   '
        to_compare = '%s%s%s' % (radical_bis, puissance, exposant)
        is_different = to_compare.replace(' ', '') != self.prc.replace(' ', '')
        return is_different

    def setRefs(self, **kwargs):
        for ref in self.refs:
            val = kwargs.get(ref, '') and str(kwargs[ref]) or ''
            if val not in['divname', 'division']:
                val = val.upper()
            setattr(self, ref, val)

    def getRelatives(self, relationship):
        return getattr(self, relationship)

    def addRelatives(self, relationship, new_relatives):
        relatives = getattr(self, relationship, None)
        if relatives is not None:
            relatives.extend(new_relatives)


def getLicenceFolderId(licencetype):
    return '%ss' % licencetype.lower()


def getAllLicenceFolderIds():
    return [getLicenceFolderId(licencetype) for licencetype in URBAN_TYPES]


def getLicenceFolder(context, licencetype):
    portal_url = getToolByName(context, 'portal_url')
    portal = portal_url.getPortalObject()
    urban = portal.urban
    folder_id = getLicenceFolderId(licencetype)
    licence_folder = getattr(urban, folder_id)
    return licence_folder
