import pygeoip
import os

def getGeoLocationData(ipaddress):
    gic = pygeoip.GeoIP(os.getcwd() + '/static/geodatabase/GeoLiteCity.dat')
    data = gic.record_by_addr(ipaddress)
    return data