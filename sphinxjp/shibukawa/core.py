# -*- coding: utf-8 -*-

import re
import urllib
from parser import parse_string


class ScheduleError(Exception):
    pass


class Schedule(object):
    baseurl = 'https://chart.googleapis.com/chart?'

    def __init__(self, code, **options):
        self.code = code
        self.options = options

    @property
    def url(self):
        params = self._url_for_chart()
        quoted = ("%s=%s" % (k, urllib.quote(v)) for k, v in params.items())
        url = self.baseurl + "&".join(quoted)

        return url

    def _url_for_chart(self):
        params = dict(cht='bhs', chxt="x,y", chco="ffffff00,0000ff", chg="7.1,0")

        schedule = parse_string(self.code)
        params['chds'] = "0,%d" % schedule.days
        params['chs'] = self.options.get('size', '480x%d' % (40 * (len(schedule.items) + 1)))

        from datetime import timedelta
        xaxis = []
        min = schedule.min
        for i in range(schedule.days):
            date = min + timedelta(days=i)
            xaxis.append("%02d/%02d" % (date.month, date.day))
        params['chxl'] = "0:|%s|1:|%s" % ("|".join(xaxis), "|".join(n.label for n in schedule.items))

        params['chd'] = "t:%s|%s" % (",".join(str(schedule.far_to(n)) for n in schedule.items),
                                     ",".join(str(n.width) for n in schedule.items))

        return params

    def save(self, filename):
        try:
            fd = urllib.urlopen(self.url)

            if not hasattr(fd, 'getcode') or fd.getcode() == 200:
                open(filename, 'w').write(fd.read())
            else:
                raise Exception()
        except:
            msg = "google chart error: a malformed or illegal request"
            raise ScheduleError(msg)
