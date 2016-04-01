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
    response = requests.get(url)
    
    if response.status_code != 200:
        # todo: log response.text
        msg = "Got non-200 response from Ruter: {}".format(response.status_code)
        raise RuterConnectionException(msg)
    try:
        return response.json()
    except e:
        # todo: log response.text
        raise RuterConnectionException("Unable to parse JSON from Ruter")

def get_next_departures(stop_id):
    json = get_raw_data(stop_id)
    result = collections.defaultdict(list)
    for departure in json:
        line = departure["MonitoredVehicleJourney"]["PublishedLineName"]
        name = departure["MonitoredVehicleJourney"]["DestinationName"]
        time_as_string = departure["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
        time = dateutil.parser.parse(time_as_string)

        key = u" ".join([line, name])
        result[key].append(time)
    return dict(result)

def minutes_until(timestamp):
    tzinfo = timestamp.tzinfo
    delta = timestamp - datetime.datetime.now(tzinfo)
    return int(delta.total_seconds() // 60)

def minutes_until_next(stop_id):
    departures = get_next_departures(stop_id)
    return { 
        dest: minutes_until(min(departures[dest]))
        for dest in departures
    }

## "main"

def format_time(dt):
    time = dt.strftime("%H:%M")
    delta = dt - datetime.datetime.now(dt.tzinfo)
    minutes = str(int(delta.total_seconds() / 60))
    return "{} ({} min)".format(time, minutes)

def main():
    departures = get_next_departures(config.stop_id)
    for name in departures:
        print name.encode('utf-8')
        print u"\n".join(["    " + format_time(t) for t in departures[name]])

if __name__ == "__main__":
    main()
