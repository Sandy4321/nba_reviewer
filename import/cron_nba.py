#!/usr/bin/env python
import urllib2
import json
import traceback
import datetime
import calendar
import pytz
from pytz import timezone
import psycopg2
import sys
import nba as NBA
from datetime import timedelta

class Game(NBA.Configuration):

	def update(self, date):
		try:
			print 'Update NBA games'
			date = date.strftime("%Y%m%d")
			url = 'http://data.nba.com/json/cms/noseason/scoreboard/%s/games.json' % date
			data = self.get_data(url)
			
			self.con = psycopg2.connect(database='nba_reviewer', user='stijn') 
			self.cur = self.con.cursor() 
			self.write_game(data)
			print 'Update finished succesfully'
		except:
			print 'An error occured during update!'
			print traceback.print_exc();


	def write_game(self, data):
		sports_content = data['sports_content']
		games = sports_content['games']
		if games:
			games = games['game']

			for game in games:

				try:
					game_id = None
					self.cur.execute('SELECT game_id FROM nba_game WHERE game_id = \'%s\'' % game['id'])
					game_id = self.cur.fetchone()

					print 'Update game %s' % game['id']
					self.cur.execute('UPDATE nba_game SET home_score = \'%s\', away_score = \'%s\' WHERE game_id = \'%s\'' % 
									(game['home']['score'], game['visitor']['score'], game['id']))
					self.con.commit()
				except psycopg2.DatabaseError, e:
					if self.con:
						self.con.rollback()
					print 'Error %s' % e

			if self.con:		
				self.con.close()


	def update_all(self, start_date, end_date):
		dates = []
		delta = datetime.timedelta(days=1)

		#convert end_date to datetime format
		end_date = end_date.date()

		while start_date <= end_date:
		    dates.append(start_date)
		    start_date += delta

		try:
			for date in dates:
				self.update(date)

		except:
			print 'An error occured!'
			print traceback.print_exc();


yesterday = datetime.datetime.now() - timedelta(hours=24)
start_date = datetime.date(2014, 10, 28)

g = Game()
g.update(yesterday)
#g.update_all(start_date, yesterday)