#!/usr/bin/env python
# encoding: UTF-8

import requests
import collections
import dateutil.parser
import datetime

import config

class RuterConnectionException(Exception):
    """Thrown when there is a problem getting data from the Ruter API"""
    pass

def get_raw_data(stop_id):
    url_template = "http://reisapi.ruter.no/stopvisit/getdepartures/{stop_id}?json=true"
    url = url_template.format(stop_id=stop_id)
    try:
        response = requests.get(url)
    except Exception, e:
        raise RuterConnectionException("Unable to connect to Ruter API", e)
    
    if response.status_code != 200:
        # todo: log response.text
        msg = "Got non-200 response from Ruter: {}".format(response.status_code)
        raise RuterConnectionException(msg)
    try:
        return response.json()
    except Exception, e:
        raise RuterConnectionException("Unable to parse JSON from Ruter", e)

def minutes_until(timestamp):
    tzinfo = timestamp.tzinfo
    delta = timestamp - datetime.datetime.now(tzinfo)
    return int(delta.total_seconds() // 60)

def get_data(stop_id):
    json = get_raw_data(stop_id)
    data = []
    for departure in json:
        time_as_string = departure["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        departure_time = dateutil.parser.parse(time_as_string)
        data.append({
            "line": departure["MonitoredVehicleJourney"]["PublishedLineName"],
            "destination": departure["MonitoredVehicleJourney"]["DestinationName"],
            "time": departure_time,
            "wait": minutes_until(departure_time)
        })
    return data

## "main"

def format_time(dt):
    time = dt.strftime("%H:%M")
    delta = dt - datetime.datetime.now(dt.tzinfo)
    minutes = str(int(delta.total_seconds() / 60))
    return "{} ({} min)".format(time, minutes)

def main():
    for dep in get_data(config.stop_id):
        try:
            print dep["destination"].encode('utf-8'), 
            print format_time(dep["time"])
        except:
            print "ERROR (probably utf-8 stuff)"
        sys.stdout.flush()

if __name__ == "__main__":
    import time
    import sys

    while True:
        main()
        time.sleep(30)
