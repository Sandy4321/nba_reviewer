#!/usr/bin/env python
import urllib2
import json
import traceback
import datetime
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
		request = urllib2.Request(url)
		f = self.opener.open(request)
		data = json.load(f)
		self.print_data(data)
		
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
					game_id = self.cur.fetchone() # self.cur.fetchall()

					if game_id:
						print 'Update game'
						self.cur.execute('UPDATE nba_game SET game_id = \'%s\' WHERE game_id = \'%s\'' % (game['id'], game['id']))
					else:
						print 'Insert game'
						self.cur.execute('INSERT INTO nba_game (game_id, home_id, away_id) VALUES (\'%s\', \'%s\', \'%s\')' % 
											(game['id'], game['home']['id'], game['visitor']['id']))
					self.con.commit()
				except psycopg2.DatabaseError, e:
					if self.con:
						self.con.rollback()
					print 'Error %s' % e

			if self.con:		
				self.con.close()


	def print_data(self, data):
		sports_content = data['sports_content']
		games = sports_content['games']
		if games:
			games = games['game']

			for game in games:
				print 'Home Team: %s %s' % ( game['home']['city'] , game['home']['nickname'] )
				print 'Away Team: %s %s' % ( game['visitor']['city'] , game['visitor']['nickname'] )

				print '-----------------------------------'


# NBA Season 2014 - 2015
# First Game: 28th October 2014
start_date = datetime.date(2014, 10, 28)
# Last Game: 15th April 2015
end_date = datetime.date(2014, 10, 28)


g = Game()
g.print_test()
g.import_all_games(start_date, end_date)
