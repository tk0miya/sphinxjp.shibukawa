# -*- coding: utf-8 -*-

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
        quoted = ("%s=%s" % (k, urllib.quote(v.encode('utf-8'))) for k, v in params.items())
        url = self.baseurl + "&".join(quoted)

        return url

    def _url_for_chart(self):
        params = dict(cht='bhs', chxt="x,y", chco="ffffff00,0000ff", chg="7.1,0")

        schedule = parse_string(self.code)
        params['chds'] = "0,%d" % schedule.days
        params['chs'] = self.options.get('size', '480x%d' % (27 * (len(schedule.items) + 1)))

        interval = self.options.get('interval', None)
        if interval:
            schedule.interval = interval

        from datetime import timedelta
        xaxis = []
        min = schedule.min
        for i in range(0, schedule.days):
            if i % schedule.interval == 0 or i == (schedule.days - 1):
                date = min + timedelta(days=i)
                xaxis.append("%02d/%02d" % (date.month, date.day))
            else:
                xaxis.append("")
        params['chxl'] = "0:|%s|1:|%s" % ("|".join(xaxis), "|".join(n.label for n in reversed(schedule.items)))

        params['chd'] = "t:%s|%s" % (",".join(str(schedule.far_to(n)) for n in schedule.items),
                                     ",".join(str(n.width) for n in schedule.items))

        return params

    def save(self, filename):
        code = None
        try:
            fd = urllib.urlopen(self.url)

            code = getattr(fd, 'code', None)
            if code == 200:
                open(filename, 'wb').write(fd.read())
            else:
                raise Exception()
        except:
            if code == 414:
                msg = "google chart error: Request URI too long"
            else:
                msg = "google chart error: a malformed or illegal request"

            raise ScheduleError(msg)
