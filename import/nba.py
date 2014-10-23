#!/usr/bin/env python
import urllib2
import json
import traceback
import datetime
import psycopg2
import sys

class Configuration():

	opener = urllib2.build_opener()
	con = None
	cur = None

	def get_data(self, url):
		request = urllib2.Request(url)
		f = self.opener.open(request)
		data = json.load(f)

		return data