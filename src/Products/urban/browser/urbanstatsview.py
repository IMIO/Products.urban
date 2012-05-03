from Acquisition import aq_inner
from datetime import date
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.urban.config import URBAN_TYPES
from DateTime import DateTime


class UrbanStatsView(BrowserView):
    """
      This manage the view of urban
    """
    def isUrbanManager(self):
        from Products.CMFCore.utils import getToolByName
        context = aq_inner(self.context)
        member = context.restrictedTraverse('@@plone_portal_state').member()
        return member.has_role('Manager') or member.has_role('Editor', getToolByName(context, 'portal_urban'))

    def getLicenceTypes(self):
        return URBAN_TYPES

    def getWfStates(self):
        context = aq_inner(self.context)
        #
        #how to get all the states available for a wf
        wftool = getToolByName(context, 'portal_workflow')
        urban_wf = wftool.getWorkflowById('urban_licence_workflow')
        urban_states = urban_wf.states
        state_names = [str(state) for state in urban_states]
        return state_names

    def getDefaultStartDate(self):
        return '%s-01-01' %(str(date.today().year))

    def getDefaultEndDate(self):
        return str(date.today())

    def getSearchArgument(self, key_to_match):
        request = aq_inner(self.request)
        if type(key_to_match) == list:
            return [request.get(key, '') for key in key_to_match]
        request = aq_inner(self.request)
        arg = request.get(key_to_match, '')
        if arg and type(arg) is not list:
            return [arg]
        return arg

    def getDisplayDate(self, field_name):
        request_keys = ['%s%s' %(field_name, key) for key in ['_year','_month','_day']]
        date = self.getSearchArgument(request_keys)
        date.reverse()
        return '/'.join(date)

    def computeStatistics(self):
        context = aq_inner(self.context)
        request = aq_inner(self.request)
        site = getToolByName(context, 'portal_url').getPortalObject()
        args = {
                'licence_type':self.getSearchArgument('licence_types'),
                'licence_state':self.getSearchArgument('licence_states'),
                'date_start':self.getSearchArgument(['from_year','from_month','from_day']),
                'date_end':self.getSearchArgument(['to_year','to_month','to_day']),
               }
        result = self.getEmptyResultTable(args)
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog(portal_type=args['licence_type'],
                         created={'query':[DateTime('/'.join(args['date_start'])), DateTime('/'.join(args['date_end']))], 'range':'minmax'},
                         review_state=args['licence_state']
                        )
        for brain in brains:
            result[brain.portal_type][brain.review_state] += 1
        self.sumPartialResults(result)
        return result

    def sumPartialResults(self, table):
        sum_line = {}
        for line in table.values():
            line['sum'] = sum(line.values())
            for column_name, cell_value in line.iteritems():
                if column_name in sum_line:
                    sum_line[column_name] += cell_value
                else:
                    sum_line[column_name] = cell_value
        table['sum'] = sum_line

    def getEmptyResultTable(self, arguments):
        matrix = {}
        for licence_type in arguments['licence_type']:
            matrix_line = {}
            matrix[licence_type] = matrix_line
            for licence_state in arguments['licence_state']:
                matrix_line[licence_state] = 0
        return matrix

class UrbanStatsMacros(BrowserView):
    """
      This manage the macros of UrbanStats
    """
