# -*- coding: utf-8 -*-

from zope.interface import implements
from plone import api
from datetime import timedelta
from datetime import datetime

from imio.schedule.interfaces import ICalendarExtraHolidays


class CollegeHolidays(object):
    implements(ICalendarExtraHolidays)

    def get_holidays(self, year):
        urban = api.portal.get_tool('portal_urban')
        holidays = []
        for date_range in urban.collegeHolidays:
            begin = datetime.strptime(date_range['from'], '%d/%m/%Y')
            end = datetime.strptime(date_range['to'], '%d/%m/%Y')
            holidays.extend([(d, '') for d in self.get_date_range(begin, end)])
        return tuple(holidays)

    def get_date_range(self, from_date, to_date):
        dates = []
        delta = timedelta(days=1)
        while from_date <= to_date:
            dates.append(from_date.date())
            from_date += delta
        return dates
