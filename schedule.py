#!/usr/bin/python
import ephem
import datetime

home = ephem.Observer()
home.lat = '42.4370'
home.lon = '-71.5056'
home.elevation = 70
print home.date

sun = ephem.Sun()
r1 = home.next_rising(sun)
s1 = home.next_setting(sun)

home.horizon = '-0:34'
r2 = home.next_rising(sun)
s2 = home.next_setting(sun)
print ("Visual sunrise %s" % ephem.localtime(r1))
print ("Visual sunset %s" % ephem.localtime(s1))
print ("Naval obs sunrise %s" % ephem.localtime(r2))
print ("Naval obs sunset %s" % ephem.localtime(s2))
