#!/usr/bin/env python

import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pickle
import sys

G = nx.Graph()
# you must pass in the path to the files.pkl file that is produced by the build Flow Graph script.
d = pickle.load(open(sys.argv[1]))

# This builds the big graph
for k in d.keys():
	G.add_edge(d[k]['info']['Source addr'], d[k]['info']['Dest addr'])

# Now, write filters for time
datetimeformat = "%a %b  %d %H:%M:%S %Y"

def getTimesForKey(d,k):
	if d[k]['info'].has_key('First time') and d[k]['info'].has_key('Last time'):
		starttime = datetime.strptime(d[k]['info']['First time'], datetimeformat)
		endtime = datetime.strptime(d[k]['info']['Last time'], datetimeformat)
	else:
		starttime = datetime.strptime(d[k]['info']['Time'], datetimeformat)
		endtime = datetime.strptime(d[k]['info']['Time'], datetimeformat)
	return starttime,endtime


def getTimesForRecord(record):
	if record.has_key('First time') and record.has_key('Last time'):
		starttime = datetime.strptime(record['First time'], datetimeformat)
		endtime = datetime.strptime(record['Last time'], datetimeformat)
	else:
		starttime = datetime.strptime(record['Time'], datetimeformat)
		endtime = datetime.strptime(record['Time'], datetimeformat)
	return starttime, endtime

def timeTest(record,trtuple):
	"""This will test a record to see if it overlaps trtuple."""
	starttime, endtime = getTimesForRecord(record)
	if endtime < trtuple[0] or starttime > trtuple[1]:
		return False
	else:
		return True

def grabGraph(records):
	G = nx.Graph()
	for record in records:
		G.add_edge(record['Source addr'], record['Dest addr'])
	return G

def grabGraphForTimeRange(records, trtuple):
	filteredRecords = filter(lambda record: timeTest(record,trtuple),records)
	return grabGraph(filteredRecords)

def grab1DHomologyTimeSeries(records,trtuples):
	return [len(nx.cycle_basis(grabGraphForTimeRange(records,tup))) for tup in trtuples]
	
