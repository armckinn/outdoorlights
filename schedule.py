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


'''
Pseudo code
1) Read scheudle file
    Date Time program
    Where:
        Date:
            *          Every Day unless there is already an event
            Month/day  Date of annual occurrance
        Time:
            sunrise    At Naval Sunrise
            sunset     At Navel Sunset
            Hour/Min   At specific time
2) Convert into internal usage list in order of occurance
3) Look for immediate events (file? REST?) Put at head of list
4) Wait for event. If present then do it
5) If a repeating event then calculate next occurrance and insert into list
6) Go to 3

'''
