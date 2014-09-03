import pygeoip
import os
import manage

def getGeoLocationData(ipaddress):
    SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__));
    gic = pygeoip.GeoIP(SITE_ROOT + '/static/geodatabase/GeoLiteCity.dat')
    data = gic.record_by_addr(ipaddress)
    return data