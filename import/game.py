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

class Game(NBA.Configuration):

	def import_all_games(self, start_date, end_date):
		print 'Start: Import NBA Games'
		
		dates = []
		delta = datetime.timedelta(days=1)
		while start_date <= end_date:
		    date = start_date.strftime("%Y%m%d")
		    dates.append(date)
		    start_date += delta

		try:
			for date in dates:
				self.import_game(date)
				
				
		except:
			print 'An error occured!'
			print traceback.print_exc();
		finally:
			print 'End:   Import NBA Games' 


	def import_game(self, date):
		url = 'http://data.nba.com/json/cms/noseason/scoreboard/%s/games.json' % date
		data = self.get_data(url)
		
		self.con = psycopg2.connect(database='nba_reviewer', user='stijn') 
		self.cur = self.con.cursor() 
		self.write_game(data)


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


					date = datetime.datetime.strptime(game['date']+game['time'], "%Y%m%d%H%M") 
					eastern = timezone('US/Eastern')
					date = eastern.localize(date) # add timezone to the date


					if game_id:
						print 'Update game %s' % game['id']
 						self.cur.execute('UPDATE nba_game SET home_id = \'%s\', away_id = \'%s\', date = \'%s\' WHERE game_id = \'%s\'' % 
											(game['home']['id'], game['visitor']['id'], date, game['id']))
					else:
						
						print 'Insert game %s' % game['id']
						self.cur.execute('INSERT INTO nba_game (game_id, home_id, away_id, date) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' % 
											(game['id'], game['home']['id'], game['visitor']['id'], date))
					self.con.commit()
				except psycopg2.DatabaseError, e:
					if self.con:
						self.con.rollback()
					print 'Error %s' % e

			if self.con:		
				self.con.close()


# NBA Season 2014 - 2015
# First Game: 28th October 2014
start_date = datetime.date(2015, 03, 29)
# Last Game: 15th April 2015
end_date = datetime.date(2015, 04, 15)


g = Game()
g.import_all_games(start_date, end_date)
