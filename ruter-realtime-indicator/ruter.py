#!/usr/bin/env python
# encoding: UTF-8

import requests
import collections
import dateutil.parser
import datetime

import config

def get_raw_data(stop_id):
	url_template = "http://reisapi.ruter.no/stopvisit/getdepartures/{stop_id}?json=true"
	url = url_template.format(stop_id=stop_id)
	response = requests.get(url)
	return response.json()

def get_next_departures(stop_id):
	json = get_raw_data(stop_id)
	result = collections.defaultdict(list)
	for departure in json:
		line = departure["MonitoredVehicleJourney"]["PublishedLineName"]
		name = departure["MonitoredVehicleJourney"]["DestinationName"].encode("utf-8")
		time_as_string = departure["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"]
		time = dateutil.parser.parse(time_as_string)
		result["{} {}".format(line, name)].append(time)
	return dict(result)

def format_time(dt):
	time = dt.strftime("%H:%M")
	delta = dt - datetime.datetime.now(dt.tzinfo)
	minutes = str(int(delta.total_seconds() / 60))
	return "{} ({} min)".format(time, minutes)

if __name__ == "__main__":
	departures = get_next_departures(config.stop_id)
	for name in departures:
		print name
		print "\n".join(["    " + format_time(t) for t in departures[name]])
